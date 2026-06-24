---
categories:
- Programming-Language
date: '2026-06-24T10:35:00.000+09:00'
layout: single
series: 프로그래밍 언어
step: 2
tags:
- 프로그래밍 언어
title: '[PL] Names, Bindings, Type Checking, and Scopes'
toc: true
toc_sticky: true
---

## ✦ Introductions


### ◆ Imperative Languages (명령형 언어)


- 변수 (variable) → memory cell 의 추상화
  - 속성 : data type, scope, life time, type checking ,initialization 등
  - 실제 세계 & data type 과 얼마나 잘 match?

## ✦ Names


- 이름 (name) : 프로그램에서 entity 식별 위해 사용하는 문자열
  - 프로그램에서 이름 짓는 것은 중요하면서도 어렵다.

### ◆ Name Forms


- 이름 길이 
  - 초창기 언어들에는 글자 수 제한 O
  - 요즘 언어들은 글자 수 제한 X
- 대소문자 구별
ex) C, C++ 구별 O

### ◆ Special Words


- Keyword : 특정 context 에서만 의미 가지는 단어
- Reserved word (예약어) : 항상 의미 가지는 단어 → 이름으로 사용 X
ex) `if`, `while`, `return`, `class`

## ✦ Variables


- Variavles (변수) : 컴퓨터 memory cell 추상화

### ◆ Name (이름)


- 이름을 가짐 (identifier)

### ◆ Address


- 변수가 위치한 메모리 주소
- 전역 변수 vs. 지역 변수 똑같은 이름
→ 지역 변수 먼저
  - scoping rule : 내가 속한 지역에서 먼저 변수명 찾음 → 없으면 지역 밖에서 찾음
- aliase : 한 memory cell 에 이름이 여러 개 → debugging 어려움
ex) pointer

### ◆ Type


- 값의 범위 & 사용 가능 연산자 정의
- Assembly 언어는 type 이 없음

### ◆ Value


- memory cell 에 들어 있는 값
{% raw %}
```c
a = a + 1;
```
{% endraw %}

  - 왼쪽 a → l-value (left, location) : 변수의 메모리 주소
  - 오른쪽 a → r-value (right, real) : 변수에 저장된 실제 값

## ✦ Binding


- Binding (바인딩) : 어떤 속성 값을 결정하는 것
  - 어떤 엔티티 (entity) & 속성 (attribute) 연결
  - 어떤 연산 (operation) & 기호 (symbol) 연결

### ◆ Binding Time


- 어떤 때에 Binding 이 일어나는가?
1. Language design time : 언어 설계 시
  - 언어를 설계할 때 `*` 를 곱하기 연산자로 정하기
1. Language implementation time 
  - 데이터 타입 (int, float) 이 가능한 값의 범위 (word size) 에 binding
    - integer 는 항상 word size 로 저장
    - 언어에 대한 compiler 를 만들 때
1. Complie time
  - 변수의 type 결정 (a 는 int, b 는 float)
  - type binding time → in C 
1. Link time
  - main & subroutine 있을 때 main - sub binding 하는 시간
1. Load time
  - 실행되기 위해 변수가 memory 에 올라오는 시간
    - 이때 변수는 local X global O
    - 빈 memory 에 올라감
  - global 변수에 대한 attribute binding 시점
1. Run time 
  - 실제 실행 중에 변수의 value binding 이 일어나는 시점
  - local 변수 attribute binding 시점

|  | C | Python |
|:--|:--|:--|
| Name | compile time | run time |
| Type | compile time | run time |
| Address | load time (전역 변수)<br>run time (지역 변수) | run time |
| Value | load time (전역 변수)<br>run time (지역 변수) | run time |
| Lifetime | run time | run time |

### ◆ Type Binding


- 변수의 type 이 언제 binding 되는가?
- 언어마다 다름
  - C → Compile time (static type binding)
  - Python → Run time (dynamic type binding)
1. Static type binding 
  - 변수 선언 시  type 결정 
  - C, C++, Java
  - language rule 에 의해 변수 이름에 이미 type 이 할당된 언어 존재
ex) in FORTRAN → 변수명이 I, J, K 면 int type

1. Dynamic type binding 
  - 실제 assignment 일어날 때 (run time) type 결정
  - JS, Python, Ruby
  - 장점 : Flexibility (Generic 프로그램 작성 쉬움)
  - 단점 : Compile 시 type error 발견 어려움

### ◆ Storage Binding


- 변수의 address 가 언제 binding 되는가?
1. Static variable
  - global 변수
  - 프로그램 시작 전 미리 할당 (load time) 
1. Stack dynamic variable
  - procedure 안에 만들어진 local 변수
  - type 할당 → compile time
  - 함수가 호출되었을 때 (run time) address 할당
  - recursion 을 위해 자주 사용
  - 같은 stack 공간 재사용 가능
1. explicit Heap Dynamic Variale 
  - `malloc` 과 같은 함수로 **프로그래머**가 직접적으로 할당하는 변수
  - 프로그래머가 `free` 할 때까지 사용하기에 stack 이 아닌 heap 에 저장
  - pointer 변수 통해 참조
1. implicit Heap Dynamic variable
  - **프로그램**에 의해 자동으로 값이 assign 될 때에만 address 할당
  - 자동적 할당 (PHP, JavaScript) 등
  - 그때 그 type 에 맞게 memory 할당

## ✦ Type Checking


- operator 와 operand 들이 서로 호환 가능한 타입인가?
- 호환 불가능 → compiler 가 error 알림
- 몇몇 compiler 는 자동 형변환 (coercion) 통해 호환 가능하게 만듬

## ✦ Strong Typing


- Strongly typed language 
  - 프로그램의 모든 변수가 static type binding 인언어
  - type error 항상 발견 가능
- C, C++ : strong typed language X 
→ `scanf` type checking 안함

## ✦ Lifetime & Scoping


### ◆ Lifetime


- 시간적 개념
- 변수가 특정 memory cell 과 binding 되어 있는 시간
- global 변수 : 프로그램 시작 전부터 끝날 때까지
- local 변수 : 선언된 procedure 안까지

### ◆ Scope


- 공간적 개념
- 변수가 visible (사용 가능) 한 영역
- global 변수 : 프로그램 전체
- local 변수 : local 변수가 선언된 procedure 안

## ✦ Scope


### ◆ Static Scope


- 대부분의 언어가 사용 
- 계층적 구조 - scope 가 nest 된 구조
![](/assets/images/notion/[pl]-names,-bindings,-type-checking,-and-scopes/img_1.png)

- Static Scoping rule : 내 지역 안에서 찾아보고 없으면 더 밖의 영역 찾는다.
ex) 서강대에 없으면 대흥동에서 찾고, 없으면 마포구에서 찾고, 없으면 서울에서 찾고, 없으면 한국에서 찾고, 없으면 global 에서 찾기

  - compile time 에 결정
- procedure 아니어도 `{}` 통해 nest 가능
- nested subprogram 가능 (Ada, JavaScript, Fortran, F#, Python)
  - 함수 내부에함수 선언
- 문제점 
  - too much access
  - 잘못된 함수 호출 compiler 가 잡지 못함
![](/assets/images/notion/[pl]-names,-bindings,-type-checking,-and-scopes/img_2.png)

    - visible 하면 안되는 것들이 보임

### ◆ Dynamic Scope


- 변수의 scope → subprogram 의 호출 순서 기반 결정
  - run-time 에 결정
  - 자신을 호출한 함수의 scope 를 찾음
- parent
  - static parent : 구조적으로 외부에 있는 함수 (ex. `sub1` 의 static parent 는 `big` )
  - dynamic parent : 함수를 실제로 호출한 함수 (ex. `sub1` 의 dynamic parent 는 `sub2` )
![](/assets/images/notion/[pl]-names,-bindings,-type-checking,-and-scopes/img_3.png)

- 거의 사용되지 않는 방법
- 장점 : parameter 넘길 필요 X
- 단점 : type checking 어려움, 신뢰성 ↓ 

## ✦ Referencing Environments


- 어떤 Statement 에서 visible 한 변수들의 집합
![](/assets/images/notion/[pl]-names,-bindings,-type-checking,-and-scopes/img_4.png)

  1. `x`, `y` → sub1 / `a`, `b` → example
  1. `x` → sub3 / `a`, `b` → example
  1. `x` → sub2 / `a`, `b` → example
  1. `a`, `b` → example

## ✦ Named Constant


- storage binding 이 일어날 때 value binding 이 동시에 + run time 중 값이 바뀌지 않음
- `#define` 과는 다른 방식 : #define 은 전처리 단계 
- Readability ↑

## ✦ Variable Initialization


- 초기화
- 대부분의 언어 : storage binding + value binding
  - 수행 도중 value 바뀔 수 있음
