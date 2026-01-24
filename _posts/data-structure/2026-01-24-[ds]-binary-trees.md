---
categories:
- Data-Structure
date: '2026-01-24'
tags:
- 자료 구조
- DS
- 트리
- 이진 트리
title: '[DS] Binary Trees'
toc: true
toc_sticky: true
---

## 5.2.1 ADT 

- 모든 node 의 degree 는 최대 2개까지.
- left와 right 를 구분한다. → children의 순서 중요
![](/assets/images/notion/[ds]-binary-trees/img_1.png)



- Special types of binary trees 
  - Skewed tree : 비대칭 트리
  - Complete binary tree : 완전 이진 트리
![](/assets/images/notion/[ds]-binary-trees/img_2.png)





## 5.2.2 Properties Of Binary Trees

- Lemma 5.1 [Maximum number of nodes]
  1. level i에서의 최대 node 갯수는
2^{i-1}, \ i \ge 1

    - 같은 level 의 node 는 왼쪽부터 세기.
  1. depth가 k인 이진 트리의 최대 node 갯수는  
2^k-1, \ k \ge 0



- Complete Binary Tree : Tree의 원소를 왼쪽에서 오른쪽으로 하나씩 빠짐없이 채워나간 형태
![](/assets/images/notion/[ds]-binary-trees/img_3.png)



## 5.2.3 Binary Tree Representation

### Array Representation

- 1차원 배열로 표현. 0 번째 위치 저장X
- Lemma 5.3
  - node 가 n개인 Complete binary tree가 있고, 각 node가 인덱스 i (1 ≤ i ≤ n) 을 갖는다면,
    1. parent(i) = \lfloor {i \over 2} \rfloor , if i ≠ 1.
if i = 1, i는 root node 이므로 parent 를 가지지 않음.

    1. left_child(i) = 2i , if i ≤ n, 
if 2i > n, i는 left child 를 가지지 않음.

    1. right_child(i) = 2i+1, if 2i+1 ≤ n
if 2i > n, i는 right child 를 가지지 않음.

![](/assets/images/notion/[ds]-binary-trees/img_4.png)

  - 단점 : complete tree 가 아니면 공간 낭비가 많음.




### Node Representation

{% raw %}
```c
typedef struct _node {
	int data;
	struct _node *leftChild, *rightChild;
} node;
typedef struct node *treePointer;
```
{% endraw %}



![](/assets/images/notion/[ds]-binary-trees/img_5.png)

![](/assets/images/notion/[ds]-binary-trees/img_6.png)



