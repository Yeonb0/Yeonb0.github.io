---
categories:
- Data-Structure
date: '2026-03-15T23:20:00.000+09:00'
tags:
- DS
- 자료 구조
- 이진 트리
title: '[DS] Threaded Binary Trees'
toc: true
toc_sticky: true
---

- tree 의 leaf node 의 NULL link 공간 낭비 → 활용 방법이 없을까?
- null link 대신 thread 로 대체
  1. ptr→leftChild 가 null 이면 inorder traversal 에서 ptr 이전의 node 를 가리킴.
→ inorder predecessor

  1. ptr→rightChild 가 null 이면 inorder traversal 에서 ptr 다음의 node 를 가리킴.
→ inorder successor

- left_thread, right_thread field 추가. (Boolean)
![](/assets/images/notion/[ds]-threaded-binary-trees/img_1.png)

→ Inorder Traversal : H D I B E A F C G



### Structure


{% raw %}
```c
typedef struct threaded_tree *threaded_pointer
typedef struct threaded_tree {
	short int left_thread;
	threaded_pointer left_child;
	short int right_thread;
	threaded_pointer right_child;
	short int right_threaed
} ;
```
{% endraw %}

- TRUE 면 thread / FALSE 면 일반 node


- threaded binary tree 는 head node 가 필요.
  - empty threaded tree → head node 만 존재
![](/assets/images/notion/[ds]-threaded-binary-trees/img_2.png)



### [Program 5.10] Finding inorder successor node


{% raw %}
```c
threaded_pointer insucc(threaded_pointer tree) {
	// threaded tree에서 다음 node 찾기
	threaded_pointer temp;
	temp = tree->right_child; // head node 의 오른쪽 이동
	if(!tree->right_thread) // rightChild 의 오른쪽 자식이 있다면
		while(!temp->left_thread) // leaf 까지
			temp = temp->left_child; // 내려가기
	return temp;
```
{% endraw %}



### [Program 5.11] Inorder traversal


{% raw %}
```c
void tinorder(threaded_pointer tree) {
	// threaded binary tree 를 inorder traverse
	threaded_pointer temp = tree;
	for ( ; ; ) {
		temp = insucc(temp); // 다음 node로 이동
		if(temp == tree) break; // head node 도착하면 break
		printf("%3c", temp->data); // data 출력
	}
}
```
{% endraw %}



### [Program 5.12] Insert node to threaded binary tree


- node 넣는 경우의 수
  1. parent 의 right child 가 비어 있을 경우
  1. parent 의 right child 가 비어 있지 않을 경우
{% raw %}
```c
void insert_right(threaded_pointer parent, threaded_pointer child) {
	// child 를 parent의 right_child로 넣기
	threaded_pointer temp;
	child->right_child = parent->right_child;
	child->right_thread = parent-> right_thread; // 오른쪽은 똑같이 설정
	child->left_child = parent; // 이전 node는 parent
	child->left_thread = TRUE; // thread 설정 on
	parent->right_child = child; // child 설정
	parent->right_thread = FALSE; // thread 설정 off (원래 설정과 상관 없이)
	if(!child->right_thread) { // parent 의 오른쪽이 node 였다면 
		temp = insucc(child); // temp 를 원래 parent의 right_child 로 이동
		temp->left_child = child; // 원래 parent의 right_child의 이전 node 를 child로 설정
	}
}
```
{% endraw %}



{% raw %}
```c
void insert_left(threaded_pointer parent, threaded_pointer child) {
    // parent의 왼쪽에 child 노드를 삽입 
    
    child->left_child = parent->left_child;   // 기존 부모의 왼쪽 자식을 child의 왼쪽 자식으로 설정
    child->left_thread = parent->left_thread; // 부모의 기존 왼쪽 스레드 상태를 상속
    
    child->right_child = parent;             // child의 오른쪽 자식을 parent로 설정
    child->right_thread = TRUE;              // child의 오른쪽 스레드를 TRUE로 설정
    
    parent->left_child = child;              // parent의 왼쪽 자식을 child로 설정
    parent->left_thread = FALSE;             // parent의 왼쪽 스레드를 FALSE로 설정
    
    // 만약 child의 left_thread가 TRUE인 경우, 이전 노드의 오른쪽 스레드를 업데이트
    if (child->left_thread) {
        threaded_pointer temp = child->left_child;
        temp->right_child = child;           // 이전 노드의 오른쪽 자식을 child로 설정
    }
}
```
{% endraw %}
