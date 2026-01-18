import re

def convert_to_markdown(input_text: str) -> str:
  """
  BaekjoonHub README.md 내용을
  Jekyll 블로그용 Markdown으로 변환
  """

  # 1. 제목 추출
  title_line = re.search(r'^# (.*)$', input_text, flags=re.MULTILINE)
  title = title_line.group(1).strip() if title_line else ""

  # 2. 문제 링크 추출
  link_line = re.search(r'\[문제 링크\]\((.*?)\)', input_text)
  link = link_line.group(1).strip() if link_line else ""

  # 3. 분류 추출
  category_match = re.search(r'### 분류\s+(.*?)\s+###', input_text, flags=re.DOTALL)
  if not category_match:
    category_match = re.search(r'### 분류\s+(.*)', input_text, flags=re.DOTALL)

  category_text = ""
  if category_match:
    category_text = category_match.group(1).strip()
    category_text = re.split(r'\n#+', category_text)[0].strip()

  # 4. 문제 설명 추출
  desc_match = re.search(r'### 문제 설명\s+(.*?)\s+###', input_text, flags=re.DOTALL)
  if not desc_match:
    desc_match = re.search(r'### 문제 설명\s+(.*)', input_text, flags=re.DOTALL)

  desc_text = ""
  if desc_match:
    desc_text = desc_match.group(1).strip()
    desc_text = re.split(r'\n#+', desc_text)[0].strip()
    desc_text = desc_text.replace("<p>", "").replace("</p>", "")

  # 5. 입력 설명 추출
  input_match = re.search(r'### 입력\s+(.*?)\s+###', input_text, flags=re.DOTALL)
  if not input_match:
    input_match = re.search(r'### 입력\s+(.*)', input_text, flags=re.DOTALL)

  input_desc = ""
  if input_match:
    input_desc = input_match.group(1).strip()
    input_desc = re.split(r'\n#+', input_desc)[0].strip()
    input_desc = input_desc.replace("<p>", "").replace("</p>", "")

  # 6. 출력 설명 추출
  output_match = re.search(r'### 출력\s+(.*)', input_text, flags=re.DOTALL)

  output_desc = ""
  if output_match:
    output_desc = output_match.group(1).strip()
    output_desc = re.split(r'\n#+', output_desc)[0].strip()
    output_desc = output_desc.replace("<p>", "").replace("</p>", "")

  # 7. 최종 Markdown 생성
  markdown_text = f"""---
layout: single
title: ""
categories:
tag: []
---

[문제 링크]({link})

---

#### 분류 🗂️

  - {category_text}

#### 문제 설명 📄

  - {desc_text}

#### 입력 ⬅️

  - {input_desc}

#### 출력 ➡️

  - {output_desc}
"""

  return markdown_text
