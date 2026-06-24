---
categories:
- Programming-Language
date: '2026-06-24T10:37:00.000+09:00'
layout: single
series: 프로그래밍 언어
step: 4
tags:
- 프로그래밍 언어
- PL
title: '[PL] Expressions and the Assignment Statement'
toc: true
toc_sticky: true
---

## ✦ Arithmetic Expressions


- 산술 표현식의 자동 평가 → 초기 프로그래밍 언어의 주요 목표

### ◆ Operator Evaluation Order


- 연산자 평가 순서 
  - 서로 다른 우선순위인 인접한 연산자 평가 순서? (binary)
ex) A + B * C

  - 항등 연산자 (unary operator : 피연산자 영향 X)
ex) +A, A + (-B) * C

- 대부분의 언어에서 우선순위 규칙 동일
- 산술 연산자 우선순위 (high ← → low)
  - FORTRAN : `*` → `, /` → `all +, -`
  - Pascal : `, /, div, mod` → `all +, -`
  - ANSI C : `++, --, unary +, -` → `, /, %` → `binary +, -`
- 결합 규칙 (Associativity Rule)
  - 같은 우선순위 인접? → 언어의 결합 규칙 의해 결정 
    - 대부분 → 이 방향, `**` (거듭제곱) 은 우결합
  - Example
    - **FORTRAN**
      - 좌결합 : `, /, +, -` / 우결합 : `*`
    - **Pascal**
      - 좌결합 : 전부
    - **ANSI C**
      - 좌결합 : `, /, %, binary +, binary -`
      - 우결합 : `++, --, unary +, unary -`
    - **APL**
      - 우선순위 없음, 오직 결합 규칙만 존재 (오른쪽 → 왼쪽)
  - 연산자 평가 순서 재배열 가능하면 더 빠를 수도?
    - 정수 연산에선 overflow 때문에 결합 법칙 깨질 수 있다
- Parentheses (괄호)
  - 표현식에 괄호 써서 우선순위 & 결합 규칙 바꿀 수 있음
  - ex) (A + B) * C

### ◆ Operand Evaluation Order


- 피연산자가 side effect 가지면 평가 순서 중요!
- Side effect : 함수가 parameter or global variable 바꾸면 발생
  - 처리 방법
    - 함수적 side effect 허용 X
    - 언어 정의 : 특정 순서 지정
{% raw %}
```pascal
procedure sub1(....) ;
  var a : integer
  function fun(x:integer) : integer ;
  ....
    a := 27 ;
    return(5);
  end

procedure sub2(....) ;
  ....
    a := 10 ;
    b := a + fun(b) ;  ← 피연산자가 함수 호출인 경우
    print(b) ;
  end
end
```
{% endraw %}

### ◆ Conditional Expressions


- `if-then-else` 구문이 조건부 표현식 대입에 사용
→ C : 삼항 연산자 `?` 

{% raw %}
```c
average = (count == 0) ? 0 : sum/count ;
```
{% endraw %}

## ✦ Overloaded Operator


- 한 operator 를 여러 방식으로 사용.
- Readability & Reliability 해치지 않으면 허용 가능
- Example
  - 사칙연산 (`+`, `-`, `*`, `/`) → int & float 공통적으로 사용
  - C의 `&` : bit AND / 주소 참조
- user-defined overloaded operator 
  - 사용자가 직접 operator 를 overload 할 수 있음 

## ✦ Type Conversions


- 여러 type 을 동시에 표현 가능 언어 → coercion (강제 변환) 규칙 
  - 컴퓨터는 보통 서로 다른 type 피연산자 계산 불가능
  - coercion : compiler 의해 implicit (암묵적) type conversion
  - casting : programmer 의해 explicit (명시적) type conversion
- Type conversion
  - Narrowing conversion : 원래 타입 모든 값 포함 불가능 
ex) float → int
  - Widening conversion : 원래타입의 모든 값 적어도 근사적으로 포함 가능
ex) int → float
    - 항상 안전, but 일부 정밀도 손실 가능
- Coercion design choices (C)
  - 숫자 데이터 타입 : int | short | long / float | double
short → int / float → double 로 강제 변환
  - C는 type checking X. 표현식 실행 중 오류 발생 가능
