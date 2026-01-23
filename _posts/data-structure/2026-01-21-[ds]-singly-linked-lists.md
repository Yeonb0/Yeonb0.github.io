---
categories:
- Data-Structure
date: '2026-01-21'
tags:
- DS
- 자료 구조
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
ptr = (list_pointer) malloc (sizeof(LNODE));
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
list_pointer ptr = NULL; // 새로운 빈 list 생성.
```

###  [Program 4.2] 

```c++
list_pointer create2(){
	// 2개의 node를 가진 list를 만듬
	list_pointer first, second;
	first = (list_pointer) malloc(sizeof(list_node));
	second = (list_pointer) malloc(sizeof(list_node)); // node만큼의 공간 할당
	second->link = NULL;
	second->data = 20;
	first->data = 10;
	first->link = second;
	return first;
}
```

![](/assets/images/notion/[ds]-singly-linked-lists/img_5.png)



##  Example 4.3 [List insertion]

- 연결 리스트를 가리키는 `list_pointer *ptr` 
- 가능한 저장 공간이 있는지 확인하는 매크로 `IS_FULL`


###  [Program 4.3] : Insert Function

```c++
void insert(list_pointer *ptr, list_pointer node){ 
	// ptr은 연결 list의 첫 node 주소, node 다음에 새 node 추가할 것임.
	// 새 node에 temp 50의 값 저장 후 node 다음에 삽입.
	list_pointer temp;
	temp = (list_pointer) malloc(sizeof(list_node));
	if(IS_FULL(temp)){ // 저장 공간이 없으면
		fprintf(stderr, "The memory is full\n");
		exit(1);
	}
	temp->data = 50; // data 저장
	if(*ptr) { // empty list가 아니라면
		temp->link = node->link; // ① 다음 노드 연결
		node->link = temp; // ② 기존 연결 바꾸기
	} else { // empty list 라면
		temp->link = NULL; // temp가 첫 node
		*ptr = temp;
	}
}
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
void delete(list_pointer *ptr, list_pointer trail, list_pointer node) {
	// ptr 리스트에서 node 삭제. trail은 node의 바로 앞 node
	if (trail) // 앞에 노드가 있으면
		trail->link = node->link; // 삭제 node의 다음을 연결
	else // node가 맨 앞일 때
		*ptr = (*ptr)->link; // 삭제 node의 다음 node를 list의 시작점으로
	free(node); // node 해방 = 삭제
}
```

![](/assets/images/notion/[ds]-singly-linked-lists/img_8.png)

![](/assets/images/notion/[ds]-singly-linked-lists/img_9.png)



##  Example 4.5 [Printing out a list]

###  [Program 4.5] : Print List Function

```c++
void print_list(list_pointer ptr) { // 값의 변경 없으므로 *값 아닌 그냥 주소 전달
	printf("The list contains: ");
	for( ; ptr; ptr->link) // ptr 값이 NULL이 아닐 때까지
		printf("%4d", ptr->data);
	printf("\n");
}
```



###  [Program 4.6] : Search Function

```c++
list_pointer search(list_pointer ptr, int num){
	// ptr은 찾을 list, num은 list 안에서 찾을 수
	for( ; ptr; ptr->link) // ptr 값이 NULL이 아닐 때까지
		if (ptr->data == num) return ptr; // 찾는 num을 data로 가지고 있는 node의 주소
	return ptr; // 못 찾을 시 NULL 반환
}
```



###  [Program 4.7] : Merge Function

```c++
void merge(list_pointer x, list_pointer y, list_pointer *z) {
	// list x, y를 오름차순으로 정렬한 list z를 반환. 
	// x, y의 값은 변화 X -> call-by-value
	// z의 값은 변화 O -> call-by-reference
	list_pointer last;
	last = (list_pointer) malloc(sizeof(LNODE)); // 빈 list 할당
	*z = last; // z는 empty list
	
	while (x && y) { // 둘 중 하나가 NULL이 될 때까지
		if (x->data <= y->data) { // 더 작은 값부터 옮기기. (x)
			last->link = x; // ①
			last = x; // ②
			x = x->link; // ③
		} else { // (y)
			last->link = y;
			last = y;
			y = y->link;
		}
	}
	// 둘 중 남아있는 list 옮기기
	if (x) last->link = x;
	if (y) last->link = y;
	
	last = *z; // ④
	*z = last->link; // ⑤
	free(last);	// ⑥
}
```

ex)

  1. x→data ≤ y→data
① last→link = x

​	② last = x	

​	③ x = x→link

2. y→data ≤ x→data

3. x→data
   ④ last = *z

​	⑤ *z = last→link	

​	⑥ free(last)

