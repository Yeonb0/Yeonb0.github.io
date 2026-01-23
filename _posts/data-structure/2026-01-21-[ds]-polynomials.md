---
categories:
- Data-Structure
date: '2026-01-21'
tags:
- DS
- 자료 구조
- 다항식
- 연결 리스트
title: '[DS] Polynomials'
toc: true
toc_sticky: true
---

##  4.4.1 Representing Polynomials As Singly Linked List

- $$A(x) = a_{m-1}x^{e_{m-1}} + \cdot\cdot\cdot \ + a_0x^{e_0}$$ 을 Linked List로 표현
  - 계수는 음이 아닌 정수의 내림차순. a는 0이 아닌 계수.


```c++
typedef struct _poly_node {
	float coef;
	int expon;
	struct _poly_node *link;
} poly_node;
typedef poly_node *poly_pointer;

poly_pointer a, b, d; // 다항식 3개 생성
```



[Figure 4.11]

$$a = 3x^{14} + 2x^8 + 1$$ 

$$b = 8x^{14} - 3x^{10} + 10x^6$$

![](/assets/images/notion/[ds]-polynomials/img_1.png)



##  4.4.2 Adding Polynomials

###  [Program 4.12] : Add 

```c++
poly_pointer padd(poly_pointer a, poly_pointer b) {
	// call-by-value : 실제 값 변경 X
	// 다항식 a 와 b의 합 반환
	poly_pointer front, rear, temp;
	float sum;
	rear = (poly_pointer) malloc(sizeof(poly_node));
	if (IS_FULL(rear)) {
		fprintf(stderr, "The memory is full\n"); 
		exit(1);
	}
	front = rear;
	while (a && b) { // 둘 중 하나가 빌 때까지
		switch (COMPARE(a->expon, b->expon)) { // 맨 앞 항의 지수 비교
			case -1 : // a의 지수 > b의 지수 -> b 붙이기
				attach(b->coef, b->expon, &rear);
				b = b->link; // b 한 칸 앞으로
				break;
			case 0 : // a의 지수 = b의 지수 -> 계수 더해서 붙이기
				sum = a->coef + b->coef; // 계수 더하기
				if (sum) // 계수의 합이 0이 아니면
					attach(sum, a->expon, &rear);
				a = a->link; b = b->link; // a, b 한 칸 앞으로
				break;
			case 1 : // a의 지수 > b의 지수 -> a 붙이기
				attach(a->coef, a->expon, &rear);
				a = a->link; // a 한 칸 앞으로
		} // switch 끝
	} // while 끝
	// 남은 다항식 옮기기
	for( ; a ; a = a->link) // a 끝까지
		attach(a->coef, a->expon, &rear);
	for( ; b ; b = b->link) // b 끝까지
		attach(b->coef, b->expon, &rear);
	rear->link = NULL; // 다항식 끝 표시.
	
	// attach 함수에서 사용했던 temp free
	temp = front;
	front = front->link;
	free(temp);
	return front;
}
```



###  [Program 4.13] : Attach 

```c++
void attach (float coefficient, int exponent, poly_pointer *ptr) {
	// ptr 을 coef, expo data 갖는 새 node로 바꾸기
	poly_pointer temp;
	temp = (poly_pointer) malloc(sizeof(poly_node));
	if (IS_FULL(temp)) { // 저장 공간이 없을 때
		fprintf(stderr, "The memory is full\n");
		exit(1);
	}
	temp->coef = coefficient;
	temp->expon = exponent;
	(*ptr)->link = temp;
	*ptr = temp;
}	
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
void erase(poly_pointer *ptr) {
	// 사용한 다항식 저장공간 free 시키는 함수 
	poly_pointer temp;
	while (*ptr) { // 다항식 끝까지
		temp = *ptr;
		*ptr = (*ptr)->link; // ptr 다음 칸으로
		free(temp);
	}
}
```



##  4.4.4 Representing Polynomials As Circularly Linked Lists

- Circular list
  - 마지막 node 와 첫 node 연결
- Chain list
  - 한 방향으로 연결된 리스트. 끝 node가 null link 를 가지고 있음.
###  [Program 4.15] : Get empty node

```c++
poly_pointer get_node(void) {
	// 사용할 node 제공
	poly_pointer node;
	if (avail) { // avail 은 data가 빈 node의 list
		node = avail;
		avail = avail->link;
	} else { // 사용 가능한 빈 node 가 없다면
		node = (poly_pointer) malloc(sizeof(poly_node)); // 새 공간 할당
		if(IS_FULL(node)) { // 메모리 공간이 부족하다면
			fprintf(stderr, "The memory is full\n");
			exit(1);
		}
	}
	return node;
}
```



- 더 이상 사용하지 않는 빈 node를 다시 avail로 보내 재사용.
- avail : freed node 리스트의 첫 node를 가리키는 포인터


###  [Program 4.16] : Return empty node

```c++
void ret_node(poly_pointer ptr) { // 값 변경 없으므로 call-by-value
	// 빈 ptr 노드를 사용 가능하도록 avail에 반납
	ptr->link = avail;
	avail = ptr;
}
```

###  [Program 4.17] : Return all node of list

```c++
void cerase(poly_pointer *ptr) {
	// circular list인 ptr의 모든 node를 avail로 보냄.
	poly_pointer temp;
	if (*ptr) {
		temp = (*ptr)->link;
		(*ptr)->link = avail;
		avail = temp;
		*ptr = NULL;
	}
}
```

![](/assets/images/notion/[ds]-polynomials/img_3.png)



- 다항식을 circular list 로 표현 
- 다항식이 빈 상태를 표현하기 위해 dummy node 집어 넣기.
ex) $$3x^{14} + 2x^8 +1$$

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
poly_pointer cpadd(poly_pointer a, poly_pointer b) {
	// head node로 시작하는 두 circular linked list a와 b를 더한 다항식 반환
	poly_pointer starta, d, lastd;
	int sum, done = FALSE;
	starta = a; // a의 head node 저장
	startb = b; // b의 head node 저장
	a = a->link;
	b = b->link; // a와 b의 head node 건너뛰기.
	d = get_node(); // 합한 다항식을 위한 head node 생성
	d->expon = -1; // head node 지수 값 설정
	lastd = d; // circular 하게 만들기
	
	do {
		switch (COMPARE(a->expon, b->expon)) { // 지수 비교
			case -1 : // a의 지수 < b의 지수
				attach(b->coef, b->expon, &lastd);
				b = b->link; break; // b 한 칸 이동
			case 0 : // a의 지수 = b의 지수
				if(start == a) done = TRUE; // a와 b 모두 -1에 도착하면, 다항식 합 끝.
				else {
					sum = a->coef + b->coef;
					if (sum) attach(sum, a->expon, &lastd); // 합이 0이 아니면, attach
					a = a->link; b = b->link; // a, b 한 칸 이동
				}
				break;
			case 1 : // a의 지수 > b의 지수
				attach(a->coef, a->expon, &lastd);
				a = a->link; // a 한 칸 이동
		} // switch 문 끝
	} while (!done); // a, b 다항식 끝까지
	lastd->link = d; // 처음과 끝 연결. circular 하게 만들기 위해.
	return d;
}
```

