---
categories:
- Computer-Architecture
date: '2026-06-24T10:56:00.000+09:00'
layout: single
series: 컴퓨터 아키텍쳐
step: 3
tags:
- CA
title: '[CA] Arithmetic for Computers'
toc: true
toc_sticky: true
---

## ✦ Integer Operations


### ◆ Integer Addition


- Range 를 벗어나면 Overflow 발생
  - `+` + `-`  → overflow 발생 X
  - `+` + `+` → overflow (underflow) 발생 가능 (MSB 가 1)
  - `-` + `-` → overflow 발생 가능 (MSB 가 0)

### ◆ Integer Subtraction


- 두 번째 operand 를 negation
- ex) 7 - 6 = 7 + (-6) 
- Range 를 벗어나면 Over flow 발생
  - `+` - `+` / `-` - `-` → overflow 발생 X
  - `+` - `-` → overflow (underflow) 발생 가능 (MSB 가 1)
  - `-` - `+` → overflow 발생 가능 (MSB 가 1)

### ◆ Overflow


- 일부 언어 (C) 는 overflow 무시
  - MIPS 의 `addu`, `addui`, `subu` 명령어 사용
- 다른 언어는 exception 발생 요구
  - MIPS 의 `add`, `addi`, `sub` 명령어 사용
→ flag bit set
  - overflow 시 exception handler 호출 

### ◆ Multiplication


![](/assets/images/notion/[ca]-arithmetic-for-computers/img_1.png)

![](/assets/images/notion/[ca]-arithmetic-for-computers/img_2.png)

![](/assets/images/notion/[ca]-arithmetic-for-computers/img_3.png)

- Optimized Multiplier
  - Multiplier → Product 하위 32 bit 로
  - Multiplicand 고정
![](/assets/images/notion/[ca]-arithmetic-for-computers/img_4.png)

![](/assets/images/notion/[ca]-arithmetic-for-computers/img_5.png)

- MIPS Multiplication
  - 특수 register
    - `HI` : 앞쪽 32 bit
    - `LO` : 뒤쪽 32 bit
  - Instruction
    - `mult rs, rt` / `multi rs, rt`
      - 64 bit 곱셈 
    - `mfhi rd` / `mflo rd`
      - HI / LO → `rd` 로 옮기기
      - 곱셈이 32 bit 넘는지 HI 값으로 체크 가능
        - **MIPS에서 곱셈 오버플로우 체크**
        - **왜 HI로 체크하냐?**
32-bit × 32-bit = 최대 **64-bit** 결과가 나옵니다.

근데 우리가 보통 결과를 32-bit 레지스터 하나에 담으려 하잖아요. 그러면 **상위 32-bit (HI) 에 의미 있는 값이 남아있으면 → 오버플로우**입니다.

{% raw %}
```text
64-bit 결과
┌──────────────┬──────────────┐
│      HI      │      LO      │
│  상위 32-bit │  하위 32-bit │
└──────────────┴──────────────┘
       ↑
  여기가 0이면 → 32-bit에 담을 수 있음 (no overflow)
  여기가 0이 아니면 → 오버플로우!
```
{% endraw %}

        - **체크 방법**
`mult` 실행 후 `mfhi` 로 HI 값을 꺼내서 직접 확인합니다.

{% raw %}
```assembly
mult $s0, $s1       ; 곱셈 실행
mfhi $t0            ; HI 값을 $t0에 복사
bne  $t0, $zero, overflow  ; HI != 0 이면 오버플로우
mflo $t1            ; 정상이면 LO에서 결과 가져옴`
```
{% endraw %}

        - **mult vs mul 차이**

| 명령어 | 동작 | 오버플로우 체크 |
|:--|:--|:--|
| `mult rs, rt` | 결과를 HI / LO에 저장 | 프로그래머가 직접 HI 확인 |
| `mul rd, rs, rt` | LO만 rd에 바로 저장 | **체크 안 함** |

    - `mul rd, rs, rt` 
      - rd = rs * rt (아래 32-bit 곱하기)

### ◆ Division


- 0 으로 나누는지 check
- divisor ≤ dividend : 나누기 가능
- divisor > dividend : 나누기 불가능 
![](/assets/images/notion/[ca]-arithmetic-for-computers/img_6.png)

![](/assets/images/notion/[ca]-arithmetic-for-computers/img_7.png)

![](/assets/images/notion/[ca]-arithmetic-for-computers/img_8.png)

![](/assets/images/notion/[ca]-arithmetic-for-computers/img_9.png)

- Optimized Divider
  - Multiplier 와 유사
![](/assets/images/notion/[ca]-arithmetic-for-computers/img_10.png)

- MIPS Division
  - 특수 register
    - `HI` : 앞쪽 32 bit
    - `LO` : 뒤쪽 32 bit
  - Instruction
    - `div rs, rt` / `divu rs, rt`
      - 64 bit 나눗셈
→ overflow / 0으로 나누기 check X

    - `mfhi rd` / `mflo rd`
      - result 접근

## ✦ Floating Point


- 정수가 아닌 숫자 표현 (매우 큰 & 매우 작은 숫자)
  - Precision : 정밀도
  - Dynamic number : 동적 범위
- in Binary Number
\pm1.\text{xxxxxxx}_2 \times 2^{\text{yyyy}}

- C 
  - float (single) : 32-bit
  - double : 64-bit
![](/assets/images/notion/[ca]-arithmetic-for-computers/img_11.png)

- Precision Range
  - Exponent 000..000 / 111..111 은 예약 → 사용 불가
  - Single
    - 가장 작은 값
      - Exponent = 00000001 (1 - 127 = 126)
      - Fraction = 000…00 (1.0)
      - \pm1.0 \times 2^{-126} \approx \pm1.2 \times 10^{-38}
    - 가장 큰 값
      - Exponent = 11111110 (254 - 127 = 127)
      - Fraction = 111..11 (2.0)
      - \pm2.0 \times 2^{127} \approx \pm3.4 \times 10^{38}
  - Double
    - 가장 작은 값
      - Exponent = 00000000001 (1 - 1023 = -1022)
      - Fraction = 000..00 (1.0)
      - \pm1.0 \times 2^{-1022} \approx \pm2.2 \times 10^{-308}
    - 가장 큰 값
      - Exponent = 11111111110 (2046 - 1023 = 1023)
      - Fraction = 111..11 (2.0)
      - \pm2.0 \times 2^{1023} \approx \pm1.8 \times 10^{308}
- Relative Precision (상대 정밀도
  - fraction 의 모든 bit 가 precision 에 기여
  - Single → 소수점 6자리까지 신뢰 가능
  - Double → 소수점 16자리까지 신뢰 가능
- 예약된 Exponent?
  - Exponent = 00000000
    - 원래 fraction 에는 기본 1 + 0.XXXX 
    - 만약 Exponent 가 전부 0이면 hidden bit 가 0으로 변함
    - 더 작은 숫자 표현 가능
x = (-1)^S \times (0 + \text{Fraction}) \times 2^{-\text{Bias}+1}

    - 0 근처에서 정밀도를 잃지 않기 위해
    - 단점 : 0 표현이 2개 생김
x = (-1)^S \times (0 + 0) \times 2^{-\text{Bias}} = \pm 0.0

### ◆ FP Addition


- Decimal / Binary 동일
1. 큰 쪽으로 지수 맞춰주기 (in decimal/binary)
1. significand 끼리 더하기
1. 결과 normalize & over/underflow 검사
1. 필요 시 rounding & renormalize
- Example
![](/assets/images/notion/[ca]-arithmetic-for-computers/img_12.png)

- int adder 보다 복잡
  - 여러 clock cycle 필요 → pipelined 가능
![](/assets/images/notion/[ca]-arithmetic-for-computers/img_13.png)

### ◆ FP Multiplication


- Decimal / Binary 동일 
1. 지수끼리 더하기 (맞출 필요 X)
1. Significand 끼리 더하기
1. 결과 Normalize & over/underflow 검사
1. 필요 시 rounding & renormalize
1. 부호 결정
- Example
![](/assets/images/notion/[ca]-arithmetic-for-computers/img_14.png)

- FP adder 랑 비슷한 복잡도

### ◆ FP Instructions in MIPS


- FP Operations
  - addition. subtraction, multiplication, division, reciprocal, square-root
  - FP ↔ integer conversion
→ 보통 여러 cycle 걸림 (pipelining 가능)

- FP Hardware 는 CPU 와는 다른 coprocessor 도 동작
- FP register
  - $f0, $f1, …, $f31 → 32-bit single
  - double 은 $f0 & $f1 처럼 두 개 묶어서 사용
- FP 명령어들은 FP register 로만 작동 

### ◆ Accurate Arithmetic


- 추가적인 rounding control 용 bit
  - guard bit
  - round bit
  - sticky bit
- rounding mode 설정 
  - RTZ : 버림
  - RTPI : 올림
  - RTNI : 내림
  - RTNE : 반올림 

## ✦ Subword Parallellism


- 큰 bit 단위 1 번의 연산 보다 작은 bit 단위의 여러 번 연산이 나은 경우 有
- Example - 128-bit adder
  - 8-bit adder × 16
  - 16-bit adder × 8
  - 32-bit adder × 4
- Subword Parallellsim = Data-level parallelism (GPU 에서 사용)
- Single Instruction, Multiple Data (SIMD) : 동일 data type 의 여러 data 를 하나의 명령어로 
  - SISD : single instruction single data → Chapter 4
  - SIMD : single instruction multiple data → GPU, NPU
  - MISD : not popular → network processor
  - MIMD : multi-core processor

### ◆ Streaming SIMD Extension 2 (SSE2)


- 128-bit × 4 registers
  - multiple FP operands 로 사용 가능
    - 64-bit × 2 double precision
    - 32-bit × 4 double precision
  - 동시에 연산 진행
    - Single-Instriction Multiple-Data (SIMD)

## ✦ Pitfalls


### ◆ Right Shift and Division


- left shift → 2배 커짐 
- right shift → 2배 작아짐?
  - unsigned integer : true
  - signed integer : 어떤 shift 인지 따라 다름
    - Arithmetic : sign bit 복사 → true
    - Logical : sign bit 복사 X → false 

### ◆ Assiociativity (결합 법칙)


- FP 에 대한 associativity 는 성립 X 
- 항상 over/underflow check 필요
![](/assets/images/notion/[ca]-arithmetic-for-computers/img_15.png)
