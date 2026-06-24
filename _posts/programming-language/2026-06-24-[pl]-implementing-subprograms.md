---
categories:
- Programming-Language
date: '2026-06-24T10:40:00.000+09:00'
layout: single
series: 프로그래밍 언어
step: 7
tags:
- 프로그래밍 언어
- PL
- 서브프로그램
title: '[PL] Implementing Subprograms '
toc: true
toc_sticky: true
---

## ✦ The General Semantics of Calls and Returns


- Subprogram Linkage
  - subprogram call + return 합친 것
  - linkage 의 semantics (의미) 기반해 구현 방법 결정
- 동작들
  - Subprogram Call
    - Parameter passing mechanism
    - local 변수 storage 할당 & binding
    - 실행 status 저장
    - control 을 subprogram 으로 이동, 실행 완료 시 control 올바른 위치로 재이동
    - nonlocal 변수 접근 제공 메커니즘
  - Subprogram Return
    - out mode parameter (a ← f)
      - copy 방식 구현: formal parameter 의 지역 값 → 실제 actual parameter 로 이동
      - 참조 (by-refercence) : 이동 필요 X, 애초에 같은 것 가리킴
    - local 변수 storage deallocate
    - nonlocal 변수 참조 메커니즘 return
    - control 을 caller 에게 return

## ✦ Implementing “Simple” Subprograms


- FORTRAN
  - 재귀 X
  - nonlocal 변수 → `COMMON` 으로 공유
  - local 변수 → static (프로그램 실행 전 미리 메모리 고정)

## ✦ Implementing Subprograms with Stack-Dynamic Local Variables


### ◆ More Complex Activation Records


- ALGOL 계열
  - Parameter Passing
    - 값 (Value)
    - 참조 (Reference)
  - local 변수 → dynamically 할당
  - 재귀 (recursion)
    - 각 실행마다 formal parameter, dynamic local, return address 복사 필요
  - nonlocal → static scoping
- Activation record 생성
  - stack 위에 dynamic 하게 생성
- Activation Record
  - 특징
    - 형식 & 크기 → compile 시점에 알 수 있음
    - 형식은 instance 의 template
  - Local 변수 : record 내의 storage 에 binding
  - Static link (static scope pointer)
    - static parent 가리킴
    - nonlocal 변수 접근 시 사용
  - Dynamic link
    - dynamic parent (caller) 가리킴
    - procedure 완료 시 stack 에서 제거할 때 사용
  - Return address : 반환 주소
  - Actual parameter : caller 가 제공한 값 or 주소
![](/assets/images/notion/[pl]-implementing-subprograms/img_1.png)

### ◆ Example Without Recursion and Nonlocal References


{% raw %}
```pascal
program MAIN_1
var P : real;
procedure A(X:integer);
  var Y:boolean;
  procedure C(Q:boolean);
  begin
    P=P+1; <------------------- 3
  end
  begin
    …  <----------------------- 2
    C(Y);
    …
  end {end of procedure A}
procedure B(R:real);
  var S,T;
  begin
    …  
    A(S);
    …
  end {end of procedure B}
begin {Main_1}
  …    <----------------------- 1
  B(P);
  …
end
```
{% endraw %}

- 호출 순서 : MAIN_1 → B(P) → A(S) → C(Y)
  - 1
![](/assets/images/notion/[pl]-implementing-subprograms/img_2.png)

  - 2
![](/assets/images/notion/[pl]-implementing-subprograms/img_3.png)

  - 3
![](/assets/images/notion/[pl]-implementing-subprograms/img_4.png)

- Dynamic Chan (call chain)
  - 특정 시점에 stack 에 존재하는 dyamic link 의 집합
  - 실행이 현 위치에 어떻게 도달했는지 dynamic history 나타냄
- Local_Offset
  - local 변수 참조 → record 시작으로부터의 offset 으로 표현 가능 
  - local offset 은 compile 시점 변수의 순서, 타입, 크기 이용 결정

### ◆ Recursion


- 재귀를 이용한 factorial 계산
{% raw %}
```pascal
Program TEST
var VALUE:integer;
function FACTORIAL(N:integer);
begin  <----------------------------------- 1
  if N<=1
  then FACTORIAL:=1
  else FACTORIAL:= N*FACTORIAL(N-1);
end    <----------------------------------- 2
begin
  VALUE:=FACTORIAL(3);
  writeln("factorial 3 is:", VALUE)  <----- 3
end.
```
{% endraw %}

## ✦ Nested Subprograms


- nonlocal 변수 접근 매커니즘
  - stack 어딘가에 존재
- nonlocal 변수 참조
  1. 해당 변수가 할당된 함수 stack 에서 찾기
  1. 변수에 접근 위해 변수의 local_offset 사용
- Static-scoped language 의 semantic rule
  - subprogram 에서 static ancestor scope 에 선언된 변수만 nonlocal 하게 접근가능
  - static ancestor 의 변수는 참조 시 stack 위에 반드시 존재
    - 자신의 모든 static ancestor 가 active 해야 호출 가능
  - 가장 close 한 nested 부터 바깥 쪽으로 탐색할 때 처음 발견되는 것
    - Static chiain 사용
    - Display 사용

### ◆ Static Chains


- Stack 내의 특정 함수들 연결하는 static link 들의 chain
  - subprogram 의 ancester 를 부모부터 순서대로 연결
- nonlocal 변수 참조 발생 → 변수가 있는 함수 찾을 때 까지 static chain 탐색
- scope nest 는 compile 시점에 알 수 있음 → nonlocal 한 참조라는 것 & 필요한 static chain 길이 결정 가능
- Static_depth : 가장 밖 scope 에서 얼마나 깊이 중첩되어 있는가?
- Nesting_depth (chain_offset) of reference
  - nonlocal 참조에 도달하기 위해 필요한 static chain 길이
  - nonlocal 사용 static depth - nonlocal 선언 static_depth 
  - Example
{% raw %}
```pascal
program A ;
  procedure B ;
    procedure C ;
    end; { of procedure C }
  end; { of procedure B)
end ;
```
{% endraw %}

    - static_depth : A(0), B(1), C(2)
    - chain_offset : C 가 A 변수 참조 → 2 (2-0)
- Example
{% raw %}
```pascal
MAIN_2
  var X : integer
  BIGSUB
    var A, B, C : integer ;
    SUB1
      var A, D : integer ;
      A : = B + C ;
    var B, E : integer ;
    SUB2
      SUB3
        var C, E : integer ;
        SUB1 ;
        E := B + A ;
      ....
      SUB3 ;
      ....
    A := D + E ;
  SUB2 ;
BIGSUB ;
```
{% endraw %}

  - 호출 순서 : MAIN_2 → BIGSUB → SUB2 → SUB3 → SUB1
  - static_depth : MAIN_2 : 0, BIGSUB : 1, SUB2 : 2, SUB3 : 3, SUB1 : 2
**SUB1에서 ****`A := B + C`**** 참조 시:**

    - `A`는 SUB1 자신의 지역 변수 → chain_offset = 0
    - `B`, `C`는 BIGSUB에 선언 → chain_offset = 1 (정적 링크 1번 이동)
**SUB3에서 ****`E := B + A`**** 참조 시:**

    - `E`는 SUB3 자신의 지역 변수 → chain_offset = 0
    - `B`는 SUB2에 선언 → chain_offset = 1
    - `A`는 BIGSUB에 선언 → chain_offset = 2
- Static chain 유지 방법
  - subprogram 반환 시 : stack 에서 제거 → 추가 할일 X
  - subroutine (값 반환 X subprogram) 호출 시 → 호출 시점 parent 의 가장 최근 activation record 찾아야 함
    1. run-time 에 dynamic chine 따라가며 탐색
    1. compile time : compiler 가 caller 랑 callee 사이 nesting_depth 계산
call time : caller 의 static link → caller 의 static chain 을 nesting_depth 만큼 내려가서 결정
- Static chain 문제점
  - static parent 넘은 scope 변수 참조는 costly 
    - 참조 → 선언 도달하려면 static chain 한 link 씩 따라가야 함
  - nonlocal 참조 비용 예측 难

### ◆ Display


- static link 를 actiavation record 가 아닌 display 에 모아 저장
- display : 단일 배열, 특정 시점에서 접근 가능한 activation record instance 주소 목록
- nonlocal 참조 : (display_offset, local_offset)
  - display_offset : display 안에 있는 올바른 record 로의 link. static 하게 계산
  - local_offset : static chain 과 동일 방식 계산 & 사용
- display 에 k 번째 위치 pointer → static_depth 가 k 인 activation record instance 가리킴
- display 수정 하기
  - static_depth 가 k 인 procedure P 를 호출
    - new record 에 display 의 k 번째에 위치한 pointer 복사본 저장
    - display k 번째 위치에 P 의 record 로의 link 저장 
  - procedure 종료 : 종료되는 subprogram 의 record 에 저장된 pointer 를 다시 display 에 복원
- Example
![](/assets/images/notion/[pl]-implementing-subprograms/img_5.png)

- 구현 
  - display 최대 크기 = subprogram 의 최대 static_depth → compiler 결정
  - memory 에 runtime static array 로 저장
  - memory 에 저장된 경우 → nonlocal 은 local 보다 memory cycle 한 번 더
  - register 에 저장된 경우 → 추가적 memory cycle X

### ◆ Static chaining vs. Display method


- display 가 memory 에 저장 → nonlocal 참조 static chaining 보다 느림
- static level 이 1개 이상 떨어진 nonlocal 참조 → display 가 더 빠름
- display → all nonlocal 참조 시간 동일
- static chain → callee 가 static level 이 너무 안 멀면 유지 비용 더 good
- Overall comparison
  - static nest 깊음, 먼 nonloacl 변수 참조 多 → Display
  - nest 적음, 먼 nonlocal 변수 참조 少 → Static chaining (일반적)

## ✦ Blocks


- Block = 데이터 선언 + 여러 문장
- Block 구현
  1. 항상 같은 위치에서 호출되는 parameterless procedure 취급
    - 최대 nest ↑ → Display 크기 ↑
  1. Block 변수에 필요한 공간 record 내의 local 변수 옆에 할당 
    - block  변수 offset 은 static 하게 계산 가능 
![](/assets/images/notion/[pl]-implementing-subprograms/img_6.png)

→ while 동시에 동작 X : 같은 offset 공간 공유

## ✦ Implementing Dynamic Scoping


- nonlocal 변수들은 record 안에 있음 → stack 어딘가에 존재
- Dynamic scope 언어에서 nonlocal 참조 구현 방법
  - Deep access
  - Shallow access

### ◆ Deep access


- 현재 active 한 다른 subprogram 의 선언 탐색 → 가장 최근 activated 된 것부터
  - dynamic chaing 따라감
- dynamic scope 언어 → 탐색 chain 길이 compile 시점 결정 불가 → static scope 언어보다 느림
- record 에 변수의 이름 (name) 저장해야 함.
![](/assets/images/notion/[pl]-implementing-subprograms/img_7.png)

### ◆ Shallow access


- subprogram 내에 선언 변수 → 해당 subprogram ARI 에 저장 X
- 프로그램 전체에서 각 변수 이름마다 별도의 stack 유지
  - 어떤 이름의 변수가 subprogram 시작 시 선언될 때 마다 해당 이름의 stack 에 cell 추가
  - 해당 이름에 대한 참조 → stack top 변수 참조
  - 참조 fast, subprogram 진입 & 종료 시 stack 유지비용 costly
