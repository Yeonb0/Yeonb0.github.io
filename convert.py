import sys
import re
import pyperclip

def convert_to_markdown(input_text: str) -> str:
    """
    문제 설명 텍스트를 받아, 
    ---
    layout: single
    title: ""
    categories:
    tag: []
    ---
    # [제목]

    [문제 링크](...)

    - 성능 요약
      - 메모리: ...
      - 시간: ...
    ...
    와 같은 형태로 출력하는 함수
    """
    # 1. 제목 추출
    title_line = re.search(r'^# (.*)$', input_text, flags=re.MULTILINE)
    title = title_line.group(1).strip() if title_line else ""

    # 2. 문제 링크 추출
    link_line = re.search(r'\[문제 링크\]\((.*?)\)', input_text)
    link = link_line.group(1).strip() if link_line else ""

# ###
#     # 3. 성능 요약 추출
#     performance_match = re.search(r'### 성능 요약\s+(.*?)\s+###', input_text, flags=re.DOTALL)
#     if not performance_match:
#         performance_match = re.search(r'### 성능 요약\s+(.*)', input_text, flags=re.DOTALL)

#     performance_text = ""
#     if performance_match:
#         # 다음 섹션(#, ### 등) 앞까지만
#         performance_text = performance_match.group(1).strip()
#         performance_text = re.split(r'\n#+', performance_text)[0].strip()
#         # 여기서 쉼표(`,`)로 분할 후 각 항목을 줄바꿈 처리
#         # 예) "메모리: 2020 KB, 시간: 0 ms" → "- 메모리: 2020 KB  \n- 시간: 0 ms"
#         items = [i.strip() for i in performance_text.split(',')]
#         # "- " 붙이고 줄바꿈은 "두 칸 공백 + 줄바꿈"으로
#         # Markdown에서 "두 칸 공백 + 엔터" → 강제 줄바꿈
#         performance_text = "  - " + "  \n  - ".join(items)
# ###

    # 4. 분류 추출
    category_match = re.search(r'### 분류\s+(.*?)\s+###', input_text, flags=re.DOTALL)
    if not category_match:
        category_match = re.search(r'### 분류\s+(.*)', input_text, flags=re.DOTALL)
    category_text = ""
    if category_match:
        category_text = category_match.group(1).strip()
        category_text = re.split(r'\n#+', category_text)[0].strip()
        # 쉼표 구분 시, 여기서도 마찬가지로 가공 가능

    # 5. 문제 설명 추출
    desc_match = re.search(r'### 문제 설명\s+(.*?)\s+###', input_text, flags=re.DOTALL)
    if not desc_match:
        desc_match = re.search(r'### 문제 설명\s+(.*)', input_text, flags=re.DOTALL)
    desc_text = ""
    if desc_match:
        desc_text = desc_match.group(1).strip()
        desc_text = re.split(r'\n#+', desc_text)[0].strip()
        desc_text = desc_text.replace("<p>", "").replace("</p>", "")

    # 6. 입력 설명 추출
    input_match = re.search(r'### 입력\s+(.*?)\s+###', input_text, flags=re.DOTALL)
    if not input_match:
        input_match = re.search(r'### 입력\s+(.*)', input_text, flags=re.DOTALL)
    input_desc = ""
    if input_match:
        input_desc = input_match.group(1).strip()
        input_desc = re.split(r'\n#+', input_desc)[0].strip()
        input_desc = input_desc.replace("<p>", "").replace("</p>", "")

    # 7. 출력 설명 추출
    output_match = re.search(r'### 출력\s+(.*)', input_text, flags=re.DOTALL)
    output_desc = ""
    if output_match:
        output_desc = output_match.group(1).strip()
        output_desc = re.split(r'\n#+', output_desc)[0].strip()
        output_desc = output_desc.replace("<p>", "").replace("</p>", "")

    # 최종 결과
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


if __name__ == "__main__":
    print("=== Markdown 변환기 ===")
    print("'s'를 입력하면 지금까지 입력된 내용을 변환합니다.")
    print("'exit'를 입력하면 프로그램이 종료됩니다.\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            # Ctrl+Z(Win) / Ctrl+D(Unix) 로 EOF 주어지면 종료
            break
        
        # exit 명령 처리
        if line.strip().lower() == 'exit':
            print("프로그램을 종료합니다.")
            sys.exit(0)
        
        # s 입력 시 변환 시작
        if line.strip().lower() == 's':
            # 변환할 텍스트 생성
            input_text = "\n".join(lines).strip()
            
            if not input_text:
                print("[입력 없음] 아무 텍스트도 변환되지 않았습니다.\n")
            else:
                # 변환
                result = convert_to_markdown(input_text)
                
                # 출력
                print("\n=== 변환 결과 ===")
                print(result)
                
                # 클립보드 복사
                pyperclip.copy(result)
                print("\n[자동 복사 완료] 변환된 텍스트가 클립보드에 복사되었습니다.")
                print("=" * 50 + "\n")
            
            # 변환 후, 리스트 초기화
            lines.clear()
        
        else:
            # 일반 텍스트는 계속 누적
            lines.append(line)
