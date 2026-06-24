---
categories:
- Programming-Language
date: '2026-06-24T10:38:00.000+09:00'
layout: single
series: 프로그래밍 언어
step: 5
tags:
- 제어문
- 프로그래밍 언어
- PL
title: '[PL] Statement-Level Control Structures'
toc: true
toc_sticky: true
---

## ✦ Introduction


- 제어 흐름 종류
  - 한 문장 내에서 제어 흐름 → 연산자 우선순위 & associativity
  - 문장 (statement) 간 제어 흐름 → 문장 수준의 제어구조
  - unit 간의 제어 흐름 → procedure 호출
- 명령형 언어의 Computation : 오른쪽 계산 후 왼쪽에 저장
- 제어문 종류 
  1. Selector
  1. Loop
→ Single-Entry & Single-Exit

- Compound Statement: 여러 개의 statement 묶은 것
  - block : 여러 statment 묶기 + 변수 선언
  - ex) C언어 (`{}`) / Python (indentation)

## ✦ Selection Statement


- 두 개 이상의 실행 경로 중 하나 선택 수단

### ◆ Two-Way Selection Statements


- 조건식의 형태 & 타입?
  - 대부분 언어 : boolean 표현식
  - C 언어 : arithmetic 표현식 (boolean 없음)
- nested if문 의미?
1. Single-Way Selector 
  - `if` (  ) `then` …
  - FORTRAN : 중첩 허용 X, single statement
  - ALGOL : 여러 statement 선택 가능 (begin ~ end)
1. Two-Way Selector
  - 두 경로 중 하나 선택
  - `if` (  ) `then` … `else` …
1. Nesting Selectors
  - 중첩 선택자의 모호성
{% raw %}
```c
if (sum = 0) then
	if (count = 0)
		then result := 0
else result := 1
```
{% endraw %}

→ 마지막 else 는 어떤 if 와 짝인가?

    - 대부분 언어 : 가장 가까운 짝이 없는 then 절 (count = 0)
    - Python : **indentation** (sum = 0)
  - 어떤 언어는 명시적으로 (`END`, `END IF`) 끝을 알림

### ◆ Multiple Selection Constructs


- 여러 문장 or 문장 그룹 선택 가능
- Case : ALGOL-W, Pascal
{% raw %}
```pascal
case expression of
    constant_list_1 : statement_1 ;
    ....
    constant_list_n : statement_n ;
end

case index of
    1,3 : begin
            odd := odd + 1 ;
          end
    2,4 : begin
            even := even + 1 ;
          end
    else writeln ("Error in case") ;
end
```
{% endraw %}

- Switch (C)
  - 조건식 → integer type 
  - `break` 로 explicit branching → 빼먹으면 모두 실행
{% raw %}
```c
switch (index) {
    case 1 :
    case 3 : odd += 1 ;
             break ;   // 명시적 분기(explicit branching)
    case 2 :
    case 4 : even += 1 ;
             break ;
    default : printf("Error in switch");
}
```
{% endraw %}

- Python
{% raw %}
```python
case
    when count < 10 then bag1 = true
    when count < 100 then bag2 = true
    when count < 1000 then bag3 = true
end
```
{% endraw %}

## ✦ Iterative Statement


- 어떤 문장들은 여러 번 반복하도록 
- recursion vs. iterative
- 반복 제어 방식 : counter or logical
- loop 조건 검사 : pretest, posttest, user defined

### ◆ Counter-Controlled Loops


- 조건 변수 (loop variable)
- 조건 parameter : 초기값 (initial) `;` 종료값 (terminal) `;` 증가값 (stepsize)
- Example
  - FORTRAN Ⅳ : posttest → 최소 한 번 실행
{% raw %}
```fortran
DO 30 I=1,100,2
….
30 CONTINUE
```
{% endraw %}

  - FORTRAN 77, 90 : pretest, single-entry
{% raw %}
```fortran
Do label variable = initial, terminal [,stepsize]
```
{% endraw %}

  - C : `for` statement
{% raw %}
```c
for (  i = 0   ;   i <= 10   ;   i++   ) 
		   ↑ 초기값    ↑ 종료조건       ↑ 증감값
```
{% endraw %}

    - pretest : 종료조건 0 이면 for 종료, 아니면 loop 실행
    - 표현식 생략 가능 (`for ( ; ; )` → 무한 loop

### ◆ Logically controlled loops


- loop 가 boolean 표현식에 기반
- pretest? posttest?
  - C언어 → 둘다 있음
    - pretest : `while`
    - posttest : `do ... while`
{% raw %}
```c
/* pretest */
scanf ("%d", &indat) ;
while (indat >= 0) {
    sum = sum + indat ;
    scanf("%d", &indat) ;
}

/* posttest */
do {
    indat = indat / 10;
    digits = digits + 1;
} while (indat>0);
```
{% endraw %}

### ◆ User-Located Loop Control Mechanisims


- programmer 가 loop 의 위 / 아래에 직접 loop 제어 배치
- C 의 `break` / `continue`
  - break 시 탈출은 한 loop ? 모든 loop ?
{% raw %}
```c
/* continue : 남은 루프 본체를 건너뜀 */
while (sum < 1000) {
    getnext(value) ;
    if (value < 0) continue ;
    sum = sum + value ;
}

/* break : 루프를 완전히 종료 */
while (sum < 1000) {
    getnext(value) ;
    if (value < 0) break ;
    sum = sum + value ;
}
```
{% endraw %}

### ◆ Iteration based on Data Structure


- 데이터 구조 원소 개수만큼 loop
- Example 
  - Java
{% raw %}
```java
for (String myElement : myList) { ….}
```
{% endraw %}

  - C# 
{% raw %}
```csharp
String[] StrList={"Bob", "Carol", "Ted", "lala"};
…
foreach (String name in StrList) …. ;
```
{% endraw %}

  - Python
{% raw %}
```python
#!/usr/bin/python
for num in range(10,20):      # 10~20 사이를 반복
    for i in range(2,num):
        if num%i == 0:        # 첫 번째 인수 판별
            j=num/i           # 두 번째 인수 계산
            print '%d equals %d * %d' % (num,i,j)
            break             # 첫 번째 FOR로 이동
    else:                     # 루프의 else 부분
        print num, 'is a prime number'
```
{% endraw %}

{% raw %}
```text
10 equals 2 * 5
11 is a prime number
...
19 is a prime number
```
{% endraw %}

## ✦ Unconditional Branching


- 무조건 분기 (goto) : 프로그램 내 지정된 위치로 이동

### ◆ Problems


- goto 문 → 프로그램 문장 실행 흐름 제어 강력 but 그래서 위험
  - readability 위배 : 문장 나타나는 순서 → 실행 순서 일 때 readability good
  - Java : goto 문 없도록 설계
- 대부분 언어는 goto 포함

### ◆ Label Forms


- 대부분 언어 사용 제한
- C : 식별자 (identifier) 형식 사용

## ✦ Guarded Commands


- by Dijkstra
- 같은 priority 일 때 non-deterministic (시스템이 random 하게)
- Concurrency Control 시 사용
  - Concurrent (병행) : 여러 작업을 **번갈아가며** 처리 
→ 동시에 진행 중이지만, 실제로 한 순간엔 하나만 실행
  - Parallel (병렬) : 실제로 CPU 를 여러 개 사용해 동시 실행

### ◆ Selection Structure


{% raw %}
```c
if <Boolean expression> -> <statement>
[] <Boolean expression> -> <statement>
[] ....
[] <Boolean expression> -> <statement>
fi
```
{% endraw %}

- 구조 도달 마다 all 조건식 평가
  - 하나 이상이 참 → 그 중 random 실행
  - 참이 0개 → error 발생
- Example
{% raw %}
```c
if i = 0 -> sum := sum + i
[] i > j -> sum := sum + j
[] j > i -> sum := sum + i
fi
```
{% endraw %}

  - if (i = 0) and (j = 1) → 1 번째 or 3 번째 random 실행
  - if (i = 0) and (i <> 0) → runtime error
![](/assets/images/notion/[pl]-statement-level-control-structures/img_1.png)

### ◆ Loop Structure


{% raw %}
```c
do q1 > q2 -> temp := q1; q1 := q2 ; q2 := temp ;
[] q2 > q3 -> temp := q2; q2 := q3 ; q3 := temp ;
[] q3 > q4 -> temp := q3; q3 := q4 ; q4 := temp ;
od
```
{% endraw %}

- do ~ while 와 유사 
  - 모든 조건이 false 면 빠져나옴
  - 여러 조건 true → random 으로 하나 실행 후 다시 실행
![](/assets/images/notion/[pl]-statement-level-control-structures/img_2.png)
