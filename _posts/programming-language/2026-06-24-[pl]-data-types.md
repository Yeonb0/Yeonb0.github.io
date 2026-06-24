---
categories:
- Programming-Language
date: '2026-06-24T10:36:00.000+09:00'
layout: single
series: 프로그래밍 언어
step: 3
tags:
- 프로그래밍 언어
- PL
- 자료형
title: '[PL] Data Types '
toc: true
toc_sticky: true
---

## ✦ Introduction


- 원래 기계어에는 type 이 존재하지 않음
- 프로그래머가 쉽게 사용하도록 여러 data type 지원

### ◆ Data Type


- 가능한 값 (value) 들의 집합
- 값들에 대해 수행 가능한 연산 (operation) 의 집합
- real-world 의 문제 영역과 얼마나 잘 맞는가? 
- language 마다 다양한 data type 존재

## ✦ Primitive Data Types


- Hardware 적으로 지원해주는 언어
- 기계어로 다룰 수 있음

### ◆ Numeric Types


1. Integer 
  - 대부분의 컴퓨터 (CPU) 는 여러 size 의 정수를 지원한다
  - word size 와 다르게 compile 될 수 있다
![](/assets/images/notion/[pl]-data-types/img_1.png)

    - `int` : 64-bit 지만 32-bit size
    - `pointer` : 64-bit → 주소의 길이가 8 byte
  - 구현
    - binary sequence 로 표현.
    - 가장 왼쪽 비트 (MSB, Most Significant Bit) → 부호 (Sign) 나타냄
    - 2’s complement 방식 사용
![](/assets/images/notion/[pl]-data-types/img_2.png)

1. Floating-Point 
  - fraction + exponent 로 표현
  - 실수를 모델링 → 정확 X, approximation (근사) 만 가능
  - 구현 : by binary
    - Sign bit : 부호를 나타내는 bit
    - exponent (지수)
    - fraction (가수)
  - bit 를 더 많이 사용할 수록 더욱 근사해진다
![](/assets/images/notion/[pl]-data-types/img_3.png)

  - IEEE Floating-Point 표준
1. Decimal
  - BCD (Binary Coded Decimal) : 10진수 각 자리를 4 bit 이진수로 표현
  - 장점 : 정확한 표현
  - 단점 : 16개 표현 가능한데 10개 밖에 표현 안함 → 메모리 낭비

### ◆ Boolean Types


- True / False - 두 가지 값만 존재
- 구현 : single bit 로만도 표현 가능, but byte 로 저장

### ◆ Character Types


- 문자 → 숫자 코드 형태로 저장
  - ASCII : 1 byte (0 ~ 127)
  - Unicode

## ✦ Character String Types


- non-primitive data type : 하드웨어적으로 지원하진 않으나, 프로그램 writability 위해 언어적으로 지원
- Design Issue
  - 언어에서 기본적오로 제공할 것인가? 아니면 char 의 array 인가? (C언어)
  - 문자열의 길이는 static? dynamic?
- Examples
  - C / C++ : 기본 타입 X, library 로 제공
  - Perl, JavaScript, Ruby, PHP → language 레벨에서 string 제공

### ◆ Primitives or Character Array


- Special kind of character array
  - 단일 문자의 배열로 저장
  - C에서 string 은 char 의 array 인데 끝에 `\0` (null) 이 있는 것
- Primitive data type
  - 언어 자체에서 string type 제공 → writability 제공
  - 여러 operation 제공 (assignment, relational operators, catenation, 부분 문자열 참조 등)

### ◆ String Length Options


- Static length string
  - 선언 시 static 하게 길이 저장. 
  - 한 번 저장 후 변경 불가
- Dynamic length string 
  - 최대 제한 X, 다양한 길이 허용
  - assign 할 때 마다 길이 설정
  - assign 할 때마다 allocation 으로 overhead 발생
→ 각자 tradeoff 있음

### ◆ Evaluation


- string type → 언어의 writability 에 중요
- string 은 그렇게 costly 하지 않으니 구현하면 좋다!

### ◆ Implementation


- Descriptor : 변수의 attribute 들 모음
  - Compile-time discriptor
    - Static 문자열
    - compile 때 만들어진 정보를 가지고 있음
  - Run-time discriptor 
    - Limited Dynamic 문자열
    - 수행 도중의 정보를 가지고 있음
- dynamic allocation 방법
  - linked list 로 저장 (연속 X)
  - 인접 memory cell 로 저장
    - 더 커질 때 그대로 복사 해야 함
    - 빠른 참조, 적은 저장공간, allocation 이 slow

## ✦ User-Defined Ordinal Types


- Ordinal (서수) : 가능한 값들의 범위를 양의 정수 집합과 연관 짓는 데이터 타입
- 서수를 이용해 프로그래머가 만든 타입
- Readability 가 좋아짐

### ◆ Enumeration Type


- 열거형 타입 : symbolic constant 가 순서대로 나옴
- ex) 
{% raw %}
```csharp
type DAYS is (Mon, Tue, Wed, Thu, Fri, Sat, Sun) ; 
type WEKEND is (Sat, Sun) ;
int i;
DAYS a;
a = Mon;
```
{% endraw %}

  - DAYS 는 Mon, Tue, Wed, Thu, Fri, Sat, Sun 중 하나의 값 가질 수 있음
- in C, C++
{% raw %}
```c
enum day {sun, mon, tue, wed, thr, fri, sat} d1, d2;
```
{% endraw %}

  - sun, mon, tue, wed, thr, fri, sat 값 가질 수 있는 변수 d1, d2 선언
- 실제 구현될 때에는 integer 로 바뀌어 수행
  - 순서 비교 가능
  - 산술 연산은 불가능
  - range error 쉽게 찾을수 있음
- Operation : Predecessor, Successor, Position, Values

### ◆ Subrange type


- 어떤 type 의 일부만 접근해서 사용하고 싶을 때
- readability, reliability ↑
- ex) 
{% raw %}
```c
type
		uppercase = 'A'..'Z';
		index = 1..100;
```
{% endraw %}

- C/C++ 에선 존재하지 않음

### ◆ Implementation


- Enumeration : 음이 아닌 정수와 연결 (0 ~ )
- Subrange : parent 타입과 동일하게 구현 + range check 

## ✦ Array Types


- 동일 type 데이터들을 묶은 것
  - 수학의 vector, matrix 같은 것들 표현 위해 만듬
- 개별 원소는 첫 번째 원소의 상대적 위치 (position) 로 식별
- cf) `record` : 데이터 묶은 것. but type 달라도 됨
- Design Issue
  - index 로 어떤 type 이 가능한가?
  - array 의 size 가 언제 결정되는가? (subscript binding)
  - storage allocation 은 언제 결정되는가? (memory binding)
  - slice 를 허용하는가?

### ◆ Arrays and Index


- 대부분의 언어는 `a[10]` 과 같이 원소에 접근한다
  - `배열이름[index]`
- array → 일종의 mapping 함수
  - `[]` 대신 `()` 를 사용하는 언어도 존재한다

### ◆ Subscript Binding and Array Categories


- index 로 어떤 데이터 type 이 올 수 있나? (int, boolean, enumeration, subrange)
  - C 에선 `int` 나 `enum` 사용
- index 의 시작
  - 0 또는 1 
  - C에선 index의 시작으로 `0` 사용
- subscript value binding (array size) / storage binding (memory 할당)
  1. Static array
    - value range & storage 모두 compile time 에결정
    - ex) FORTRAN → recursion X
    - 장점 : 빠르다
  1. Fixed stack-dynamic array
    - range 는 compile time, storage 는 run time 에 stack 영역에 할당
    - 장점 : space efficiency
    - ex) C 에서의 일반 array
  1. Fixed heap-dynamic array
    - range & storage 모두 run time 에 memory 는 heap 영역에 할당
    - 중간에 크기 변경 X
    - ex) C 의 `malloc`
  1. Heap dynamic array
    - range & storage 모두 run time 에 memory 는 heap 영역에 할당
    - 중간에 크기 변경 O
    - ex) C 의 `realloc`

|  | range binding | storage binding |
| Static array | compile time | compile time |
| Fixed stack-dynamic array | compile time | run time |
| Fixed heap-dynamic array | run time (변화  X) | run time |
| Heap dynamic array | run time (변화 可) | run time |

- 언어마다 제공하는 array 종류가 다름

### ◆ Heterogeneous Array


- 여러 data type 을 모은 array
- `record` 와 차이점
  - array 는 index 로 접근
  - record 는 name 으로 접근
- 대부분 heap dynamic 하게 구현

### ◆ Number of Subscripts in Array


- 과거에는 3차원까지만 표현 가능
- 현재는 차원에 제한이 없다
- C언어는 엄밀히 1차원. but 배열 자체가 또 다른 배열을 요소로 가질 수 있음 → multidimensional array
  - Orthogonal design

### ◆ Array Initialization


- C
  - static array → 초기화 가능
  - dynamic array → 초기화 불가능
{% raw %}
```c
int list_t[] = {4, 5, 7, 83}; 
char name[] = "Nang Jongho"; 
char *names[] = {"Mike", "Fred", "Mary Lou"};
```
{% endraw %}

- 초기화 불가능한 언어 / 독특하게 초기화 하는 언어 존재
- Python → list comprehension 
  - compact, but readability ↓ 

### ◆ Array Operation


- 가장 기본적인 operation : 원소 가져오기
- language 마다 구현된 operation 다름
- assignment, arithmetic, relation, logical
  - arithmetic → 사칙연산이 overloading 되어 있음
- ex) APL `+.*` → inner product

### ◆ Type of Array


- Rectangular array : ㅁ 모양, 모든 행 / 열 마다 동일한 개수 요소 가짐
- Jagged matrix / array : 각 행마다 가진 요소의 개수 다름

### ◆ Slice


- numpy
{% raw %}
```python
a = np.array([1,2,3])
b = np.array([4,5,6])

# 각 요소 더하기
c = a + b
c = np.add(a, b)
# c = [5 7 9]

# 각 요소 빼기
c = b - a
c = np.subtract(a, b)
# c = [3 3 3]

# 각 요소 곱하기
c = a * b
c = np.multiply(a, b)
# c = [4 10 18]

# 각 요소 나누기
c = a / b
c = np.divide(a, b)
# c = [0.25 0.4 0.5]
```
{% endraw %}

{% raw %}
```python
list1 = [
	[1, 2],
	[3, 4]
]

list2 = [
	[5, 6],
	[7, 8]
]

a = np.array(list1)
b = np.array(list2)

# matrix 곱하기
c = np.dot(a, b)
# c = [[19 22]
#      [43 50]]
```
{% endraw %}

{% raw %}
```python
a = np.array([[1, 2], [3, 4]])

# array 값 더하기
s = np.sum(a) # 10

# axis = 0 -> column 끼리 더하기
# axis = 1 -> row 끼리 더하기
s = np.sum(a, axis = 0)
# s = [4 6]

# array 값 곱하기
s = np.prod(a) # 24
```
{% endraw %}

### ◆ Implementation


- Single-dimensioned array
> address(list[k]) = address(list[1]) + (k-1) * element_size
                            = (address(list[1]) - element_size) + (k * element_size)

(address(list[1]) - element_size) 는 상수 → compile time 에 계산 가능

- Multidimensional array
  - memory 는 1차원 → 다차원 array 저장 시 memory 에는 1차원으로 바꿔 저장
  - row major order (→) 
    - 일반적으로 사용
  - column major order ( ↓ )
  - Example

| 3 | 4 | 7 |
| 6 | 2 | 5 |
| 1 | 3 | 8 |

    - row major : 3 4 7 / 6 2 5 / 1 3 8
    - column major : 3 6 1 / 4 2 3 / 7 5 8
> location(a[i][j])
= (address of a[1, 1] - ((n + 1) * element_size) + ((i * n + j) * element_size)

→ 그 이전까지의 모든 주소값 계산

## ✦ Associative array


- 보통 array 는 index 로 요소 접근
- Associative array 는 사용자가 정의한 `key` 를 통해 value 를 찾음
- 각 원소는 (`key`, `value` ) 쌍으로 구성 & unordered
- readability 향상
  - Python : 기본 자료구조
  - C++, Java, C# : library 로 제공

## ✦ Record Types


- 서로 다른 type 의 데이터를 모은 타입 
  - cf) array 는 type 이 같은 데이터를 모음
- 원소를 이름 (name) 을 통해 접근 (ex. `employee.name.first`)
- Example
  - COBOL (nested)
{% raw %}
```sql
01 EMPLOYEE-RECORD.
   02 EMPLOYEE-NAME.
      05 FIRST          PICTURE IS X(20).
      05 MIDDLE         PICTURE IS X(10).
      05 LAST           PICTURE IS X(20).
   02 HOURLY-RATE       PICTURE IS 99V99.
```
{% endraw %}

    - `MOVE CORRESPONDING` 
      - 두 레코드에서 같은 이름을 가진 필드끼리만 자동 복사

### ◆ Implement


- 각 필드들은 인접한 memory 공간에 **순서대로** 저장된다
- word alignment : 성능을 위해 메모리 주소가 4의 배수 (만약 8 byte 짜리 type 있으면 8의 배수) 가 되도록 padding 넣음
  - ex) 
{% raw %}
```c
struct aa {
	char c; // 1 byte
	int i; // 4 byte
} a;
```
{% endraw %}


| 1000 | 1001 | 1002 | 1003 | 1004 | 1005 | 1006 | 1007 |
|:--|:--|:--|:--|:--|:--|:--|:--|
| c | pad | pad | pad | i | i | i | i |

  - 실행 속도 ↑ 프로그램 실행 자체에는 문제 없음

## ✦ List Type


- Python List
  - Python 에서 list 는 array 역할도 함 (사실상 heterogeneous array)
  - 다른 언어와는 달리 가변 → 수정 가능
  - 원소는 어떤 type 이라도 다 가능!
{% raw %}
```python
# 리스트 생성
myList = [3, 5.8, "grape"] 

# 원소 접근 (index 는 0부터)
x = myList[1] # x = 5.8

# 원소 삭제 
del myList[1]
```
{% endraw %}

  - List Comprehension
    - 수학의 집합 표기법에서 유래
{% raw %}
```python
[x * x for x in range(7) if x % 3 == 0]
# [0, 9, 36]

[x * x for x in range(6) if x % 3 == 0]
# [0, 9]
```
{% endraw %}

## ✦ Union Types


- 같은 memory 공간에 서로 다른 type 의 값이 번갈아 저장 가능한 자료 구조
- Storage allocation
  - 크기 가장 큰 변수 기준 공간 잡고, 나머지는 앞부분만 사용
  - Example 
{% raw %}
```pascal
type shape = (circle, triangle, rectangle) ;
object =
  record
    case form : shape of
      circle    : (diameter : real) ;
      triangle  : (leftside : integer; rightside : integer; angle : real) ;
      rectangle : (side1 : integer; side2 : integer)
  end ;

var thing : object
```
{% endraw %}

![](/assets/images/notion/[pl]-data-types/img_4.png)

### ◆ Implementation


- Discriminated union → 모든 가능한 variant 가 같은 주소 사용
  - 제일 큰 변수에 storage 크기 맞추기
  - Example
    - Ada
{% raw %}
```pascal
type NODE (TAG : BOOLEAN) is
  record
    case TAG is
      when TRUE  => COUNT : Integer
      when FALSE => SUM   : char
    end case;
  end record;
```
{% endraw %}

      - `TAG` 가 `TRUE` 면 `COUNT(Integer)` 필드 사용 → 이만큼 공간 할당
      - `TAG` 가 `FALSE` 면 `SUM(char)`  필드 사용
→ 같은 memory 주소 공유

![](/assets/images/notion/[pl]-data-types/img_5.png)

  - `tag` 사용 → 현재 저장되어 있는게 어떤 type 인지 나타내는 값
    - tag 또한 하나의 저장 공간을 차지한다.
- Safety issue 있음

## ✦ Set type


- 같은 type 값을 unordered & 중복 X 하게 모은 자료 구조
- set 의 최대 원소 개수는?

### ◆ Implementation


- 메모리에서 bit string 으로 저장 
  - 합집합 : OR
  - 교집합 : AND

## ✦ Pointer and Reference Types


- Pointer : 변수의 값이 memory address (아무것도 가리키지 않음 `nil`)
- 용도
  - 간접 주소 지정 (indirect addressing) : 다른 변수 가리킴
  - 동적 메모리 관리 (dynamic storage management) : heap 메모리 할당 / 해제

### ◆ Pointer Operation


- Assignment (대입) : pointer 에 address 저장
  - C 에서 `&`
{% raw %}
```c
int *aa, bb, cc; // aa 만 포인터 변수
aa = &bb; // aa에 bb의 주소 저장
```
{% endraw %}

- Dereferencing (역참조) : pointer 가 가리키는 곳의 값을 가져옴
  - C 에서 `*`
{% raw %}
```c
cc = *aa; // cc에 aa가 가리키는 bb의 값 저장
```
{% endraw %}

![](/assets/images/notion/[pl]-data-types/img_6.png)

- pointer 의 arithmetic 연산 (+ / - )
{% raw %}
```c
char *c;
int  *i;

*(c + 1)   /* c가 가리키는 곳에서 1바이트 앞 */
*(i + 1)   /* i가 가리키는 곳에서 4바이트 앞 */
```
{% endraw %}

### ◆ Pointer 의 문제접


- Type Checking 
- Dangling Pointer : `free` 된 동적 변수 주소를 가리키고 있는 포인터
{% raw %}
```c
int *i;

sub1() {
    int j;
    j = 5;
    i = &j;
}

*i = ??
```
{% endraw %}

- Lost Object
  - 잃어버린 객체 (Garbage)
  - 접근 불가하지만 메모리 공간 차지 중인 동적 개체
→ `free` 불가 & 사용 불가 → memory leak (메모리 누수)

{% raw %}
```c
char *c;
c = malloc(...);   /* 첫 번째 할당 */
...
c = malloc(...);   /* 두 번째 할당 — 첫 번째 주소를 잃어버림 */
```
{% endraw %}

### ◆ Implementation


- pointer → word size
- Dangling Pointer 해결법
  1. Tombstone Approch (묘비석 방식)
    - 모든 동적 변수에 tombstone 이라는 중간 cell 둠.
    - pointer 는 변수를 직접 X tombstone 가리킴
    - 동작 방식
      - 동적 변수 할당 → tombstone 생성 & 실제 변수 가리킴
      - 동적 변수 해제 → tombstone `nil` 설정
      - 이후 pointer 로 접근 →tombstone 이 `nil` 이면 해제
![](/assets/images/notion/[pl]-data-types/img_7.png)

    - 단점 : tombstone 유지 시간 & 공간 비용 
  1. Locks-and-key Approach
    - pointer 값을 (key, address) 쌍으로 표현. 동적 변수에 lock 값 함께 저장
    - 동작 방식
      - 동적 변수 할당 → lock 값 생성, pointer 의 key 에 같은 값 복사
      - pointer 복사 → key 값도 함께 복사
      - 역참조 → pointer 의 key 와 변수의 lock 비교, 일치 시 접근 허용
      - 동적 변수 해제 → lock 값을 지움
![](/assets/images/notion/[pl]-data-types/img_8.png)

- Heap Management
  - 가정 : Heap 은 고정 크기로 할당된 공간 & 사용 가능한 cell 은 linked list 로 연결되어 관리
  - 해제가 암묵적으로 이루어지면 언제 수행?
    1. Reference Counter (참조 카운터) → 점진적 회수 (incremental reclamation)
      - 구현 방법 : 모든 cell 에 카운터 두고, 현재 그 cell 을 가리키는 pointer 수 저장
        - pointer 가 가리킴 → counter++
        - pointer 가 떠남 → counter—
        - counter 가 0이 됨 → memory 회수
      - 단점 
        - counter 저장 공간 overhead
        - counter 유지 실행 시간 overhead
        - circular reference 문제 → 서로를 가리키는 두 객체는 counter 절대 0 XX
![](/assets/images/notion/[pl]-data-types/img_9.png)

    1. Garbage Collection (가비지 컬렉션) → 일괄 회수 (batch reclamation)
      - run-time 시스템이 memory 계속 할당. 모든 memory 소진 → 한꺼번에 garbage 수거!
      - 모든 heap cell 에는 garbage 여부 표시 indicator bit (마크 비트) 있음
      - 고정 크기 Garbage Collection
        1. heap 의 모든 cell 을 garbage 로 표시
        1. 프로그램의 모든 pointer 추적해 접근 가능한 cell 은 garbage X 표시
        1. 남은 garbage 들 사용 가능 공간 리스트로 변환
      - 단점 
        - 메모리가 꽉 찼을 때 수행 → 필요할 때 가장 느리게 동작..
        - 마크 비트 저장 공간 overhead
        - 모든 pointer 추적 시간 overhead
      - 가변 크기 Garbage Collection 추가 문제
        - heap 의 모든 cell 을 garbage 로 초기 설정 어려움
        - pointer 없는 cell 있어 마킹 과정 발생
        - 회수 후 단편화 (fragmentation) 문제 → 사용 가능 공간 흩어짐
