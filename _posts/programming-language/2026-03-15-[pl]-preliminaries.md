---
categories:
- Programming-Language
date: '2026-03-15T20:00:00.000+09:00'
tags: []
title: '[PL] Preliminaries'
toc: true
toc_sticky: true
---

## ✦ 프로그래밍 언어를 공부해야 하는 이유


- 표현 능력의 확장 
  - 어휘력 (기능) 을 많이 알아야 내 idea 잘 표현 가능
- 어떤 특정 기능 위한 언어 → 내 분야 맞는 언어 선택 가능
ex) FORTRAN → 과학 계산용 언어 
계산 by user or compiler 차이

- 새로운 언어 배우기 쉬움
- 구현 방식 더 잘 이해 → 언어의 효율적 사용
ex) 대부분 함수는 subprogram (함수) 기능 有
parameter 이동 overhead 알면 더 효율적인 코드 만들 수 있음

- 컴퓨팅 전체의 발전

## ✦ 프로그래밍 분야


- 어떤 영역에서 어떤 프로그래밍 언어 사용?
1. 과학 계산 : floating point 계산
ex) FORTRAN

1. Business 영역 : 10진수 처리, 복잡한 입출력
ex) COBOL

1. AI : Symbol 처리
ex) LISP, PROLOG → 현재는 사용하지 않음

1. System Programming : 하드웨어 제어 위한 bit 단위 operation
ex) C
→ 사실 high-level 은 bit & memory 접근 하지 않기 위한 것. 그러나 OS 작성 위한 언어 필요성 때문에 만들어짐

1. Web Software : Dynamic 한 content
ex) Javascript
→ 웹 브라우저 안에 interpreter 내장. Wep OS 에서 돌아가는 Wep App

## ✦ 프로그래밍 언어 평가 기준


### ◆ Readability (가독성)


→ 얼마나 쉽게 읽고 이해할 수 있는가?

- Simplicity (단순성)
  - 기본 구성 요소 (기능) 적을 수록 이해 쉬움
    - 가장 simple 한 언어 → Assembly (기능이 적음)
  - Feature Multiplicity : 같은 기능 수행 방법 여러 개 → 가독성 ↓
ex) 

{% raw %}
```c
count++
++count
count += 1
count = count + 1
```
{% endraw %}

  - Operator Overloading : 같은 연산자에 여러 개의 기능
ex) `+` : 정수 덧셈, 실수 덧셈, 문자열 더하기 등
→ 기계어에선 동작 방법 다 다름. but 개념적으로는 동일. simple 하게 디자인하기 위해 똑같은 symbol 사용

ex) C언어에서 `&` → 잘못된 사용

{% raw %}
```c
a = &b; // 주소 가져오기
a = a & b; // and operation
```
{% endraw %}

- Orthogonality (직교성)
  - 기능이 겹치지 않음. 똑같은 기능을 여러 언어로 표현 X
  - `if` 와 `switch` 는 orthogonal 하지 않음 (같은 조건 제어문)
  - data type 과 control 은 orthogonal.
data + control 조합 했을 때 예외 발생 X 해야 함
- Control Statement (제어문)
  - Von-neumann 구조 → 위에서 아래로 자연스러운 흐름 
  - GOTO-less : jump 하는 구조. 최대한 적게 사용. but 아주아주 급하면 사용 가능
  - Structured Programming : goto-less, 들어오는 곳 1, 나가는 곳 1
- Data Types & Structures
  - 데이터 표현 명확할 수록 가독성 ↑
ex) boolean → C언어에는 존재 X, 오류 많이 발생

- Syntax Consideration (문법 고려)
  - 이름 규칙 : `_` 허용?
  - block 규칙 : `{}` 사용? `end_loop` 사용? 들여쓰기로 표현?
  - 생긴 모양이 비슷해야 함

### ◆ Writability (작성 용이성)


→ 얼마나 쉽게 표현할 수 있는가?

- Simplicity & Orthogonality
- Abstraction (추상화) : 속내용 감추기
  - 사용하는 사람들이 내부 내용 모르고도 사용할 수 있도록
  - Process Abstraction : Subprogram 
→ 함수 내부 구현 모르고 사용
  - Data Abstraction : 실제로 데이터가 어떻게 저장되어 있는지 모름
- Expressivity : 기능 많으면 Writability 에선 좋을 수 있음 → 계산 간결히 표현
ex) 

{% raw %}
```c
count++
count = count + 1
```
{% endraw %}

### ◆ Reliability (신뢰성)


→ 신뢰도 있는 프로그램인가?

어떤 조건 하에서도 프로그램이 잘 돌아가도록

- Type Checking : 피연산자 타입이 다르면?
ex) C 는 Type Checking X, Pascal 은 배열 범위 검사 제공

- Exception Handling 
ex) 0으로 나누기, 메모리 부족 등

  - run-time error 잡기 (dynamic) ↔ compile 단계에서 하는 것 (static)
  - data binding → 용도에 따라
    - static : 컴파일 할때 (C)
      - 융통성 ↓, 속도 ↑ 
    - dynamic : 일단 변수 설정, 실제 run-time 에서 입력 시 저장 공간 설정 (Java, Python)
      - 융통성 ↑, 속도 ↓ 
- Aliasing : 같은 저장 공간에 대해 여러 이름 가짐
  - debugging 어려움 → 위험함

### ◆ Cost (비용)


- 프로그래머 교육 비용
- 프로그램 작성 비용
- 컴파일 비용
- 실행 비용
- 유지보수 비용

### ◆ Portability


- 얼마나 많은 플랫폼에 compiler 존재?

### ◆ Generality


- 얼마나 많은 기능, 분야 커버 가능?
  - but 너무 많은 기능 → compile 시간 오래 걸림

### ◆ Well-definedness


- 언어 문서화 얼마나 잘 되어 있음?

## ✦ 언어 설계에 영향 미친 요소


### ◆ Computer Architecture


- Imperative Language (명령형 언어) 
  - von-Neumann 컴퓨터 구조(하드웨어)
    - Memory, ALU, Control Unit, Input/Output
    - Memory 에서 변수 가져와 ALU 에서 계산 후 다시 Memory 로
→ word 단위
![](/assets/images/notion/[pl]-preliminaries/img_1.png)

  - 명령어 & 데이터 같은 메모리에 저장

| 하드웨어 | 언어 |
| Memory cell | Variable |
| Store Operation | Assignment |
| Arithmetic Operation | Expression |
| Conditional Jump | Loop / If |

→ 프로그램은 하드웨어가 동작하는 시나리오. 하드웨어와 연결해서 생각

### ◆ Programming Methodologies


- Subroutine 은 하드웨어랑 관계 없음
→ 프로그래밍 방법론으로 관리
- 프로그래머가 코드를 잘 짤 수 있도록 언어의 기능 추가
1. Structured Programming (goto-less)
  - top-down 디자인 : 큰 프로그램을 잘라서 만들자
→ 자르는 기준?
  - Procedure-oriented programming (함수 지향 프로그래밍) 
    - task 중심으로 나눔
1. Data-Oriented Programming 
  - data 중심으로 나눔
  - data abstraction 기능
class, record, subroutine, array 등
> 🗣 

  - CISC (Computer Instruction Set Computer) 
    - ISA 가 복잡 & 다양한 CPU 구조
    - 초기 컴퓨터 (60 ~ 70년대)
→ 너무 복잡!

  - RISC (Reduced Instruction Set Computer)
    - ISA 단순하게 만든 CPU 구조
    - 80년대 이후
    - ISA 갯수 줄이고 register 갯수 늘림
→ 빨리 빨리 수행 & 조합

1. Object-Oriented Programming
  - data abstraction + encapsulation + dynamic type binding
1. Process-Oriented Programming 
  - Concurrency
> 🗣 메모리 계층 : register / memory / disk

- speed ↔ cost trade-off
- cache : 자주 참조하는 것을 근처에
- buffer : 속도 차이 해결

## ✦ 언어 설계 Trade-Off


- Reliability ↔ Execution cost
ex) Run-time type checking

- Compactness ↔ Readability
- Flexibility ↔ Safety
ex) C의 pointer

- Flexibility ↔ Efficiency
ex) Dynamic typing

## ✦ 언어 구현 방법


- 하드웨어는 오로지 machine language (기계어) 만 이해
- 가상 머신 (virtual machine) : 실제로 존재하지 않지만, 있는 것처럼 보이는 기계
ex) C 가상 머신 : C로 명령하면 이해
ex) JVM (Java Virtual Machine)

  - 하드웨어를 시뮬레이션 하는 인터페이스

### ◆ Compilation (컴파일)


    - 소스 코드 → 전체 기계어로 번역 → 실행
      - 번역 후에는 실행 빠름
      - ex) C, COBOL, Ada
![](/assets/images/notion/[pl]-preliminaries/img_2.png)

### ◆ Hybrid Implementation System


    - source → 중간 언어 (intermediate language) 로 번역 → byte code 를 interpreting
ex) Java

![](/assets/images/notion/[pl]-preliminaries/img_3.png)

### ◆ Interpretation (인터프리트)


- source 번역하지 않고 한 줄씩 기계어로 번역해 실행
  - 실행 느림
  - 기계어로 번역이 어려울 때 & dynamic binding 이 많을때
  - ex) python


- 언어 & 구현 방법은 따로 생각 
→ C 로 interpreting, python 으로 compile 가능. 얼마나 쉽게 구현 가능한가의 차이

## ✦ 개발 환경


- IDE : Integrated Development Environment
- 통합 개발 환경
ex) VS Studio, Eclipse
