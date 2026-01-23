---
categories:
- Data-Structure
date: '2026-01-21'
tags:
- DS
- 자료 구조
- 연결 리스트
- 스택
- 큐
title: '[DS] Dynamically Linked Stacks and Queues'
toc: true
toc_sticky: true
---

- 여러 스택 & 큐 관리
- 1개의 stack이나 queue를 가지고 있다면 sequential 표현이 효율적이다.
- 여러 stack이나 queue가 공존하면, sequential 표현은 효율적이지 않다.
![](/assets/images/notion/[ds]-dynamically-linked-stacks-and-queues/img_1.png)



##  4.3.1 Stack

- Declarations
```c++
#define MAX_STACKS 10 // 총 stack의 갯수의 최댓값
typedef struct {
	int key;
	/* other fields */
} element;
typedef struct _stack {
	element item;
	struct _stack *link;
} stack;
typedef stack *stack_pointer; // stack의 주소를 갖는 포인터

stack_pointer top[MAX_STACKS]; // stack 10개를 저장하는 배열
```



- empty stack 초기화
```c++
top[i] = NULL, 0 <= i < MAX_STACKS
```

- 경계 설정
  - top[i] == NULL ↔ i번째 stack이 empty
  - IS_FULL(temp) ↔ 저장 공간이 꽉 참


###  [Program 4.8] : Add to Stack

```c++
void add(stack_pointer *top, element item) {
	// item을 i번째 stack의 top에 추가
	stack_pointer temp = (stack_pointer) malloc(sizeof(stack));
	if (IS_FULL(temp)) { // 저장 공간이 없을 경우
		fprintf(stderr, "The memory is full\n");
		exit(1);
	}
	temp->item = item; // data 저장
	temp->link = *top; // top에 temp 연결
	*top = temp; // top을 한 칸 앞으로 이동
}
```

- 호출 : add(&top[i], item)
→ i 번째 stack의 top에 item 추가

ex) add(&top[8], 3)

![](/assets/images/notion/[ds]-dynamically-linked-stacks-and-queues/img_2.png)



###  [Program 4.9] : Delete from Stack

```c++
element delete(stack_pointer *top) {
	// i 번째 stack에서 top 삭제
	stack_pointer temp = *top; // call-by-ref, temp는 double pointer
	element item;
	if(IS_EMPTY(temp)) { // stack 이 비었을 경우
		fprintf(stderr, "The stack is empty\n");
		exit(1);
	}
	item = temp->item;
	*top = temp->link;
	free(temp);
	return item;
}
```

- 호출 : delete(&top[i]);
→ i 번째 stack의 top pop

ex) delete(&top[8])

![](/assets/images/notion/[ds]-dynamically-linked-stacks-and-queues/img_3.png)



##  4.3.2 Queue

- Declarations
```c++
#define MAX_QUEUES 10 // 총 queue 갯수의 최댓값
typedef struct {
	int key;
	/* other fields */
} element;
typedef struct _queue {
	element item;
	struct _queue *link;
} queue;
typedef queue *queue_pointer;

queue_pointer front[MAX_QUEUES], rear[MAX_QUEUES]; // queue 10개를 저장
```

- empty queue 초기화
```c++
front[i] = NULL, 0 <= i < MAX_QUEUES
```

- 경계 설정
  - front[i] == NULL ↔ i번째 queue가 empty
  - IS_FULL(temp) ↔ 저장 공간이 꽉 참


###  [Program 4.10] : Add to Queue

```c++
void addq(queue_pointer *front, queue_pointer *rear, element item) {
	// i번째 queue의 rear에 item 추가
	queue_pointer temp = (queue_pointer) malloc(sizeof(queue));
	if IS_FULL(temp)) {
		fprintf(stderr, "The memory is full\n");
		exit(1);
	}
	temp->item = item;
	temp->link = NULL;
	if (*front) // front가 존재하면 
		(*rear)->link = temp;
	else // 비었을 때
		*front = temp; 
}
```

![](/assets/images/notion/[ds]-dynamically-linked-stacks-and-queues/img_4.png)

- 호출 : add(&front[i], item)
→ i 번째 queue의 rear에 item 추가

ex) add(&front[8], 3)

![](/assets/images/notion/[ds]-dynamically-linked-stacks-and-queues/img_5.png)

ex) add(&front[9], 4)

![](/assets/images/notion/[ds]-dynamically-linked-stacks-and-queues/img_6.png)



###  [Program 4.11] : Delete from Queue

```c++
element deleteq(queue_pointer *front) {
	// i번째 queue에서 front 한 칸 뒤로
	queue_pointer temp = *front;
	element item;
	if (IS_EMPTY(*front)) { // queue 가 비었으면
		fprintf(stderr, "The queue is empty\n");
		exit(1);
	}
	item = temp->item;
	*front = temp->link;
	free(temp)
	return item;
}
```

- 호출 : delete(&front[i])
→ i 번째 queue의 front 삭제

ex) delete(&front[8])

![](/assets/images/notion/[ds]-dynamically-linked-stacks-and-queues/img_7.png)



