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
IMAGE_DIR = "assets/images/notion"

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

notion = Client(auth=NOTION_TOKEN)

# ==================================================
# 유틸
# ==================================================
def slugify(text: str) -> str:
  return text.strip().replace(" ", "-").lower()

# ==================================================
# 이미지 다운로드
# ==================================================
def download_image(url, name):
  ext = url.split("?")[0].split(".")[-1]
  filename = f"{name}.{ext}"
  path = os.path.join(IMAGE_DIR, filename)

  if not os.path.exists(path):
    r = requests.get(url)
    r.raise_for_status()
    with open(path, "wb") as f:
      f.write(r.content)

  return f"/{IMAGE_DIR}/{filename}"

# ==================================================
# 블록 → Markdown
# ==================================================
def block_to_md(block, page_id):
  t = block["type"]

  if t == "paragraph":
    text = "".join(x["plain_text"] for x in block[t]["rich_text"])
    return text + "\n\n"

  if t == "heading_1":
    return "# " + block[t]["rich_text"][0]["plain_text"] + "\n\n"

  if t == "heading_2":
    return "## " + block[t]["rich_text"][0]["plain_text"] + "\n\n"

  if t == "heading_3":
    return "### " + block[t]["rich_text"][0]["plain_text"] + "\n\n"

  if t == "code":
    lang = block[t]["language"]
    code = block[t]["rich_text"][0]["plain_text"]
    return f"```{lang}\n{code}\n```\n\n"

  if t == "image":
    img = block[t]["image"]
    url = img["file"]["url"] if img["type"] == "file" else img["external"]["url"]
    img_path = download_image(url, f"{page_id}_{block['id']}")
    return f"![]({img_path})\n\n"

  if t == "bulleted_list_item":
    return "- " + block[t]["rich_text"][0]["plain_text"] + "\n"

  if t == "numbered_list_item":
    return "1. " + block[t]["rich_text"][0]["plain_text"] + "\n"

  return ""

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
# 페이지 처리 (🔥 핵심)
# ==================================================
def process_page(page):
  props = page["properties"]

  # ----------------------
  # 상태 안전 처리 (Select + Status)
  # ----------------------
  status_prop = props.get("상태")
  if not status_prop:
    return

  status_value = None

  if status_prop["type"] == "select" and status_prop["select"]:
    status_value = status_prop["select"]["name"]

  elif status_prop["type"] == "status" and status_prop["status"]:
    status_value = status_prop["status"]["name"]

  if status_value != "진행중":
    return

  # ----------------------
  # 필수 필드 체크
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

  # ----------------------
  # 카테고리 폴더
  # ----------------------
  safe_category = slugify(category)
  category_dir = os.path.join(POSTS_DIR, safe_category)
  os.makedirs(category_dir, exist_ok=True)

  filename = f"{date_prefix}-{slugify(title)}.md"
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
  # 본문
  # ----------------------
  blocks = notion.blocks.children.list(page["id"])["results"]
  for block in blocks:
    content += block_to_md(block, page["id"])

  # ----------------------
  # 파일 생성 + 상태 변경
  # ----------------------
  try:
    with open(file_path, "w", encoding="utf-8") as f:
      f.write(content)

    update_status_done(page["id"])
    print(f"✔ Uploaded: {safe_category}/{filename}")

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
