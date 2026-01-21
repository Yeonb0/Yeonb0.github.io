---
categories:
- Data-Structure
date: '2026-01-21'
tags:
- DS
- 자료구조
- 연결 리스트
title: '[DS] Singly Linked Lists'
toc: true
toc_sticky: true
---

[Figure 4.1]

![](/assets/images/notion/[ds]-singly-linked-lists/img_1.png)

  - ptr은 연결 리스트의 이름.
  - Note that
    1. node들은 연속적인 위치에 존재하지 않는다.
    1. node의 위치는 실행할 때마다 달라질 수 있다.
  - 특정 주소 값을 보는 경우는 거의 없다.


- 연결 리스트에 새 node 삽입
![](/assets/images/notion/[ds]-singly-linked-lists/img_2.png)

  1. 사용하지 않는 새 node 생성. 그 주소는 paddr이라 하자.
  1. 새 node의 data 부분을 넣기.
  1. 2번 node의 link를 paddr로 지정.
  1. paddr의 link를 3번 node로 지정.


- 연결 리스트에서 node 삭제
![](/assets/images/notion/[ds]-singly-linked-lists/img_3.png)

  1. 삭제할 node의 앞 node를 찾기.
  1. 앞 node의 link를 삭제할 node의 다음 node로 지정.


- 연결 리스트의 필수 요소
  1. self-referential structure : node의 구조 정의 방법. 자기 참조 구조체.
  1. malloc : 새 node를 만들 때 필요
  1. free : 더 이상 필요 없는 node를 삭제할 때 필요


##  Example 4.1 [List of words ending in *at*]

- Declarations
```c++
typedef struct _list_node { // 구조체 이름 _ 사용
	char data[4];
	struct _list_node *link; // 자기 참조. 다음을 가리킬 pointer
} list_node;
typedef list_node *list_pointer; // list 전체를 가리키는 pointer


```



- 빈 list 확인 매크로
```c++
#define IS_EMPTY(ptr) (!(ptr)) 
// 비었으면 true, 요소가 있다면 false
```



- 새 node 생성 : malloc 이용.
```c++
ptr = (
```



- node 의 data에 값 넣기
```c++
strcpy(ptr->data, "bat");
ptr->link = NULL;
```



![](/assets/images/notion/[ds]-singly-linked-lists/img_4.png)

##  Example 4.2 [Two-node linked list]

- Declarations
```c++
typedef struct _list_node {
	char data[4];
	struct _list_node *link;
} list_node;
typedef list_node *list_pointer; // list 전체를 가리키는 pointer

```

###  [Program 4.2] 

```c++
list_pointer
```

![](/assets/images/notion/[ds]-singly-linked-lists/img_5.png)



##  Example 4.3 [List insertion]

- 연결 리스트를 가리키는 `list_pointer`` ``*ptr` 
- 가능한 저장 공간이 있는지 확인하는 매크로 `IS_FULL`


###  [Program 4.3] : Insert Function

```c++
void insert(
```

![](/assets/images/notion/[ds]-singly-linked-lists/img_6.png)

![](/assets/images/notion/[ds]-singly-linked-lists/img_7.png)



##  Example 4.4 [List deletion] 

- 삭제될 node의 위치에 의존적
- 3개의 pointer 필요
  - ptr : list의 시작점
  - node : 삭제하고 싶은 node
  - trail : 삭제하고 싶은 node의 앞 node
###  [Program 4.4] : Delete Function

```c++
void delete(
```

![](/assets/images/notion/[ds]-singly-linked-lists/img_8.png)

![](/assets/images/notion/[ds]-singly-linked-lists/img_9.png)



##  Example 4.5 [Printing out a list]

###  [Program 4.5] : Print List Function

```c++
void print_list(
```



###  [Program 4.6] : Search Function

```c++
list_pointer
```



###  [Program 4.7] : Merge Function

```c++
void merge(
```

ex)

  1. x→data ≤ y→data
① last→link = x

② last = x

③ x = x→link

  1. y→data ≤ x→data
  1. x→data
④ last = *z

⑤ *z = last→link

⑥ free(last)

