import os
import requests
import yaml
from datetime import datetime
from notion_client import Client

# ==================================================
# 환경 변수
# ==================================================
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DB_ID"]

POSTS_DIR = "_posts"
IMAGE_BASE_DIR = "assets/images/notion"

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGE_BASE_DIR, exist_ok=True)

notion = Client(auth=NOTION_TOKEN)

# ==================================================
# 유틸
# ==================================================
def slugify(text: str) -> str:
  return (
    text.strip()
    .lower()
    .replace(" ", "-")
    .replace("/", "-")
  )

# ==================================================
# 이미지 다운로드 (글별 폴더)
# ==================================================
def download_image(url, post_slug, image_name):
  headers = {
    "User-Agent": "Mozilla/5.0 (GitHub Actions Notion Sync)",
    "Accept": "*/*"
  }

  try:
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
  except Exception:
    print(f"[WARN] Image download failed: {url}")
    return None

  content_type = r.headers.get("Content-Type", "")
  ext = "png"

  if "jpeg" in content_type or "jpg" in content_type:
    ext = "jpg"
  elif "png" in content_type:
    ext = "png"
  elif "gif" in content_type:
    ext = "gif"

  post_image_dir = os.path.join(IMAGE_BASE_DIR, post_slug)
  os.makedirs(post_image_dir, exist_ok=True)

  filename = f"{image_name}.{ext}"
  path = os.path.join(post_image_dir, filename)

  with open(path, "wb") as f:
    f.write(r.content)

  return f"/{IMAGE_BASE_DIR}/{post_slug}/{filename}"

# ==================================================
# Notion 블록 페이지네이션 (🔥 글 안 짤림)
# ==================================================
def get_all_blocks(block_id):
  blocks = []
  cursor = None

  while True:
    response = notion.blocks.children.list(
      block_id=block_id,
      start_cursor=cursor
    )

    blocks.extend(response["results"])

    if not response["has_more"]:
      break

    cursor = response["next_cursor"]

  return blocks

# ==================================================
# 블록 → Markdown
# ==================================================
def block_to_md(block, page_id, post_slug, img_index):
  t = block["type"]

  if t == "paragraph":
    text = "".join(x["plain_text"] for x in block[t]["rich_text"])
    return text + "\n\n", img_index

  if t == "heading_1":
    return "# " + block[t]["rich_text"][0]["plain_text"] + "\n\n", img_index

  if t == "heading_2":
    return "## " + block[t]["rich_text"][0]["plain_text"] + "\n\n", img_index

  if t == "heading_3":
    return "### " + block[t]["rich_text"][0]["plain_text"] + "\n\n", img_index

  if t == "code":
    lang = block[t]["language"]
    code = block[t]["rich_text"][0]["plain_text"]
    return f"```{lang}\n{code}\n```\n\n", img_index

  if t == "bulleted_list_item":
    return "- " + block[t]["rich_text"][0]["plain_text"] + "\n", img_index

  if t == "numbered_list_item":
    return "1. " + block[t]["rich_text"][0]["plain_text"] + "\n", img_index

  if t == "image":
    img = block["image"]

    # Notion 내부 이미지 → 글별 폴더에 저장
    if img["type"] == "file":
      url = img["file"]["url"]
      img_path = download_image(
        url,
        post_slug,
        f"img_{img_index}"
      )
      img_index += 1

      if img_path:
        return f"![]({img_path})\n\n", img_index
      return "", img_index

    # 외부 이미지 → URL 그대로
    if img["type"] == "external":
      return f"![]({img['external']['url']})\n\n", img_index

  return "", img_index

# ==================================================
# 상태 → 완료
# ==================================================
def update_status_done(page_id):
  notion.pages.update(
    page_id=page_id,
    properties={
      "상태": {
        "select": {
          "name": "완료"
        }
      }
    }
  )

# ==================================================
# 페이지 처리
# ==================================================
def process_page(page):
  props = page["properties"]

  # ----------------------
  # 상태 처리 (Select / Status)
  # ----------------------
  status_prop = props.get("상태")
  status_value = None

  if status_prop:
    if status_prop["type"] == "select" and status_prop["select"]:
      status_value = status_prop["select"]["name"]
    elif status_prop["type"] == "status" and status_prop["status"]:
      status_value = status_prop["status"]["name"]

  if not status_value or status_value == "완료":
    return

  # ----------------------
  # 필수 필드
  # ----------------------
  if not props["이름"]["title"]:
    return
  if not props["작성일"]["date"]:
    return
  if not props["카테고리"]["select"]:
    return

  title = props["이름"]["title"][0]["plain_text"]
  date_str = props["작성일"]["date"]["start"]
  category = props["카테고리"]["select"]["name"]
  tags = [t["name"] for t in props["태그"]["multi_select"]]

  date_obj = datetime.fromisoformat(date_str)
  date_prefix = date_obj.strftime("%Y-%m-%d")

  post_slug = slugify(title)
  category_slug = slugify(category)

  # ----------------------
  # 카테고리 폴더
  # ----------------------
  category_dir = os.path.join(POSTS_DIR, category_slug)
  os.makedirs(category_dir, exist_ok=True)

  filename = f"{date_prefix}-{post_slug}.md"
  file_path = os.path.join(category_dir, filename)

  # ----------------------
  # Front Matter
  # ----------------------
  front_matter = {
    "title": title,
    "date": date_str,
    "categories": [category],
    "tags": tags,
    "toc": True,
    "toc_sticky": True
  }

  content = "---\n"
  content += yaml.dump(front_matter, allow_unicode=True)
  content += "---\n\n"

  # ----------------------
  # 본문 (페이지네이션 + 이미지 분리)
  # ----------------------
  blocks = get_all_blocks(page["id"])
  img_index = 1

  for block in blocks:
    md, img_index = block_to_md(block, page["id"], post_slug, img_index)
    content += md

  # ----------------------
  # 파일 생성 + 상태 변경
  # ----------------------
  try:
    with open(file_path, "w", encoding="utf-8") as f:
      f.write(content)

    update_status_done(page["id"])
    print(f"✔ Uploaded: {category_slug}/{filename}")

  except Exception as e:
    print(f"❌ Failed: {title}")
    print(e)

# ==================================================
# 메인
# ==================================================
def main():
  pages = notion.databases.query(database_id=DATABASE_ID)["results"]
  for page in pages:
    process_page(page)

if __name__ == "__main__":
  main()
