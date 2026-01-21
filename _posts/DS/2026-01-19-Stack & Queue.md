---
layout: single
title: "[DS] Stack & Queue"
categories:
  - Data-Structure
tag: [DS, 자료구조, 스택, 큐]
---



# Stack & Queue

---

ordered list(순차 리스트)의 특수한 형태

# 1. Stack

- top 에서 모든 입력(insertion)과 삭제(deletion)이 이루어지는 순차리스트
  
    $$
    S = {\{a_0, a_1, ..., a_{n-1}\}}
    $$
    
- Last-In-First-Out (LIFO) list

- <img src="../../assets/images/posts/2026-01-19-Stack & Queue/image.png" alt="image" style="zoom: 50%;" />



- Example 3.1 [System Stack]
  
    프로그램 실행 시의 함수 호출 처리 방법
    
    함수가 호출될 때 마다 프로그램은 활성 레코드(activation record) or 스택 프레임(stack frame) 구조 생성 → 시스템 스택의 top에 push
    
    함수가 종료될 시 시스템 스택에서 pop
    
    
    
- [ADT 3.1] : Stack

> **ADT** Stack
>**objects** : 0개 이상의 원소를 가진 유한 순서 리스트
>**functions :**
>  모든 stack ∈ *Stack*, item ∈ *element*, maxStackSize ∈ *positive integer*
>
>  *Stack* `CreateS(maxStackSize)` ::= 최대 크기가 maxStackSize 인 공백 스택을 생성
>
>  *Boolean* `IsFull(stack, maxStackSize)` ::= 
>    **if** (stack의 원소 수  == maxStackSize)
>    **return** TRUE
>    **else return** FALSE
>
>  *Stack* `Push(stack, item)` ::=
>    **if** (`IsFull(stack)`) stackFull
>    **else** stack의 top에 item을 삽입하고 **return**
>
>  *Boolean* `IsEmpty(stack)` ::=
>    **if** (stack == CreateS(maxStackSize))
>    **return** true
>    **else return** false
>
>  *Element* `Pop(stack)` ::=
>    **if** (`IsEmpty(stack))` **return**
>    **else** stack top의 item을 제거해서 반환
> 

- <Stack의 구현>
    - 1차원 배열을 사용

```c
Stack CreateS(maxStackSize) ::=
	#define MAX_STACK_SIZE 100 // 스택의 최대 사이즈
	typedef struct {
		int key;
		// 다른 field;
	} element;
	element stack[MAX_STACK_SIZE];
	int top = -1; // 초기 top 위치
	
Boolean IsEmpty(stack) ::= top < 0; // top이 0보다 작으면 빈 stack
Boolean IsFull(stack) ::= top >= MAX_STACK_SIZE - 1;
```

- [Program 3.1] : Add to a stack

```c
void push(element item){ // 전역 stack에 item 추가
	if(top >= MAX_STACK_SIZE - 1) // 더 증가할 수 없으면
		stackFull(); // 오류
	stack[++top] = item; // 선 증가 후 push
}
```

- [Program 3.2] : Delete from a stack

```c
element pop(){  // 전역 stack에서 item 반환 (+ 삭제)
	if(top == -1) // 더 감소할 수 없으면
		return stackEmpty(); // pop의 반환 값이 element이기 때문에 stackEmpty는 error key를 반환해야 함.
	return stack[top--]; // 반환 후 감소
}
```

# 2. Stack Using Dynamic Arrays

- 동적 배열 사용하는 stack

```c
Stack CreateS() ::=
	typedef struct{
		int key;
		// 다른 field;
	} element;
element *stack;
MALLOC(stack, sizeof(*stack));
int capacity = 1; // 총 공간
int top = -1; // 초기 top 위치
}

Boolean IsEmpty(stack) ::= top < 0; // top이 0보다 작으면 빈 stack
Boolean IsFull(stack) ::= top >= capacity; // top이 총 공간보다 크면 꽉 참

void stackFull(){
	REALLOC(stack, 2 * capacity * sizeof(*stack)); // 기존 공간의 2배로 stack 크기 늘림
	capacity *= 2; // 공간을 늘린 후에 capacity 늘리기
```

# 3. Queues

- 한쪽 끝에서 삽입(insertion) 하고 반대쪽 끝에서 삭제(deletion) 하는 순서 리스트
    - 원소가 나가는 곳(delete) : front
    - 원소가 들어오는 곳(add) : rear
    
    $$
    Q = {\{a_0, a_1, ..., a_{n-1}\}}
    $$
    
- First-In-First-Out(FIFO) list

<img src="../../assets/images/posts/2026-01-19-Stack & Queue/image (1).png" alt="image (1)" style="zoom:50%;" />

- [ADT 3.2] : Queue

> **ADT** Queue
>**Objects** : 0개 이상의 원소를 가진 유한 순서 리스트
>**Functions** :
>  모든 queue ∈ *Queue*, item ∈ *element*, maxQueueSize ∈ *positive integer*
>
>  *Queue* `CreateQ(maxQueueSize)` ::= 최대 크기가 maxQueueSize 인 공백 큐 생성
>
>  *Boolean* `IsFullQ(queue, maxQueueSize)` ::=
>    **if** (queue의 원소수 == maxQueueSize)
>    **return** TRUE
>    **else return** FALSE
>
>  *Queue* `AddQ(queue, item)` ::=
>    **if** (IsFullQ(queue)) queueFull
>    **else** queue의 뒤에 item을 삽입하고 이 queue를 반환
>
>  *Boolean* `IsEmptyQ(queue)` ::=
>    **if** (queue == CreateQ(maxQueueSize))
>    **return** TRUE
>    **else return** FALSE
>
>  *Element* `DeleteQ(queue)` ::=
>    **if** (IsEmpty(queue)) **return**
>    **else** queue 앞에 있는 item을 제거해서 반환

- <Queue의 구현>
    - 1차원 배열 + 두 개의 변수(front, rear)
    - front는 배열의 앞쪽, rear은 뒤쪽. front == rear 일 때 배열 비었음

```c
Queue CreateQ(maxQueueSize) ::=
	#define MAX_QUEUE_SIZE 100 // 최대 queue 크기
	typedef struct {
		int key;
		// 다른 field
	} element;
	element queue[MAX_QUEUE_SIZE]; // 전역 queue 선언
	int rear = -1; // 초기 rear 값
	int front = -1; // 초기 front 값;
	
	Boolean IsEmptyQ(queue) ::= front == rear; // front와 rear가 같을 때 queue 비었음
	Boolean IsFullQ(queue) ::= rear == MAX_QUEUE_SIZE // rear가 더 증가할 수 없을 때 queue 꽉 참
```

<img src="../../assets/images/posts/2026-01-19-Stack & Queue/image (2).png" alt="image (2)" style="zoom:50%;" />

→ front 인덱스 자체에는 값이 존재하지 않음

- [Program 3.5] : Add to a queue

```c
void addq(element item){ // queue에 item 추가
	if(rear == MAX_QUEUE_SIZE - 1) // 더 증가할 수 없으면
		queueFull(); // 꽉 찼다는 것 반환
	queue[++rear] = item; // 선 증가 후 그 인덱스에 item 저장
```

- [Program 3.6] : Delete from a queue

```c
element deleteq(){ // queue의 front에서 데이터 삭제
	if(front == rear) // 삭제할 값이 없으면
		return queueEmpty(); // 오류값 반환 (element라는 값을 반환하는 함수기에)
	return queue[++front]; // 선 증가 후 그 queue 반환(실제로 값이 할당되어 있긴하지만, 제거나 마찬가지)
}
```

- Example 3.2 [Job scheduling]
  
    작업 큐(job queue) : 작업들을 시스템에 들어간 순서대로 처리(우선 순위가 없을 때)
    
    
    
    <img src="../../assets/images/posts/2026-01-19-Stack & Queue/image (5).png" alt="image (5)" style="zoom:50%;" />
    
    
    
- queueFull의 문제점
  
    - `rear`가 `MAX_QUEUE_SIZE - 1` 에 도달하면 그 queue는 더 이상 늘릴 수 없음.
    - front를 옮기며 쓸모 없어진 앞쪽을 사용하고 싶은데 그건 힘듬..
    - 시간복잡도도  높음 : 최악의 경우 O(MAX_QUEUE_SIZE)
    
- Circular Queue
    - `queue[MAX_QUEUE_SIZE]` 를 원형이라고 취급.
    - <img src="../../assets/images/posts/2026-01-19-Stack & Queue/image (3).png" alt="image (3)" style="zoom:50%;" />
    
    
    
    
    
    
    
    - `front` 인덱스는 element들이 들어있는 곳의 시계 반대 방향으로 한 칸 이동한 위치
    - `rear` 인덱스는 마지막 element의 위치. queue의 끝 가리킴
    - `front == rear` 일 때 queue 가 꽉 참
    - 총 element 가 `MAX_QUEUE_SIZE - 1` 개 일 때 꽉 참 → 항상 1칸은 비어있음(실제 값이 비어있는 것은 아님. front와 rear간의 거리가 1)
    - <img src="../../assets/images/posts/2026-01-19-Stack & Queue/image (4).png" alt="image (4)" style="zoom:50%;" />

- 원형 큐에서 회전은 어떻게 일어나는가?
  
    ```c
    rear = (rear + 1) % MAX_QUEUE_SIZE; // 다음 rear의 위치
    front = (front + 1) % MAX_QUEUE_SIZE; // 다음 front의 위치
    ```
    
- 초기 값
  
    ```c
    rear = 0;
    front = 0;
    ```
    
- [Program 3.7]  : Add to a circular queue

```c
void addq(element item){ // 원형 큐에 item 추가
	rear = (rear + 1) % MAX_QUEUE_SIZE; // rear 한 칸 앞으로 이동
	if(front == rear) // 빈 칸이 없어졌다면
		queueFull(); // 에러 발생
	queue[rear] = item; // 그게 아니라면 값 넣기
}
```

- [Program 3.8] : Delete from a circular queue

```c
element deleteq(){ // 원형 큐에서 item에 삭제
	if(front == rear) // queue가 비었다면
		return queueEmpty(); // error key 반환
	front = (front + 1) % MAX_QUEUE_SIZE; // front 한칸 앞으로 이동
	return queue[front]; // front 인덱스 값 반환
}
```

# 4. Circular Queues Using Dynamically Allocated Arrays

- 꽉 찬 queue에 element를 추가하기 위해선, 먼저 REALLOC을 이용해 queue의 크기를 늘려야 한다.
- 동적 할당 stack처럼 두 배로 증가.

- <Doubling queue>
    - `capacity`를 queue에서 사용 가능한 칸 수라고 하자.
        1. `capacity` 가 2배인 새로운 배열 `newQueue` 를 만든다.
        2. [front+1] ~ [capacity-1] 값 까지를 0에서부터 채운다.
        3. [0] ~ [rear] 값 까지를 capacity-front-1 부터 채운다.
    
    <img src="../../assets/images/posts/2026-01-19-Stack & Queue/IMG_1188-1768978765341-36.png" alt="IMG_1188" style="zoom:50%;" />

<img src="../../assets/images/posts/2026-01-19-Stack & Queue/IMG_1189.png" alt="IMG_1189" style="zoom:50%;" />

- [Program 3.9] : Add to a circular queue

```c
void addq(element item){ // 원형 큐에 item 추가
	rear = (rear + 1) % MAX_QUEUE_SIZE; // rear 한 칸 앞으로 이동
	if(front == rear) // 빈 칸이 없다면
		queueFull(); // capacity를 두 배로!
	queue[rear] = item; // 그게 아니라면 값 넣기
}
```

- [Program 3.10] : Doubling queue capacity
    
    - 
      
        ```c
        copy(a, b, c) : a부터 b-1 까지의 값을 c의 시작에 복사
        ```
        

```c
void queueFull() { // 원형 큐의 capacity를 두 배로
	element *newQueue;
	MALLOC(newQueue, 2 * capacity * sizeof(*queue));
	
	// 기존 Queue에서 newQueue로 복사
	int start = (front+1) % capacity; // front + 1 부터
	if(start < 2) // 0 ~ rear 복사할 필요 없음
		copy(queue+start, queue+start+capacity-1, newQueue); // front+1 부터 front+capacity-1 까지 newQueue의 맨 앞에 복사
	else{ // 0 ~ rear 도 복사 해야함
		copy(queue+start, queue+start+capacity-1, newQueue); // front+1 부터 front+capacity-1 까지 newQueue의 맨 앞에 복사
		copy(queue, queue+rear+1, newQueue+capacity-start); // 0부터 rear 까지 newQueue의 front+capacity 부터 채우기
	
	// newQueue로 교체
	front = 2 * capacity - 1; // 시작이 0 이니까 front는 맨 뒤
	rear = capacity - 2; // 항이 꽉찬 상태기에 0 ~ capacity-2 까지의 길이 (-1은 0때문에, -1은 원형 큐가 비워야 하는 칸)
	capacity *= 2; // 먼저 front, rear 구하고 2배
	free(queue); // 기존 공간 해방
	queue = newQueue; // 새로운 queue에 연결
```