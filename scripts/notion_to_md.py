import os
import re
import requests
import yaml
from notion_client import Client

# ==================================================
# ENV
# ==================================================
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DB_ID"]

POSTS_DIR = "_posts"
IMAGE_BASE_DIR = "assets/images/notion"

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGE_BASE_DIR, exist_ok=True)

notion = Client(auth=NOTION_TOKEN)

# ==================================================
# Utils
# ==================================================
def slugify(text: str) -> str:
  return (
    text.strip()
    .lower()
    .replace(" ", "-")
    .replace("/", "-")
  )

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
  - heading 위/아래 공백 보장
  - 4칸 이상 들여쓴 리스트를 2칸 단위로 정규화
  - 코드블록 내부는 건드리지 않음
  """
  lines = content.splitlines()
  out = []

  heading_re = re.compile(r"^#{1,6}\s+")
  list_re = re.compile(r"^\s*([-*+]\s+|\d+[.)]\s+)")
  indent_list_re = re.compile(r"^(\s+)([-*+]\s+|\d+[.)]\s+)")

  in_code_block = False

  for line in lines:

    # ----------------------------------------
    # fenced code block 감지
    # ----------------------------------------
    if line.strip().startswith("```"):
      in_code_block = not in_code_block
      out.append(line)
      continue

    if in_code_block:
      out.append(line)
      continue

    # ----------------------------------------
    # heading 위/아래 공백 보장
    # ----------------------------------------
    if heading_re.match(line):
      if out and out[-1].strip() != "":
        out.append("")
      out.append(line)
      out.append("")
      continue

    # ----------------------------------------
    # 4칸 이상 들여쓴 리스트 정규화
    # ----------------------------------------
    m = indent_list_re.match(line)
    if m:
      spaces = len(m.group(1))
      bullet = m.group(2)
      rest = line[m.end():]

      # 2칸 단위 depth 계산
      depth = spaces // 2
      depth = max(1, depth)   # 최소 depth 1

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
  
  # ==================================================
  # ✅ heading 처리 (공백 완전 정리 + bold 안전 처리)
  # ==================================================
  elif t.startswith("heading_"):
    text = rich_text_to_md(block[t]["rich_text"])

    # 🔥 공백 완전 정리
    text = text.replace("\u00A0", " ")      # non-breaking space 제거
    text = text.strip()                     # 앞뒤 공백 제거
    text = re.sub(r"^\s+", "", text)        # 앞쪽 모든 공백 제거
    text = re.sub(r"\s+$", "", text)        # 뒤쪽 모든 공백 제거

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
    code_text = block[t]["rich_text"][0]["plain_text"]  

    md += "{% raw %}\n"
    md += f"```{block[t]['language']}\n"
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

  elif t == "callout":
    callout = block["callout"]
    icon = ""
    if callout.get("icon") and callout["icon"]["type"] == "emoji":
      icon = callout["icon"]["emoji"] + " "

    text = rich_text_to_md(callout["rich_text"])
    md += f"> {icon}{text}\n"

    if block.get("has_children"):
      for c in get_children(block["id"]):
        child_md, img_idx = block_to_md(c, post_slug, img_idx, depth)
        for line in child_md.splitlines():
          if line.strip():
            md += f"> {line}\n"
        md += "\n"

  # =========================
  # 📊 table → Markdown table
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

      # 🔥 항상 왼쪽 정렬 + 들여쓰기 제거
      table_md.append("| " + " | ".join(cells) + " |")

      # 🔥 헤더 구분선 → |:--| 형태로 생성
      if i == 0 and has_header:
        col_count = len(cells)
        sep = "|" + "|".join([":--"] * col_count) + "|"
        table_md.append(sep)

    # 🔥 표는 항상 왼쪽에 붙여 출력
    md += "\n" + "\n".join(table_md) + "\n\n"

    return md, img_idx
  # ==================================================

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
    properties={"상태": {key: {"name": "완료"}}}
  )

# ==================================================
# Page process
# ==================================================
def process_page(page):
  props = page["properties"]
  status_prop = props.get("상태")

  status = None
  if status_prop:
    if status_prop["type"] == "select" and status_prop["select"]:
      status = status_prop["select"]["name"]
    elif status_prop["type"] == "status" and status_prop["status"]:
      status = status_prop["status"]["name"]

  if not status or status == "완료":
    return

  title = props["이름"]["title"][0]["plain_text"]
  date = props["작성일"]["date"]["start"]
  category = props["카테고리"]["select"]["name"]
  tags = [t["name"] for t in props["태그"]["multi_select"]]

  post_slug = slugify(title)
  cat_slug = slugify(category)

  os.makedirs(os.path.join(POSTS_DIR, cat_slug), exist_ok=True)
  filename = f"{date[:10]}-{post_slug}.md"
  path = os.path.join(POSTS_DIR, cat_slug, filename)

  front = {
    "title": title,
    "date": date,
    "categories": [category],
    "tags": tags,
    "toc": True,
    "toc_sticky": True
  }

  content = "---\n" + yaml.dump(front, allow_unicode=True) + "---\n\n"

  img_idx = 1
  for b in get_children(page["id"]):
    md, img_idx = block_to_md(b, post_slug, img_idx)
    content += md

  content = normalize_markdown(content)

  with open(path, "w", encoding="utf-8") as f:
    f.write(content)

  update_status_done(page["id"], status_prop)
  print(f"✔ Uploaded: {cat_slug}/{filename}")

# ==================================================
# Main
# ==================================================
def main():
  pages = notion.databases.query(database_id=DATABASE_ID)["results"]
  for p in pages:
    process_page(p)

if __name__ == "__main__":
  main()
