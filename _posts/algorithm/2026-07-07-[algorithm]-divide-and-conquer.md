---
categories:
- Algorithm
date: '2026-07-07T19:43:00.000+09:00'
layout: single
series: 알고리즘 설계와 분석
step: 2
tags:
- 알고리즘
- 분할 정복
- 정렬
- 점화식
title: '[Algorithm] Divide-and-Conquer'
toc: true
toc_sticky: true
---

## ✦ Divide-and-Conquer


### ◆ Recap


- Divide : base case 만날 때까지 쪼개기
- Conquer : 쪼갠 case 들을 recursive 하게 풀기
- Combine : 푼 case 들을 원래대로 합치기
- 실행 시간 구하기 
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_1.png)

  - 점화식 정의
    - base case : 보통 실행 비용 아주 작음
    - recursive case : Divide + Conquer + Combine 실행 시간 더하기 
      - a : 나눈 것에 대해 Conquer 실행 횟수
      - b : 전체 데이터를 나누는 횟수
  - 점화식을 풀어 점근 해 구하기
- ex) Merge Sort
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_2.png)

![](/assets/images/notion/[algorithm]-divide-and-conquer/img_3.png)

  - 두 개의 부분으로 나눔 → 두 번 conquer 실행

### ◆ Recurrences (점화식, 재귀식)


- 수학적 점화식
- 반드시 등호로 주어진다 (X) → 등식 / 부등식 모두 가능
- ex) 피보나치 수열 : F_n = F_{n-1} + F_{n-2}
- 점화식
  - 1개 이상의 base case 
  - recursive case

### ◆ Algorithmic Recurrences


- 알고리즘 점화식
- n_0 : base case 가르는 기준
→ n_0 미만 : base case ⇒ 실행 시간 상수 T(n) = \Theta(1) 
→ n_0 이상 : recursive case

  - base case 보통 생략
→ n_0 은 적당한 bound 로 자유롭게 설정 가능 ⇒ 상수 시간 \Theta(1)
  - 올림, 내림은 보통 제거 (해가 바뀌지 않음)
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_4.png)

  - 어떤 점화식은 부등호로 나타냄
    - ex) T(n) ≤ 2T(n/2) + \Theta(n) → 상한 (Big-O) 구하는 점화식

## ✦ Multiplying Square Matrix


- 정사각행렬 곱하기 
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_5.png)

  - C + A × B 구하기
{% raw %}
```cpp
MATRIX_MULTIPLY(matrix A, B, C, size n)
for i = 1 ~ n
	for j = 1 ~ n
		for k = 1 ~ n
			c_ij = c_ij + a_ik * b_kj
```
{% endraw %}

### ◆ Simple Divide-and-Conquer Algorithm


- 문제 간단하게 C = A · B 라고 설정
- matrix A, B, C 를 \frac{n}{2} \times \frac{n}{2} 로 나누기 → 총 4 부분
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_6.png)

![](/assets/images/notion/[algorithm]-divide-and-conquer/img_7.png)

  - 총 8 개의 곱셈 식 필요
- Divide : matrix 반으로 쪼개기  \frac{n}{2}\times\frac{n}{2}
- Conquer : 행렬 곱
- Combine : 행렬까리 곱한 것 합치기
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_8.png)

![](/assets/images/notion/[algorithm]-divide-and-conquer/img_9.png)

- Analysis
  - base case (n = 1) : 두 수 곱하기 → \Theta(1)
  - recursive case (n > 1) 
    - Divide : \Theta(1)
    - Conquer : 8T(\frac{n}{2})
    - Combine : C를 바로 update 하므로 X
  - T(n) = 8T(\frac{n}{2}) + \Theta(1) 
→ 점화식으로 시간 복잡도 구하기

      - master method 사용 → \Theta(n^3)
Merge Sort : T(n) = 2T(\frac{n}{2}) + \Theta(n) → \Theta(n\lg n)

Matrix Multiply : T(n) = 8T(\frac{n}{2}) + \Theta(1) → \Theta(n^3)

→ Merge Sort 가 더 빠름! 

### ◆ Strassen’s Algorithm


- matrix 의 곱셈 식을 줄이자 
  - How? → 합차 공식
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_10.png)

  - 덧셈(or 뺄셈) +1, 곱셈 -1
- Algorithm
  1. n = 1 이면 base case
→ 비용 : \Theta(1)
  1. n > 1 이면 recursive case
matrix 를 \frac{n}{2}\times\frac{n}{2} 로 나누기
→ 비용 : \Theta(1)
  1. S_1 \sim S_{10} 의 기존 matrix 를 더하거나 뺀 matrix 만들기 
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_11.png)

→ 비용 : 중첩 2번 → 10 \Theta(n^2) 

  1. 곱셈 사용해서 기존 matrix & S 이용해 P 구하기
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_12.png)

→ 비용 : 중첩 3번 → 7 T(\frac{n}{2})

  1. P 로 원래 구하려던 matrix C 구하기
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_13.png)

  1. 검증 : 각각의 C 가 원래 원하던 값과 동일하게 나옴!
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_14.png)

  - 최종 실행 시간 : T(n) = 7T(\frac{n}{2}) + \Theta(n^2)
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_15.png)

→ n 이 커질수록 차이 ↑

## ✦ Methods for Solving Recurrences


1. 점화식 정의하기
1. 점근해 찾기 
1. 점근적 표기법으로 나타내기
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_16.png)

### ◆ Substitution Method


- 대입법
- 방법
  1. 해를 추측한다 (Guess)
  1. 수학적 귀납법으로 추측이 맞다는 걸 증명한다 (Prove)
→ loose 한 bound 로 시작.

상한을 높게, 하한을 낮게 설정하고 점점 tight 하게

- Example
  - 병합 정렬의 점화식 : T(n)=2T(⌊\frac{n}{2}⌋)+Θ(n)
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_17.png)

  1. Guess
    - 병합 정렬 점화식의 해가 T(n) = O(n \lg n) 이라고 가정
→ 어떤 상수 c > 0 에 대해 T(n) ≤ cn \lg n 이 성립

  1. Prove
    1. inductive case 
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_18.png)

명제 : Uppder bound 가 Guess 라고 가정 

      - n_0 보다 크거나 같은 모든 숫자 + n 보다 작은 숫자에선 성립 (induction)
      - n ≥ 2n_0 가정
      - 내가 Guess 한 식을 점화식에 대입
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_19.png)

    1. base case
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_20.png)

      - n_0 ≤ n < 2n_0, n_0 > 1 (log 조건, 실행 시간은 0 보다 커야 함)
→ 2n_0 보다 크면 inductive case
      - n_0 = 2 선택 → n = 2, 3 
        - base case 수행 시간은 상수 시간
      - c = \text{max}\{T(2), T(3)\}
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_21.png)

![](/assets/images/notion/[algorithm]-divide-and-conquer/img_22.png)

    - 상수 17은 무시
    - n 이 커지면 17 은 영향 적음

### ◆ Recursion Tree


- Substitution Method 보다 정확
  - Node 종류
    - Root : 트리의 꼭대기 node
    - Internal Node : Leaf 가 아닌 node
    - Leaf : 맨 밑바닥에 있는 node. child 가 없음
  - Metrics (Edge 수로 count)
    - Depth : root 로부터의 거리
      - root 자신은 0
      - 아래로 향함
    - Height : target node 로부터 leaf 까지의 거리 
      - leaf 자신은 0
      - 위로 향함
    - Level = Depth
- 방법
  1. root 부분에 Divide & Combine 부분을 넣는다
  1. root 에서 Conquer 횟수 만큼 child node 그리기
  1. n = 1 이 될 때까지 내려간다
  1. Total cost 를 구한다
  - Tree 의 답이 맞는지 검증 → Substitution Method 사용!
- Example
  - T(n) = 3T(\frac{n}{4}) + \Theta(n^2) 의 Upper bound 구하기
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_23.png)

  1. root : \Theta(n^2) → cn^2
  1. root 에 Conquer 횟수 (3번) 만큼 child 만들기
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_24.png)

  1. n = 1 될 때까지 내려가기
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_25.png)

    - depth 가 +1 될 때마다 size \frac{1}{4} 배
→ depth i 에서의 node 크기 : \frac{n}{4^i}
    - 부분 문제의 크기가 1 → leaf 
\frac{n}{4^i} = 1 ⇒ i = \log_4n
    - 0 ~ \log_4{n-1} → internal node
\log_4n → leaf node
    - 각 노드가 3개의 child node 가짐 
→ depth i 에서의 node 갯수 : 3^i
  1. Total cost 구하기 
    - Internal node
      - depth i 에서의 총 비용 : node 1개의 비용 × node 갯수
<div class="equation-box">

$$
3^i \times c(\frac{n}{4^i})^2 = (\frac{3}{16})^icn^2
$$

</div>

      - i 에서의 총 비용 공식을 depth 0 ~ \log_4n-1 까지 적용
→ \frac{16}{13}cn^2
    - Leaf node
      - 각 node 당 실행 시간 \Theta(1) 
      - node 갯수 : 3^{\log_4n} = n^{\log_43}
      - 잎 전체 비용 
→ \Theta(n^{\log_43}) 
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_26.png)

    - 뿌리의 비용 (cn^2) 이 전체를 지배
  - ∴ Upper bound → O(n^2)
    - T(n) = \Omega(n^2) → 첫 recursion call 의 비용
    - T(n) = \Theta(n^2)
  - T(n) = T(\frac{n}{3}) + T(\frac{2n}{3}) + \Theta(n)
    - 불균형 트리
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_27.png)

    - 각 레벨의 총합이 cn (멈추는데 까지)
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_28.png)

  - Lower bound : 중간에 멈추는 곳
  - Upper bound : 끝까지 가는 곳

### ◆ Master Method


- 조건 : T(n) = aT(\frac{n}{b}) + f(n) & a ≥ 1 & b >1 일 때
  - ex) T(n) = T(\frac{n}{3}) + T(\frac{2n}{3}) + \Theta(n) → 적용 불가능 (T 항이 2개)
- 방법 : Driving Function 과 Watershed Function 비교
  - Driving Function : f(n)
    - divide & combine
  - Watershed Function : n^{\log_ba}
    - recursion tree 의 leaf node 들
→ 누가 더 dominant 한가?

- Cases
  - Case 1) Watershed Function 우위 
    - f(n) < O(n^{\log_ba}) → T(n) = \Theta(n^{\log_ba})
  - Case 2) Driving Function & Watershed Function 비슷
    - f(n) = \Theta(n^{\log_ba} \lg^kn) → T(n) = \Theta(n^{\log_ba} \lg^{k+1}n)
    - ex) merge sort
  - Case 3) Driving Function 우위
    - f(n) > O(n^{\log_ba}) → T(n) = \Theta(f(n))
- Examples
![](/assets/images/notion/[algorithm]-divide-and-conquer/img_29.png)
