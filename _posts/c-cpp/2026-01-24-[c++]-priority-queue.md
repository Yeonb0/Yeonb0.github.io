---
categories:
- c-cpp
date: '2026-01-24'
tags:
- 자료 구조
- C++
- 우선순위 큐
- STL
title: '[C++] Priority Queue'
toc: true
toc_sticky: true
---

## Typedef



`std::priority_queue<T>` : **우선순위 큐(최대 힙 구조)**를 제공하는 컨테이너 어댑터

기본적으로 **최댓값**이 먼저 나옴 (내부적으로 `make_heap` 기반)

- 기본 컨테이너: `std::vector<T>`
- 정렬 기준: `std::less<T>` (최댓값이 먼저)
- 선언 예시
{% raw %}
```c++
#include <queue>
#include <vector>
#include <functional>
#include <iostream>

using namespace std;

priority_queue<int> pq1;                              // 기본: 최대 힙
priority_queue<int, vector<int>, greater<int>> pq2;   // 최소 힙
```
{% endraw %}

## 연산자

- `=` : 우선순위 큐 간 복사 및 대입
- `==`, `!=`, `<`, `>`, `<=`, `>=` : 비교 연산자 없음 (직접 비교 불가)
## 함수

### 1. 입력

- `void push(const T& value)`
  - 큐에 원소 추가 (우선순위 기준 자동 정렬)
{% raw %}
```c++
pq1.push(30);
pq1.push(10);
pq1.push(50);
```
{% endraw %}

### 2. 특정 원소 접근

- `const T& top()`
  - 가장 높은 우선순위(가장 큰/작은 값) 원소 반환
{% raw %}
```c++
cout << pq1.top();  // 50 (최대 힙일 경우)
```
{% endraw %}

### 3. 크기 관련 함수

- `size_t size()`
  - 원소 개수 반환
{% raw %}
```c++
cout << pq1.size();  // 3
```
{% endraw %}

- `bool empty()`
  - 큐가 비어 있는지 확인
{% raw %}
```c++
cout << pq1.empty();  // false
```
{% endraw %}

### 4. 삭제

- `void pop()`
  - 가장 높은 우선순위의 원소 제거
{% raw %}
```c++
pq1.pop();  // 50 제거
```
{% endraw %}

## 커스터마이징 (사용자 정의 정렬 기준)

사용자 정의 비교 함수 구조체 또는 람다 사용 가능

{% raw %}
```c++
struct Compare {
  bool operator()(int a, int b) {
    return a > b;  // 오름차순 (작은 값 우선)
  }
};

priority_queue<int, vector<int>, Compare> pq_custom;
```
{% endraw %}

또는 람다 사용 (C++11 이상)

{% raw %}
```c++
auto cmp = [](int a, int b) { return a > b; };
priority_queue<int, vector<int>, decltype(cmp)> pq_lambda(cmp)
```
{% endraw %}

