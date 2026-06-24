---
categories:
- Programming-Language
date: '2026-06-24T10:41:00.000+09:00'
layout: single
series: 프로그래밍 언어
step: 8
tags:
- PL
- 프로그래밍 언어
- 예외 처리
- 이벤트
title: '[PL] Exception Handling and Event Handling'
toc: true
toc_sticky: true
---

## ✦ Introduction to Exception Handling


### ◆ Exception Handling


- Exception (예외) : 프로그램 실행 중 비정상적인 일이 발생했다는 신호
  - H/W exception : FP overflow, divide-by-zero, I/O 오류
  - S/W exception (compiler 가 생성한 코드) : 배열 range 오류, 사용자 코드 등
- Exception Handling : 예외 감지 후 필요할 수 있는 특별한 처리
  - Pre-defined : 암묵적으로 발생
  - User-defined : 사용자 코드 의해 명시적 발생
- Exception Handler : 예외 처리 코드 단위
{% raw %}
```cpp
void example() {
    ...
    average = sum / total;
    ...
    return;
/* Exception handlers */
    when zero_divide {
        average = 0;
        printf("Error-divisor (total) is zero\n");
    }
    ...
}
```
{% endraw %}

- C : 예외처리 기능 X, 예외 발생 → 제어가 OS 로 넘어가 프로그램 죽어버림

### ◆ Advantages of Built-in Exception Handling


1. 오류 감지 코드 → 작성 번거로움 + 프로그램 어수선하게 함
{% raw %}
```java
`if (row >= 0 && row < 10 && col >= 0 && col < 20)
    sum += mat[row][col];
else
    System.out.println("Index range error on mat, row = " +
                        row + " col = " + col);
```
{% endraw %}

  - 예외 처리 기능 존재 → compiler 가 모든 배열 요소 접근 전에 기계어 코드 삽입 가능
→ 소스 프로그램 단축 & 단순화 가능
1. Exception propagation → 예외 처리 코드 재사용 가능
  - 한 프로그램 단위에서 발생한 예외 → dynamic / static 상위 계층에서도 처리 가능
  - 여러 곳에서 발생하는 동일한 예외 모두 처리 가능
1. 프로그래머가 다양한 가능한 오류들 고려하도록 장려 → 안정성 ↑ 

### ◆ Design Issue


1. handler 의 위치 & 범위 : 어디에 작성? 어느 범위의 코드에 적용?
1. binding : 임의의 예외 발생 시 어떤 handler 가 처리?
1. 정보 전달 : 예외 발생 원인 & 상세 정보 전달?
1. continuation vs. resumption : handle 이후 재개? 중단?
1. finalization : 어떤 형태의 종료 처리 제공?
![](/assets/images/notion/[pl]-exception-handling-and-event-handling/img_1.png)

## ✦ Exception Handling in C++


- C++ : 사전 정의된 예외 X
  - 예외 → 사용자 or library 의해 정의 & 명시적 발생
- Handler : `try` & `catch`
{% raw %}
```cpp
try {
//** Code that might raise an exception
}
catch (formal parameter) {
//** A handler body
}
...
catch (formal parameter) {
//** A handler body
}
```
{% endraw %}

  - `catch` : formal parameter 1개만 가능
  - `catch` 블록 적용 범위 → 예외 핸들러의 범위
- Example
  - C++ → divide-by-zero 직접 예외처리 해야함
{% raw %}
```cpp
// Program to depict how to handle
// divide by zero exception

#include <iostream>
#include <stdexcept>
using namespace std;

// Defining function Division
float Division(float num, float den){
    // If denominator is Zero throw runtime_error
    if (den == 0) {
        throw runtime_error("Math error: 
Attempted to divide by Zero\n");}
    return (num / den);
}

int main(){
    float numerator, denominator, result;
    numerator = 12.5;
    denominator = 0;
    try {
        result = Division(numerator, denominator);
        // this will not print in this example
        cout << "The quotient is "
             << result << endl;
    }
    catch (runtime_error& e) {
        cout << "Exception occurred" << endl
             << e.what();
    }
} // end main
```
{% endraw %}

- handler 에 예외 바인딩 : `throw [expression]`
  - `throw` 로 던진 객체의 타입을 확인, 일치하는 타입의 `catch` 블록을 위 → 아래 순서대로 탐색
- `catch` : 매개변수로 `(...)` 사용 → type 상관없이 모든 예외 잡음. 마지막에 사용 (모든 예외 잡기 보장)
- Unhandled Exceptions
  - 함수에서 예외 못잡음 → 점점 위로 올라감
  - `main` 에서도 처리 X → 프로그램 비정상 종료
→ Exception propagation
- Continuation
  - handler 실행 완료 후 → try { } 바로 다음 문장
{% raw %}
```cpp
// x = 10, y = 0 인 경우
try {
    if(y==0)
      throw 10;
        count<<"x/y = "<<x/y;
}
catch(int i) {  ← 예외 잡힘
    count<<"Exception Division by 0";
}
return 0;
```
{% endraw %}

{% raw %}
```cpp
// x = 10, y = 2 인 경우
try {
    if(y==0)
        throw 10;
      count<<"x/y = "<<x/y;  ← 정상 실행
}
catch(int i) {
    count<<"Exception Division by 0";
}
→ return 0;  ← catch 이후로 계속
```
{% endraw %}

- Evaluation
  - 함수 내에서 처리 X 예외 → caller 에게 전파
  - 사전 정의된 H/W 예외 X
{% raw %}
```cpp
#include <stdexcept>  // standard exception types

class Fraction {
    int numer_;
    int denom_;
public:
    explicit constexpr
    Fraction (int numerator, int denominator):
        numer_{numerator}, denom_{denominator}
    {
        if (denom_ == 0)
            throw std::invalid_argument{"denominator must not be zero"};
    }
    ...
};

int main () {
    try {
        int d = 1;
        std::cin >> d;
        Fraction f {1,d};
        ...
    }
    catch (std::invalid_argument const& e) {
        // deal with / report error here
        std::cerr << "error: " << e.what() << '\n';
    }
    ...
}
```
{% endraw %}

- Example 2
{% raw %}
```cpp
#include <iostream>
#include <stdexcept>

void func3(int input) {
    if (input < 10)
        throw std::runtime_error("Exception in func3");
}
void func2(int input) {
    func3(input);
}
void func1(int input) {
    func2(input);
}
int main(int argc, char* argv[]) {
    int input = std::stoi(argv[1]);
    try {
        func1(input);
    } catch (const std::exception& e) {
        std::cerr << "Exception caught: " << e.what() << std::endl;
    }
    return 0;
}
```
{% endraw %}

  - func3 에서 예외 발생 시 func2, func1 나머지 부분 실행 X

## ✦ Exception Handling in Java


- Java Virtual Machine (JVM) : 암묵적 발생 사전 정의된 예외 모음 포함
- Classes of Exceptions
  - 모든 예외 → `Throwable` 클래스의 자손
    - Error
      - Java interpreter 가 throw (ex. heap overflow)
      - 사용자 프로그램에서 처리 X
    - Exception
      - IOExeption : [`java.io`](http://java.io/) 패키지에서 입출력 연산 중 오류 발생 시 thrown
      - RuntimeException : 배열 range, null pointer 문제 등
      - 사용자 정의 예외
  - 사용자 정의 예외는 Exception 상속
- Java Excpetion Handler
  - 모든 catch → 이름이 있는 parameter 요구. 모든 parameter 는 throwable 의 자손.
  - `try` & `catch` → C++ 과 동일
    - `try` : 예외 발생 가능 코드
    - `catch` : 예외 처리 코드
  - 예외 → `throw new MyException();`  (new 연산자 이용 객체 생성)
  - `finally` : 예외 발생 여부 관계없이 항상 실행되는 블록
{% raw %}
```java
public class Main {
    public static void main(String[] args) {
        try {
            int[] myNumbers = {1, 2, 3};
            System.out.println(myNumbers[10]);
        } catch (Exception e) {
            System.out.println("Something went wrong.");
        } finally {
            System.out.println("The 'try catch' is finished.");
        }
    }
}
```
{% endraw %}

![](/assets/images/notion/[pl]-exception-handling-and-event-handling/img_2.png)

## ✦ Exception Handling in Python


{% raw %}
```python
try:
    my_file = open('0001-Copy1.1999-12-10.farmer.ham.txt', "r")
    file_content = my_file.read()

except NameError:
    print("Undefined variable is used!!")

else:
    print("Content read successfully.")

finally:
    my_file.close()
    print("File is closed.")

## Content read successfully.
## File is closed.
```
{% endraw %}

- `try` : 이 코드를 실행
- `except` : 예외 발생 시, 이 코드를 실행
- `else` : 예외가 없으면, 이 코드를 실행
- `finally` : 마지막에 항상 이 코드를 실행
{% raw %}
```python
# 다중 except 블록

try:
    num1 = int(input("enter value of number1: "))
    num2 = int(input("enter value of number2: "))
    result = num1/num2
    print(result)
except ValueError:
    print("Not valid number")
except ZeroDivisionError:
    print("Number Cannot be Divided by Zero")
except:
    print("This is the Generic Error")
```
{% endraw %}

- `sys.exc_info()[0]` : 현재 발생한 예외의 class 타입 반환하는 함수
{% raw %}
```python
# define Python user-defined exceptions
class InvalidAgeException(Exception):
    "Raised when the input value is less than 18"
    pass

# you need to guess this number
number = 18

try:
    input_num = int(input("Enter a number: "))
    if input_num < number:
        raise InvalidAgeException
    else:
        print("Eligible to Vote")

except InvalidAgeException:
    print("Exception occurred: Invalid Age")
```
{% endraw %}

- `raise` : Java/C++ 의 `throw` . 사용자가 직접 예외 발생시킬 때 사용
{% raw %}
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    retval = 10/0
except ZeroDivisionError as e:
    pass
```
{% endraw %}

- `except ... as` : 발생한 예외 객체를 변수에 담아 사용
  - `catch(Exception e)`  에서 `e` 에 해당
- `pass` : 아무것도 하지 않음
  - 예외 잡았지만 별도 처리 없이 넘어가고 싶을 때 사용

## ✦ Introduction to Event Handling


### ◆ Event Handling


- Event : 특정한 일이 발생했다는 알림 (click, drag, key 입력 등)
- Event Handler : Event 에 반응해 실행되는 code segment
- Event Handling : exeception handling 과 유사
  - 공통점 : Handler 는 암묵적으로 호출 (by. event, exeception)
  - 차이점
    - exception : 사용자 코드 의해 명시적 / 하드웨어 & 소프트웨어 interpreter 의해 암묵적으로 생성
    - event : 외부 행동 (GUI 로 사용자 상호 작용) 으로 인해 생성

### ◆ Event Driven Programming Model


- 프로그램이 event 에 의해 실행 → 유저가 정확히 언제 실행할지 예측 불가능
![](/assets/images/notion/[pl]-exception-handling-and-event-handling/img_3.png)
