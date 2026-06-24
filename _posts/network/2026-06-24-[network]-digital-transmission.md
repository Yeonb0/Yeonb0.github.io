---
categories:
- Network
date: '2026-06-24T10:15:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 2
tags:
- 네트워크
- 전송
- 물리 계층
title: '[Network] Digital Transmission'
toc: true
toc_sticky: true
---

# ⭐Digital-to-Digital Conversion


## ✦ Digital-to-Digital Conversion


- binary data → digital data 로 변환

### ◆ Data Element & Signal Element


- Data Element : 보내야 할 데이터
- Signal Element : signal 을 끊어 읽는 단위
![](/assets/images/notion/[network]-digital-transmission/img_1.png)

- r = signal element 에 들어가는 data element 수
  - r = \frac{\text{data element}}{\text{signal element}}
![](/assets/images/notion/[network]-digital-transmission/img_2.png)

### ◆ Units of Data and Signal Transmission


- Data transmission rate
  - 초당 보내지는 data element 수
  - 단위 : bps
- Signal transmission rate
  - 초당 보내지는 signal element 수
  - 단위 : baud
→ r 값 알면 bps 로 변환 가능

### ◆ DC Component


- frequency 가 zero 인 component
- 움직임이 없음
- 문제점 : AC-coupled link 통과 불가
- 2 가지 결과
  - Baseline wandering 
  - Clock drift
1. Baseline wandering
  - 같은 bit 가 계속 지속되면 signal 이 0V 쪽으로 서서히 가게 된다
  - 0V 에 가까워 질수록 noise margin 높아짐
1. Clock drift
  - device 마다 clock speed 살짝씩 다르다
  - 그렇기에 Self Sychronization 통해서 clock을 맞춤
    - 그러나 bit 에 변화가 없으면 보정할 수 없다
    - NRZ-L 보다 NRZ-I 가 나음
      - NRZ-L : 0 or 1 계속되면 DC 생김
      - NRL-I : 0 계속되면 DC 생김, 1 반복되면 계속 변화 → DC 안생김
→ 우리는 이 문제들 해결 위해 최대한 변화가 있도록 만들어야 한다!

## ✦ Line Coding Schemes


### ◆ Unipolar Encoding


- polar : 극
- Unipolar : 한쪽 극만사용
- Unipolar NRZ (Non-Return-to-Zero)
  - bit 1 → high volt
  - bit 0 → zero volt 
![](/assets/images/notion/[network]-digital-transmission/img_3.png)

### ◆ Polar Encoding


- 양쪽 극 모두 사용 : +V, -V
- NRZ-L (Level) : volate level 따라 값 결정
  - bit 0 → +V
  - bit 1 → -V
![](/assets/images/notion/[network]-digital-transmission/img_4.png)

- NRZ-I (Inverted) : 신호 전이(transition) 유무로 데이터를 인코딩
  - bit 0 → 전이 없음
  - bit 1 → 전이 발생
![](/assets/images/notion/[network]-digital-transmission/img_5.png)

- Unipolar 보다 많이 사용
  - 평균이 0 에 가까워야 좋다.
  - 평균이 0 이 아니면 DC component 존재
- RZ (Return-to-Zero)
  - 각 bit 가 2 signal 사용 (1 bit : 2 baud)
![](/assets/images/notion/[network]-digital-transmission/img_6.png)

  - 장점 : 계속 변화 → Self synchronization
  - 단점
    - baud 가 2배
    - signal level 3개 (+V, 0V, -V) → noise margin 높아짐
    - baseline wandering 문제 여전히 존재
- Manchester encoding
  - signal element 2개 사용
    - 0 : 위 → 아래
    - 1 : 아래 → 위
  - differential Manchester : NRZ-I 와 비슷
    - 0 : 앞이랑 반대로
    - 1 : 앞이랑 똑같이
  - 장점 
    - level 2개 사용
    - DC component (X), baseline wandering (X), clock drift(X)
  - 단점
    - 한 bit 에 2 signal element 사용 (baud 가 두 배)

### ◆ Bipolar Encoding


- level 3개 사용 : +V, 0V, -V
- AMI (Alternate Mark Inversion)
  - 0 → 0V
  - 1 → +V, -V 번갈아서
→ 평균 맞추기 위함!

  - DC component (X), but 0 만 계속 등장하면 clock drift 발생 가능

### ◆ Multilevel Encoding


- mBnL : n개의 signal element 로 m 개의 data element 표현
  - L 은 signal level 수
    - B : Binary (2)
    - T : Ternary (3)
    - Q : Quaternary (4)
  - ex) 2B1Q / 8B6T
- 2B1Q
  - 2 bit 가 한 signal element 로 mapping
  - 4 signal levels (Q)
  - DSL 에서 사용
![](/assets/images/notion/[network]-digital-transmission/img_7.png)

  - 00 / 01 / 10 / 11 → 2 bit 씩 묶어서 표현
    - 0X → 앞이랑 부호 같음
    - 1X → 앞이랑 부호 반대
    - X0 → 1
    - X1 → 3
- 8B6T
  - 100BASE-4T 에서 사용
  - level 3개 6 signal element 로 8 bit 표현
    - 3^6 = 729 로 2^8 = 256 개 표현
    - 특정한 pattern 만 사용
  - `+`, `-` 균형이 맞는 pattern 만 사용
    1. `+` 와 `-` 갯수가 일치
    1. `+` 가 한 개 더 많음 → 이 다음 나오는 불균형 신호는 **invert** 해서 `-` 가 하나 더 많도록 해 상쇄한다.
![](/assets/images/notion/[network]-digital-transmission/img_8.png)

### ◆ MLT-3


- LAN 0 에서 사용
  - 다음 bit 가 0 → 앞이랑 똑같이
  - 다음 bit 가 1 → 
    - 현재 level 이 0 이 아님 → 0
    - 현재 level 이 0 임 → 바로 직전 `+`, `-` 의 반대
![](/assets/images/notion/[network]-digital-transmission/img_9.png)

- baseline wandering → 발생 가능성 낮지만 완전 없지는 않음.
- clock drift → 0이 연속적으로 나오면 level 고정

## ✦ Block Coding


- mB/nB coding
  - m bits 의 data (원래 input) → n bits 로 coding 해서 보냄
  - 더 “큰” bit 로 mapping
- 목표 : self-sychronization, error detection

### ◆ 4B/5B


- NRZ-I 는 좋은 transmission rate (r = 1) 보여줌, but self-synchronization 문제 있음
- 0 이 계속 나오면 문제 발생
→ 연속적인 0이 나오지 않도록 만들기

![](/assets/images/notion/[network]-digital-transmission/img_10.png)

- 4 bit → 5 bit 로 바꿔서 0이 연속으로 4개 이상 안 나오도록
  - 앞 둘 중 반드시 1 들어가기
  - 뒤 셋 중 반드시 1 들어가기
→ 조건에 모두 만족하는 pattern 만 선택

ex) 01001 (O)   00111 (X)

![](/assets/images/notion/[network]-digital-transmission/img_11.png)

  - 몇 개의 pattern 이 가능한가?
![](/assets/images/notion/[network]-digital-transmission/img_12.png)

    - 조건을 만족하지 않는 pattern 은 특수 sequence 로 사용 or 오류 검출에 사용

## ✦ Scrambling


- 목표 : 0 지속 막기 → bit 추가 사용 X
- AMI 를 변형해 사용

### ◆ B8ZS


- 북미 표쥰
- 00000000 → 000VB0VB
  - V (Violation) : 원래 AMI 에선 위 → 아래 → 위 순서여야 하지만, 그걸 위반하고 전 신호를 그대로 사용
  - B (Bipolar) : 원래 rule 대로 위 → 아래 → 위 순서 이동
![](/assets/images/notion/[network]-digital-transmission/img_13.png)

### ◆ HDB3


- 유럽 표준
- 직전 V 이후 1의 개수가 
  - 홀수 : 0000 → 000V
  - 짝수 : 0000 → B00V
![](/assets/images/notion/[network]-digital-transmission/img_14.png)

→ 한쪽 polar 로 치우치치 않도록

## ✦ Case Study : Ethernet Physical Layer


### ◆ Ethernet


- 유선 인터넷
- LAN (local, 강의실 정도), MAN (metropolitan, 마포구 정도), WAN (wide, 우리나라 정도)
→ 네트워크 커버 영역

- IEEE 802.3 → Ethernet 표준
cf) IEEE 802.11 → Wi-Fi 표준

### ◆ Ethernet Cable


- 여러 다양한 종류의 전선 있음
- Cat 높을 수록 max transmission speed ↑

### ◆ Ethernet Standards


- Major
  - 10BASE5 : 10Mbps, baseband transmission, max 500m
    - RG-8 thick cable 사용
  - 10BASE2 : 10Mbps, baseband transmission, max 200m
    - RG-8 thin cable 사용
  - 10BASE-T : 10Mbps, baseband transmission, twisted pair
    - max 길이 약 100m
  - 100BASE-TX : 100Mbps, 2 twisted pair → Fast Ethernet
  - 1000BASE-T : 1Gbps, 4 twisted pari, 5 level coding
  - 10GBASE-T : 10Gbps
- Coding Scheme
  - 10BASE-5, 10BASE-2, 10BASE-T → Manchester Encoding
  - 100BASE-TX → MLT-3 + 4B/5B
  - 1000BASE-T → 8B1Q4 & 4D-PAN5
  - 10GBASE-T → PAM-16 + DSQ128 + LDPC

# ⭐Analog-to-Digital Conversion


## ✦ Analog-to-Digital Conversion


- analog data : multimedia data (음성, 음악, 영화 등)
→ digital 로 어떻게 변환?

## ✦ Pulse Code Modulation (PCM)


![](/assets/images/notion/[network]-digital-transmission/img_15.png)

- analog data → digital data 변환 방법
1. Sampling 
연속적인 signal 을 0, 1 로 mapping → 주기적으로 점을 읽음
⇒ PAM signal

1. Quantizing
연속적인 점의 높이를 discrete 하게 만들기 (양자화)

1. Encoding
양자화한 data 를 digital 로 만들기

### ◆ Sampling


![](/assets/images/notion/[network]-digital-transmission/img_16.png)

- 주기적으로 진폭 읽기
  - Sampling period : 한번 sampling 을 하는 주기
  - Sampling rate : 1초에 sampling 하는 횟수
    - Sampling period × Sampling rate = 1
- Nyquist Theorem (Sampling theorem)
  - Sampling rate 는 signal frequency 의 최소 2배여야 한다
    - 더 많이하면 oversampling → 용량 ↑, 정확도 ↑
    - 더 적게하면 undersampling → signal 복구 불가
![](/assets/images/notion/[network]-digital-transmission/img_17.png)

c. Undersampling: f_s = \frac{3}{4}f

### ◆ Quantizing


- amplitude 값을 discrete level 로 바꾸기 → 양자화
  - 듬성듬성 → 용량 ↓, 오차 심함
  - 뺵빽하게 → 용량 ↑, 정확도 ↑
![](/assets/images/notion/[network]-digital-transmission/img_18.png)

- Example : 8개의 level 로 나누기
  - normalized PAM values → 원래 값을 5로 나눈 값
  - normalized quantized value → X.5 중간 값으로 바꾼 값
  - normalized error → quantized values - PAM values 차이값
  - quantization code → 각 level 번호
  - encoded word → 보내지는 신호
- Quantization Error : 실제 값과 quantizied value 의 차이
  - 최대 있을 수 있는 error
-\frac{D}{2} ≤ \text{error} ≤ \frac{D}{2}

  - 원본과의 차이
- \text{SNR}_{dB}
  - 높음 : 원본과 비슷
  - 낮음 : 노이즈가 많음
  - \text{SNR}_{dB} = 6.02n_b + 1.76_{dB} 
→ 유도식

![](/assets/images/notion/[network]-digital-transmission/img_19.png)

    - n_b = sample 당 bit 수
    - quantization error 만 이용해 고려 (noise 고려 X)

### ◆ Encoding


- quantizied 된 level 을 bit pattern 으로 바꾸기
- L 개 level 있으면 n_b = \log_2L
- 단위 : bit rate
  - bit rate = sampling rate × n_b

### ◆ PCM Decoder


![](/assets/images/notion/[network]-digital-transmission/img_20.png)
