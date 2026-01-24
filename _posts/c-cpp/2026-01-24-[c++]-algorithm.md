---
categories:
- c-cpp
date: '2026-01-24'
tags:
- STL
- C++
- 알고리즘
- 정렬
title: '[C++] Algorithm'
toc: true
toc_sticky: true
---

## **1. 개요**

`<algorithm>` 헤더는 C++ STL에서 다양한 범용 알고리즘 함수들을 제공합니다. 이들은 대부분 반복자 범위(예: `[first, last)`)를 기반으로 작동하며, 시퀀스 컨테이너(`vector`, `list`, 등)에서 사용됩니다.

{% raw %}
```c++
 #include <algorithm>
```
{% endraw %}

## **2. 분류별 주요 알고리즘**

### **🔹 정렬 및 관련**

| **함수** | **설명** |
| `sort(first, last)` | 오름차순 정렬 |
| `stable_sort(first, last)` | 안정 정렬 |
| `partial_sort(first, middle, last)` | 일부 정렬 |
| `nth_element(first, nth, last)` | n번째 원소를 그 위치에 |
| `is_sorted(first, last)` | 정렬 여부 확인 |
| `reverse(first, last)` | 역순 정렬 |
| `rotate(first, middle, last)` | 회전 (앞으로 당김) |

### **🔹 탐색**

| **함수** | **설명** |
| `find(first, last, val)` | 값 찾기 |
| `find_if(first, last, pred)` | 조건 만족하는 첫 값 |
| `find_end()` | 마지막 일치 시퀀스 찾기 |
| `find_first_of()` | 첫 일치 요소 |
| `binary_search(first, last, val)` | 이진 탐색 (정렬 필요) |
| `lower_bound()` / `upper_bound()` | 범위 탐색 |
| `equal_range()` | 값이 들어갈 범위 쌍 |

### **🔹 비교**

| **함수** | **설명** |
| `equal(first1, last1, first2)` | 두 시퀀스 비교 |
| `lexicographical_compare()` | 사전 순 비교 |
| `mismatch(first1, last1, first2)` | 처음 불일치 위치 |

### **🔹 복사 및 이동**

| **함수** | **설명** |
| `copy(first, last, dest)` | 복사 |
| `copy_if()` | 조건 만족하는 요소만 복사 |
| `copy_n(first, n, dest)` | n개 복사 |
| `move(first, last, dest)` | 이동 |
| `swap_ranges()` | 범위 교환 |
| `fill(first, last, val)` | 범위 채우기 |
| `fill_n(dest, n, val)` | n개 채우기 |
| `generate()` / `generate_n()` | 함수로 값 생성 |

### **🔹 제거**

| **함수** | **설명** |
| `remove(first, last, val)` | 값 제거 (재배치) |
| `remove_if()` | 조건 만족 제거 |
| `unique(first, last)` | 중복 제거 (연속된 중복) |
| `erase()`와 함께 사용해야 실제 삭제 가능 |  |

### **🔹 수정 및 변형**

| **함수** | **설명** |
| `replace(first, last, old, new)` | 값 교체 |
| `replace_if()` | 조건 만족 값 교체 |
| `transform()` | 변환하여 저장 |
| `for_each()` | 각 요소에 함수 적용 |

### **🔹 집계 및 검사**

| **함수** | **설명** |
| `count(first, last, val)` | 특정 값 개수 |
| `count_if()` | 조건 만족 개수 |
| `min()`, `max()` | 최소, 최대 값 |
| `min_element()`, `max_element()` | 최소, 최대 반복자 |
| `accumulate()` (헤더 `<numeric>`) | 합계 계산 |
| `all_of()` / `any_of()` / `none_of()` | 조건 검사 |

### **🔹 집합 연산 (정렬 필요)**

| **함수** | **설명** |
| `set_union()` | 합집합 |
| `set_intersection()` | 교집합 |
| `set_difference()` | 차집합 |
| `set_symmetric_difference()` | 대칭차 |

### **🔹 기타**

| **함수** | **설명** |
| `iota(first, last, val)` (헤더 `<numeric>`) | 연속된 값으로 채우기 |
| `next_permutation()` / `prev_permutation()` | 순열 생성 |
| `random_shuffle()` / `shuffle()` | 셔플 |

## **3. 예제 코드**

{% raw %}
```c++
 #include <iostream>
 #include <vector>
 #include <algorithm>
 using namespace std;
 
 int main() {
     vector<int> v = {5, 3, 1, 4, 2};
 
     sort(v.begin(), v.end());
     reverse(v.begin(), v.end());
 
     for_each(v.begin(), v.end(), [](int x) {
         cout << x << " ";
     });
     cout << endl;
 
     if (binary_search(v.begin(), v.end(), 3)) {
         cout << "Found 3" << endl;
     }
 
     return 0;
 }
```
{% endraw %}

## **4. 주의사항**

- 대부분의 알고리즘은 반복자 범위를 사용
- 수정 알고리즘은 원본 컨테이너를 변경함
- `remove()`와 `erase()`를 함께 사용하는 idiom은 중요
{% raw %}
```c++
 v.erase(remove(v.begin(), v.end(), value), v.end());
```
{% endraw %}

