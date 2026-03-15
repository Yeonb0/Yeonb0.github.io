---
categories:
- Data-Structure
date: '2026-03-15T23:26:00.000+09:00'
tags:
- DS
- 자료 구조
- 이진 트리
- 이진 탐색
title: '[DS] Binary Search Tree'
toc: true
toc_sticky: true
---

## 5.7.1 Introduction


- Binary Search Tree (이진 탐색 트리) : 삽입, 삭제, 탐색에 가장 효율적인 자료구조.
  - key value, rank 에 의해 수행.
- Definition : Binary Search Tree는 이진 트리 중 하나로, 공백일 수 있다. 만약 공백이 아니라면 다음의 성질들을 만족한다.
  1. 모든 원소는 key를 가지며, 어떤 두 원소도 동일한 key를 가지지 않는다 (모든 key는 unique 하다.)
  1. 왼쪽 서브 트리에 있는 key 는 root의 key 보다 작다.
  1. 오른쪽 서브 트리에 있는 key 는 root의 key 보다 크다.
  1. 왼쪽, 오른쪽 서브 트리 또한 Binary Search Tree 이다.
![](/assets/images/notion/[ds]-binary-search-tree/img_1.png)



## 5.7.2 Searching A Binary Search Tree


### [Program 5.15] : Recursive Search


{% raw %}
```c
tree_pointer search(tree_pointer root, int key) {
	// key 값을 지닌 node의 포인터 반환.
	// 그런 node가 없다면 NULL 반환
	if(!root) return NULL; // empty tree
	if(key == root->data) return root;
	if(key < root->data) 
		return search(root->left_child, key); // 작으면 왼쪽 서브 트리에서 찾기
	return search(root->right_child, key); // 크면 오른쪽 서브 트리에서 찾기
}
```
{% endraw %}



### [Program 5.16] : Iterative Search


{% raw %}
```c
tree_pointer search2(tree_pointer tree, int key) {
	// key 값을 지닌 node의 포인터 반환.
	// 그런 node가 없다면 NULL 반환
	while (tree) {
		if (key == tree->data) 
			return tree;
		else if (key < tree->data)
			tree = tree->left_child;
		else 
			tree = tree->right_child;
	}
	return NULL;
}
```
{% endraw %}



→ 시간 복잡도 : 둘 다 O(h) = O(log₂n) 

- 정렬 리스트의 이진 탐색과 유사


## 5.7.3 Inserting Into A Binary Search Tree


- 새 key 삽입하기
  - 똑같은 key가 있는지 탐색
  - 탐색 실패 시, 탐색이 실패하고 마지막으로 검사한 node 의 자식으로 삽입
![](/assets/images/notion/[ds]-binary-search-tree/img_2.png)



### [Program 5.17] : Insert Element


{% raw %}
```c
void insert_node(tree_pointer *node, int num) [
	// num 이 이미 tree 안에 있으면 아무것도 하지 않음
	// 그렇지 않으면 data = num 인 새 node 추가.
	tree_pointer ptr, temp = modified_search(*node, num);
	if(temp || !(*node)) { // temp 가 NULL 이 아니거나 tree가 비었거나
		// num 이 tree 안에 없음
		ptr = (tree_pointer) malloc(sizeof(node));
		if (IS_FULL(ptr)) {
			fprintf(stderr, "The memory is full");
			exit(1);
		}
		ptr->data = num;
		ptr->left_child = ptr->right_child = NULL;
		if (*node) { // 빈 tree 가 아니라면 child 로 삽입
			if (num < temp->data)
				temp->left_child = ptr;
			else
				temp->right_child = ptr;
		} else *node = ptr; // 빈 tree 라면 root node 로 설정.
	}
}
```
{% endraw %}



- modified_search 함수
  - tree에 num 존재하면 return NULL
  - 존재하지 않으면 있어야 할 node 주소 return
{% raw %}
```c
tree_pointer modified_search(tree_pointer *node, int num)
```
{% endraw %}



→ 시간 복잡도 : O(h) = O(log₂n)



## 5.7.4 Delete From A Binary Search Tree


- leaf node의 삭제
  - parent의 leaf 가리키는 쪽 NULL 로 설정 후 free
- single child 가지는 parent node 삭제
  - grandparent 의 parent 대신 single child 연결하고 free
- two children 가지는 parent node 삭제
  - 그 원소를 왼쪽 서브 트리에서 가장 큰 원소 or 오른쪽 서브 트리에서 가장 작은 원소로 대체.
  - 대체 후 delete 과정 
![](/assets/images/notion/[ds]-binary-search-tree/img_3.png)

![](/assets/images/notion/[ds]-binary-search-tree/img_4.png)



## 5.7.5 Height Of A Binary Search Tree


- n개의 원소를 가진 이진 탐색 트리의 높이는 n 만큼 커질 수 있다. 
- but 평균적으로 이진 탐색 트리의 높이는 O(log₂n)
- 최악의 경우에도 높이가 O(log₂n)인 탐색 트리 → 균형 탐색 트리(balanced search tree)
ex) AVL 트리, 2-3 트리, red-black 트리
