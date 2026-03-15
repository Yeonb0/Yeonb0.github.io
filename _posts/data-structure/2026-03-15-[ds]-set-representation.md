---
categories:
- Data-Structure
date: '2026-03-15T23:28:00.000+09:00'
tags:
- DS
- 자료 구조
- 트리
- 집합과 맵
title: '[DS] Set Representation'
toc: true
toc_sticky: true
---

- 트리를 사용해 집합을 표현하기
- 집합의 원소 : 0, 1, 2, …, n-1
- 모든 집합은 쌍 별로 분리
![](/assets/images/notion/[ds]-set-representation/img_1.png)

→ Possible representation



## 5.10.1 Union and Find Operation


- S1, S2의 두 집합이 있다고 하자.
- 한 트리를 다른 한 트리의 subtree로 만들기
![](/assets/images/notion/[ds]-set-representation/img_2.png)



- 배열로 표현
- [i] = 자신의 parent. root node 일 시 -1 저장
![](/assets/images/notion/[ds]-set-representation/img_3.png)


| [i] | [0] | [1] | [2] | [3] | [4] | [5] | [6] | [7] | [8] | [9] |
| parent | -1 | 4 | -1 | 2 | -1 | 2 | 0 | 0 | 0 | 4 |

→ root node 는 -1 저장, 나머지는 자신의 root 저장



### [Program 5.18] : Initial Union-Find functions


{% raw %}
```c
int find1(int i) {
	for(;parent[i] >= 0; i = parent[i]); // root node 로 이동 
	return i;
}
```
{% endraw %}

→ n-1 번의 find를 수행하기 위한 시간 복잡도 

<div class="equation-box">

$$
\sum^n_{i=2}i=O(n^2)
$$

</div>

{% raw %}
```c
void union1(int i, int j) {
	parent[i] = j; // root node 바꾸기 = subtree 로 만들기
}
```
{% endraw %}

→ n-1 개의 합집합 연산을 수행하기 위한 시간 복잡도 : O(n)



- union에 가중 규칙(weighting rule)을 적용해 더욱 효율적으로 구현 가능
> ➡️ 

- 가중 규칙(Weighting rule)
→ 작은게 아래로.



- 가중 규칙을 적용하기 위해 트리의 root에 count 필드 넣기.

### [Program 5.19] Union Operation with Weighting Rule


![](/assets/images/notion/[ds]-set-representation/img_4.png)

count[0] = 3 / parent[3] = -3

count[4] = 2 / parent[4] = -2

count[2] = 2 / parent[3] = -2

{% raw %}
```c
void union2(int i, int j) {
	// parent[i] = -count[i] & parent[j] = -count[j]
	int temp = parent[i] + parent[j]; // 총 노드 갯수 (음수)
	if(parent[i] > parent[j]) { // i의 원소가 더 적으면 (음수이기에)
		parent[i] = j; // j를 새로운 root로
		parent[j] = temp; // 총 갯수 바꾸기
	} else { // i의 원소가 같거나 더 많으면
		parent[j] = i; // i를 새로운 root로
		parent[i] = temp; // 총 갯수 바꾸기
	}
}
```
{% endraw %}



- 보조 정리 5.4 : 
![](/assets/images/notion/[ds]-set-representation/img_5.png)

→ 노드 8개, level 4



- 붕괴 규칙(Collapsing rule)


### [Program 5.20] : Find Function with Collapsing rule


{% raw %}
```c
int find2(int i) {
	// 원소 i를 포함하고 있는 트리의 root 찾기.
	// 붕괴 규칙을 이용해 i로부터 root로 가는 모든 노드 붕괴 시킴
	int root, trail, lead;
	for (root = i; parent[root] >= 0; root = parent[root]); // 트리 root 노드로 이동
	for (trail = i; trail != root; trail = lead) {
		lead = parent[trail];
		parent[trail] = root;
	}
	return root;
}
```
{% endraw %}

![](/assets/images/notion/[ds]-set-representation/img_6.png)

→ 가는 길에 지나가는 parent 도 바꿈. 반복 작업 할 때 유용.



- 개별적인 탐색 시간 증가. 
- 연속적 탐색 시간 감소.


## 5.10.2 Equivalence Class


- Stack 대신 Union-Find 사용하면 더 빠르게 구할 수 잆음
![](/assets/images/notion/[ds]-set-representation/img_7.png)
