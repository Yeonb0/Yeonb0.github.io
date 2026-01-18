import os
import re
from datetime import datetime
from github import Github
from convert import convert_to_markdown

GITHUB_TOKEN = os.environ["BLOG_TOKEN"]
REPO_NAME = "Yeonb0/Code-Practice"
BLOG_REPO = "Yeonb0/Yeonb0.github.io"
OUTPUT_DIR = "generated"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_problem_info(path: str):
  # 백준/Bronze/10093. 숫자/README.md
  parts = path.split("/")
  tier = parts[1] if len(parts) > 1 else "Unknown"
  for p in parts:
    if "." in p:
      num, title = p.split(".", 1)
      return tier, num.strip(), title.strip()
  return None, None, None

def extract_tags_from_readme(readme: str):
  tags = set()

  # 분류 섹션에서 태그 추출
  match = re.search(r"### 분류\s+(.*)", readme)
  if match:
    raw = match.group(1)
    raw = re.split(r"\n#+", raw)[0]
    for t in raw.split(","):
      tags.add(t.strip())

  tags.add("C++")
  return sorted(tags)

def main():
  g = Github(GITHUB_TOKEN)
  repo = g.get_repo(REPO_NAME)
  blog_repo = g.get_repo(BLOG_REPO)

  today = datetime.now().strftime("%Y-%m-%d")

  # 이미 블로그에 있는 문제 번호 (중복 방지)
  existing = set()
  for p in blog_repo.get_contents("_posts"):
    if "boj-" in p.name:
      try:
        existing.add(p.name.split("boj-")[1].split(".")[0])
      except:
        pass

  with open("changed.txt", encoding="utf-8") as f:
    changed = f.readlines()

  processed = set()

  for line in changed:
    line = line.strip()

    if not line.startswith("백준/"):
      continue

    tier, problem_number, problem_title = extract_problem_info(line)
    if not problem_number:
      continue

    if problem_number in processed or problem_number in existing:
      continue

    processed.add(problem_number)

    folder_path = "/".join(line.split("/")[:-1])
    files = repo.get_contents(folder_path)

    readme = None
    code = None

    for f in files:
      if f.name == "README.md":
        readme = f.decoded_content.decode("utf-8")
      elif f.name.endswith(".cc"):
        code = f.decoded_content.decode("utf-8")

    if not readme or not code:
      continue

    tags = extract_tags_from_readme(readme)

    md = convert_to_markdown(readme)

    md = md.replace(
      "categories:",
      f"categories:\n  - BOJ\n  - {tier}"
    )

    md = md.replace(
      "tag: []",
      "tag:\n" + "\n".join([f"  - {t}" for t in tags])
    )

    md = md.replace(
      'title: ""',
      f'title: "[BOJ] {problem_number} - {problem_title}"'
    )

    md += (
      "\n## 💻 코드 (C++)\n\n"
      "```cpp\n"
      f"{code}\n"
      "```\n"
    )

    filename = f"{today}-boj-{problem_number}.md"
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as out:
      out.write(md)

    print(f"[생성 완료] {filename}")

if __name__ == "__main__":
  main()
