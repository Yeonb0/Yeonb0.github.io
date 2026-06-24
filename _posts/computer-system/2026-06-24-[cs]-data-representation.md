---
categories:
- Computer-System
date: '2026-06-24T10:44:00.000+09:00'
layout: single
series: 컴퓨터 시스템 개론
step: 1
tags:
- CS
title: '[CS] Data Representation'
toc: true
toc_sticky: true
---

## ✦ 컴퓨터는 Bit 로 이루어진다


- 컴퓨터의 모든 것 (정보, 데이터, 실행 파일 등) 은 모두 bit 로 이루어져 있다
- bit : 0 or 1 의 값을 가지는 binary digit
→ 컴퓨터는 모든 것을 bit 의 sequence 로 저장한다

### ◆ 컴퓨터 내부 실행


- CPU : 데이터 process
  - memory 에 저장된 데이터 read 
  - Register : CPU 안에 있는 작은 저장 공간
    - 계산의 피연산자 제공
→ how? bit 형식으로 저장
- Memory : CPU 가 계산한 데이터 store

## ✦ 정보를 Bit 로 나타내기


### ◆ Number System


- r → radix / base / 기수 / 진법
<div class="equation-box">

$$
(a_{n-1} a_{n-2} \cdots a_1 a_0)_r
= a_{n-1} r^{\,n-1} + a_{n-2} r^{\,n-2} + \cdots + a_1 r + a_0
\\
\text{(where } 0 \le a_i < r \text{)}
$$

</div>

  - 10진수 : r = 10 → decimal
  - 2진수 : r = 2 → binary
  - 16진수 : r = 16 → hexadecimal (A 10, B 11, C 12, D 13, E14, F15)
![](/assets/images/notion/[cs]-data-representation/img_1.png)


| Hexadecimal | Decimal | Binary |
|:--|:--|:--|
| 0 | 0 | 0000 |
| 1 | 1 | 0001 |
| 2 | 2 | 0010 |
| 3 | 3 | 0011 |
| 4 | 4 | 0100 |
| 5 | 5 | 0101 |
| 6 | 6 | 0110 |
| 7 | 7 | 0111 |
| 8 | 8 | 1000 |
| 9 | 9 | 1001 |
| A | 10 | 1010 |
| B | 11 | 1011 |
| C | 12 | 1100 |
| D | 13 | 1101 |
| E | 14 | 1110 |
| F | 15 | 1111 |

### ◆ Byte


- 1 byte = 8 bit
  - CS 에서 사용하는 데이터 단위
  - 2진수 : 00000000 ~ 11111111
  - 10진수 : 0 ~ 255
  - 16진수 : 0 ~ FF
→ C 에서 `0x` 를 prefix 로 사용해 16진수 쓰기 가능
- 1 byte = 2진수 8 digit
            = 16진수 2 digit
- 2진수 ↔ 16진수 변환 : binary 4 bit 씩 묶어서 hexadecimal 로 표시
![](/assets/images/notion/[cs]-data-representation/img_2.png)

### ◆ Bit Opration


- Boolean Algebra
  - True = 1 / False = 0
  - And (&) → 둘 다 1일 때만 1

| & | 0 | 1 |
| 0 | 0 | 0 |
| 1 | 0 | 1 |

  - Or ( | ) → 하나라도 1이면 1

| | | 0 | 1 |
| 0 | 0 | 1 |
| 1 | 1 | 1 |

  - Not (~) → 0 ↔ 1 바꾸기

| ~ |  |
| 0 | 1 |
| 1 | 0 |

  - Xor (^) → A ≠ B 면 1

| ^ | 0 | 1 |
| 0 | 0 | 1 |
| 1 | 1 | 0 |

  - Commutative property (교환 법칙) 성립
ex) A & B = B & A 
  - Associative property (결합 법칙) 성립
ex) A & (B & C) = (A & B) & C

→ bit sequence (= bit vector) 에도 확장 가능

→ Boolean Algebra 가 중요한 이유
CPU 는 기본적으로 gate 로 구성. gate 는 Boolean operation 실행하는 회로 !

- C 에서의 Bit operation : `&`, `|`, `~`, `^` 
  - 다양한 데이터 타입에 적용 가능
  - 피연산자 → bit vector 처럼 보임
  - bit-wise 로 연산자 적용
![](/assets/images/notion/[cs]-data-representation/img_3.png)

- C 에서의 Logical operation : `&&`, `||`, `!` → Bit operation 과 유사
  - 0 → false / 0이 아닌 값 → true
  - Early termination : 조기 종료
    - `&&` 에서 앞이 false 면 바로 false
    - `||` 에서 앞이 true 면 바로 true
ex) `if(p && *p == 1)` 사용하면 NULL 포인터 사용 방지 가능

- Representing Set
  - Bit 로 Set 표현가능
  - 원소가 n 개 → bit n 개 사용해 on, off 표현
  - `&` : 교집합
  - `|` : 합집합
  - `~` : 여집합

## ✦ Integer Representation


### ◆ 음수 표현하기


- 양수 (unsigned int) 는 표현하기 쉬움
- 음수의 표현법 ?
  1. 첫 번째 bit를 부호 표현하는데 사용해보자
    - 0 → 양수 / 1 → 음수
    - 산술 연산 복잡 → 직관적이지만 사용 X
  1. Two’s Complement (2의 보수)
![](/assets/images/notion/[cs]-data-representation/img_4.png)

    - 첫 bit → 부호 표현 (Most Significant Bit, MSB)
    - 하드웨어에서 더 효율적 
![](/assets/images/notion/[cs]-data-representation/img_5.png)

### ◆ Unsigned vs. Signed


- Unsigned → 부호 X (표현 범위 좀 더 넓음)
  - Min = 0
  - Max = 2^w - 1
<div class="equation-box">

$$
\text{B2U}_w(x) = \sum^{w-1}_{i=0}x_i\cdot2^i
$$

</div>

- Signed → 부호 O
  - Min = -2^{w-1}
  - Max = 2^{w-1} - 1 
→ 음수 범위가 1 개 많음 (asymmetric)

<div class="equation-box">

$$
\text{B2S}_w(x) = x_{w-1} \cdot(-2^{w-1})+\sum^{w-2}_{i=0}x_i\cdot2^i
$$

</div>

![](/assets/images/notion/[cs]-data-representation/img_6.png)

- 0000 ~ 0111 table
- 1000 ~ 1111 table
→ |Unsigned| + |Signed| = 2^w 

### ◆ Mapping


- 같은 bit pattern → 두 개의 다른 수로 해석 가능
![](/assets/images/notion/[cs]-data-representation/img_7.png)

### ◆ C에서의 Type Conversion


- 똑같은 bit 인데 다시 해석
- Explicit type conversion : 프로그래머가 직접적으로 type 명시
{% raw %}
```c
int si = -10;
unsigned int ui = (unsigned int) si;
```
{% endraw %}

  - unsigned → bit → signed 변환
  - signed → bit → unsigned 변환
- Implicit conversion : 명시하지 않고 자동으로 C에서 해주는 형 변환 
  - 기본적으로 C에서 int 를 만들면 signed int. unsigned integer 만들기 위해선 접미사로 `U` 붙여야 한다.
  - signed + unsigned 연산 섞어서 하면 unsigned 로 자동 casting
ex) 


| C 표현식 | Evaluation | Result |
| `0 == 0U` | Unsigned | true |
| `-1 < 0` | Signed | ture |
| `-1 < 0U` | Unsigned | false |

→ 마지막 경우에서 -1 은 unsigned 로 바뀌면서 429496729U 로 자동 형변환.

## ✦ Integer Operations


- 지금까지는 register 에 ‘어떻게 저장하는가’ 를 배움
- 이제부터는 ‘어떻게 연산하는가’

### ◆ Unsigned Addition


- Unsigned 끼리 더하기 → bit sequence 형태로 실행
  - 두 binary number 더하기
  - CPU 회로에서 gate 통해 똑같은 방식으로 구현 
  - 단 carry output 은 버려짐.
→ modular sum : \text{UAdd}_w(u, v) = (u + v) \mod 2^w

![](/assets/images/notion/[cs]-data-representation/img_8.png)

→ w + 1 bit 는 버림. (overflow 로 실제 값과 다른 결과)

### ◆ Signed Addition


- Unsigned 방법과 똑같이 계산
  - 두 binary number 더하기
  - 2의 보수 방법으로 해석하기
  - 옳은 결과가 나온다. (마찬가지로 carry output 버림)
![](/assets/images/notion/[cs]-data-representation/img_9.png)

### ◆ Visualization of Addition


- 현실 세계의 u, v 더하기
  - under, overflow 없음.
  - linear 하게 증가
![](/assets/images/notion/[cs]-data-representation/img_10.png)

- Unsigned Addition
  - 2^w \sim 2^{w-1} 까지는 0 \sim 2^w 에 mapping 
  - overflow 발생 
![](/assets/images/notion/[cs]-data-representation/img_11.png)

- Signed Addition
  - overflow, underflow 발생 가능
    - overflow : 음수 + 음수 = 양수
    - underflow : 양수 + 양수 = 음수
![](/assets/images/notion/[cs]-data-representation/img_12.png)

![](/assets/images/notion/[cs]-data-representation/img_13.png)

  - Signed 의 최소 : 1000 0000 …. 0000
  - Signed 의 최대 : 0111 1111 …. 1111

### ◆ Negation in 2’s Complement


- -x 구하기 
  - bit-flip & +1
- why?
         ~x + x == 1111..1111 == -1
     1 + x + x == 0
(~x + 1) + x == 0
 ~x + 1         == -x

- 만약 SMin (-2^{w-1}) 를 Negation 하면? 
  - overflow 되어 똑같은 값이 나온다

### ◆ Subtraction


- 컴퓨터는 빼기를 양수 + 음수로 구현한다
  - x + BFI(y)
  - BFI = Bit-Flip and Increment
- x - y = x + (-y)
- Unsigned & Signed 연산 똑같음
  - 단, Unsigned 에선 underflow 가 발생할 수 있다

### ◆ Extension


1. Zero Extension
  - Unsigned integer x bit 를 (x+k) bit 로 extend 하기
  - 위쪽에 새로 추가된 k bit 를 0 으로 채우기
![](/assets/images/notion/[cs]-data-representation/img_14.png)

1. Sign Extension
  - Signed integer x bit 를 (x+k) bit 로 extend 하기
  - 위쪽에 새로 추가된 k bit 를 MSB 로 채우기
![](/assets/images/notion/[cs]-data-representation/img_15.png)

### ◆ Truncation


- Unsigned / Signed integer (x+k) bit 를 x bit 로 바꾸기
- 위쪽 k bit 를 버림
![](/assets/images/notion/[cs]-data-representation/img_16.png)

→ MSB도 그대로 삭제하므로 부호 보존 X

### ◆ Shifting


1. Left Shifting : `x << y`
  - x 를 y 만큼 왼쪽으로 옮김
  - 왼쪽에 튀어나오는 bit 는 버림, 오른쪽은 0 으로 채움
  - x \times 2^y 와 같음 → overflow 발생 가능
ex) `10100010 << 3` = `00010000`

1. Right Shifting : `x >> y`
  - x 를 y 만큼 오른쪽으로 옮김
  - 종류
    - Logical : 왼쪽을 0 으로 채움
    - Arithmetic : 왼쪽을 x 의 MSB 로 채움
  - 오른쪽에 튀어나오는 bit 는 버림
  - x \times \frac{1}{2^y} 와 같음
  - 대부분의 언어는 Unsigned 대해선 Logcal shift, Signed 대해선 Arithmetic shift 실행
  - Example
    - Logical shift : `10100011 >> 2` = `00101000`
    - Arithmetic shift : `10100011 >> 2` = `11101000`

## ✦ Data representation in memory


### ◆ Basic Structure of Memory


- High level → 아주 큰 byte 의 array
  - address 는 array 의 index
- 한 cell 에는 1 byte 저장 가능
  - 1 byte 가 넘는 data 는 여러 cell 걸쳐 저장
![](/assets/images/notion/[cs]-data-representation/img_17.png)

### ◆ Byte Ordering (Endian)


- Multi-byte data 를 표현하는 방법
  - Big Endian : MSB (Most Significant Byte) 를 앞쪽으로 (가장 낮은 주소로)
  - Little Endian : MSB (Most Significant Byte) 를 뒤쪽으로 (가장 높은 주소로)
    - x86 에서는 Little Endian 을 사용.
![](/assets/images/notion/[cs]-data-representation/img_18.png)

### ◆ Checking Byte Order


- byte 값을 나타내주는 함수
{% raw %}
```c
void show_bytes(unsigned char* start, size_t len) {
	size_t i;
	for (i = 0; i < len; i++) {
		printf("%p: 0x%.2x\n", start + i, start[i]);
	}
}
```
{% endraw %}

- integer 의 memory 에서의 representation
  - byte 의 sequence 출력
{% raw %}
```c
int a = 303030;
show_bytes((unsigned char*) &a, sizeof(int));
```
{% endraw %}

![](/assets/images/notion/[cs]-data-representation/img_19.png)

→ 결과 : 실행마다 다를 수 있음 (memory 저장 위치)

- pointer 의 memory 에서의 representation
  - CPU 의 관점에서 pointer 는 integer 와 다르지 않다.
  - pointer → 메모리 주소를 나타내는 integer
{% raw %}
```c
int *p = &a;
show_bytes((unsigned char*) &p, sizeof(int*));
```
{% endraw %}

![](/assets/images/notion/[cs]-data-representation/img_20.png)

- String 의 memory 에서의 representation
  - C 에서 String 은 char 의 array 의 표현
    - 각 char 는 ASCII (1 byte) 로 인코딩 되어 있음
    - `null` 로 끝나야 함
  - Big & Little endian system 모두 순서가 같음 → 읽는 순서로
{% raw %}
```c
char s[6] = "AB123";
show_bytes((unsigned char*) s, sizeof(s));
```
{% endraw %}

![](/assets/images/notion/[cs]-data-representation/img_21.png)

### ◆ Word (Word Size)


- CPU 가 가장 효율적으로 다룰 수 있는 data 단위
  - 요즘 대부분의 CPU 는 64 bit (8 byte) word size
- word size
  1. size of register (CPU)
    - 요즘 register 는 8 byte
    - CPU 와 memory 사이 주고 받을 수 있는 최대 데이터 크기
  1. size of memory address
    - pointer 변수의 size
    - ex) `sizeof(int*)` = 8
    - memory address 의 가능한 범위 결정 : 0 \sim 2^{64} -1
- C 의 Data Type 크기
![](/assets/images/notion/[cs]-data-representation/img_22.png)
