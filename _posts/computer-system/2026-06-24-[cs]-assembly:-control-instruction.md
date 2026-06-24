---
categories:
- Computer-System
date: '2026-06-24T10:47:00.000+09:00'
layout: single
series: 컴퓨터 시스템 개론
step: 3
tags:
- 제어문
- 어셈블리어
- x86-64
- CS
title: '[CS] Assembly: Control Instruction'
toc: true
toc_sticky: true
---

## ✦ Flag registers


### ◆ Flag registers


![](/assets/images/notion/[cs]-assembly:-control-instruction/img_1.png)

- 특별한 목적의 register
  - 1 : 켜짐
  - 0 : 꺼짐
- `%ZF` : Zero Flag (값이 0 인지 확인)
- `%SF` : Sign Flag (MSB 와 같음)
- `%CF` : Unsigned overflow flag 
- `%OF` : Signed overflow flag
- operation 따라 update
  - arithmetic & logical → update
  - `mov` & `lea` → update X
- 가장 최근 연산의 결과 대한 flag 저장

## ✦ Conditional Operations


### ◆ Conditional Jump


1. 어떤 operation 실행 (`sub`, `cmp`, `and`, `test` 등)
→ 실행 결과에 따라 flag register update
1. flag register 상태에 따라 jump instruction 실행 (`je`, `jne`, `j__`)
- Jump 명령어 종류

| mp | 항상 |
| e (or z) | zero flag 1 이면 (zero 이면) |
| ne (or nz) | zero flag 0 이면 (zero 가 아니면) |
| s | sign flag 1 이면 (값이 음수면) |
| ns | sign flag 0 이면 (값이 음수가 아니면) |
| g | greater (<) |
| ge | greater or equal (≤) |
| l | less (>) |
| le | less or equal (≥) |
| a | above (unsigned) |
| ae | above or equal (unsigned) |
| b | below (unsigned) |
| be | below or equal (unsigned) |

![](/assets/images/notion/[cs]-assembly:-control-instruction/img_2.png)

- 0 check or 부호 check → `and`/ `test` 사용
{% raw %}
```assembly
and %rax, %rax  ; 자기 자신과 and -> 자기 자신
js  0x100       ; rax < 0 이면 jump

cmp $0, %rax    ; 0 ?= %rax 0이면 1, 아니면 0
and %rax, %rax  ; 자기 자신과 and -> 자기 자신
je  0x100       ; rax == 0 이면 jump
```
{% endraw %}

### ◆ `sub` vs `cmp` / `and` vs `test`


- `sub` & `and` → destination register 를 update 함
- `cmp` & `test` → destination register update X, flag register 만 변화

### ◆ More Operation


- `cmov_` : conditional move
- `set_` : 조건 만족하면 destination 1, 불만족하면 0 set
- Example
{% raw %}
```c
long absdiff (long x, long y) {
	long result;
	if (x > y) 
		result = x - y;
	else 
		result = y - x;
	return result;
}
```
{% endraw %}


| Register | Use |
| %rdi | x (첫 번째 argument) |
| %rsi | y (두 번째 argument) |
| %rax | return |

{% raw %}
```assembly
absdiff:
		mov    %rdi, %rdx  ; rdx = x
		mov    %rsi, %rax  ; rax = y
		sub    %rsi, %rdx  ; rdx = x - y
		sub    %rdi, %rax  ; rax = y - x
		cmp    %rsi, %rdi  ; if (x > y)
		cmovg  %rdx, %rax  ; rax = rdx (x - y)
		ret
```
{% endraw %}

## ✦ Loop Statement


### ◆ while


{% raw %}
```c
while (test) {
	Body
}
```
{% endraw %}

- if & goto 로 나타내기
{% raw %}
```c
	goto test;
loop:
	Body
test:
	if (Test)
		goto loop;
```
{% endraw %}

- Another version
{% raw %}
```c
	if (!Test)
		goto done;
loop:
	Body
	if (Test)
		goto loop;
done:
```
{% endraw %}

### ◆ for


- `while` 문 → if & goto 문
{% raw %}
```c
for (Init; test; Updata) {
	Body
}
```
{% endraw %}

{% raw %}
```c
Init;
while (Test) {
	Body;
	Update;
}
```
{% endraw %}

→ if & goto

### ◆ Example


{% raw %}
```assembly
0x000000000040114a <+0>:     mov $0x0,%edx    ; result
0x000000000040114f <+5>:     mov $0x1,%eax    ; i (임시 변수)
0x0000000000401154 <+10>:    jmp 0x40115d <whatAmI+19>

0x0000000000401156 <+12>:    add %rax,%rdx    ; result += i
0x0000000000401159 <+15>:    add $0x1,%rax    ; i++

0x000000000040115d <+19>:    cmp %rdi,%rax    ; n, i 비교
0x0000000000401160 <+22>:    jle 0x401156 <whatAmI+12> ; i <= n 이면 jump

0x0000000000401162 <+24>:    mov %rdx,%rax    ; rax = result
0x0000000000401165 <+27>:    ret
```
{% endraw %}

→ C 언어로

{% raw %}
```c
long sum(long n) {
	long result = 0;
	for (int i = 1; i <= n; i++) {
		result += i;
	}
	return result;
}
```
{% endraw %}

## ✦ Switch Statement


{% raw %}
```c
long switch_ex(long x, long y) {
	long z = y;
	switch (x) {
		case 0:
			z = 5;
			break;
		case 1:
			z += 1;
		case 2:
			z -= 2;
			break;
		case 4:
		case 5:
			z *= 3;
			break;
		default:
			z + 1;
		}
		return z;
	}
}
```
{% endraw %}

- case 0 : 일반적인 switch-case 문
- case 1 → case 2 : fall-through
- case 3 : 존재 X → default
- case 4 & case 5 → multiple labels
- default : case 이외 경우 

### ◆ Assembly Code


{% raw %}
```assembly
0x401106 <+0>:  cmp $0x5,%rdi
0x40110a <+4>:  ja 0x401127 <switch_ex+33>
0x40110c <+6>:  jmp *0x402008(,%rdi,8)
0x401113 <+13>: mov $0x5,%eax
0x401118 <+18>: ret
0x401119 <+19>: add $0x1,%rsi
0x40111d <+23>: lea -0x2(%rsi),%rax
0x401121 <+27>: ret
0x401122 <+28>: lea (%rsi,%rsi,2),%rax
0x401126 <+32>: ret
0x401127 <+33>: mov $0x1,%eax
0x40112c <+38>: ret
```
{% endraw %}

{% raw %}
```assembly
0x401106 <+0>:  cmp $0x5,%rdi
; case 가 5 까지 있으므로 x > 5 check
0x40110a <+4>:  ja 0x401127 <switch_ex+33>
; x > 5 면 defalut 로 jump

...
defalut: 
0x401127 <+33>: mov $0x1,%eax
; z = 1
```
{% endraw %}

### ◆ Jump Table


- `switch` 문에서 어디로 jump 할지 나타내는 table 
{% raw %}
```assembly
0x401106 <+0>:  cmp $0x5,%rdi
; defalut 이동
0x40110a <+4>:  ja 0x401127 <switch_ex+31>
; jump table 이동
0x40110c <+6>:  jmp *0x402008(,%rdi,8)
...
0x401127 <+33>: mov $0x1,%eax
0x40112c <+38>: ret
```
{% endraw %}

### ◆ case 0


- 일반적인 switch-case 문
{% raw %}
```assembly
0x401106 <+0>:  cmp $0x5,%rdi
0x40110a <+4>:  ja 0x401127 <switch_ex+33>
; jump table 이동
0x40110c <+6>:  jmp *0x402008(,%rdi,8)

case_0:
0x401113 <+13>: mov $0x5,%eax
0x401118 <+18>: ret
```
{% endraw %}

### ◆ case 1 & 2


- case 1 → case 2 : fall-through
{% raw %}
```assembly
0x401106 <+0>:  cmp $0x5,%rdi
0x40110a <+4>:  ja 0x401127 <switch_ex+33>
0x40110c <+6>:  jmp *0x402008(,%rdi,8)
...
case_1:
0x401119 <+19>: add $0x1,%rsi
; 끝에 ret 없음
case_2:
0x40111d <+23>: lea -0x2(%rsi),%rax
0x401121 <+27>: ret
```
{% endraw %}

### ◆ case 3


- 존재 X → default
{% raw %}
```assembly
0x401106 <+0>:  cmp $0x5,%rdi
0x40110a <+4>:  ja 0x401127 <switch_ex+33>
0x40110c <+6>:  jmp *0x402008(,%rdi,8)
; jump table 에서 default 로 jump
default:
0x401127 <+33>: mov $0x1,%eax
0x40112c <+38>: ret
```
{% endraw %}

### ◆ case 4 & 5


- case 4 & case 5 → multiple labels
{% raw %}
```assembly
0x401106 <+0>:  cmp $0x5,%rdi
0x40110a <+4>:  ja 0x401127 <switch_ex+33>
0x40110c <+6>:  jmp *0x402008(,%rdi,8)

case_4:
case_5:
0x401122 <+28>: lea (%rsi,%rsi,2),%rax
0x401126 <+32>: ret
```
{% endraw %}

### ◆ In General


- single solution X
- Q) 다음과 같은 상황에는 어떻게 assembly code 짜야 할까?
  1. case 101, case 102, ... case 106, case 107
  1. case -2, case -1, ... case 4, case 5
  1. case 1, case 48, case 105, ... case 306
    - **Switch-Case의 Assembly 구현 전략**
컴파일러는 case 분포에 따라 **세 가지 전략** 중 하나를 선택합니다.

    - **전략 1 : Jump Table (점프 테이블)**
    - **상황 1 - case 101 ~ 107**
{% raw %}
```c
switch (x) {
    case 101: ...; break;
    case 102: ...; break;
    // ...
    case 107: ...; break;
}
```
{% endraw %}

**핵심 아이디어** : x를 **베이스 값 (101) 기준으로 정규화**한 뒤, 배열 인덱스처럼 사용합니다.

{% raw %}
```assembly
; x = eax
sub  eax, 101          ; 정규화 : eax = x - 101 (0 ~ 6 범위로 변환)
cmp  eax, 6            ; 범위 초과 검사
ja   .default          ; eax > 6이면 default로
jmp  [table + eax * 8] ; 점프 테이블 인덱싱 (64-bit : *8)

.table:
    dq .case101
    dq .case102
    dq .case103
    dq .case104
    dq .case105
    dq .case106
    dq .case107

.case101: ...; jmp .end
.case102: ...; jmp .end
; ...
```
{% endraw %}

    - **상황 2 - case -2 ~ 5**
{% raw %}
```assembly
; x = eax
sub  eax, -2           ; 즉, add eax, 2 → 정규화 (0 ~ 7 범위)
cmp  eax, 7
ja   .default
jmp  [table + eax * 8]
```
{% endraw %}

음수가 포함되어도 **정규화만 하면 동일**하게 점프 테이블 적용 가능합니다.

    - **전략 2 : Binary Search Tree (이진 탐색)**
    - **상황 3 - case 1, 48, 105, ..., 306**
값들 사이 간격이 커서 점프 테이블을 만들면 **메모리 낭비**가 심합니다.
( case 1 ~ 306이면 테이블 크기 306, 실제 사용은 일부뿐 )

컴파일러는 **중간값 비교를 재귀적으로** 수행합니다.

{% raw %}
```assembly
; case 값들 : 1, 48, 105, 189, 230, 270, 306 (예시)
; 중간값 = 189

cmp  eax, 189
je   .case189
jl   .left_half        ; eax < 189 → 왼쪽 절반 탐색
jg   .right_half       ; eax > 189 → 오른쪽 절반 탐색

.left_half:
    cmp  eax, 48
    je   .case48
    jl   .ll_half      ; 1 탐색
    jg   .lr_half      ; 105 탐색
; ...
```
{% endraw %}

    - **전략 3 : Linear Search (선형 비교)**
{% raw %}
```assembly
cmp  eax, 1
je   .case1
cmp  eax, 48
je   .case48
cmp  eax, 105
je   .case105
jmp  .default
```
{% endraw %}

    - **전략 선택 기준 요약**

| 상황 | 전략 | 기준 |
|:--|:--|:--|
| 101 ~ 107 | ✅ Jump Table | 연속 범위 → O(1) |
| -2 ~ 5 | ✅ Jump Table | 음수 포함 연속 범위 → 정규화 후 O(1) |
| 1, 48, 105, ..., 306 | ✅ Binary Search | sparse → O(log n) |
| case 2 ~ 3개 | Linear | 개수 적음 → 단순 비교 |
