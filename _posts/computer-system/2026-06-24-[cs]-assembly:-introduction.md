---
categories:
- Computer-System
date: '2026-06-24T10:47:00.000+09:00'
layout: single
series: 컴퓨터 시스템 개론
step: 2
tags:
- 어셈블리어
- x86-64
- CS
title: '[CS] Assembly: Introduction'
toc: true
toc_sticky: true
---

## ✦ Basic concepts of CPU, memory and Assembly


### ◆ Overview


- 우리는 왜 Assembly 를 배우는가?
  - CPU 가 이해할 수 있는 코드의 형태
  - 컴퓨터가 내부적으로 어떻게 동작하는지 알 수 있다.

### ◆ CPU 의 작동 방식


![](/assets/images/notion/[cs]-assembly:-introduction/img_1.png)

- Program Counter (PC) : 다음 실행할 명령어를 저장하는 register
- Instruction 과 data 는 모두 memory 에 저장된다
  - instruction 은 약속된 의미를 지닌 bit sequence


1. CPU 는 memory 로부터 명령어를 가져온다
  - 이때 가져온 명령어의 주소를 PC 에 저장한다
1. 저장된 명령어가 CPU 가 무엇을 해야할 지 알려준다
  - Machine instruction : CPU 가 무얼 해야할지 알려주는 0, 1 로 이루어진 명령어
ex) `0x48 0x01 0xd8`
  - Assembly insturction : Machine instruction 을 사람이 읽을 수 있도록 한 것
ex) `add $rax $rbx`
→ 내용 자체는 동일. 이해 주체의 차이

1. 실행 후, PC 가 자동적으로 다음 명령어를 가리킨다
→ CPU 는 1 ~ 3 을 반복하여 동작

### ◆ C Source → Machine code


![](/assets/images/notion/[cs]-assembly:-introduction/img_2.png)

- 최종 output 인 `p.bin` → executable file (binary)
- Compile
  - 좁은 의미 : `.c` → `.s` 변환 과정
  - 넓은 의미 : `.c` → `.s` → `.o` → `.bin` 변환 전체 과정

## ✦ Introduction of x86-64 architecture


### ◆ Architecture 의 정의


- Instruction Set Architecture (ISA) → 이번 수업에서의 내용
  - CPU 가 따라야하는 명령어의 집합 
  - 어떤 명령어가 가능한가? 어떤 register 이름이 있는가?
  - high level & abstract level 
- Microarchitecture
  - ISA 가 hardware level 에서 구현 & 최적화 되어 있는 방법 
  - low level / hardware level

### ◆ Intel x86


- CPU 의 계열
- Intel 에서 만든 CPU 가 공통적으로 사용하는 ISA
![](/assets/images/notion/[cs]-assembly:-introduction/img_3.png)

→ 이 수업에선 `x86-64` 사용 (일종의 language)

- Intel x86 의 역사
![](/assets/images/notion/[cs]-assembly:-introduction/img_4.png)

![](/assets/images/notion/[cs]-assembly:-introduction/img_5.png)

### ◆ Abstraction 의 level


- C language model : 가장 높은 단계의 추상화
  - C 프로그래머가 알아야 할 언어
{% raw %}
```c
int main() {
	int i, n;
	for (i = 1; i <= n; ++i) {
		...
	}
}
```
{% endraw %}

- ISA : 중간 단계의 추상화
  - compiler 개발자가 알아야할 언어
- microarchitecture : 가장 낮은 단계의 추상화
  - Hardware-level 의 최적화

### ◆ Registers in x86-64


![](/assets/images/notion/[cs]-assembly:-introduction/img_6.png)

- `%rip` : instruction pointer (program counter, PC)
- `%rsp` : stack pointer
![](/assets/images/notion/[cs]-assembly:-introduction/img_7.png)

- register 의 부분 이름
  - 끝 4 byte → `%e__`
  - 끝 2 byte → 앞에 r 빼고 `%__`
    - 앞 1 byte → 앞에 r 빼고 `%_h`
    - 뒤 1 byte → 앞에 r 빼고 `%_l`
→ 호환성 위해 register 이름 남겨줌

### ◆ x86-64 Assembly 모습


- C code
{% raw %}
```c
int sum(long x, long y, long *dst) {
	*dst = x + y;
	return 1;
}
```
{% endraw %}

- Assembly code
{% raw %}
```assembly
sum:
	add   %rsi, %rdi
	mov   %rdi, (%rdx)
	mov   $0x1, %eax
	ret
```
{% endraw %}

- Convention
  - 함수의 인수
    - 첫 번째 → `%rdi`
    - 두 번째 → `%rsi`
    - 세 번째 → `%rdx`
  - 함수의 결과 값 → `%rax` 

## ✦ Various x86-64 assembly instructions


### ◆ Data Move Instruction : `mov`


- 형태 : `mov Source, Destination`
  - source → destination 으로 데이터 복사
  - 접두사 (Suffix) 로 이동 data 양 결정 가능
    - `b` = 1 byte
    - `w` = 2 byte
    - `l` = 4 byte
    - `q` = 8 byte
→ 명확할 때에는 (ex. `mov rax rdi` ) 접두사 생략 가능
  - source & destination 에는 다양한 operand type 이 올 수 있다
    - register
    - immediate : 접두사 `$` 사용
    - memory : 특정 주소의 내용 (접두사 X)
      - ex) `mov 0x1000, %rbx` : `0x1000` 에 위치한 메모리 주소 load
      - ex) `mov (%rax), %rbx` : `%rax` 가 point 하고 있는 주소 load 
![](/assets/images/notion/[cs]-assembly:-introduction/img_8.png)

-  destination 이 Imm 불가능 / Mem →  Mem 불가능
- register 에 부분적으로 접근 가능 
![](/assets/images/notion/[cs]-assembly:-introduction/img_9.png)

> 💡 `%eax` 는 위쪽 4 byte 를 0으로 바꿈

### ◆ Byte Extension : `movz` / `movs`


- 접미사로 extend 할 byte 표시 가능
- `movz` : zero extension
  - ex) `movzbw` : zero extension (byte 1→ word 2) 
- `movs` : sign extension
  - ex)** **`movslq` : sign extension (long 4 → quad 8)

### ◆ Memory Access


![](/assets/images/notion/[cs]-assembly:-introduction/img_10.png)

- `movl $0x4142, (%rax)`
  - `(%rax)` 메모리 주소에서 4 byte 만큼 상수 `0x41`, `0x42` 가리키도록 (little endian)
  - 이때 접미사 `l` 생략 불가 → 4 byte 만 update 명시적 알림 
  - 다른 suffix 도 사용 가능
- `mov 0x20(%rbx, %rcx, 4), %rax`
`%rax` = `0x20` + `%rbx` + `(%rcx * 4)`

  - 이때 `4` 는 scale factor (1, 2, 4, 8 가능)
  - array access 할 때 유용
  - 요소 생략 가능
![](/assets/images/notion/[cs]-assembly:-introduction/img_11.png)

### ◆ Arithmetic Instruction


![](/assets/images/notion/[cs]-assembly:-introduction/img_12.png)

- signed, unsigned 차이 X
- 여러 operand 사용 가능
  - ex) `addq $1, (%rax)`
- `%e__` 가 destination 으로 사용 → 앞쪽 4 byte 는 0으로 초기화 (`mov` 처럼)
- CPU 에선 그냥 bit level manipulation

### ◆ Logical Instructions


![](/assets/images/notion/[cs]-assembly:-introduction/img_13.png)

- `shl %rax` → source 생략, 1만큼 left shift

### ◆ `lea` Instruction


- `mov` 랑 형태 비슷, 행동 다름
- `lea 0x20(%rbx, %rcx, 4), %rax` 
  - `%rax` = `0x20` + `%rbx` + `(%rcx * 4)` 
  - `%rbx` = 0x3000, `%rcx` = 0x100 이면 `%rax` = 0x3420
- pointer 계산을 위한 instruction
  - 그러나 더 빠르기에 정수 산술 연산에서 사용되기도 함
![](/assets/images/notion/[cs]-assembly:-introduction/img_14.png)

- `mov` 와 파이점
  - `mov` : 주소 계산 & 메모리 접근
  - `lea` : 주소 계산만, 메모리 접근 X → 속도 빠름
→ arithmetic 명령어에 가까움
