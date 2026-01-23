---
categories:
- Data-Structure
date: '2026-01-21'
tags:
- DS
- 자료 구조
title: '[DS] Equivalence Relations'
toc: true
toc_sticky: true
---

### Example

0 부터 11까지 숫자가 있고,

0≡4, 3≡1, 6≡10, 8≡9, 7≡4, 6≡8, 3≡5, 2≡11, 11≡0

라는 관계 쌍이 있을 때,

{0, 2, 4, 7, 11}

{1, 3, 5}

{6, 8, 9, 10} 

과 같이 서로 관계 있는 수들 끼리 묶어서 출력하기.



- How to Solve?
  - Fisrt phase : 동치 쌍을 읽고 저장.
  - Second phase : 동치 쌍을 판단
  <0, j> 부터 시작.

​		<j, k> 가 있을 때, <0, k> 

​		0과 관련된 모든 동치 출력, 그 후 다른 수에 대해서도 반복(중복 X)



### [Program 4.23] : Fisrt Pseudo Code of Algorithm 

```c
void equivalence() {
	initialize;
	while (there are more pairs) {
		read the next pair <i,j>;
		process this pair;
	}
	initialize the output;
	do {
		output a new equivalence class;
	} while (not done);
}
```



### [Program 4.24] : Linked list pseudo code

- pair 들을 담을 자료구조
  - m : pair 의 갯수 (9개)
  - n : 원소의 갯수 (0~11, 12개)
  → array 사용 : pairs[n][m]

ex) 0≡4, pairs[0][0] 에 4 저장

  - 접근에 용이.
  - 공간 낭비가 심함. 관계가 추가되면 더 많은 공간 사용
→ linked list 사용 : 각 항을 node 로 저장 

  - seq[n] : 0~11까지. n 번째 행에 접근
  - out[n] : 중복 체크용 배열.


```c
void equivalence() {
	initialize seq to NULL and out to TRUE;
	while (there are more pairs) {
		read the next pair <i,j>;
		put j on the seq[i] list;
		put i on the seq[j] list;
	}
	for (i = 0; i < n; i++) {
		if (out[i]) { // TRUE 이면
			out[i] = FALSE; // FALSE 로 바꾸고
			output this equivalence class; // 관계 있는 수들 출력
		}
	}
}
```



- First Phase : 관계 쌍 저장
![](/assets/images/notion/[ds]-equivalence-relations/img_1.png)



- Second Phase : *seq* array 스캔. 
  - For the first i, 0 ≤ i < n
  - such that *out*[i] = TRUE
  - *seq*[i] 안에 있는 요소들 출력


### [Program 4.25] Print Equivalence

- Declaration
```c
#include <stdio.h>
#include <alloc.h>
#define MAX_SIZE 24
#define IS_FULL(ptr) (!(ptr))
#define FALSE 0
#define TRUE 1

typedef struct _node {
	int data;
	struct _node *link;
} node;

typedef node *node_pointer;
```

```c
void main(void) {
	short int out[MAX_SIZE];
	node_pointer seq[MAX_SIZE];
	node_pointer x, y, top;
	int i, j, n;
	
	printf("Enter the size (<= %d)", MAX_SIZE); 
	// 0 부터 어디까지?
	scanf("%d", &n);
	for (i = 0; i < n; i++) {
		// seq 배열, out 배열 초기화
		out[i] = TRUE;
		seq[i] = NULL;
	}
	
	// Phase 1 : 동치 쌍 입력
	printf("Enter a pair of numbers (-1 -1 to quit): ");
	scanf("%d %d", &i, &j);
	while (i >= 0) { 
		x = (node_pointer) malloc(sizeof(node));
		if(IS_FULL(x)) {
			fprintf(stderr, "The memory is full\n");
			exit(1);
		}
		// i 쪽 저장
		x->data = j;
		x->link = seq[i];
		seq[i] = x;
		x = (node_pointer) malloc(sizeof(node));
		if (IS_FULL(x)) {
			fprintf(stderr, "The memory is full\n");
			exit(1);
		}
		// j 쪽 저장
		x->data = i;
		x->link = seq[j]; 
		seq[j] = x;
		// 새 노드는 linked list의 맨 앞으로
		
		printf("Enter a pair of numbers (-1 -1 to quit): ");
		scanf("%d %d", &i, &j);
	}
	
	// Phase 2 : 동치 쌍 출력
	for (i = 0; i < n; i++) {
		if (out[i]) { // out[i] 가 TRUE 라면
			printf("\nNew Class : %5d", i); // 새로운 클래스 출력 시작
			out[i] = FALSE; // i 출력했다는 것 표시
			// stack 초기화
			x = seq[i];
			top = NULL;
			for ( ; ; ) { // 나머지 클래스 원소를 찾음 
				while (x) { // stack 스캔
					j = x->data;
					if (out[j]) { // j가 아직 출력 되지 않았다면
						printf("%5d", j); // j를 출력한 후
						out[j] = FALSE; // j 출력했다는 것 표시
						// push
						y = x->link;
						x->link = top;
						top = x;
						x = y;
					} else { // j가 이미 출력되었다면
						x = x->link; // list의 다음 원소 확인
					}
				} // while 문 끝
				if (!top) break; // 현재 클래스의 모든 원소 출력 완료
				// pop
				x = seq[top->data];
				top = top->link;
			} // for 문 끝
		} // if 문 끝
	}
} 						
```

- 과정
![](/assets/images/notion/[ds]-equivalence-relations/img_2.png)

![](/assets/images/notion/[ds]-equivalence-relations/img_3.png)

![](/assets/images/notion/[ds]-equivalence-relations/img_4.png)

![](/assets/images/notion/[ds]-equivalence-relations/img_5.png)

![](/assets/images/notion/[ds]-equivalence-relations/img_6.png)



