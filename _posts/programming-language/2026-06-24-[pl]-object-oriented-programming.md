---
categories:
- Programming-Language
date: '2026-06-24T10:43:00.000+09:00'
layout: single
series: 프로그래밍 언어
step: 10
tags:
- OOP
- 프로그래밍 언어
- PL
- 캡슐화
- 상속
- C++
title: '[PL] Object-Oriented Programming'
toc: true
toc_sticky: true
---

## ✦ Introduction


### ◆ Programming Language Paradigms


- Procedure-Oriented Paradigm - 절차 지향
  - Block structure : 프로그램은 block + procedure 중첩 집합
  - 1960 ~ 1970 년대 - Algol, Pascal, PL/I, Ada, Modula
- Object-Oriented Paradigm - 객체 지향
  - Object-Based : 프로그램은 상호작용하는 객체 (object) 의 집합
  - Simula (67), Smalltalk (70s), 많은 언어들 (80s) (Simula, Smalltalk, C++, Eiffel, CLOS, ..)
- Concurrent, Distributed Programming Paradigm - 동시성, 분산
  - 다중 스레드, 동기화, 통신
  - fork-join (60s) → Ada-CSP (70s) → Linda (CSP, Argus, Actors, Linda, Monitors)
- Functional Programming Paradigm - 함수형
  - 프로그램은 함수 정의의 집합
  - semantic 명확, 암묵적 parallelism (LISP, ML, Miranda, Haskel, ..)
- Logic Programming Paradigm - 논리 프로그래밍
  - 프로그램은 theorem 의 집합
  - semantic 명확, 암묵적 parallelism (Prolog, Parlog, GHC, ..)

### ◆ Why OOP?


- 실세계 문제의 자연스러운 모델링
  - 여러 자율적 개체
  - 시뮬레이션 시스템
- 모듈성 (Modularity)
  - Data + Procedure
  - 문제 분해 (Software engineering)
  - 정보 은닉 (캡슐화)
- 소프트웨어 재사용성
  - 상속 (inheritance)
  - 유용한 class library (Smalltalk)
- 병렬성 (Parallelism) 
  - 각 객체는 병렬로 실행 가능
- 만능은 아닌 하나의 paradigm

## ✦ Basic Concepts of OOP


- Object-Oriented Programming
  - 프로그램이 객체 (object) 들의 협력적인 집합으로 조직되는 구현법
  - 각 객체 (object) → 어떤 class 의 instance 
  - class 는 모두 상속 (inheritance) 관계로 통합
- OOP Paradigm
  - 어떤 class 를 원하는지 결정
  - 각 class 에 대해 완전한 연산 집합 제공
  - 상속 (inheritance) 사용해 공통성 명시적으로 만듬 
- 단계
  1. **추상화 (Abstraction)
***"관련 없는 것을 제거하고, 본질적인 것을 강조한다 (Eliminate the Irrelevant, Amplify the Essential)"*
⬇

  1. **캡슐화 (Encapsulation)
***"불필요한 것을 숨긴다 (Hiding the Unnecessary)"*
⬇

  1. **상속 (Inheritance)
***"유사성을 모델링한다 (Modeling the Similarity)"*
⬇

  1. **다형성 (Polymorphism)
***"같은 함수, 다른 동작 (Same Function Different Behavior)"*

### ◆ Abstract Data Type


- 캡슐화 & 정보 은닉 모두 지원하는 데이터 구조
- Encapsulation (캡슐화)
  - Data & 조작하는 code 함께 정의 → 분리 / 따로 접근 불가능
  - Data 는 code 안에 캡슐화
  - procedure 만으로 데이터 직접 조작
  - 상호 의존성 ↓ → 시스템 신뢰성 & 수정 가능성 보장
- Information Hiding (정보 은닉)
  - 프로그램이 구현 or 내부 표현 모른다고 가정
  - 캡슐화 사용 방법
  - how 가 아닌 what 을 강조
  - Procedure Abstraction (subroutime) vs. Data Abstraction (ADT)
- 추상화 → 생각을 도움
- 캡슐화 → 변경을 안전하게 만듬

### ◆ Object and Message Sending


- Object
  - private data & method 가진 entity
    1. 상태 (states) : instance 변수 → private data
    1. operation set : method → private data 다루는 함수
- Message Sending
  - data → object 에 message 보내서 얻음
{% raw %}
```java
// 절차지향: 함수에 데이터를 넘긴다
push(stack, 5);

// 객체지향: 객체에게 "이걸 해줘"라고 부탁한다
myStack.push(5);   // myStack에게 "5를 push해라"는 메시지 전송
```
{% endraw %}

  - 간접 함수 호출
    - 함수 호출 전달 → 실제 어떤 함수 실행은 객체가 결정
      - dynamic vs. static message binding (25p.)
    - 객체끼리 소통 → message 전달에서 비롯
    - Selector (선택자) : 누구에게(receiver) + 무엇을(selector) + 어떤 정보(argument)
- Traditional Programming vs. OOP
  - Traditional → Procedure-Oriented Programming
    - data & 독립적 procedure 의 집합 → 함수 / 데이터 분리
    - 같은 인자면 같은 결과 → 예측 가능 but 상태 표현 难
    - 특정 타입에만 작동
  - OOP → Data-Oriented Programming
    - object 의 집합 (data + procedure)
    - 결과가 인자 + 객체의 내부 상태 (호출 이력) 에도 의존
    - 올바른 procedure 찾는 건 언어가 지원

| 관점 | 절차지향 | 객체지향 |
|:--|:--|:--|
| **주인공** | 함수(프로시저) | 객체 |
| **데이터와 함수의 관계** | 분리됨 | 캡슐화됨 (한 몸) |
| **결과 결정 요인** | 인자만 | 인자 + 객체 상태 |
| **함수 선택 방식** | 프로그래머가 명시 | 언어가 자동 (동적 바인딩) |
| **호출 방식** | `함수(데이터)` | `객체.메시지()` |
| **상태 관리** | 전역 변수 등으로 산만함 | 객체가 자기 상태 보유 |
| **다형성** | 어려움 | 자연스러움 |

### ◆ Classes and Instances


- Class
  - 객체를 만들기 위한 설계도
    - 구조 (Structure) = instace 변수 → 어떤 data 를 가지는가?
    - 행위 (Behavior) = method → 객체가 무엇을 할 수 있는가?
    - 상속 (Inheritance) = 부모 → 어떤 class 물려 받는가?
  - 변수의 종류
    - Class 변수 : class 에 저장되어 모든 instance 가 공유하는 변수
    - Instance 변수 : 각 instance 마다 독립적 local 저장소 가지는 변수
  - class 가 객체라면 class 도 class 를 가져야 함 → metaclass
- Example
{% raw %}
```java
// Student 클래스 예시
public class Student {
    // Data Members (Static attributes) - 인스턴스 변수
    private String name;
    private String grade;

    // Member Functions (Dynamic Operations) - 메소드
    public String getName() { return name; }
    public void printGrade() { System.out.println(grade); }
}

// Circle 클래스 예시
public class Circle {
    // Data Members
    private double radius;
    private String color;

    // Member Functions
    public double getRadius() { return radius; }
    public double getArea() { return Math.PI * radius * radius; }
}

// SoccerPlayer 클래스 예시
public class SoccerPlayer {
    // Data Members
    private String name;
    private int number;
    private int xLocation;
    private int yLocation;

    // Member Functions
    public void run() { /* 달리기 로직 */ }
    public void jump() { /* 점프 로직 */ }
    public void kickBall() { /* 공차기 로직 */ }
}

// Car 클래스 예시
public class Car {
    // Data Members
    private String plateNumber;
    private int xLocation;
    private int yLocation;
    private int speed;

    // Member Functions
    public void move() { /* 이동 로직 */ }
    public void park() { /* 주차 로직 */ }
    public void accelerate() { /* 가속 로직 */ }
}
```
{% endraw %}

### ◆ (Multiple) Inheritance


- Inheritance
  - class 간 부모 - 자식 관계

| 용어 | 다른 이름 | 의미 |
|:--|:--|:--|
| **Superclass** | Parent class, Base class | 부모 클래스 (물려주는 쪽) |
| **Subclass** | Child class, Derived class | 자식 클래스 (물려받는 쪽) |

  - 장점 : refinement (정제) & software reuse (재사용) 
    - 부모 기반으로 자식 Override 가능 
  - Classfication (분류) & Specialication (특수화)
  - Example
![](/assets/images/notion/[pl]-object-oriented-programming/img_1.png)

- 상속되는 것
  - instance 변수
  - method 
  - specialization
    - Adding : 새로운 instance 변수 & method 추가
    - Substitution (Overriding) : 부모가 이미 정의한 method를 자식이 자기 방식대로 다시 정의
    - Class Precendence List (클래스 우선순위 리스트) : 같은 이름 method / 변수가 여러 조상 → 가장 가까운 superclass 부터 찾기
- 상속 구조
  1. Hierarchical Inheritance (계층적 상속) - 트리 구조
    - 1 자식 - 1 부모
    - 대부분 OOP 언어가 사용
    - 장점 : 간단 & 효율적 
    - 단점 : 표현력 제한
  1. Inheritance by Delegation (위임에 의한 상속) 
    - 각 객체가 자기가 처리하지 못하는 메시지를 받으면, 다른 객체에게 위임(delegate)
  1. Multiple Inheritance (다중 상속)
    - 1 자식 - 多 부모
    - 장점: 공유 증가
    - 단점 : 변수 & 메소드 충돌 발생 가능 
      - class 우선순위 리스트 사용 
- 상속의 장점
  - 더 나은 개념적 모델링 
    - 일상 생활 직접적 모델링
    - 계층적 모델링 → 프로그램 이해 쉽게 만듬
  - Factorization (인수 분해)
    - 한 번만 기술하고 필요할 때 재사용
  - 설계에서 단계적 정제
    - 하향식 설계 & 검증
  - 다형성 (Polymorphism)

### ◆ Dynamic Method Binding and Polymorphism


- Dynamic Method Binding
  - Static message binding
    - compile time 에서 어떤 함수 호출할지 결정
    - statically typed language
  - Dynamic message binding
    - run time 에서 어떤 함수 호출할지 결정
    - Polymorphism (다형성) 지원

| 항목 | 정적 바인딩 | 동적 바인딩 |
|:--|:--|:--|
| **결정 시점** | compile time | run time |
| **판단 기준** | 선언 타입 | 실제 객체 타입 |
| **속도** | ⚡ 빠름 | 🐌 약간 느림 |
| **유연성** | 😐 낮음 | 😊 높음 |
| **다형성** | ❌ 불가능 | ✅ 가능 |
| **메모리 비용** | 없음 | vtable 공간 필요 |
| **Java 기본값** | static, final, private, 생성자 | 일반 메소드 (모두!) |
| **C++ 기본값** | 일반 멤버 함수 | `virtual` 키워드 붙은 메소드만 |

- Polymorphism (다형성)
  - 연산이 둘 이상이 타입 (or class) 에 대해 작동할 수 있는 능력
  - 분류
    - ad hoc polymorphism (임시 다형성) : 제한된 몇 가지 타입에만 각각 따로 정의
      - 강제 변환 (coercion)
      - operator overloading : 연산자 중복 정의
    - universal polymorphism (보편 다형성) : 한 코드가 무한히 많은 타입에 대해 동일하게 작동
      - 매개변수적 (parametric) : Generics `<>`
      - 상속 (inclusion) : 상속 계층을 통한 다형성
{% raw %}
```text
                      다형성 (Polymorphism)
                   ╱                      ╲
        Ad hoc 다형성              Universal 다형성
        (임시 다형성)               (보편 다형성)
        ╱          ╲                ╱            ╲
   Coercion    Overloading    Parametric      Inclusion
   (강제변환)   (중복정의)    (매개변수적)     (포함=상속)
```
{% endraw %}


| 종류 | 분류 | 작동 범위 | 구현 방식 | Java 예시 |
|:--|:--|:--|:--|:--|
| **Coercion** | Ad hoc | 정해진 타입 | 자동 타입 변환 | `int → double` 자동 변환 |
| **Overloading** | Ad hoc | 정해진 타입 | 같은 이름 여러 정의 | `print(int)`, `print(String)` |
| **Parametric** | Universal | 무한 타입 | 제네릭/템플릿 | `Box<T>`, `List<T>` |
| **Inclusion** | Universal | 무한 타입 | 상속 + 동적 바인딩 | `사람 a = new 학생()` |

## ✦ Object-Oriented Programming Languages


### ◆ Classification


- 언어의 분류 : Object / Class / Inheritance 를 지원하는가?
  - Obejct-based Language : 객체 (object) 지원
  - Class-based Language : 모든 객체 (object) 가 class 에 속해야 함
  - Object-Oriented Language : Class 가 상속 지원
    - 전통적 언어 확장 & 순수 객체 지향 언어
{% raw %}
```text
┌─────────────────────────────────────────┐
│ Object-Based                            │
│  Ada                                    │
│  ┌──────────────────────────────────┐   │
│  │ Class-Based                      │   │
│  │  Clu                             │   │
│  │  Actors                          │   │
│  │  ┌────────────────────────────┐  │   │
│  │  │ Object-Oriented            │  │   │
│  │  │  Simula  Smalltalk  C++    │  │   │
│  │  └────────────────────────────┘  │   │
│  │            + class inheritance   │   │
│  └──────────────────────────────────┘   │
│              + class                    │
└─────────────────────────────────────────┘
```
{% endraw %}

## ✦ A Case Study : C++


- C++ 
  - C 의 상위 집합 : C + class, 상속, 다형성, template
  - 객체지향 개념 통합
  - generic 기능 지원 : template `<>`
  - 효율성 + C 호환성
![](/assets/images/notion/[pl]-object-oriented-programming/img_2.png)

### ◆ Data Abstraction


- Class : 데이터 & 메소드 묶기
- Access Levels

| 접근 수준 | 의미 | 누가 접근 가능? |
|:--|:--|:--|
| **private** | 비공개 | 그 클래스 자신만 |
| **protected** | 보호됨 | 그 클래스 + 자식 클래스 |
| **public** | 공개 | 누구나 |

![](/assets/images/notion/[pl]-object-oriented-programming/img_3.png)

- Access Mode
  - public 파생 클래스 : superclass 와 동일
  - private 파생 클래스 : superclass 의 public 와 protected 가 private 으로 됨
- Example
{% raw %}
```cpp
const int MAXSIZE = 100;
class stack {
private:
    char stack[MAXSIZE];
    int top;
public:
    stack() {top = 0;}              // constructor
    void push(char);
    char pop();
};

void stack::push(char x) { 
    if ((top+1) == MAXSIZE) 
        error("stack is full\n");
    stack[++top] = x;
}

char stack::pop() {
    if (top == 0)
        error("stack is empty\n");
    return(stack[top--]);
}

stack st1;    /* static object creation */

main() { 
    char x, y;
    st1.push('a'); st1.push('b');
    x = st1.pop(); y = st1.pop();
    printf("%c, %c \n", x,y);
}
```
{% endraw %}

### ◆ Interitance


- Subtyping : inclusion 기반. 자식은 부모 타입의 한 종류
- Multiple Inheritance : 한 클래스가 여러 부모로 부터 상속
- Virtual Base Class : 가상 기반 클래스 (`virtual` 키워드 사용)

### ◆ Dynamic Binding


- Virtual Functions : 가상 함수. 동적 바인딩 켜기

### ◆ Polymorphism


- Template Function / Classes 
  - 타입을 매개 변수로 받기 → 한 코드가 여러 type 에 작동
- Operator Overloading : 같은 기호 or 함수 이름이 다른 의미로 사용
{% raw %}
```cpp
#include <iostream.h>
#include <string.h>
class String {
    char* str; int len;
public:
    String(const char*);
    ~String() {delete[] str;}
    char* getString() {return str;}
    String& operator += (String&);
}

String::String(const char* s) {
    len = strlen(s);
    str = new char[len+1];
    strcpy(str,s);
}

String& String::operator+= (String& s){
    len += s.len ; 
    char *p = new char[len+1];
    strcpy(p, str);
    strcat(p, s.str);
    delete str;
    str = p;
    return *this;
}

main() {
    String s1("I am");
    String s2("hungry");
    String s3("and sleepy");
    s1 += s2;
    cout << "The result is";
    cout << s1.getString() << "\n";
}
```
{% endraw %}

## ✦ Analysis


- OOP 장점
  - 캡슐화 & 데이터 추상화
    - reliability 향상
    - 절차적 명세 & 표현 명세 ↔ 구현 분리
  - 동적 바인딩 (Dynamic Binding)
    - 유연성 ↑ 
  - 상속 (Inheritance)
    - 소프트웨어 재사용성 증가
- OOP 단점
  - 높은 run time 비용 
    - 동적 바인딩
    - message passing
  - 구현 어려움
    - semantic gap
    - 소프트웨어 시뮬레이션
  - 클래스 라이브러리 배우기 어려움
![](/assets/images/notion/[pl]-object-oriented-programming/img_4.png)

## ✦ C++ as a Better C


1. `//` 주석
1. `inline` 인라인 함수
{% raw %}
```cpp
// C 매크로 — 위험
#define SQ(X) X*X
SQ(a+b)  →  a+b*a+b   // 연산자 우선순위 문제!

// C++ inline — 안전
inline int sq(int x) {return x*x;}
sq(a+b)  →  (a+b)*(a+b)  // 올바르게 처리
```
{% endraw %}

1. `const` 타입 있는 상수 → 값 변경 불가능
{% raw %}
```cpp
// C 방식 — 타입 없음, 디버거에 안 보임
#define PI 3.14159
#define MAXSIZE 100

// C++ 방식 — 타입 있음, 디버거에 보임, 컴파일러가 검증
const float pi = 3.14159;
const int max_size = 100;
const double* d_p = &pi;  // pi의 주소를 가리키는 포인터 (변경 불가)
char* const s = "abcd";   // 상수 포인터 (가리키는 대상 변경 불가)
```
{% endraw %}

1. `::` 선언 & scope 결정 
{% raw %}
```cpp
int i = 1;     // 외부 변수 i

main() {
    int i = 2; // 지역 변수 i (외부 i를 가림)
    {
        int n = i;   // n = 2 (지역 i)
        int i = 3;   // 또 다른 i
        cout << i;       // 3 (가장 안쪽 i)
        cout << ::i;     // 1 (외부 i — :: 로 접근)
        cout << "n = " << n;   // n = 2
    }
    cout << i;       // 2 (지역 i)
    cout << ::i;     // 1 (외부 i)
}
```
{% endraw %}

1. 함수 선언 시 인자 타입 명시 필수
1. 참조 선언 - 변수 별명 
{% raw %}
```cpp
int n;
int& nn = n;    // nn은 n의 별명(alias)
                // nn을 바꾸면 n도 바뀜

double a[10];
double& last = a[9];    // last는 a[9]의 별명
```
{% endraw %}


|  | 포인터 (`*`) | 참조 (`&`) |
|:--|:--|:--|
| null 가능 | ✅ | ❌ (반드시 초기화) |
| 역참조 필요 | `*p` | 그냥 변수처럼 사용 |
| 재할당 가능 | ✅ | ❌ |
| 산술 연산 | ✅ | ❌ |

1. 함수 매개 변수에 default 값 설정 가능 (뒤쪽 부터)
