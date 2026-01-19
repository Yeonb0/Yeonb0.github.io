---
layout: single
title: "[DS] Evaluation of Expression"
categories: Data-Structure
tag: [DS, 자료구조]
---



# 3.6 Evaluation of Expressions

---

## 3.6.1 Expressions

- token 요소
    - operator 연산자
    - operand 피연산자
    - parentheses 괄호
- precedence hierachy : 연산자 간 우선순위
    1. unary
    2. ×, ÷
    3. +, -
    4. 같은 연산자는 왼쪽 부터.
- Parentheses(괄호) 는 안쪽 괄호 부터 실행.

- 수식의 표현 방법
    - Infix : 연산자가 안에 → 일반적인 표현법
        - a * b
    - Prefix : 연산자가 앞에
        - * a b
    - Postfix : 연산자가 뒤에 → 컴퓨터의 표현법
        - a b *
    
    → Prefix, Postfix 는 괄호가 필요 없다!
    
    → 피연산자의 위치는 동일. 연산자의 위치가 다르다
    
    | Infix | Postfix |
    | --- | --- |
    | (1 + 2) * 7 | 1 2 + 7 * |
    | ((a / (b - c + d)) * (e - a) * c | a b c - d + / e a - * c * |
    | a / b - c + d * e - a * c | a b / c - d e * + a c * - |

## 3.6.2 Evaluating Postfix Expressions

- 한 번 스캔해서 스택으로 저장하면서 postfix로 만듬.
    1. 연산자를 찾을 때 까지 피연산자를 stack에 넣음
    2. 연산자를 만나면 operator 계산에 필요한 수 만큼을 stack에서 꺼내옴
       
        ex) stack 안에 a b c 있고 연산자 * 를 만나면 c 와 b 를 꺼냄.
        
    3. 연산 실행
    4. 연산 결과를 다시 stack에 넣음

→ 피연산자들은 모두 push, 연산자 만나면 2개 pop, 계산 후 다시 push

<img src="../images/2026-01-19-Evaluation of Expressions/e5a93ad3-48e3-41e8-b91f-00635a962603.png" alt="e5a93ad3-48e3-41e8-b91f-00635a962603" style="zoom: 50%;" />



### [Program 3.13] : Function to evaluate a postfix

- Declaration
  
    ```cpp
    #define MAX_STACK_SIZE 100 
    #define MAX_EXPR_SIZE 100 
    typedef enum {lparen, rparen, plus, minus, times, divide, mod, eos, operand} precedence;
    int stack[MAX_STACK_SIZE]; // global stack
    char expr[MAX_EXPR_SIZE]; // input string
    ```
    

```cpp
int top = -1; // stack의 맨 위. 초깃값으로 -1 설정

int eval(void){
  // 전역 변수 expr 연산. 피연산자는 한 자리 수 가정
  // '\0'은 수식의 끝 표현.
  // 함수 getToken 은 토큰의 타입과 문자 심벌을 반환.
  
  precedence token;
  char symbol;
  int op1, op2; // 뽑는 순 2 -> 1 | 계산 순 1 -> 2
  int n = 0; // 수식 문자열을 위한 변수, 초깃값 0
  token = getToken(&symbol, &n); // call-by-reference, 원본 값 변경 O
  while(token != eos) { // 수식 끝까지
	  if (token == operand) // 피연산자면 push
		  push(symbol-'0'); // 문자열에서 정수로 바꿔서 push
		else { 
		// 연산자면 피연산자 두 개 pop, 연산 후 결과 stack에 넣기
			op2 = pop(); // 2부터 뽑는 것 유의.
			op1 = pop();
			switch (token) {
				case plus : push(op1 + op2); break;
				case minus : push(op1 - op2); break;
				case times : push(op1 * op2); break;
				case divide : push(op1 / op2); break;
				case mod : push(op1 % op2); break;
			}
		} // else 문 끝
		token = getToken(&symbol, &n); // token 구한 후 다음 칸 이동
	} // while 문 끝
	return pop(); // 수식 결과 출력
}
```

### [Program 3.14] : Function to get a token from the input string

```cpp
precedence getToken(char *symbol, int *n) {
  // 다음 token 취하기.
  // 반환값은 enum 값
  *symbol = expr[(*n)++]; // *symbol 에 문자 저장 후, n++
  switch (*symbol) {
	  case '(' : return lparen;
	  case ')' : return rparen;
	  case '+' : return plus;
	  case '-' : return minus;
	  case '/' : return divide;
	  case '*' : return times;
	  case '%' : return mod;
	  case ' ' : return eos;
	  default : return operand; // 기본 값은 피연산자.
	}
}
```

## 3.6.3 Infix to Postfix

- Infix 에서 Postfix로 바꾸는 알고리즘
    1. 표현에 괄호를 추가해서 바꾼다
    2. 이항 연산자들을 모두 그들 오른쪽에 있는 괄호와 대체한다
    3. 모든 괄호를 삭제한다

ex) a / b - c + d * e - a * c

1. ((((a / b) - c) + (d * e)) - (a * c))

2&3. a b / c - d e * + a c * -

→ 손으론 간단하지만, 컴퓨터에겐 두 번의 연산 과정이 필요하기에 비효율적.

- 피연산자의 순서는 Infix & Postfix 동일
- → 방향으로 scan 하며 Postfix로 바꿀 수 있다.
- 연산자 a 가 top에 있을 때 새로운 연산자 b가 들어오려 할 때
    - a의 우선순위 ≥ b의 우선순위 : a pop 시킴
    - a의 우선순위 < b의 우선순위 : 그대로 b push
- 괄호는 가장 높은 우선순위 → 무조건 stack 에 넣는다.
    - `(` 의 우선순위
        - stack으로 들어갈 때 : 20. 반드시 들어감.
        - stack에서 나갈 때(다른 것과 비교) : 0. `)` 나오기 전까진 `(` 위에 연산자 쌓임

<img src="../images/2026-01-19-Evaluation of Expressions/789b3ed4-f41c-4c70-8450-5d1eca08a920.png" alt="789b3ed4-f41c-4c70-8450-5d1eca08a920" style="zoom:80%;" />

```cpp
precedence stack[MAX_STACK_SIZE];
// isp = in-stack precedence, stack 안에서, stack에서 pop 할 때의 우선순위
// icp = icome precedence, stack 밖에서, stack으로 push 할 때의 우선순위
// lparen, rparen, plus, minus, times, divide, mod, eos 순서.
                     '('  ')'  '+'  '-'  '*'  '/'  '%'  
static int isp[] = { 0,  19,  12,  12,  13,  13,  13,  0}; // stack 안에서
static int icp[] = {20,  19,  12,  12,  13,  13,  13,  0}; // stack 밖에서
int top = 0; 
```

→ 새 연산자의 icp > top의 isp : 새 연산자 push

→ 새 연산자의 icp ≤ top의 isp : top을 pop

### [Program 3.15] : Function to convert from Infix to Postfix

```cpp
void postfix(void) {
	// infix -> postfix 변환. 
	// 수식, stack, top은 전역 변수
	int n = 0;
	stack[0] = eos; // stack의 끝 넣기
	for (token = getToken(&symbol, &n); token != eos; token = getToken(&symbol, &n) {
		// 수식의 끝까지 token 뽑아오기
		if (token == operand) // 피연산자면
			printf("%c", symbol); // 바로 출력
		else if (token == rparen) { // ')' 이면
			while (stack[top] != lparen) // stack에서 '(' 나올 때까지
				printToken(pop()); // 연산자 pop 해서 출력
			pop(); // '(' 제거
		} else { // 일반 연산자면
			// isp >= icp 면 isp pop & icp push
			// isp < icp 면 그냥 icp push
			while (isp[stack[top]] >= icp[token])
				printToken(pop()); // isp pop
			push(token); // icp push
		}
	} // for문 끝
	while ((token = pop()) != eos) // stack끝까지 pop
		printToken(token);
	printf("\n");
}
```

- Postfix 변환 함수 분석
    - 수식에 n개의 token이 있으면,
        - Θ(n) : token 꺼내기
        - Θ(n) : while loop
    
    → `postfix` 의 시간 복잡도는 Θ(n)