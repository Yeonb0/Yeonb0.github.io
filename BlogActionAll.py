import os
import re
from datetime import datetime
from github import Github
from convert import convert_to_markdown

GITHUB_TOKEN = os.environ["BLOG_TOKEN"]
REPO_NAME = "Yeonb0/Code-Practice"
BLOG_REPO = "Yeonb0/Yeonb0.github.io"
BASE_PATH = "백준"
OUTPUT_DIR = "generated"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_problem_info(folder_name: str, tier: str):
  # "10093. 숫자" -> ("10093", "숫자")
  num, title = folder_name.split(".", 1)
  return tier, num.strip(), title.strip()

def extract_tags_from_readme(readme: str):
  tags = set()

  match = re.search(r"### 분류\s+(.*)", readme)
  if match:
    raw = match.group(1)
    raw = re.split(r"\n#+", raw)[0]
    for t in raw.split(","):
      t = t.strip()
      if t:
        tags.add(t)

  tags.add("C++")
  return sorted(tags)

def main():
  g = Github(GITHUB_TOKEN)
  repo = g.get_repo(REPO_NAME)
  blog_repo = g.get_repo(BLOG_REPO)

  today = datetime.now().strftime("%Y-%m-%d")

  # 이미 블로그에 있는 문제 번호 (중복 방지)
  existing = set()
  posts = blog_repo.get_contents("_posts")
  for p in posts:
    if "boj-" in p.name:
      try:
        existing.add(p.name.split("boj-")[1].split(".")[0])
      except:
        pass

  tiers = repo.get_contents(BASE_PATH)

  for tier in tiers:
    if tier.type != "dir":
      continue

    tier_name = tier.name
    problems = repo.get_contents(tier.path)

    for problem_dir in problems:
      if problem_dir.type != "dir":
        continue

      tier_name, problem_number, problem_title = extract_problem_info(
        problem_dir.name, tier_name
      )

      if problem_number in existing:
        continue

      files = repo.get_contents(problem_dir.path)

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
        f"categories:\n  - BOJ\n  - {tier_name}"
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
