---
categories:
- Data-Structure
date: '2026-03-15T23:18:00.000+09:00'
tags:
- 자료 구조
- 이진 트리
- DS
title: '[DS] Additional Binary Tree Operations'
toc: true
toc_sticky: true
---

### [Program 5.6] Copying Binary Tree


- postorder 와 유사
{% raw %}
```c
treePointer copy(treePointer original) {
	treePointer temp;
	if (original) { // 복사할 tree가 null 이 아니면
		temp = (treePointer) malloc(sizeof(node)); // 공간 할당
		if(IS_FULL(temp)) {
			fprintf(stderr, "The memory is full\n");
			exit(1);
		}
		temp->leftChild = copy(original->leftChild);
		temp->rightChild = copy(original->rightChild);
		temp->data = original->data;
		return temp;
	} else return NULL; // 복사할 tree 가 null 이면
}
```
{% endraw %}





### [Program 5.7] Testing Equality


- 똑같은 tree 인지 check
{% raw %}
```c
int equal (treePointer first, treePointer second) {
	return ((!first&&!second || // 1) 둘다 null 이면 같음
	(first && second && (first->data == second->data) && // 2) 둘다 존재하고, 값이 같음 &
	equal(first->leftChild, second->leftChild) && // 왼쪽 자식 같음 &
	equal(first->rightChild, second->rightChild)); // 오른쪽 자식 같음
}
```
{% endraw %}



## Satisfiability Problem


- 주어진 논리식이 참이 되도록 변수들의 값을 설정할 수 있는지를 결정하는 문제
ex) a ∨ ( b ∧ ~c) → 참이 될 수 있는 경우?

### [Program 5.8] Pseudo Code of Logic


{% raw %}
```c
for (all 2ⁿ possible combinations) {
	generate the next combination;
	replace the variables by their values;
	evaluate the expression;
	if (its value is true) {
		printf(<combination>);
		return;
	}
printf("No satisfiable combination\n");
```
{% endraw %}



- 식이 이미 binary tree 안에 있다면 → postorder 로 순회 가능.
![](/assets/images/notion/[ds]-additional-binary-tree-operations/img_1.png)



- Structure
{% raw %}
```c
typedef enum {not, and, or, true, false} logical;
typedef struct _node {
	struct _node leftChild;
	logical data;
	short int value;
	struct _node rightChild;
} node;
typedet struct _node *treePointer;
```
{% endraw %}



### [Program 5.9] : Postorder Evaluation


{% raw %}
```c
void postOrderEval (treePointer node) {
	if (node) {
		postOrderEval(node->leftChild); // 왼쪽 자식
		postOrderEval(node->rightChild); // 오른쪽 자식
		switch(node->data) {
			case not:
				node->value = !node->rightChild->value; // 오른쪽 자식의 값 반전
				break;
			case and:
				node->value = node->rightChild->value&&node->leftChild->value; // 왼쪽 ∧ 오른쪽
				break;
			case or:
				node->value = node->rightChild->value||node->leftChild->value; // 왼쪽 ∨ 오른쪽
				break;
			case true:
				node->value = TRUE;
				break;
			case false:
				node->value = FALSE;
		}
	}
}
```
{% endraw %}
