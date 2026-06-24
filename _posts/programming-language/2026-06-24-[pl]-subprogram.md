---
categories:
- Programming-Language
date: '2026-06-24T10:39:00.000+09:00'
layout: single
series: 프로그래밍 언어
step: 6
tags:
- 서브프로그램
- 프로그래밍 언어
- PL
title: '[PL] Subprogram'
toc: true
toc_sticky: true
---

## ✦ Introduction


### ◆ Abstraction 의 두가지 근본적 기능


- Process abstraction (subprogram)
  - Procedure call (함수 호출) → statement 의 모음의 추상화
- Data Abstraction
  - Abstract Data Type
- Statement 의 모음은 재사용 됨 → 함수화 통해 메모리 공간 & 코딩 시간 절약
- Caller vs. Callee
- Procedure vs. Macro

## ✦ Fundamentals of Subprograms


### ◆ 일반적 특성


- 각 subprogram 은 단일 진입점 (single entry point) 를 가짐
- caller 는 subprogram 실행 중에 pause 됨 → 주어진 시간에 subprogram 만 실행 중
- subprogram 실행 종료 시 → caller 에게 제어권 돌아감

### ◆ 기본 정의


- Subprogram definition : subprogram 추상화 동작 기술
- Subprogram call : subprogram 실행되도록 하는 명시적 요청
- Active : subprogram 실행 ~ 완료 전까지
- Subprogram header : definition 의 첫 번째 줄
  - 뒤따르는 구문 단위가 subprogram 이라는 것을 명시
  - Subprogram 이름 제공
  - parameter 목록 명시 가능 (선택적)
  - Example
    - FORTRAN
`SUBROUTINE ADDER (parameters)`
    - Ada
`procedure ADDER (parameters) is`
    - C → function 만 존재
`adder (parameters)` 
      - header 는 문맥에 의해 인식

### ◆ Parameters


- Subprogram 이 데이터 접근하는 2가지 방법
  1. nonlocal 변수에 직접적 접근 (global, static 등)
    - nonlocal 에 과도하게 접근 시 reliability ↓
  1. parameter passing
    - parameterized computation (subprogram 이 어떤 computation 을 할지는 parameter 에 의해 결정)
- 어떨 때는 데이터 아니라 연산 (computation) 을 parameter 로 전달하는게 편리함
  - subprogram 의 이름을 parameter 로 사용 가능
- Parameter 종류 
  - Formal parameter : subprogram header 에 있는 parameter
  - Actual parameter : subprogram 호출 시 parameter 목록. formal parameter 에 binding 됨
- Parameter Passing
  - Positional parameters : actual parameter & formal parameter 의 binding 은 위치에 의해 결정
  - Keyword parameters : actual parameter 에 연결될 formal parameter 의 이름 명시
    - Example
      - Ada
`SUMER (LENGTH => MY_LENGTH, LIST => MY_LIST, SUM => MY_SUM);`

    - subprogram 사용자가 formal parameter 의 이름을 알아야 함
- Default values
  - formal parameter 가 기본값 (default value) 가질 수 있음
  - actual parameter 가 전달되지 않으면 default 값 사용

### ◆ Procedures and Functions


- Procedure 
  - parameter 화 된 연산을 정의하는 statement 의 모음
  - new statement 정의
  - caller 에게 결과 전달 방법
    - visible 변수를 변경 (formal parameter 제외)
    - formal parameter(caller 에게 데이터 전달 허용) 변경 
- Function
  - 이름 + 필요한 actual parameter 로 호출 → user defined operator
  - 함수 실행으로 생성된 값 → 호출 코드로 반환.
  - Example
    - Pascal
{% raw %}
```pascal
function power (base, exp : real) : real ;
  begin
    .....
  end
  .......
  result := 3.4 * power(10.0, x)
```
{% endraw %}

    - FORTRAN
`Result = 3.4*10.0**x`

## ✦ Design Issues for Subprograms


- 어떤 parameter passing 방법 사용?
  - Pass-by-Value
  - Pass-by-Result
  - Pass-by-Value-Result
  - Pass-by-Reference
  - Pass-by-Name
- actual parameter 의 타입이 formal parameter 의 타입과 맞는지 검사?
- local 변수는 statically 할당 or dynamically 할당?
- parameter 로 넘겨진 subprogram 의 referencing environment (참조 환경)
- subprogram 이 parameter 로 전달 가능 → 전달된 subprogram 호출 시 parameter type checking?
- subprogram overload 가능?
- subprogram generic 가능?
- separate compile or independent compilation 가능?

## ✦ Local Referencing Environments


- Local 변수 : Subprogram 내부에서 선언된 변수
  - scope : local 변수가 선언된 subprogram 안
- Stack-dynamic local variables
  - subprogram 실행 시작 시 storage bind, 실행 종료 시 해제
  - 장점 
    - 재귀적 subprogram 허용
    - 저장 공간 공유
  - 단점 
    - 각 호출 마다 변수 할당, 초기화, 해제 시간 비용
    - 간접 참조 → slow
    - history-sensitive procedure 허용 X
- Static local variables
  - program 실행 시작 시 storage bind
  - 장점
    - 빠른 참조 허용
    - history-sensitive procedure 가능
  - 단점
    - 재귀 허용 X
- local 변수 → 기본적으로 stack dynamic
  - Example : C
{% raw %}
```c
adder (list, listlen)
    int list[], listlen ;
    { static int sum = 0 ; /* → 정적 지역 변수 */
      int count ;          /* → 스택-동적 지역 변수 */
      for (count = 0 ; count < listlen ; count++)
            sum = sum + list[coㅋunt] ;
      return sum ;
    }
```
{% endraw %}

  - FORTRAN 77 → 재귀 X, 모든 local 변수는 static

## ✦ Parameter-Passing Methods


### ◆ Semantics Models of Parameter Passing


![](/assets/images/notion/[pl]-subprogram/img_1.png)

- 세 가지 모드
  1. in mode : actual parameter → (data) → formal parameter
  1. out mode : actual parameter ← (data) ← formal parameter
  1. inout mode : actual parameter ← (data) → formal parameter
- parameter 전달 시 데이터 이동 방법
  - 실제 값이 물리적으로 이동 (actual data transfer)
  - 접근 경로 (pointer) 가 이동

### ◆ Implementation Models of Parameter Passing


- Pass-by-Value (call-by-value)
  - actual paratmeter 의 값 → 대응하는 formal parameter 초기화 시 사용
  - formal parameter 는 subprogram 내에서 지역 변수 (local variable) 처럼 동작
  - in-mode (actual → formal)
  - 실제 데이터 전송 통해 구현 (원본 변경 X)
  - parameter 가 큰 객체면 costly
- Pass-by-Result
  - out-mode (actual ← formal)
    - subprogram 으로 값 전달 X
  - formal parameter 가 지역 변수처럼 동작 → caller 의 actual parameter 로 전달. 이때 actual parameter 는 반드시 변수
  - 문제점
    - 추가 저장 공간 & move 연산의 문제
    - actual parameter collision 문제
{% raw %}
```c
subroutine sub(x, y) {
    x = 3;
    y = 5;
}
main() {
    int p1;
    sub(p1, p1);
    p1???
}
```
{% endraw %}

    - actual parameter 주소 평가 시점 문제
{% raw %}
```c
int index, list[10];

subroutine sub(a) {
    index = 5;
    a = 3;
}
main() {
    index = 3;
    sub(list[index]);
}
```
{% endraw %}

- Pass-by-Value-Result (pass-by-copy)
  - inout-mode (actual ↔ formal)
  - formal 이 actual 로 초기화, return 시 formal 값이 actual 로 전달
- Pass-by-Reference
  - inout-mode (actual ↔ formal)
  - 접근 경로, 주로 주소 (address) 전달 
  - actual parameter 가 호출된 subprogram 과 공유 됨 → 원본 변경 O
  - 장점 : 복사 overhead X, 중복 공간 X
  - 단점 : formal parameter 접근 느림 (indirect addressing), actual paramter 의 의도치 않은 변경, alias 생성 
- Pass-by-Name
  - inout-mode (actual ↔ formal)
  - actual parameter → formal parameter 에 텍스트적으로 치환
  - late binding : formal parameter 는 subprogram 호출 시점에 접근 방법binding, but 값 or 주소로의 실제 바인딩은 할당 / 참조 시까지 지연
→ 같은 formal parameter 참조 마다 값 변화 가능
  - actual parameter 형태 따라 구현 방법 化
    - 변수 전달 → pass-by-reference
    - 상수 전달 → pass-by-value
    - 배열 원소 (or 변수 포함 표현식) 전달 → formal parameter 참조 마다 배열 원소 (표현식) 값 변화 가능 
  - 장점 : 유연성 
  - 단점 : 느린 처리 속도, 구현 어려움, read & write 어려움 
- Jesen’s Device
  - 1 개의 procedure 를 여러 목적으로 사용
  - subprogram 에 표현식 + 1개 이상의 변수를 parameter 로 전달
  - parameter 에 무엇을 전달하는지에 따라 계산 방법 변화
![](/assets/images/notion/[pl]-subprogram/img_2.png)

### ◆ Parameter-Passing Methods of the Major Languages


- C
  - Pass-by-Value
  - Pass-by-Reference → parameter 로 pointer 사용 시
- C++
  - Pass-by-Reference 위한 reference type (특별한 pointer 타입) 제공
- Java
  - Pass-by-Value
  - Pass-by-Reference → 객체 (Object)
- Python  
  - Pass-by-Assignment 
    - 모든 데이터 → 객체 (object)
{% raw %}
```c
def spam(eggs):
    eggs.append(1)
    eggs = [2, 3]

ham = [0]
spam(ham)
print(ham)
```
{% endraw %}

    - 객체 내부 수정 → caller 반영 (call-by-reference)
    - 객체 새로 할당 → caller 에 영향 X (call-by-value)
  - Call-by-Object
    - 함수에 불변 (정수, 문자열, 튜플) 인자 전달 → call-by-value
→ 수정 X 새로운 객체를 가리킴
    - 함수에 가변 (list, dict, set) 인자 전달 → call-by-reference
→ 단, new list 할당 시는 영향 X 
  - Arguments

| 기능 | 방법 | 특징 |
|:--|:--|:--|
| 커맨드 라인 인자 | `sys.argv` | 리스트 형태로 저장 |
| 가변 길이 인자 | `*변수명` | 튜플 형태로 묶임 |

- 대부분 언어는 기본적으로 Pass-by-Value 사용

### ◆ Type-Checking Parameters


- actual - formal parameter 타입 검사해야한다고 받아들여 지고 있음
- 예시
  - C : parameter 개수, 타입 검사 X 
  - ANSI C : formal parameter 두 가지 방식 선언 
    - C 와 동일 → 타입 검사 X
    - prototype 방식 → 타입 검사 O & 강제 변환 (coercion)
  - C++ : 타입이 지정된 parameter & ellipsis(`…`) 사용 가능
  - Perl, JS, PHP : 타입 검사 X
  - Python, Ruby : 객체가 타입 가짐 → 타입 검사 불가능 

### ◆ Implementing Parameter-Passing Methods


- Pass-by-Value 
  - 값이 stack 위치에 복사
- Pass-by-Result
  - actual parameter 값이 stack 에 저장 subprogram 종료 시 호출하는 프로그램이 가져올 수 있음
- Pass-by-Value-Result
  - pass-by-value & pass-by-result 조합
- Pass-by-Reference
  - actual parameter → 주소 (address) 만 stack 에 저장
  - 표현식 → subprogram 넘어가기 직전 표현식 평가 → 결과 저장 주소가 stack 에 저장
- Pass-by-Name
  - thunk : parameter 없는 procedure / run-time 상주 code segment 
    - 비용 높음
    - 호출된 subprogram 내의 pass-by-name parameter 모든 참조마다 호출
    - referencing environment 에서 참조 평가 & actual parameter 주소 반환 
![](/assets/images/notion/[pl]-subprogram/img_3.png)

### ◆ Design Consideration


- 효율성
- 단방향 or 양방향 데이터 전달 
  - 소프트웨어 공학 원칙 → in-mode only

## ✦ Parameters That are Subprogram Names


- subprogram 이름이 다른 subprogram 의 parameter 로 전달
- 전달된 subprogram 실행 시 참조 환경 (referencing environment)
  - shallow binding : callee 을 call 하는 subprogram의 환경 (`SUB4`)
    - dynamically scoped language 에서 사용
  - deep binding : callee 가 선언된 subprogram 의 환경 (`SUB1`)
    - 블록 구조 (block structured) 언어에서 사용
  - others : callee 를 actual parameter 로 전달하는 호출문을 포함하는 subprogram 의 환경 (`SUB3`)
{% raw %}
```pascal
procedure SUB1;
    var x : integer;
    procedure SUB2;
        begin
            write('x=', x);
        end; {of SUB2}
    procedure SUB3;
        var x : integer;
        begin
            x := 3; SUB4(SUB2); 
        end; {of SUB3}
    procedure SUB4(SUBX);
        var x : integer;
        begin
            x := 4; SUBX;
        end; {of SUB4}
    begin {of SUB1}
        x := 1; SUB3;
    end; {of SUB1}
```
{% endraw %}

## ✦ Overloaded Subprograms


- 동일한 참조 환경 (referencing environment) 내에서 다른 subprogram 과 같은 이름을 가진 subprogram
- overloading 된 procedure 끼리는 parameter type 과 return 값이 유일해야 함
- overload 된 subprogram 은 actual parameter 목록에 따라 결정
- C++
  - 각 함수의 parameter 개수 또는 type 이 유일 → overloading 가능 
{% raw %}
```cpp
void fun(float b = 0.0) {
    …
}
void fun() {
    …
}
main() {
    …
    fun() ; /* ?? */
    …
}
```
{% endraw %}

## ✦ Generic Subprogram


- 타입에 관계없이 동작하는 범용 함수
- 함수를 한 번만 정의하고 사용 시 타입 결정 → compiler 가 타입에 맞는 버전 자동 생성

## ✦ Design Issues for Functions


- side effect 허용?
- 어떤 타입의 값 반환 가능?

### ◆ Functional Side Effects


- Side Effect : 함수가 return 값 이외에 외부 변수 or 상태 변경
- Ada
  - 함수의 paramter 는 항상 in-mode → side effect 방지
- Pascal & C
  - 함수는 pass-by-value / pass-by-reference parameter
→ side effect 함수 허용

### ◆ Type of Returned Values


- 대부분의 명령형 언어 → 반환 타입 제한 
- FORTRAN 77 : 함수는 비구조적 타입(unstructured types)만 반환 가능
- Pascal and Modula-2 : 함수는 단순 타입만 반환 가능
  - integer, real, char, Boolean, pointers, enumeration types
- C : 배열과 함수를 제외한 **모든 타입** 반환 가능
- Java and C# : 메서드는 **모든 타입** 반환 가능

## ✦ Accessing Nonlocal E nvironments


- nonlocal variables (비지역 변수) : subprogram 내에서 보이지만, 내부적으로 선언되지 않은 변수
  - static scoping languages : 필요한 것보다 더 많은 nonlocal 접근
  - dynamic scoping languages : nonlocal 변수 참조 static 하게 타입 검사 불가능

### ◆ FORTRAN


- `COMMON` 통해 전역 저장소 블록에 접근
  - 첫 `COMMON` 문 발견 시 생성
- 문제점 : 두 subprogram 이 서로 다른 이름으로 동일한 데이터 블록 포함 가능

### ◆ External Declarations and Modules


- C 언어 (procedure 의 중첩 없음)
  - 전역 변수 : 함수 정의 외부에 선언해 생성
  - `extern` 문으로 변수 선언 → 외부에서 선언한 함수에서 변수 접근 가능

## ✦ User-Defined Overloaded Operators


- 유저에 의해서 연산자 (`+`, `*`, `-`) overloading 가능 
  - Parameter 갯수 & 타입 변화
  - return 타입 변화
- Closures
  - subprogram + 정의된 참조 환경 (referencing environment)
    - 함수가 자신이 만들어질 때의 변수 환경 기억
  - 익명 함수 (anonymous function)

## ✦ Coroutines


- 여러 개의 진입점 (multiple entries) 지님 & 스스로 그것을 제어
- symmetric control : caller & callee coroutine 은 더 동등한 관계
- resume : coroutine 호출
  - 첫 번째 resume → 처음부터
  - 이 후 resume → 마지막 coroutine 실행 다음 문장 부터
  - quasi-concurrent execution of program unit (표면 상 concureent)
    - 실행 interleaved (교차, 번갈아가며) O, overlapped (중첩) X
![](/assets/images/notion/[pl]-subprogram/img_4.png)
