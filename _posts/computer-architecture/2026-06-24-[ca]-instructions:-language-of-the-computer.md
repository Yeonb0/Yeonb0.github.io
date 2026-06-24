---
categories:
- Computer-Architecture
date: '2026-06-24T10:55:00.000+09:00'
layout: single
series: 컴퓨터 아키텍쳐
step: 2
tags:
- 어셈블리어
- MIPS
- CA
title: '[CA] Instructions: Language of the Computer'
toc: true
toc_sticky: true
---

## ✦ Instruction Set


- 컴퓨터가 사용 가능한 명령어 집합
- 컴퓨터마다 instruction set 다름
  - but 공통 부분도 많음
- 초기 컴퓨터 → 간단한 instruction set
- 현대 컴퓨터도 간단한 instruction set 가짐
  - CISC CPU (Intel, Apple) : 복잡한 명령어
  - RISC CPU : 간단한 명령어

### ◆ MIPS Instruction Set


- instruction set 중 하나
- embedded 에서 사용
- 매우 간단 (ARM 과 유사하지만 더 간단)

## ✦ Operands


- Operands : 피연산자

### ◆ Register Operands


- MIPS : 32 bit 짜리 register 가 32개 → register file
- register : $0 ~ $31
  - $t0 ~ $t7 ($8 ~ $15), $t8 ($24), $t9 ($25) → temporary 값 저장
  - $s0 ~ $s7 ($16 ~ $23) → saved 값 저장
> 🗣 

- CISC : 명령어 복잡 → Intel
  - 명령어에 memory operand 가능
- RISC : 명령어 단순 → MIPS
  - 명령어에 memory operand 불가능 (오래 걸림)
> Design Principle 2 : Smaller is faster

- Example : Read (register) Write (register)
  - C
{% raw %}
```c
f = (g + h) - (i + j);
```
{% endraw %}

  - MIPS code
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_1.png)

- register 구조

| register | 역할 | register | 역할 |
| $0 | $zero (0) | $16 | $s0 (saved) |
| $1 | $at (Assembler Temporary) | $17 | $s1 |
| $2 | $v0 (result value) | $18 | $s2 |
| $3 | $v1 | $19 | $s3 |
| $4 | $a0 (arguments) | $20 | $s4 |
| $5 | $a1 | $21 | $s5 |
| $6 | $a2 | $22 | $s6 |
| $7 | $a3 | $23 | $s7 |
| $8 | $t0 (temporaries) | $24 | $t8 (temporaries) |
| $9 | $t1 | $25 | $t9 |
| $10 | $t2 | $26 | $k0 (kernel Reserved) |
| $11 | $t3 | $27 | $k1 |
| $12 | $t4 | $28 | $gp (global pointer) |
| $13 | $t5 | $29 | $sp (stack pointer) |
| $14 | $t6 | $30 | $fp (frame pointer) |
| $15 | $t7 | $31 | $ra (return address) |

  - arguments → 인자 저장
  - result value → 결과 값 저장
  - temporaries → callee 에 의해 overwrite 가능
  - saved → callee 가 저장해놓고 복구해야할 값
  - global pointer → static data 위한 pointer
  - stack pointer → stack 범위 지정 위한 pointer
  - frame pointer → frame 위치 나타내는 pointer
  - return address → procedure 가 돌아가야하는 address 저장하는 공간

### ◆ Memory Operands


- data 연산 위한 memory 접근
- load : register 가 계산하기 위해 memory 의 데이터 가져오기
- store : 계산 끝난 후 register 에 memory 에 저장하기
{% raw %}
```assembly
lw $t0, 32($s3) ; s3 (base register) 에서 32bit 떨어진 값을 t0 에 load
```
{% endraw %}

- word 
  - 컴퓨터가 한 번에 처리하는 bit 의 양
  - memory 에 접근하기 위한 data 의 단위
  - 꼭 word 단위가 아니라 byte 단위로 접근 가능 (32 bit : 1 word → 4 byte)
- byte = 8 bit
- Endian : MSB (부호 결정 bit) 의 위치에 따라
  - Big Endian : MSB 가 앞에 등장 → MIPS
    - 사람이 읽기 쉬움
  - Small Endian : MSB 가 뒤에 등장 → Intel
    - CPU 가 연산하기 쉬움
- Example : Read (memory, register) Write (register)
  - C
{% raw %}
```c
g = h + A[8];
```
{% endraw %}

  - MIPS code
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_2.png)

  - 4 byte 짜리 8개 → 4 × 8 = 32 → offset
- Example : Read (memory, register) Write (memory)
  - C
{% raw %}
```c
A[12] = h + A[8];
```
{% endraw %}

  - MIPS code
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_3.png)

  - 4 byte 짜리 8개 → 4 × 8 = 32 → offset
- Local Data on the Stack
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_4.png)

### ◆ Immediate Operands


- 상수 (constant) 가 필요할 때가 있음
  - memory 에 constant 저장할 때
  - constant 를 명령어에 불러올 때
> Design Principle 3 : Make the common case fast

- substract 명령어 존재 X 
  - `addi $s2, $s1, -1` : 음수를 더하는 거로 대체


1. Constant Zero
  - 항상 0 으로 설정되어 있는 값
  - `$zero`
  - overwrite 불가능
  - register 옮길 때 사용
    - `add $s2, $s1, $zero`
1. Unsigned Binary Integers
  - 범위 : 0 \sim 2^n - 1
  - 32 bit 사용
1. 2’s Complement Signed Integers
  - bit 31 은 부호 (sign) bit
    - 1 : 음수
    - 0 : 양수 (& 0)
  - -(-2^{n-1}) 표현 불가 → negation 해도 자기 자신 나옴
  - 특정 숫자
    - 0 : 0000 0000 …. 0000
    - 1 : 1111 1111 …. 1111
    - 최대 : 0111 1111 …. 1111
    - 최소 : 1000 0000 …. 0000
- 32-bit Constant
  - 대부분의 상수는 작기에 16 bit 만으로 충분하다
  - 가끔 32 bit 상수를 써야할 때
`lui rt, constant` : rt 의 왼쪽 16 bit 를 constant 값으로 채움. 오른쪽 16 bit 는 0 으로 채움

![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_5.png)

## ✦ Operation


- Operation : 연산자

### ◆ Arithmetic Operation


- add (더하기), subtract (빼기) → operand 3개
  - 2 sources & 1 destination
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_6.png)

- 모든 산술 연산자는 같은 형태를 가짐 
> Design Principle 1 : Simplicity favours regularity

- Example
  - C
{% raw %}
```c
f = (g + h) - (i + j);
```
{% endraw %}

  - MIPS code
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_7.png)

### ◆ Signed Negation


- bit flip (complement) 후 + 1
- ex) 
  - 2 : 0000 0000 …. 0010
  - -2 : 1111 1111 …. 1110

### ◆ Sign Extension


- 같은 숫자를 값 보존 + 더 많은 bit 써서 표현하기
- MSB 를 왼쪽에 붙임 (arithmetic)
  - cf) unsigned 면 0 붙임 (logical)
- MIPS instruction set
  - `addi` : immediate 값 extend
  - `lb`, `lh` : load 된 byte / halfword 를 extend
    - load byte : load 자체는 1 byte → 나머지 byte 는 extend
    - load halfword : load 자체는 2 byte → 나머지는 extend
→ 결과적으로 4 byte 로 extend

  - `beq`, `bne` : displacement 를 extend
    - displacement : 분기 명령어 (branch instruction) 의 목적지 주소를 인코딩 하는 값
    - `beq $1, $2, 100`

### ◆ Logical Operations


![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_8.png)

1. Shift Operations 
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_9.png)

  - shamt (shift amount) : shift 할 bit 수
    - 총 32 bit이므로 2^5 → 5 bit 할당
  - shift left logical - `sll`
    - ← 이동 & 0 으로 채우기 
    - 2배
  - shift right logical - `srl`
    - → 이동 & 0 으로 채우기 (logical)
    - \frac{1}{2}
1. AND Operation
  - bit 를 mask 할 때 : 둘 다 1 일 때만 선택
  - `and $t0, $t1, $t2`
1. OR Operation
  - bit 를 include 할 때 : 하나라도 1 이면 1
  - `or $t0, $t1, $t2`
1. NOT Operation
  - bit 를 invert 할 때 : 0 ↔ 1
  - `not` 명령어 존재 X → `nor` 로 표현
    - `nor $t0, $t1, $zero` 와 같이 표현
  - `a NOR b` == `NOT (a OR b)`

### ◆ Conditional Operation


- condition 이 참이면 label 된 명령어로 branch 하기
  - 거짓이면 계속 진행
- `beq rs, rt, L1` : rs = rt 면 L1 으로 가기
- `bne rs, rt, L1` : rs ≠ rt 면 L1 으로 가기
- `j L1` : 무조건 L1 가기
- Example
  - If Statement
    - C
{% raw %}
```c
if (i == j)
	f = g + h;
else 
	f = g - h;
```
{% endraw %}

    - MIPS code
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_10.png)

![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_11.png)

  - Loop Statements
    - C
{% raw %}
```c
while (save[i] == k) i += 1;
```
{% endraw %}

    - MIPS code
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_12.png)

![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_13.png)

### ◆ More Conditional Operations


- 조건이 참 → 결과 1 설정
- 조건이 거짓 → 결과 0 설정
- slt (Set on Less Than)
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_14.png)

- `beq`, `bne` 와 함께 사용
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_15.png)

→ why `blt` , `bge` 가 존재하지 않을까?

Hardware 에서 비교의 구현은 `=`, `≠` 보다 느리다.
Common case 인 `beq`, `bne` , `slt` , `slti` 만 구현

- Signed 비교 : `slt` , `slti`
- Unsigned 비교 : `sltu` , `sltui` 
→ compiler 자체는 저장되어 있는 값이 signed 인지, unsigned 인지 character 인지 모름

![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_16.png)

### ◆ Byte / Halfword Operations


- bitwise 이용해 byte / halfword 구할 수 있지만, 편의 위한 operation
- MIPS 의 byte / halfword 단위 load / store
  - 문자열 처리

|  | byte | halfword |
| sign extend | `lb rt, offset(rs)` | `lh rt, offset(rs)` |
| zero extend | `lbu rt, offset(rs)` | `lhu rt, offset(rs)` |
| store | `sb rt, offset(rs)` | `sh rt, offset(rs)` |

### ◆ Sychronization Operation


- 2 processor 가 memory 공간 공유
  - P1 이 쓰고, P2 가 읽음
  - sychronize 해야 침범 X
- 단일 instruction 
- Load linked : `ll rt, offset(rs)`
- Store conditional : `sc rt, offset(rs)`
  - `ll` 이후 위치 변경 X → rt = 1 
  - `ll` 이후 위치 변경 O → rt = 0
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_17.png)

## ✦ Instruction Format


### ◆ Representing Instruction


- 명령어는 binary 형태로 인코딩 됨 → machine code
- MIPS 명령어
  - 32-bit 명령어로 저장
  - regularity
- Register number
  - $t0 ~ $t7 → $8 ~ $15
  - $s0 ~ $s7 → $16 ~ $23
  - $t8 = $24 / $t9 = $25

### ◆ Stored Program Computers


- instruction 은 data 처럼 binary 로 표현된다.
- instruction & data 모두 memory 에 저장된다
- Binary compatibility (바이너리 호환성) : 컴파일된 프로그램이 서로 다른 컴퓨터에서도 동작할 수 있게 해줌

### ◆ R-format Instruction


- register 간 연산
- 형태
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_18.png)

  - op : 명령어 코드 (opcode) 
  - rs : 첫 번째 source register number
  - rt : 두 번째 source register number
  - rd : destination register number
{% raw %}
```assembly
add $1(rd), $2(rs), $3(rt)
; $1 = $2 + $3
; rd = rs + rt
```
{% endraw %}

- Example
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_19.png)

  - 명령어 : binary → hexadecimal 형태로 바꿀 수 있음

### ◆ I-format Instruction


- memory or immediate 사용 연산
- 형태
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_20.png)

  - op : 명령어 코드 6 bit
  - rs : source register
  - rt : source or destination → instruction 따라
  - 나머지 16 bit
    - Constant (상수) : -2^{15} \sim 2^{15}-1
    - Address offset : rs (base address) 에 더할 offset
> Design Principle 4 : Good design demands good compromises

- Branch Addressing
  - **앞 or 뒤쪽** branch 로 이동
  - Target Address (TA) = PC + (offset × 4)

### ◆ J-Format Instruction


- Jump (`j` , `jal` ) 목표는 code 의 어느 곳이든 가능하다
- 형태
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_21.png)

  - op : 명령어 코드 6 bit
  - address : 명령어에 full address 인코딩
- 너무 branch 가 멀어 16-bit offset 으로 불가능 → assembler 가 code 다시 씀
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_22.png)

### ◆ Basic Blocks


- 아래 조건 만족하는 명령어의 연속
  - 끝을 제외하곤 branch X
  - 처음을 제외하곤 branch 목적지 X
  - 한 번 들어오면 끝까지 실행
→ compiler 최적화 기준

## ✦ Procedure


### ◆ Procedure Calling Steps


1. Register 에 함수에 넘길 parameter 저장 (`$a0` ~ `$a3`)
1. 함수로 점프 (`jal`)
1. 함수가 사용할 stack 공간 확보 (`$sp` 감소)
1. 함수 실행 
1. result 를 register 에 저장 (`$v0`, `$v1`)
1. 함수를 호출한 곳으로 복귀 (`jr $ra`)

### ◆ Procedure Call Instructions


- 함수 호출 : jump and link
`jal procedureLabel` 
→ Label 로 이동 + 이 다음줄 주소를 `$ra` 에 저장

- 함수 복귀 : jump register
`jr $ra`
→ 저장해놓은 `$ra` 로 돌아가기

### ◆ Leaf Procedures


- 다른 함수를 호출하지 않는 함수
- C code
{% raw %}
```c
int leaf_example (int g, h, i, j) { // g($a0), h($a1), i($a2), j($a3)
	int f; // f($s0) -> stack 에 저장
	f = (g + h) - (i - j);
	return f;
}
```
{% endraw %}

- MIPS code 
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_23.png)

### ◆ Non-Leaf Procedures


- 다른 함수를 호출하는 함수
- nested call 이 필요함 → stack 에 저장해야 할 것
  - return address 
  - 함수 호출 이후 사용해야 할 $a, $t
- call 이후 stack 에서 복구
- C code
{% raw %}
```c
int factorial (int n) { // n($a0)
	if (n < 1) return 1;
	else return n * factorial(n-1);
	// result($v0)
}
```
{% endraw %}

- MIPS code
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_24.png)

### ◆ String Copy


- C code
  - `null` 로 끝나는 string
{% raw %}
```c
void strcpy(char x[], char y[]) { // $a0 (x 주소), $a1 (y 주소)
	int i ; // $s0 (i)
	i = 0;
	while ((x[i] = y[i] != '\0')
		i += 1;
	}
}
```
{% endraw %}

- MIPS code
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_25.png)

### ◆ Target Addressing


![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_26.png)

$s3 ≠ $s5 일때 까지 $s3++

## ✦ Addressing Mode


![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_27.png)

## ✦ How Program Works?


![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_28.png)

### ◆ Assembler Pseudoinstructions


- 대부분의 assembler 명령어는 machine 명령어와 1 대 1 대응
- Pseudoinstructions : 프로그래머 편의를 위한 가상 명령어
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_29.png)

  - `$at` ($1) : assembler 가 임시로 사용하는 register

### ◆ Object Module 생성


- `foo.c` → `foo.o`
  - 소스코드 → 기계어로 번역
- 내용
  - Header : 모듈 내용 설명
  - Text segment : 번역된 명령어들
  - Static data segment : 프로그램 수명 동안 유지되는 데이터
  - Relocation info (R.I) : loaded program 의 절대 주소에 의존하는 내용 처리 정보
  - Symbol table (S.T) : global 정의 & 외부 참조
  - Debug info (D.I) : source code 와 연결 정보

### ◆ Object Module Linking


- 여러 Object Modue 연결 → executable 만듬
  1. Segment 합침
  1. label 주소 결정 
  1. 위치 의존적 참조 & 외부 참조 수정 
- Linking 종류
  - Static Linking 
    - 라이브러리 함수 미리 link / load
    - 처음엔 느린데 실제 작동 중엔 빠름
    - 단점 : 사용하지 않을 함수까지 load 
  - Dynamic Linking
    - 라이브러리 함수 실제 호출 시 link / load
    - 신 버전 라이브러리 사용 가능
    - Lazy Linkage
      - 처음부터 linking 하지 않고 실제로 호출되는 것만 linking
      - 첫 호출 → 모든 routine 호출 → overhead 높음
      - 그 다음부터는 간접 점프 → overhead X 
    - Immediate Linkage

### ◆ Loading Program


- 실행 파일 memory 에 올리기
  1. header 읽어 segment 크기 확인
  1. 가상 주소 공간 생성
  1. text(code) 와 초기화된 data 메모리에 복사
  1. stack 에 argument 설정
  1. register (`$sp`, `$fp`, `$gp`) 초기화
  1. 시작 루틴으로 jump
    - argument 를 `$a0`, .. 등에 복사
    - `main` 호출 
    - `main` 이 return 하면 `exit` 시스템 콜 시행

## ✦ Java Application


- CPU Time 10배 : Poor performance
- 어디서나 실행가능 : Portability
- Intermediate language
- Java/JIT compiled code 는 JVM interpreted 보다 빠르다

## ✦ Example


### ◆ Swap


{% raw %}
```c
void swap(int v[], int k) {
	int temp;
	temp = v[k];
	v[k] = v[k+1];
	v[k+1] = temp;
}
```
{% endraw %}

![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_30.png)

### ◆ Sort


- insertion sort
{% raw %}
```c
void sort(int v[], int n ) {
	int i, j;
	for (i = 0; i < n; i++) {
		for (j = i - 1;
				 j >= 0 && v[j] > v[j+1];
				 j--) {
			swap(v, j);
		}
	}
}
```
{% endraw %}

![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_31.png)

- 전체 과정
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_32.png)

### ◆ Clearing Array


- array[index]
{% raw %}
```c
clear1(int array[], int size) {
	int i;
	for (i = 0; i < size; i++) {
		array[i] = 0;
	}
}
```
{% endraw %}

![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_33.png)

- *array
{% raw %}
```c
clear2(int *array, int size) {
	int *p;
	for (p = &array[0]; p < &array[size]; p++) {
		*p = 0;
	}
}
```
{% endraw %}

![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_34.png)

→ pointer 가 더 안전하고 명확함

## ✦ Assembly Language


### ◆ MIPS


- typical of RISC ISAs

### ◆ ARM


- 가장 인기 있는 embedded core
- MIPS 와 유사한 ISA 
- MIPS 와 비교

|  | ARM | MIPS |
|:--|:--|:--|
| 발표 연도 | 1985 | 1985 |
| 명령어 크기 | 32비트 | 32비트 |
| 주소 공간 | 32비트 플랫 | 32비트 플랫 |
| 데이터 정렬 | 정렬됨 | 정렬됨 |
| 데이터 주소 지정 모드 | 9 | 3 |
| 레지스터 | 15 × 32비트 | 31 × 32비트 |
| 입출력 | 메모리 맵 | 메모리 맵 |

→ 기본으로 제공하는 register 수가 더 적음 

- flag register : Negatice, Zero, Carry, Overflow
  - 산술 / 논리 연산 수행 시 자동으로 설정
- 조건 분기 시 flag register 확인해 실행 
→ 분기 명령어 필요 X 효율적!
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_35.png)

- ARM v7 → v8 바뀌면서 MIPS 와 더 닮아짐

### ◆ Intel x86 ISA


- 기본적으로 8개의 register 사용 
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_36.png)

- Instruction `source` `destination` 
- Instruction code 길이가 다름
![](/assets/images/notion/[ca]-instructions:-language-of-the-computer/img_37.png)

## ✦ Pitfall (함정) & Fallacy (오류)


### ◆ Fallacies


- 강력한 명령어 → 더 높은 성능
  - 더 적은 명령어 필요
  - but 복잡한 명령어 → 구현 어려움
  - 단순한 명령어로 빠른 코드 만드는게 더 좋음!
- 고성능을 위해 Assembly 언어 차용
  - but 현대 compiler 는 현대 Processor 더 잘 다룸
  - code line ↑ → error ↑, 생산성 ↓
- Backward compaltibility 
  - Instruction Set 은 변하지 않음
  - but 실제로는 계속 추가
  - 그러나 예전에 만든 프로그램은 새로 만든 CPU 에서도 돌아감 

### ◆ Pitfall


- 순차적인 word 는 순차적 address 에 있지 않음
  - 1 이 아니라 4 씩 증가해야 함!
- Procedure 가 return 후 자동 변수에 대해 pointer 유지하는 것
  - ex) argument 통해 pointer 다시 전달
  - stack 이 pop 되면 pointer 는 무효가 됨
→ dangling pointer

## ✦ Conclusion


- Design Principles
  1. Simplicity favours regularity
  1. Smaller is faster
  1. Make the common case fast
  1. Good design demands good compromises
- Layers of software / hardware 
  - Compiler - Assembler - Hardware
- MIPS : typical of RISC ISAs

| 명령어 분류 | MIPS 예시 | SPEC2006 int | SPEC2006 FP |
|:--|:--|:--|:--|
| Arithmetic | add, sub, addi | 16% | 48% |
| Data transfer | lw, sw, lb, lbu, lh, lhu, sb, lui | 35% | 36% |
| Logical | and, or, nor, andi, ori, sll, srl | 12% | 4% |
| Conditional Branch | beq, bne, slt, slti, sltiu | 34% | 8% |
| Jump | j, jr, jal | 2% | 0% |
