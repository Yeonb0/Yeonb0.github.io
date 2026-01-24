---
categories:
- c-cpp
date: '2026-01-24'
tags:
- 자료 구조
- 집합과 맵
- STL
- C++
title: '[C++] Multiset'
toc: true
toc_sticky: true
---

# → set 헤더 안에 있는 중복 가능 set

## **1. 개요**

`std::multiset`은 **중복을 허용하는 정렬된 컨테이너**입니다.

모든 요소는 자동으로 정렬되며, 내부적으로 **Red-Black Tree(균형 이진 탐색 트리)** 로 구현되어 있습니다.

{% raw %}
```c++
#include <set>
multiset<int> ms;
```
{% endraw %}

## **2. 주요 특징**

- **중복 요소 허용**
- 삽입 시 **자동 정렬**
- 트리 기반 → 탐색, 삽입, 삭제: **O(log N)**
- Key는 변경 불가 (요소 수정 시 재삽입 필요)
- 정렬 기준은 기본적으로 `<` 연산(오름차순), 필요 시 비교 함수 지정 가능
## **3. 주요 멤버 함수**

- **최솟값 = *****`begin()`**
- **최댓값 = *****`rbegin()`**
| 함수 | 설명 |
| --- | --- |
| `insert(val)` | 요소 삽입 (중복 허용) |
| `emplace(args...)` | 직접 생성하여 삽입 |
| `erase(val)` | 값이 `val`인 모든 요소 제거 |
| `erase(it)` | 특정 iterator가 가리키는 요소 제거 |
| `count(val)` | 특정 값의 개수 반환 |
| `find(val)` | 해당 값의 첫 위치 iterator 반환 |
| `equal_range(val)` | 값이 `val`인 구간의 `[first, last)` 반환 |
| `lower_bound(val)` | `val` 이상 첫 위치 |
| `upper_bound(val)` | `val` 초과 첫 위치 |
| `clear()` | 모든 요소 삭제 |
| `begin(), end()` | 반복자 접근 |
| `size()` | 요소 개수 반환 |
| `empty()` | 비어있는지 확인 |

## **4. 예제 코드**

### 기본 사용

{% raw %}
```c++
#include <iostream>
#include <set>
using namespace std;

int main() {
  multiset<int> ms;

  ms.insert(3);
  ms.insert(1);
  ms.insert(3);
  ms.insert(2);

  for (int x : ms) {
    cout << x << " ";
  }
  // 출력: 1 2 3 3

  return 0;
}
```
{% endraw %}

### 값의 개수 세기

{% raw %}
```c++
multiset<int> ms = {1, 2, 2, 2, 3};
cout << ms.count(2); // 3
```
{% endraw %}

### `equal_range()`로 동일한 값 범위 얻기

{% raw %}
```c++
auto [first, last] = ms.equal_range(2);
for (auto it = first; it != last; ++it)
  cout << *it << " ";
```
{% endraw %}

### 정렬 기준 커스터마이징

{% raw %}
```c++
multiset<int, greater<int>> ms2;  // 내림차순 정렬
```
{% endraw %}

### 특정 값 하나만 제거하기

{% raw %}
```c++
auto it = ms.find(3);
if (it != ms.end())
  ms.erase(it);  // 3 하나만 제거
```
{% endraw %}

## **5. **`multiset` vs `set` vs `unordered_multiset` 비교

| 항목 | `set` | `multiset` | `unordered_multiset` |
| --- | --- | --- | --- |
| 중복 허용 | ❌ | ✅ | ✅ |
| 정렬 여부 | 정렬됨 | 정렬됨 | 정렬되지 않음 (해시 기반) |
| 탐색/삽입/삭제 | O(log N) | O(log N) | 평균 O(1) |
| 내부 구조 | RB-tree | RB-tree | Hash-table |
| 순회 | 정렬된 순서 | 정렬된 순서 | 임의 순서 |



