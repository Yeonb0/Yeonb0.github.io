---
categories:
- Computer-System
date: '2026-06-24T10:49:00.000+09:00'
layout: single
series: 컴퓨터 시스템 개론
step: 5
tags:
- 어셈블리어
- CS
- x86-64
- 자료형
title: '[CS] Assembly: Array and Struct'
toc: true
toc_sticky: true
---

## ✦ Array


### ◆ One-dimensional array


- Allocation
  - `T A[N];` 
    - `T` → type
    - `A` → 이름 
    - `N` → 원소 갯수
  - memory 할당 : `N` × `sizeof(T)`
![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_1.png)

- Access
  - `A` (array name) 은 배열의 첫 번째 요소를 가리키는 pointer 로도 사용 가능
![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_2.png)

### ◆ Array & Pointer


- 항상 interchangeable X
{% raw %}
```c
char str1[32];
char str2[64];
char *p = str1;
```
{% endraw %}

  - str1, p 는 같은 값 → 같은 address
  - `sizeof(str1)` = 32
  - `sizeof(p)` = 8 → pointer 
  - p = str2 → 가능 (가리키는 거 바꾸기)
  - str2 = p → 불가능 (배열이 포인터?)

### ◆ Multi-dimensional (2D) Array


- `T A[N][M]`
  - `N` row / `M` columns
  - size : `N` × `M` × `sizeof(T)`
- Row-major ordering
  - Table like 2-dimensional structure
- Array of array
  - 각 행 하나하나가 1차원 배열 
  - memory 에선 linear 하게 저장되어 있음
![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_3.png)

- `arr[i]` 의 시작 주소
  - arr[4][5] 와 같을 때 5개의 요소 만큼을 더해야 함
![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_4.png)

- In assembly
  - Address access
{% raw %}
```c
int* get_row(int arr[][5], int row_idx) {
	return arr[row_idx];
}
```
{% endraw %}

{% raw %}
```assembly
movslq  %esi, %rsi
lea    (%rsi, %rsi, 4), %rax ; 5 × row_idx
lea    (%rdi, %rax, 4), %rax ; arr + 20 × row_idx
ret
```
{% endraw %}

    - 2차원 배열을 input 으로 받음
    - `lea` instruction 으로 memory 값 주소 계산만 해서 return
  - Element access
{% raw %}
```c
int get_elem(int arr[][5],
						 int row_idx,
						 int col_idx)
{
	return arr[row_idx][col_idx];
}
```
{% endraw %}

{% raw %}
```assembly
movslq  %esi, %rsi
lea    (%rsi, %rsi, 4), %rax  ; 5 × row_idx
lea    (%rdi, %rax, 4), %rax  ; arr + 20 × row_idx
movslq  %edx, %rdx            ; col_idx
mov    (%rax, %rdx, 4), %eax  ; memory load
```
{% endraw %}

    - `mov` instruction 으로 실제 값을 가져옴

### ◆ Array of Pointer


![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_5.png)

- 2차원 배열의 또 다른 표기 방법
- 이름 있는 1차원 배열들의 모음
- Memory Layout
![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_6.png)

  - 같은 배열끼리는 연속적, 배열 전체는 연속 X 
  - `univ` 는 포인터의 배열 → 각 요소는 8 byte
- In assembly
  - Element Access
    - `*(*(arr + 8 × ptr_idx) + 4 × int_idx)`
{% raw %}
```c
int get_elem(int *arr[],
						 int ptr_idx,
						 int int_idx)
{
	return arr[ptr_idx][int_idx];
}
```
{% endraw %}

{% raw %}
```assembly
movslq  %esi, %rsi
mov    (%rdi, %rsi, 8), %rax   ; %rax = arr[ptr_idx(8)]
movslq  %edx, %rdx
mov    (%rax, %rdx, 4), %eax   ; return %rax[int_idx]
ret
```
{% endraw %}

### ◆ 2차원 배열 비교


    - 2D Array
{% raw %}
```c
int get_elem(int arr[][5],
						 int row_idx,
						 int col_idx)
{
	return arr[row_idx][col_idx];
}
```
{% endraw %}

      - `*(arr+(20×row_idx)+(4×col_idx))`
    - Array of pointer
{% raw %}
```c
int get_elem(int *arr[],
						 int ptr_idx,
						 int int_idx)
{
	return arr[ptr_idx][int_idx];
}
```
{% endraw %}

      - `*(*(arr+(8×ptr_idx))+4×int_idx)`
- C 코드 상에선 유사하지만, low level 에선 다르다.

### ◆ Common Mistakes


{% raw %}
```c
char strs[4][64]; // 2D array
char* ptrs[4];    // Array of char*

strcpy(strs[1], "ABC");  // (1)
strcpy(ptrs[1], "ABC");  // (2)
strs[2] = "DEF";         // (3)
ptrs[2] = "DEF";         // (4)
```
{% endraw %}

1. correct 
1. segment fault 
  - `ptrs[1]` → 초기화 X 쓰레기 주소. 이상한 곳 접근하려 해서 seg fault 발생
{% raw %}
```c
ptrs[1] = (char*) malloc(4);
strcpy(ptrs[1], "ABC");
```
{% endraw %}

1. compile error 
  - 대입 → pointer 가능 / array 불가능
  - `strs[2]` 자체는 `char[64]` → 대입 불가
  - `strcpy` 사용 해야함
1. correct

## ✦ Struct


### ◆ Struct in C


{% raw %}
```c
struct Student {
	int id;
	char name[MAXLEN];
	double GPA;
};

struct Student s, *ps;
struct Student CSE3030[150];

s.id = 20230123
ps = &s;
printf("Student ID: %d\n", ps->id);
```
{% endraw %}

- `struct` 의 각 변수 → field 라고 부름
- 정의 자체는 변수 X, data type 처럼 사용
- memory → 연속된 block 처럼 표현
{% raw %}
```c
struct node {
	int a[4];          // 4(int) * 4 
	long l;            // 8(long)
	struct node *next; // 8(pointer)
```
{% endraw %}

![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_7.png)

  - compiler 가 전체 size 결정
  - assembly 에선 offset 이용 접근
- Example
{% raw %}
```c
void set(struct node *n, int v, int idx) {
	while (n) {
		n->a[idx] = v;
		n = n->next;
	}
}
```
{% endraw %}

{% raw %}
```assembly
0x401106 <+0>:  jmp 0x401112 <set+12>
0x401108 <+2>:  movslq %edx,%rax       ; %rax: 'idx'
0x40110b <+5>:  mov %esi,(%rdi,%rax,4) ; n->a[idx] = v;
0x40110e <+8>:  mov 0x18(%rdi),%rdi    ; n = n->next
0x401112 <+12>: test %rdi,%rdi
0x401115 <+15>: jne 0x401108 <set+2>   ; if (n) goto ...
0x401117 <+17>: ret
```
{% endraw %}

  - `0x18` → 24 (next 의 offset)

### ◆ Alignment


- 어떤 data type 이 K byte 면, 그 타입의 변수는 K 의 배수에 위치해야 함
  - ex) int type 은 메모리 시작 위치 → 4의 배수
![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_8.png)

- Why? 하드웨어 레벨에선 word 단위로 메모리 접근
  - alignment 필수인 CPU도 존재, x86 에서는 recommended

### ◆ Structure Alignment


{% raw %}
```c
struct S1 {
	char c;    // 1
	int i[2];  // 4
	double d;  // 8
	short s;   // 2
};
```
{% endraw %}

![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_9.png)

- 각 요소는 align 된 위치에 놓여야 함
→ padding 통해서 위치 맞추기
  - int → 4의 배수
  - double → 8의 배수
  - short → 2의 배수
- struct 전체 길이 → struct 안의 가장 큰 size 의 배수에 맞추기 (8 byte)

### ◆ Array of Struct


- struct size * 배열 요소 만큼 배치
{% raw %}
```c
struct S2 {
	short i;
	int j;
	short k;
};

struct S2 a[8];
```
{% endraw %}

- a 배열 개당 12 byte
![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_10.png)

- struct 배열의 요소 구하기
{% raw %}
```c
short get_k (struct S2 arr[], int idx) {
	return arr[idx].k;
}
```
{% endraw %}

{% raw %}
```assembly
movslq  %esi, %rsi
lea    (%rsi, %rsi, 2), %rax     ; %rax = idx * 3
movzwl  0x8(%rdi, %rax, 4), %eax ; %rax = arr[] + idx * 12 + 8
ret
```
{% endraw %}

### ◆ Saving Memory Space


- alignment 를 고려해 struct 를 만들면 memory 공간 절약 가능
![](/assets/images/notion/[cs]-assembly:-array-and-struct/img_11.png)
