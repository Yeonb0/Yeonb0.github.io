import argparse
import glob
import os
import re
import requests
import yaml
from notion_client import Client

# ==================================================
# Config
# ==================================================
CONFIG_PATH = "_notion_sync/config.yml"

# _notion_sync/config.yml 이 없을 때 쓰는 기본값 (기존 하드코딩 값과 동일)
DEFAULT_CONFIG = {
  "properties": {
    "title": "이름",
    "date": "작성일",
    "category": "카테고리",
    "tags": "태그",
    "series": "series",
    "step": "step",
    "status": "상태",
  },
  "status_done": "완료",
  "posts_dir": "_posts",
  "image_dir": "assets/images/notion",
}


def load_config():
  Config = {**DEFAULT_CONFIG, "properties": dict(DEFAULT_CONFIG["properties"])}
  if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, encoding="utf-8") as f:
      User = yaml.safe_load(f) or {}
    Config["properties"].update(User.get("properties") or {})
    for key in ("status_done", "posts_dir", "image_dir"):
      if User.get(key):
        Config[key] = User[key]
  return Config


CONFIG = load_config()
PROPS = CONFIG["properties"]

# ==================================================
# ENV
# ==================================================
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
# DB 모드에서만 필요
DATABASE_ID = os.environ.get("NOTION_DB_ID")

POSTS_DIR = CONFIG["posts_dir"]
IMAGE_BASE_DIR = CONFIG["image_dir"]

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGE_BASE_DIR, exist_ok=True)

notion = Client(auth=NOTION_TOKEN)

# ==================================================
# Utils
# ==================================================
def slugify(text: str) -> str:
  # 기존 규칙 (소문자, 공백 · 슬래시 → 하이픈) 에 URL을 깨는 문자 제거만 추가
  slug = (
    text.strip()
    .lower()
    .replace(" ", "-")
    .replace("/", "-")
  )
  slug = re.sub(r"[?#%:\"'<>|\\*]", "", slug)
  return re.sub(r"-{2,}", "-", slug).strip("-")


def normalize_id(raw: str) -> str:
  return raw.replace("-", "").lower()


def page_id_from_url(url: str) -> str:
  # notion.so/<slug>-<32hex>?v=... 형식에서 마지막 32자리 hex 추출
  path = url.split("?")[0].split("#")[0]
  Matches = re.findall(r"[0-9a-fA-F]{32}|[0-9a-fA-F-]{36}", path)
  if not Matches:
    raise ValueError(f"Notion page id를 찾을 수 없습니다 : {url}")
  return normalize_id(Matches[-1])


def find_post_by_notion_id(page_id: str):
  # R14 : 같은 notion_id 를 가진 기존 글이 있으면 그 경로를 재사용
  target = normalize_id(page_id)
  for path in glob.glob(os.path.join(POSTS_DIR, "**", "*.md"), recursive=True):
    with open(path, encoding="utf-8") as f:
      head = f.read(4000)
    m = re.search(r"^notion_id:\s*['\"]?([0-9a-fA-F-]+)", head, re.MULTILINE)
    if m and normalize_id(m.group(1)) == target:
      return path
  return None

# --------------------------------------------------
# rich_text → Markdown
# --------------------------------------------------
def rich_text_to_md(rich_text):
  if not rich_text:
    return ""

  raw_text = "".join(t["plain_text"] for t in rich_text)

  # $$ LaTeX block (문단 전체일 때만)
  m = re.fullmatch(r"\$\$\s*([\s\S]+?)\s*\$\$", raw_text.strip())
  if m:
    expr = m.group(1)
    return "$$\n" + expr + "\n$$"

  md = ""
  for t in rich_text:
    # 인라인 수식은 서식 없이 $...$ 로 감싸서 MathJax가 처리하게 함
    if t.get("type") == "equation":
      md += "$" + t["equation"]["expression"].strip() + "$"
      continue

    txt = t["plain_text"]
    ann = t["annotations"]

    if ann.get("code"):
      txt = f"`{txt}`"
    if ann.get("bold"):
      txt = f"**{txt}**"
    if ann.get("italic"):
      txt = f"*{txt}*"
    if ann.get("strikethrough"):
      txt = f"~~{txt}~~"

    if t.get("href"):
      txt = f"[{txt}]({t['href']})"

    md += txt

  return md


def normalize_markdown(content: str) -> str:
  """
  - heading 위 / 아래 공백 보장
  - 4칸 이상 들여쓴 리스트를 2칸 단위로 정규화
  - 코드블록 / HTML wrapper 내부는 건드리지 않음
  """
  lines = content.splitlines()
  out = []

  heading_re = re.compile(r"^#{1,6}\s+")
  indent_list_re = re.compile(r"^(\s+)([-*+]\s+|\d+[.)]\s+)")

  in_code_block = False
  in_html_block = False

  for line in lines:
    stripped = line.strip()

    # fenced code block 감지
    if stripped.startswith("```"):
      in_code_block = not in_code_block
      out.append(line)
      continue

    # custom html block 감지
    if stripped.startswith('<div class="equation-box">'):
      in_html_block = True
      out.append(line)
      continue

    if stripped == "</div>":
      in_html_block = False
      out.append(line)
      continue

    if in_code_block or in_html_block:
      out.append(line)
      continue

    # heading 위 / 아래 공백 보장
    if heading_re.match(line):
      if out and out[-1].strip() != "":
        out.append("")
      out.append(line)
      out.append("")
      continue

    # 4칸 이상 들여쓴 리스트 정규화
    m = indent_list_re.match(line)
    if m:
      spaces = len(m.group(1))
      bullet = m.group(2)
      rest = line[m.end():]

      depth = spaces // 2
      depth = max(1, depth)

      indent = "  " * depth
      line = indent + bullet + rest

    out.append(line)

  return "\n".join(out).rstrip() + "\n"


# ==================================================
# Image
# ==================================================
def download_image(url, post_slug, name):
  headers = {"User-Agent": "Mozilla/5.0 (Notion Sync)"}
  try:
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
  except Exception:
    print(f"[WARN] Image download failed: {url}")
    return None

  ct = r.headers.get("Content-Type", "")
  ext = "png"
  if "jpeg" in ct or "jpg" in ct:
    ext = "jpg"
  elif "gif" in ct:
    ext = "gif"

  img_dir = os.path.join(IMAGE_BASE_DIR, post_slug)
  os.makedirs(img_dir, exist_ok=True)

  filename = f"{name}.{ext}"
  path = os.path.join(img_dir, filename)

  with open(path, "wb") as f:
    f.write(r.content)

  return f"/{IMAGE_BASE_DIR}/{post_slug}/{filename}"

# ==================================================
# Block pagination
# ==================================================
def get_children(block_id):
  blocks, cursor = [], None
  while True:
    res = notion.blocks.children.list(block_id=block_id, start_cursor=cursor)
    blocks.extend(res["results"])
    if not res["has_more"]:
      break
    cursor = res["next_cursor"]
  return blocks

# ==================================================
# Block → Markdown
# ==================================================
def block_to_md(block, post_slug, img_idx, depth=0):
  md = ""
  t = block["type"]
  indent = "  " * depth

  if t == "paragraph":
    text = rich_text_to_md(block[t]["rich_text"])
    md += text + "\n\n"

  elif t == "equation":
    expr = block["equation"]["expression"].strip()
    md += '<div class="equation-box">\n\n'
    md += "$$\n" + expr + "\n$$\n\n"
    md += "</div>\n\n"

  # ==================================================
  # heading 처리
  # ==================================================
  elif t.startswith("heading_"):
    text = rich_text_to_md(block[t]["rich_text"])

    text = text.replace(" ", " ")
    text = text.strip()
    text = re.sub(r"^\s+", "", text)
    text = re.sub(r"\s+$", "", text)

    if depth > 0:
      md += indent + "- **" + text + "**\n"
    else:
      level = int(t[-1])
      md += "#" * level + " " + text + "\n\n"

  elif t == "bulleted_list_item":
    md += indent + "- " + rich_text_to_md(block[t]["rich_text"]) + "\n"

  elif t == "numbered_list_item":
    md += indent + "1. " + rich_text_to_md(block[t]["rich_text"]) + "\n"

  elif t == "code": 
    code_text = "".join(rt["plain_text"] for rt in block[t]["rich_text"])
    lang = block[t]["language"]

    lang_map = {
      "plain text": "text",
      "plaintext": "text",
      "c++": "cpp",
      "c#": "csharp",
      "objective-c": "objc"
    }

    lang = lang_map.get(lang, lang)

    md += "{% raw %}\n"
    md += f"```{lang}\n"
    md += code_text.rstrip()
    md += "\n```\n"
    md += "{% endraw %}\n\n"

  elif t == "image":
    img = block["image"]
    if img["type"] == "file":
      path = download_image(img["file"]["url"], post_slug, f"img_{img_idx}")
      if path:
        md += f"![]({path})\n\n"
        img_idx += 1
    else:
      md += f"![]({img['external']['url']})\n\n"

  elif t == "quote":
    text = rich_text_to_md(block[t]["rich_text"]).strip()
    for line in text.split("\n"):
      md += indent + "> " + line + "\n"
    md += "\n"

  elif t == "divider":
    md += "---\n\n"

  elif t == "to_do":
    mark = "x" if block[t].get("checked") else " "
    md += indent + f"- [{mark}] " + rich_text_to_md(block[t]["rich_text"]) + "\n"

  elif t == "toggle":
    # 토글 제목은 굵게, 내용은 아래 children 재귀로 이어서 출력
    md += indent + "- **" + rich_text_to_md(block[t]["rich_text"]).strip() + "**\n"

  elif t in ("bookmark", "link_preview", "embed"):
    url = block[t].get("url", "")
    caption = rich_text_to_md(block[t].get("caption", [])).strip()
    if url:
      # 앞의 리스트에 붙어 들어가지 않도록 빈 줄로 시작
      md += f"\n[{caption or url}]({url})\n\n"

  elif t == "callout":
    callout = block["callout"]
    icon = ""
    if callout.get("icon") and callout["icon"]["type"] == "emoji":
      icon = callout["icon"]["emoji"] + " "

    text = rich_text_to_md(callout["rich_text"]).strip()

    if text:
      md += f"> {icon}{text}\n\n"
    elif icon:
      md += f"> {icon}\n\n"

    # Git blog 렌더링 안정성을 위해
    # 자식 블록은 blockquote 안에 넣지 않고 바깥으로 평탄화
    if block.get("has_children"):
      for c in get_children(block["id"]):
        child_md, img_idx = block_to_md(c, post_slug, img_idx, depth)
        md += child_md

  # =========================
  # table → Markdown table
  # =========================
  elif t == "table":
    rows = get_children(block["id"])
    has_header = block["table"].get("has_column_header", False)

    table_md = []

    for i, row in enumerate(rows):
      if row["type"] != "table_row":
        continue

      cells = []
      for cell in row["table_row"]["cells"]:
        cell_md = rich_text_to_md(cell).replace("\n", "<br>")
        cell_md = cell_md.strip()
        cells.append(cell_md)

      table_md.append("| " + " | ".join(cells) + " |")

      if i == 0 and has_header:
        col_count = len(cells)
        sep = "|" + "|".join([":--"] * col_count) + "|"
        table_md.append(sep)

    md += "\n" + "\n".join(table_md) + "\n\n"
    return md, img_idx

  # children (재귀)
  if block.get("has_children") and t not in ("callout", "table"):
    for c in get_children(block["id"]):
      child_md, img_idx = block_to_md(c, post_slug, img_idx, depth + 1)
      md += child_md

  return md, img_idx

# ==================================================
# Status update
# ==================================================
def update_status_done(page_id, status_prop):
  key = "select" if status_prop["type"] == "select" else "status"
  notion.pages.update(
    page_id=page_id,
    properties={PROPS["status"]: {key: {"name": CONFIG["status_done"]}}}
  )

# ==================================================
# Property helpers
# ==================================================
def get_status(props):
  status_prop = props.get(PROPS["status"])
  if not status_prop:
    return None, None
  if status_prop["type"] == "select" and status_prop["select"]:
    return status_prop["select"]["name"], status_prop
  if status_prop["type"] == "status" and status_prop["status"]:
    return status_prop["status"]["name"], status_prop
  return None, status_prop


def get_title(props):
  for prop in props.values():
    if prop.get("type") == "title":
      return "".join(t["plain_text"] for t in prop["title"]).strip()
  return ""


def get_select(props, key, default=""):
  prop = props.get(PROPS[key])
  if prop and prop.get("type") == "select" and prop.get("select"):
    return prop["select"]["name"]
  return default

# ==================================================
# Page process
# ==================================================
def process_page(page, force=False):
  # force=False : DB 모드 (상태가 완료가 아닌 페이지만)
  # force=True  : URL 모드 (상태와 관계없이 변환)
  props = page["properties"]
  status, status_prop = get_status(props)

  if not force and (not status or status == CONFIG["status_done"]):
    return

  # [기존 데이터 추출]
  title = get_title(props)
  date_prop = props.get(PROPS["date"])
  if date_prop and date_prop.get("date"):
    date = date_prop["date"]["start"]
  else:
    # 작성일이 비어 있으면 페이지 생성 시각으로 대체
    date = page["created_time"]
  category = get_select(props, "category", "Notion")
  tags_prop = props.get(PROPS["tags"])
  tags = [t["name"] for t in tags_prop["multi_select"]] if tags_prop else []

  # ==================================================
  # 1. 추가 속성 추출 (Series, Step)
  # ==================================================
  # series가 'select' 타입일 경우
  series = get_select(props, "series")

  # step이 'number' 타입일 경우
  step = 0
  step_prop = props.get(PROPS["step"])
  if step_prop and step_prop.get("number") is not None:
    step = step_prop["number"]
  # ==================================================

  post_slug = slugify(title)
  cat_slug = slugify(category)

  existing = find_post_by_notion_id(page["id"])
  if existing:
    # R14 : 기존 파일 이름을 유지해서 URL이 바뀌지 않게 함
    path = existing
  else:
    os.makedirs(os.path.join(POSTS_DIR, cat_slug), exist_ok=True)
    filename = f"{date[:10]}-{post_slug}.md"
    path = os.path.join(POSTS_DIR, cat_slug, filename)

  # ==================================================
  # 2. Front Matter에 반영 (layout, series, step 추가)
  # ==================================================
  front = {
    "title": title,
    "date": date,
    "categories": [category],
    "tags": tags,
    "toc": True,
    "toc_sticky": True,
    "series": series,   # 추가
    "step": step,       # 추가
    "layout": "single",
    "notion_id": normalize_id(page["id"])
  }

  content = "---\n" + yaml.dump(front, allow_unicode=True) + "---\n\n"

  img_idx = 1
  for b in get_children(page["id"]):
    md, img_idx = block_to_md(b, post_slug, img_idx)
    content += md

  content = normalize_markdown(content)

  with open(path, "w", encoding="utf-8") as f:
    f.write(content)

  if status_prop and status != CONFIG["status_done"]:
    update_status_done(page["id"], status_prop)
  action = "Updated" if existing else "Uploaded"
  print(f"✔ {action}: {path}")
  return path

# ==================================================
# Modes
# ==================================================
def run_database():
  if not DATABASE_ID:
    raise SystemExit("NOTION_DB_ID 가 없습니다 (DB 모드)")
  cursor = None
  while True:
    Kwargs = {"database_id": DATABASE_ID}
    if cursor:
      Kwargs["start_cursor"] = cursor
    res = notion.databases.query(**Kwargs)
    for p in res["results"]:
      process_page(p)
    if not res.get("has_more"):
      break
    cursor = res["next_cursor"]


def run_page(url):
  page = notion.pages.retrieve(page_id=page_id_from_url(url))
  return process_page(page, force=True)


def run_queue(queue_dir):
  # _notion_queue/*.yml 을 처리하고, 성공한 요청 파일은 삭제
  Failed = []
  for req_path in sorted(glob.glob(os.path.join(queue_dir, "*.yml"))):
    with open(req_path, encoding="utf-8") as f:
      req = yaml.safe_load(f) or {}
    url = req.get("url", "")
    try:
      run_page(url)
      os.remove(req_path)
    except Exception as e:
      print(f"[ERROR] {req_path} ({url}) : {e}")
      Failed.append(req_path)
  if Failed:
    raise SystemExit(f"{len(Failed)}개 요청 실패 : {', '.join(Failed)}")

# ==================================================
# Main
# ==================================================
def main():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("--page", help="Notion 페이지 URL 하나를 변환")
  group.add_argument("--queue", help="요청 파일 폴더 (예 : _notion_queue)")
  args = parser.parse_args()

  if args.page:
    run_page(args.page)
  elif args.queue:
    run_queue(args.queue)
  else:
    run_database()

if __name__ == "__main__":
  main()
