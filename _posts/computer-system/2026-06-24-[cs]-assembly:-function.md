---
categories:
- Computer-System
date: '2026-06-24T10:48:00.000+09:00'
layout: single
series: 컴퓨터 시스템 개론
step: 4
tags:
- CS
- 어셈블리어
- x86-64
- 서브프로그램
title: '[CS] Assembly: Function'
toc: true
toc_sticky: true
---

## ✦ Memory Structure


### ◆ Stack


- stack 에 data 추가 → top 에서 변화 일어남
![](/assets/images/notion/[cs]-assembly:-function/img_1.png)

### ◆ `push` Instruction


- `push` src
  1. `%rsp` + 8 → stack 공간 확보
  1. 얻은 공간에 src 작성
- ex) `push %rax`
![](/assets/images/notion/[cs]-assembly:-function/img_2.png)

### ◆ `pop` Instruction


- `pop` reg
  1. reg 에 기존 `%rsp` 저장되어 있던 값 저장
  1. `%rsp`+ 8
- ex) `pop %rbx`
![](/assets/images/notion/[cs]-assembly:-function/img_3.png)

- 여전히 memory 공간에는 값이 저장되어 있으나, 더 이상 사용 X

## ✦ Change of control-flow


![](/assets/images/notion/[cs]-assembly:-function/img_4.png)

- Example
  - C code
    - `multstore`
{% raw %}
```c
void multstore(long *dest) {
	long t = mult2(5L, 3L);
	*dest = t;
}
```
{% endraw %}

→ Caller function : `mult2` call

    - `mult2`
{% raw %}
```c
long mult2(long a, long b) {
	long s = a * b;
	return s;
}
```
{% endraw %}

→ Callee function : `mult2` 에 의해 call 당함

  - Asssembly
    - `multstore`
{% raw %}
```assembly
0000000000400536 <multstore>:
400536: push %rbx
400537: mov %rdi,%rbx
40053a: mov $0x3,%esi # Setup 2nd arg
40053f: mov $0x5,%edi # Setup 1st arg
400544: call 0x400550 <mult2> # mult2(5,3)
400549: mov %rax,(%rbx) # Update *dest
40054c: pop %rbx
40054d: ret
```
{% endraw %}

    - `mult2`
{% raw %}
```assembly
0000000000400550 <mult2>:
400550: mov %rdi,%rax # %rax := a
400553: imul %rsi,%rax # %rax := a * b
400557: ret # Return
```
{% endraw %}

### ◆ Call to the entry of a function


- `call` Dest
  1. `return address` (call 명령어 다음 줄) stack 에 저장
    - stack 에 `0x400544` 저장
{% raw %}
```assembly
0000000000400536 <multstore>:
...
400544: call 0x400550 <mult2> # mult2(5,3)
```
{% endraw %}

  1. Dest 로 jump
    - `mult2` 로 이동
{% raw %}
```assembly
0000000000400536 <multstore>:
...
400544: call 0x400550 <mult2> # mult2(5,3)
400549: mov %rax,(%rbx) # Update *dest ; *dest = t
; mul2 가 계산 한 값 (%rax) 를 %rbx 가 가리키는 메모리에 저장
```
{% endraw %}

### ◆ Return to the call-site


- `ret` 
  1. stack 에서 값 pop
  1. pop 된 값 (`return address`) 로 jump
= `pop %rip` 와 동일

## ✦ Passing data


- 함수들 사이에 data 어떻게 전송 → promise 
  - argument 6개 (인자)
    - %rdi
    - %rsi
    - %rdx
    - %rcx
    - %r8
    - %r9
  - return value (반환값)
    - %rax
- Saved
  - caller-saved
    - callee 가 자유롭게 사용할 수 있는 register
    - stack 에 따로 저장 X
    - %rdi, $rsi, %rdx, %rcx, %r8 ~ %r11
  - callee-saved
    - callee 가 복원해야 하는 register
    - 함수가 끝난 후에도 사용해야하는 register
    - %rbx, %r12 ~ %r14
  - caller 와 callee 는 상대적

### ◆ Function arguments


{% raw %}
```c
void multstore(long *dest) {
	long t = mult2(5L, 3L);
	*dest = t;
}
```
{% endraw %}

{% raw %}
```assembly
0000000000400536 <multstore>:
400536: push %rbx
400537: mov %rdi,%rbx
40053a: mov $0x3,%esi # Setup 2nd arg
40053f: mov $0x5,%edi # Setup 1st arg
400544: call 0x400550 <mult2> # mult2(5,3)
400549: mov %rax,(%rbx) # Update *dest
40054c: pop %rbx
40054d: ret
```
{% endraw %}

- function argument
  - %esi → `3` 저장 : 2nd argument
  - %edi → `5` 저장 : 1st argument
- `%rbx` 는 왜 push / pop 되는가?
  - 약속된 argument 값 아님 → 함수가 백업 & 복구해야 하는 값
  - `multstore` 가 callee 입장. `multstore` 시작 전 & 후 동일

### ◆ Return value


- `%rax` → caller-saved 
  - return value 전달 용도 약속
  - `call` 이전 값 보장 X, but return address 채워져 있다는 것은 보장
