---
categories:
- Data-Structure
date: '2026-01-21'
tags:
- DS
- 자료 구조
- 포인터
title: '[DS] Pointers'
toc: true
toc_sticky: true
---

- Sequential 표현 
  - 장점
    - 연속적인 요소들을 고정된 거리를 두고 저장함. 
    - 많은 연산에 적용 가능
  - ex) 배열 int a[10] 등.
  - 단점
    - 삽입, 삭제에 O(n)의 시간 복잡도 소요. (∵ 위치 정렬이 필요)
    - 배열의 크기는 고정되어 있기에 데이터 공간의 낭비가 있음.


- Linked 표현
  - node 를 통해 list를 표현
    - data : 정보를 담고 있음
    - pointer : 다음 list 요소를 가리킴. (link)
  - 크기 제한이 없음.
  ![](/assets/images/notion/[ds]-pointers/img_1.png)



- C의 pointer 
  - operator 
    - & : 주소를 나타내는 operator
    - * : 주소가 가리키는 값(value)을 나타내는 operator
    ![](/assets/images/notion/[ds]-pointers/img_2.png)

```c++
int i; // i에는 정수형 변수 저장
int *pi; // pi에는 정수형 변수의 주소 저장
pi = &i; // i의 주소 pi에 할당

// i의 저장값 변경 방법
i = 10; // 1
*pi = 10; // 2
```

    - null pointer : 아무것도 가리키지 않는 포인터.
      - 정수 0으로 표현
      - 체크 방법
`if (pi == NULL)` or `if(!pi)`



![](/assets/images/notion/[ds]-pointers/img_3.png)



##  4.1.1 Pointers Can Be Dangerous

- pointer는 유연성 & 효율성 면에서 좋음
- 예상치 못한 메모리 공간에 접근해 위험할 수 있음
  - 아무것도 가리키지 않을 때는 NULL로 바꿔야 함
  - pointer 타입을 바꿀 때 type cast를 반드시 해야 함.
```c++
pi = malloc(sizeof(int)); // 4 만큼의 정수형 공간 할당
pf = (float *) pi; // 정수 -> 실수로 type cast
```



##  4.1.2 Using Dynamically Allocated Storage

- `malloc` 을 하면 반드시 `free` 해주자.
###  [Program 4.1]

```c++
int i, *pi;
float f, *pf;
pi = (int *) malloc(sizeof(int)); // 4 byte 동적 할당
pf = (float *) malloc(sizeof(float)); // 8 byte 동적 할당
*pi = 1024; // i = 1024
*pf = 3.14; // f = 3.14
printf("an integer = %d, a float = %f\n", *pi, *pf);
free(pi); // 사용 완료 후엔 free
free(pf); // 사용 완료 후엔 free
```



만약 8번째 줄 아래에 

```c++
pf = (float *) malloc(sizeof(float));
```

을 넣는다면, 기존에 할당한 공간은 미아가 되고, 3.14라는 값 또한 사라진다. 

그리고 새로운 공간이 할당되고, 9번째 줄을 통해 free된다.



