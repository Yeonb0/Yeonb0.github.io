---
categories:
- Data-Structure
date: '2026-01-21'
tags:
- DS
- 자료구조
- 다항식
- 연결 리스트
title: '[DS] Polynomials'
toc: true
toc_sticky: true
---

##  4.4.1 Representing Polynomials As Singly Linked List

- A(x) = a_{m-1}x^{e_{m-1}} + \cdot\cdot\cdot \ + a_0x^{e_0} 을 Linked List로 표현
  - 계수는 음이 아닌 정수의 내림차순. a는 0이 아닌 계수.


```c++
typedef struct _poly_node {
	float coef;
	int expon;
	struct _poly_node *link;
} poly_node;
typedef poly_node *poly_pointer;


```



[Figure 4.11]

a = 3x^{14} + 2x^8 + 1 \\ b = 8x^{14} - 3x^{10} + 10x^6

![](/assets/images/notion/[ds]-polynomials/img_1.png)



##  4.4.2 Adding Polynomials

###  [Program 4.12] : Add 

```c++
poly_pointer 
```



###  [Program 4.13] : Attach 

```c++
void attach (float coefficient, int exponent, 
```

![](/assets/images/notion/[ds]-polynomials/img_2.png)



- padd 분석
  1. 계수 합하기
  1. 지수 비교하기
  1. 새 노드들 만들기
- 0 ≤ 계수 합 횟수 ≤ min{m, n}
→ 시간 복잡도 = O(m + n)



##  4.4.3 Erasing Polynomials

###  [Program 4.14] : Erase 

```c++
void erase(
```



##  4.4.4 Representing Polynomials As Circularly Linked Lists

- Circular list
  - 마지막 node 와 첫 node 연결
- Chain list
  - 한 방향으로 연결된 리스트. 끝 node가 null link 를 가지고 있음.
###  [Program 4.15] : Get empty node

```c++
poly_pointer
```



- 더 이상 사용하지 않는 빈 node를 다시 avail로 보내 재사용.
- avail : freed node 리스트의 첫 node를 가리키는 포인터


###  [Program 4.16] : Return empty node

```c++
void ret_node(
```



###  [Program 4.17] : Return all node of list

```c++
void cerase(
```

![](/assets/images/notion/[ds]-polynomials/img_3.png)



- 다항식을 circular list 로 표현 
- 다항식이 빈 상태를 표현하기 위해 dummy node 집어 넣기.
ex) 3x^{14} + 2x^8 +1

![](/assets/images/notion/[ds]-polynomials/img_4.png)



- circular list 로 바꾸면 달라지는 점
  1. (*ptr) check 삭제.
  1. starta = a, startb = b 라는 head node 를 가리키는 변수 추가
  1. while, for 조건 바꾸기
  1. NULL 검사 삭제
  1. 마지막에 circular로 만들기


- head node 의 expon을 -1로 설정. 


###  [Program 4.18] : Circular Polynomial add

```c++
poly_pointer
```

