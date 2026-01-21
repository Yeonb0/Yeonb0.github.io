---
layout: single
title: "[DS] Polynomial"
categories:
  - Data-Structure
tag: [DS, 자료구조, 다항식]
---

- # Polynomial

  ---

  ### ADT
  
  > **ADT** Polynomial
  >
  > 
  >
  > **Objects** :
  >
  > $$
  > P(x) = a_1x^{e_1} + a_2x^{e_2} + ... + a_nx^{e_n}
  > $$
  >
  > <e**ᵢ**, a**ᵢ**> 의 순서쌍으로 된 집합이다. 여기서 a**ᵢ**는 계수이고, e**ᵢ**는 지수(거듭제곱)이다. e는 0 또는 0 보다 큰 정수이다.
  >
  > 
  >
  > **Function** : 
  > 모든 poly, poly1, poly2∈Polynomial / coef∈Coefficients / expon∈Exponents
  >
  > 
  >
  > *Polynomial*  `Zero()`
  >
  > ​	**return** 다항식, p(x) = 0
  >
  > 
  >
  > *Boolean*  `IsZero(poly)`
  >
  > ​	**if**(poly) **return** *FALSE*
  >
  > ​	**else return** *TRUE*
  >
  > 
  >
  > *Coefficient*  `Coef(poly, expon)`
  >
  > ​	**if**(expon∈poly) **return** 계수
  >
  > ​	**else return** 0
  >
  > 
  >
  > *Exponent*  `LeadExp(poly)`
  >
  > ​	**return** poly에서 가장 큰 지수(차수)
  >
  > 
  >
  > *Polynomial*  `Attach(poly, coef, expon)`
  >
  > ​	**if**(expon∈poly) **return** error
  >
  > ​	**else return** <coef, exp> 항이 삽입된 다항식 poly
  >
  > 
  >
  > *Polynomial*  `Remove(poly, expon)`
  >
  > ​	**if**(expon∈poly) 
  >
  > ​		**return** 지수가 expon인 항이 삭제된 다항식 poly
  >
  > ​	**else return** 에러
  >
  > 
  >
  > *Polynomial*  `SingleMult(poly, coef, expon)`
  >
  > ​	**return** 다항식 poly·coef·xᵉˣᵖᵒ 
  >
  > 
  >
  > *Polynomial*  `Add(poly1, poly2)`
  >
  > ​	**return** 다항식 poly1+poly2
  >
  > 
  >
  > *Polynomial* `Mult(poly, poly2)`
  >
  > ​	**return** 다항식 poly1 · poly2
  
  
  
  ### Polynomial Representation
  
  - [Program 2.5] : Initial version of padd function
    - padd function : polynomial add
  
  ```c
  // d = a + b, where a, b, and d are polynomials
  
  d = Zero();  // 0으로 초기화
  while(!IsZero(a)&&!IsZero(b)) {  // 다항식 a, b가 0이 아니면
  	switch COMPARE(Lead_Exp(a), Lead_Exp(b)) {  // a와, b의 최고차항 비교
  		case -1 : // a가 b보다 최고차항이 작으면
  			d = Attach(d, Coef(b, Lead_Exp(b)), Lead_Exp(b)); // d에, b의 최고차항의 계수를 가진, 차수의 항 붙임
  			b = Remove(b, Lead_Exp(b)); // b에서, 최고차항 제거
  			break;
  		case 0 : // a와 b의 최고차항이 같으면
  			sum = Coef(a, Lead_Exp(a)) + Coef(b, Lead_Exp(b));  // a와 b의 최고차항 더하기
  			if (sum) { // 두 최고차항의 합이 0이 아니면
  				Attach(d, sum, Lead_Exp(a)) // d에, 두 최고차항의 합을 더한, 차수의 항 붙임(b를 사용해도 무관)
  			}
  			a = Remove(a, Lead_Exp(a)); // a에서, 최고차항 제거
  			b = Remove(b, Lead_Exp(b)); // b에서, 최고차항 제거
  			break;
  		case 1 : // a가 b보다 최고 차항이 크면
  			d = Attach(d, Coef(a, Lead_Exp(a)), Lead_Exp(a)); // d에, a의 최고차항의 계수를 가진, 차수의 항 붙임
  			a = Remove(a, Lead_Exp(a)); // a에서, 최고차항 제거
  	}
  }
  //insert any remaining terms of a or b into d 
  ```
  
  - 필요한 함수
    - `COMPARE(a, b)` : a가 작으면 -1, 같으면 0, 크면 1
    - `Zero()` : 다항식 0으로 초기화
    - `IsZero()` : 다항식 0인지 참/거짓
    - `Attach(a, b, c)` : 다항식 a에 $bx^c$ 항 추가
    - `Remove(a, c)` :  다항식 a에서 $nx^c$ 항 제거
  
  - Representation of Polynomial
  
  ```c
  #define MAX_DEGREE 1001 // 최고차는 1001
  typedef struct {
  	int degree; // 차수
  	float coef[MAX_DEGREE];  // 각 차수별 계수
  } polynomial;
  ```
  
  $$
  A(x) = \Sigma{a_ix^i}
  $$
  
  → 그런데 이런 식으로 배열의 길이를 고정시키면 버려지는 공간이 많이 생긴다.
  
  → 희소 행렬과 유사하게 나타내기
  
  ```c
  #define MAX_TERMS 100
  typedef struct {
  	float coef; // 계수
  	int expon; // 차수
  } polynomial;
  polynomial terms[MAX_TERMS];  // 100개의 계수&차수 쌍으로 이루어진 구조체 배열
  int avil = 0; 
  ```
  
  → 한 개 terms 배열로 여러 개의 다항식 표현 가능.
  
  계수는 내림차순으로 정렬되어 있음.
  
  <img src="../../assets/images/posts/2026-01-19-Polynomial/image.png" alt="image" style="zoom:67%;" />
  
  
  
  - avail index 부터 새로운 다항식 표현가능, avail 은 전역 변수
  
  - 0 을 표현하기  : startc > finishc
  
  - [Program 2.6] : Function to add two polynomials
  
    - padd 를 위한 함수
  
    ```c
    void attach(float coefficient, int exponent){ // 차수 & 계수를 인자로 받음
    	// 다항식에 새로운 항 추가
    	if (avail >= MAX_TERMS) {  // avail 이 최대 항을 넘어서면
    	 fprintf(stderr, "Too many terms in the polynomial");
    	 exit(1);
    	}
    	// 그렇지 않다면
    	terms[avail].coef = coefficient; // 빈 항에 계수
    	terms[avail++].expon = exponent; // 차수 채우고, avail은 다음 항으로 넘어가기
    ```
  
  ```c
  void padd(int starta, int finisha, int startb, int finishb, int *startd, int *finishd){  
  	// a, b의 시작 & 끝 인덱스 -> 값을 참조하기만 할 뿐 변화 하지는 않음.
  	// d는 실제로 변화 시킬 값이기 때문에 포인터로 받음.
  	float coefficient;  // 계수 
  	*startd = avail; // startd 의 인덱스를 avail로 설정
  	while(starta <= finisha && startb <= finishb) { // 두 다항식의 길이가 끝날 때 까지
  		switch(COMPARE(terms[starta].expon, terms[startb].expon){ // a의 최고차항과 b의 최고차항 비교
  			case -1 :  // b가 더 클 때
  				attach(terms[startb].coef, terms[startb].expon);  // 계수, 차수 저장하고 avail은 다음 칸 넘어가기
  				startb++; // b의 최고차항 없애기 
  				break;
  			case 0 : // a와 b가 같을 때
  				coefficient = terms[starta].coef + terms[startb].coef; // a와 b의 최고차항의 계수 더하기
  				if (coefficient) // 계수의 합이 0이 아니라면
  					attach(coefficient, terms[starta].expon); // 계수, 차수 저장하고 avail 다음 칸 넘어가기
  				starta++; startb++; // a, b의 최고차항 없애기
  				break;
  			case -1 :  // a가 더 클 때
  				attach(terms[starta].coef, terms[starta].expon);  // 계수, 차수 저장하고 avail은 다음 칸 넘어가기
  				starta++; // a의 최고차항 없애기 
  		}
  	}
  	// a, b의 나머지 항들 없애기(&&로 비교했기에 하나라도 다항식이 0이면 더이상 비교가 안됌. 한 쪽만 남았을 경우엔 그 앞 항들보다 무조건 차수가 낮음)
  	for( ; starta <= finisha ; starta++)
  		attach(terms[starta].coef, terms[starta].expon);
  	for( ; startb <= finishb ; startb++)
  		attach(terms[startb].coef, terms[startb].expon);
  	*finishd = avail-1; // finishd의 값은 계속 증가한 avail - 1 
  }
  ```
  
  → padd의 시간 복잡도 : 다항식 a, b의 항수 만큼 반복 O(n+m) = O(n)
