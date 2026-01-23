---
categories:
- Data-Structure
date: '2026-01-21'
tags:
- DS
- 자료 구조
- 연결 리스트
title: '[DS] Additional List Operation'
toc: true
toc_sticky: true
---

##  4.5.1 Operations For Chains

- Singly Linked List 관리 함수들
- Declarations
```c
typedef struct _list_node {
	char data;
	struct _list_node *link;
} list_node; 
typedef list_node *list_pointer;
```



###  [Program 4.19] : Inverting list

```c
list_pointer invert(list_pointer lead) {
	// lead를 list의 끝으로 향하도록 방향 바꾸기. 역순 만들기.
	list_pointer middle, trail;
	middle = NULL;
	while (lead) { // lead가 null이 아니라면
		trail = middle; 
		middle = lead;
		lead = lead->link;
		middle->link = trail;
	}
	return middle;
}
```

![](/assets/images/notion/[ds]-additional-list-operation/img_1.png)



###  [Program 4.20] : Concatenate two list

```c++
list_pointer concatenate(list_pointer ptr1, list_pointer ptr2) {
	// 두 리스트를 ptr1, ptr2 순으로 연결한 리스트를 반환
	list_pointer temp;
	if (IS_EMPTY(ptr2))
		return ptr1; // ptr2가 비었다면 그냥 ptr1 반환
	else {
		if (!IS_EMPTY(ptr2)) { // 둘 다 빈 list가 아니라면
			for (temp = ptr1; temp->link; temp = temp->link) 
				; // link가 null 이 아니라면 한 칸 앞으로
			temp->link = ptr2; // ptr1 끝까지 저장 후 ptr2 연결
		}
		return ptr1; // ptr2 비었으면 그냥 ptr1 반환
								 // 안 비었으면 ptr1+ptr2 반환
	} // else 문 끝
}
```

![](/assets/images/notion/[ds]-additional-list-operation/img_2.png)



##  4.5.2 Operations For Circularly Linked Lists

###  [Program 4.21] : Insert at front

- 새 node 를 circular list의 front 에 삽입.
  - 맨 앞에 추가하기 위해선 *끝 node* 를 알아야 함.
  - circular list 의 이름은 first 보다 last 를 지정하는게 편하다. 
```c++
void insert_front(list_pointer *ptr, list_pointer node) { // ptr은 double pointer
	// ptr list의 첫 번째에 node 삽입.
	// ptr은 list의 가장 마지막 노드를 가리킴.
	if (IS_EMPTY(*ptr)) { // list 가 비었으면
		*ptr = node; 
		node->link = node; // node 1개인 circular list 
	} else { // 빈 list가 아니라면
		node->link = (*ptr)->link;
		(*ptr)->link = node;
	}
}
```

![](/assets/images/notion/[ds]-additional-list-operation/img_3.png)



- 맨 뒤에 node 를 넣고 싶을 때
```c++
else {
	node->link = (*ptr)->link;
	(*ptr)->link = node;
	*ptr = node; // 추가된 code
}
```

→ else 안을 다음과 같이 수정



###  [Program 4.22] : Length of List

```c++
int length(list_pointer ptr) {
	// list의 길이를 구함. ptr은 list의 가장 마지막 node
	list_pointer temp;
	int count = 0;
	if (ptr) { // 빈 list가 아니라면
		temp = ptr;
		do {
			count++;
			temp = temp->link; // 한 칸 앞으로
		} while (temp != ptr); // 다시 끝으로 돌아올 때까지
	} 
	return count;
}
```

