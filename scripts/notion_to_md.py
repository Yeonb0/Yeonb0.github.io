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

OUTPUT_DIR = "_posts"
IMAGE_DIR = "assets/images/notion"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

notion = Client(auth=NOTION_TOKEN)

HEADERS = {
  "Authorization": f"Bearer {NOTION_TOKEN}",
  "Notion-Version": "2022-06-28"
}

# ==================================================
# 이미지 다운로드
# ==================================================
def download_image(url, name):
  ext = url.split("?")[0].split(".")[-1]
  filename = f"{name}.{ext}"
  path = os.path.join(IMAGE_DIR, filename)

  if not os.path.exists(path):
    r = requests.get(url)
    with open(path, "wb") as f:
      f.write(r.content)

  return f"/{IMAGE_DIR}/{filename}"

# ==================================================
# Notion 블록 → Markdown
# ==================================================
def block_to_md(block, page_id):
  t = block["type"]

  if t == "paragraph":
    text = "".join([x["plain_text"] for x in block[t]["rich_text"]])
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
# 상태 → 완료로 변경
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
  status = props["상태"]["select"]["name"]

  # 진행중만 업로드
  if status != "진행중":
    return

  title = props["이름"]["title"][0]["plain_text"]
  date = props["작성일"]["date"]["start"]
  category = props["카테고리"]["select"]["name"]
  tags = [t["name"] for t in props["태그"]["multi_select"]]

  date_obj = datetime.fromisoformat(date)
  filename = f"{date_obj.strftime('%Y-%m-%d')}-{title.replace(' ', '-').lower()}.md"

  # ----------------------
  # Front Matter
  # ----------------------
  front_matter = {
    "title": title,
    "date": date,
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
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
      f.write(content)

    update_status_done(page["id"])
    print(f"✔ Uploaded & marked done: {title}")

  except Exception as e:
    print(f"❌ Failed: {title}")
    print(e)

# ==================================================
# DB 조회
# ==================================================
def main():
  pages = notion.databases.query(database_id=DATABASE_ID)["results"]
  for page in pages:
    process_page(page)

if __name__ == "__main__":
  main()
