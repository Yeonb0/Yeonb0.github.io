---
categories:
- Network
date: '2026-06-24T10:18:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 4
tags:
- 네트워크
- 데이터 링크 계층
title: '[Network] Error Detection and Correction'
toc: true
toc_sticky: true
---

## ✦ Errors


### ◆ Error


- 전송된 data 에서 bit 가 flip (0 ↔ 1) 되어 오는 것
- 한 block 에서 flip 된 bit 의 수가 error 의 심각성 결정’
- why?
  - attenuation, distortion, noise, interference 
→ amplitude, frequency, phase 변화

![](/assets/images/notion/[network]-error-detection-and-correction/img_1.png)

- n-bit error 
  - error 은 한 bit 단위 X
  - 한 block 안에 몇 개의 error 가 있냐?
  - ex)
    - 원본 : `01101100`
    - 수신 : `01``01``110``1`  → 3-bit error

### ◆ Error detection vs. correction


- Error detection
  - error 가 발생했다는 것을 앎
  - 어떻게 수정해야하는지 모름 → 오류 나면 버림 
- Error correction
  - error 가 발생했다는 것을 앎
  - error 수정까지 가능함 → 오류 나면 수정
![](/assets/images/notion/[network]-error-detection-and-correction/img_2.png)

→ Redundancy (추가 비트) 필요

## ✦ Block Coding


- ex) 4B / 5B
  - 예상한 16 pattern 이외의 bit 도착 → error detection
- 검증 기준
  - 속도 : redundancy
  - 오류 검출 (detection) 능력 
  - 오류 수정 (corretion) 능력
→ 모든 경우에 대해 가능

### ◆ Term


- dataword (k) : original message block
- codeword (n) : block-coded 된 message
  - n > k
- r (redundancy) = n - k

### ◆ Example


- Example 1
![](/assets/images/notion/[network]-error-detection-and-correction/img_3.png)

  - k = 2
  - n = 1
  - r = 1
→ 1-bit detection O, 2-bit detection X, correction X

- Example 2
![](/assets/images/notion/[network]-error-detection-and-correction/img_4.png)

  - k = 2
  - n = 5
  - r = 3
  - 성능?
    - overhead : 150%
    - 1 bit error → detection O, correction O
    - 2 bit error → detection O, correction X
    - 3 bit error → detection X, correction X
  - MHD = 3 → 2 bit error detection & 1 bit error correction

### ◆ Hamming distance


- 어떤 두 codeword 사이 다른 bit 의 수
  - d(000, 000) = 0
  - d(000, 011) = 2
  - d(0100, 0010) = 2
  - d(10101, 11110) = 3
- Minimum Hamming Distance (MHD) 
  - 어떤 codeword set 의 최소 distance 
  - (MHD - 1) 까지 error detection 가능
  - correction bit = n 이라고 할 때, MHD > 2n (최소 2n + 1)
![](/assets/images/notion/[network]-error-detection-and-correction/img_5.png)

## ✦ Linear Block Codes


### ◆ Linear Block Code


- codeword set 에서 임의의 두 codeword 꺼내서 XOR 하면 codeword set 에 존재
- Linear Block Code 에서 MHD 는 1의 갯수가 가장 적은 codeword (00..00 제외)

### ◆ Simple Parity Check Codes


- parity → error checking code
- k-bit → (k+1)-bit codeword 
  - 1-bit parity bit 추가
  - codeword 가 짝수개 (또는 홀수개) 의 1 가지도록 만들기
- 110101 + `[1 | 0]`  → 110101`0` 
  - 수신 error X → parity bit 빼고 올림
  - 수신 error O → 그 block 버림
- MHD = 2
  - 1-bit error (+ 홀수-bit error) 검출 가능 / 짝수-bit error 검출 불가
  - 가성비가 좋아서 많이 사용됨
- 장점
  - 2-bit error 가능성 낮음 → 대부분 error 커버 가능
  - dataword 길이 (k) 조정 가능 → 길게 하면 효율성 good
- ex) 
![](/assets/images/notion/[network]-error-detection-and-correction/img_6.png)

### ◆ 2-dimensional parity


![](/assets/images/notion/[network]-error-detection-and-correction/img_7.png)

- 28-bit → 7 × 4 bit + 7 + 4 + 1
  - 7 : Column parity
  - 4 : Row parity
![](/assets/images/notion/[network]-error-detection-and-correction/img_8.png)

- 성능
  - error detection → 1, 2, 3-bit 까지 가능
    - 4-bit error : 대부분 가능, but 발견 불가능 경우 有
![](/assets/images/notion/[network]-error-detection-and-correction/img_9.png)

→ 오류가 2개씩 같은 row, column 일 때

  - error correction → 1-bit 가능
- overhead ↑ , detect 능력 ↑ 

### ◆ Hamming Code


- 1-bit error correct 가능한 MHD = 3 인 codeword set 만들기
- d_{min} = 3
  - 2-bit error detect 가능
  - 1-bit error correct 가능
- Hamming (n, k) code 
  - k-bit dataword → n-bit codeword (k < n)
- Voting (Hamming (3, 1) code)

| dataword (k) | → | codeword (n) |
| 0 |  | 000 |
| 1 |  | 111 |

  - 1-bit error → 다수결 따라 1 많으면 111, 0 많으면 000
  - overhead : \frac{1}{3}
  - efficiency : 33%
- Hamming (7, 4) code
  - 4-bit → 7-bit

| C_1 | C_2 | D_3 | C_4 | D_5 | D_6 | D_7 |
| 001 | 010 | 011 | 100 | 101 | 110 | 111 |

  - 1 (`001`), 2 (`010`), 4 (`100`) → check bit
    - check bit 에 영향 주는 값 XOR (1 갯수 세기)
      - 1이 짝수개 → 0
      - 1이 홀수개 → 1
    - 1 (`001`) → 3 (`011`), 5 (`101`), 7 (`111`)
    - 2 (`010`) → 3 (`011`), 6 (`110`), 7 (`111`)
    - 4 (`100`) → 5 (`101`), 6 (`110`), 7 (`111`)
  - 3, 5, 6, 7 → data bit
  - 무엇에 영향을 주고 받는가? 
![](/assets/images/notion/[network]-error-detection-and-correction/img_10.png)

  - MHD = 3
→ 1-bit correction 가능
  - efficiency : \frac{4}{7} = 57.1 %
- Hamming (15, 11) code
  - 11-bit → 15-bit 
  - 원리 same 
    - 1 (`0001`), 2 (`0010`), 4 (`0100`), 8 (`1000`) → check bit
      - 영향 주는 값 1 갯수 세기
    - 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15 → data bit
- Hamming (n, k) code 일반화
  - codeword 수 = 2^k -1
  - dataword 수 = 2^k - 1 - k
  - efficiency = \frac{2^k-1-k}{2^k-1} 
  - Example
    - k = 3 → (7, 4)
    - k = 4 → (15, 11)
    - k = 5 → (31, 26)
  - k 높아질 수록 efficiency ↑, but 2-bit error 확룔 ↑
  - correction 은 항상 1-bit 만 가능
→ 더 많은 오류 발생 시 다른 방법 사용 (ex. CRC)
  - 7-bit 전송 case → 8개 
    - 최소 3개의 bit 필요
    - Hamming code 가 가장 효율적인 방법

## ✦ Checksum


### ◆ Checksum


- Parity check code 보다 좀 더 복잡한 error detection 방식
- IP (layer 3) / TCP, UDP (layer 4) 에서 사용
header 에 error 없는지 확인
- 방식
ex) 5개의 4-bit 숫자 보냄

![](/assets/images/notion/[network]-error-detection-and-correction/img_11.png)

→ 수신 측에서 받은값 다 더해서 0 나오면 no error

### ◆ Wrapped sum


- 위의 예시에서 36 을 bit 로 표현하면 `100100` → 4-bit 초과
- wrapped sum → 5-bit 초과를 4-bit 로 나타내기
![](/assets/images/notion/[network]-error-detection-and-correction/img_12.png)

- Error Detection : 수신 측에서 받은 값 다 더해서 wrapped sum & 1’s complement 
  - 0000 → no error
  - 그 이외 값 → error 

## ✦ Cyclic Redundancy Check (CRC)


### ◆ Modulo Arithmetic


- Modulo-N : 숫자 0 ~ N-1 까지 사용
  - N으로 나눈 나머지로 숫자 쓰기
  - ex) Modulo-5 : 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, …
- CRC → Modulo-2 사용
  - 덧셈과 뺄셈 연산이 같음 (XOR operation)
![](/assets/images/notion/[network]-error-detection-and-correction/img_13.png)

### ◆ Cyclic Redundancy Check


- Divisior = Generator : 보낼 data 에 붙일 숫자
- Dataword : 보낼 data
  - Dataword + `000` 를 Divisior 로 나눔
- Codeword 
- ex)
  - Dataword : 1001
  - Divisor (Generator) : 1011
![](/assets/images/notion/[network]-error-detection-and-correction/img_14.png)

- Error Detection : 수신자가 generator (divisior) 로 나눔
  - remainder 000 → no error
  - remainder 가 000 아님 → error

### ◆ Binary Polynomial


- CRC 다항식으로 표현하기
  - g(x) : generator
  - d(x) : dataword
  - r(x) : remainder
  - T(x) : 송신 codeword
  - T'(x) : 수신 codeword
    - T'(x) = T(x) + e(x)
  - e(x) : 오류
    - e(x) 가 0이 아닌데 나눠 떨어지는 경우
→ 오류 있는데 검출 안됨
![](/assets/images/notion/[network]-error-detection-and-correction/img_15.png)

### ◆ Performance of CRC


- x^0 있고, 최소 하나의 다른 항 존재
→ 모든 1-bit error 발견 가능
![](/assets/images/notion/[network]-error-detection-and-correction/img_16.png)

- burst error : error 시작 ~ 끝 길이 
  - ex) 5-bit burst error : 1 _ _ _ 1  
- g(x) 의 최고차항 : n
→ n-bit 이하 burst error 발견 가능
- if burst size = n + 1
  - 검출 안될 확률 : 1 - (\frac{1}{2})^{n-1}
  - 대부분은 검출 가능
  - ex) n = 6 이면 (n+1 = 7) \frac{31}{32} 확률로 검출 가능
- if burst size = n + 2  ↑
  - 나눠 떨어질 확률 \frac{1}{2^n}
  - 검출 안될 확률 :  1 - (\frac{1}{2})^{n}
  - ex) n = 6 이면 (n+2 = 8) \frac{63}{64} 확률로 검출 가능
8, 9, 10 넘어가도 다 똑같이 \frac{63}{64}
- 성능이 좋음 
![](/assets/images/notion/[network]-error-detection-and-correction/img_17.png)

  - Ethernet 에서 CRC-32 사용
    - why CRC-32 처럼 복잡한 값 사용?
      1. 상수항이 1 → single-bit error 검출 가능
      1. (x + 1) 을 인수로 가짐 → 홀수 개-bit error 검출 가능
      1. Primitive Polynomial → 2^{32}-1 이하인 double-bit error 검출 가능
        - Primitive Polynomial → 기약다항식. 더 이상 인수 분해 불가 다항식
