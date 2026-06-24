---
categories:
- Network
date: '2026-06-24T10:25:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 7
tags:
- 네트워크
- WiFi
- 데이터 링크 계층
- 물리 계층
title: '[Network] Case Study: Wi-Fi'
toc: true
toc_sticky: true
---

## ✦ Wi-Fi의 역사


### ◆ IEEE 802.11


- 국제 표준 → layer 1, 2 정의
- 약 5년 마다 세대 발전
  - 802.11 (1997)
  - 802.11a / 802.11b (1999)
  - 802.11g (2003)
  - 802.11n (2009)
  - 802.11ac (2014)
  - 802.11ax (Wi-Fi 6, 2019)
  - 802.11be (Wi-Fi 7, 2024)
- Main Stream 외의 other 기술 
  - 802.11ad → 60GHz 에서 통신
  - 802.11bb (Li-Fi) : 가시광선 통신. 빠르지만 직진
  - 802.11bf (WLAN Sensing) : Wi-Fi 통해서 움직임 감지

## ✦ Wireless Channel


- Wi-Fi 는 무선 Channel 사용
- TX (tranmit) 안테나 → RX (receive) 안테나 
  - 쏠 때 펴지기 때문에 파워 손실 ↑
![](/assets/images/notion/[network]-case-study:-wi-fi/img_1.png)

- 무선 전송 시 영향 미치는 요인들
  - Pathloss 
  - Fading
  - SNR
  - Receiver Sensitivity

### ◆ Pathloss


- 거리에 따라 감소하는 신호 양
- 잃어버리는 양 modeling (send power & receiver power 관계)
- Friis propagation model
<div class="equation-box">

$$
\frac{P_r}{P_t} = G_tG_R \left( \frac{\lambda}{4\pi R} \right)^2
$$

</div>

  - P : Power, 전력
  - G : 안테나 gain (기본적으로 1)
  - λ : 전파의 파장 (Wavelength)
  - R : sender - receiver 거리
- General log-distance Pathloss model (일반화)
<div class="equation-box">

$$
P_r \propto \frac{1}{R^n}
$$

</div>

  - 측정을 통해 n 결정
- 안테나에서 신호 증폭 가능

### ◆ SNR


- 신호 대 잡음 비율
- 수신 세기 이외의 noise
<div class="equation-box">

$$
\text{SNR} = \frac{P_\text{signal}}{P_\text{noise}}
$$

</div>

- SNR 높으면 (신호 good) → 높은 MCS level 사용 가능
  - ex) BPSK, 64-QAM

### ◆ Receiver Sensitivity


- 수신 감도
- 조용할 때 얼마 정도의 세기까지 받을 수 있음?
<div class="equation-box">

$$
\text{Sensitivity (dBm) = Noise Floor (dBm) + Required SNR (dB)}
$$

</div>

![](/assets/images/notion/[network]-case-study:-wi-fi/img_2.png)

### ◆ Fading


- Receive 할 때 영향 주는 요소
  1. Pathloss → 거리
  1. Fading
1. Slow (large-scale) fading
  - 내 신호가 아파트와 같은 큰 건물 or 동산에 가려짐 
→ 감쇠 발생
1. Fast (small-scale) fading
  - 신호가 반사되어 여러 경로로 옴
    - 속도 차이에 의해 위상 증폭 / 상쇄 가능
  - 작은 움직임에 의해 변화하는 신호
![](/assets/images/notion/[network]-case-study:-wi-fi/img_3.png)

## ✦ Physical Layer Aspects


- bit 로 signal 만들기
- receive 한 signal 에서 bit 복구

### ◆ Modulation


- Wi-Fi 한 Channel 당 20MHz 할당
- Example : 2.4 GHz
![](/assets/images/notion/[network]-case-study:-wi-fi/img_4.png)

  - Channel 1 → 2402 ~ 2422 MHz
  - Channel 6 → 2427 ~ 2447 MHz
  - 한 Channel 당 5 MHz 이동
    - 그러나 channel 2~5 는 channel 끼리 겹치거나 딱 붙는 곳 생김 → 간섭 발생
    - 1, 6, 11 사용
- Modulation → QAM 사용
  - Wi-Fi 5 → 256 QAM
  - Wi-Fi 6 → 1024 QAM
  - Wi-Fi 7 → 4096 QAM
  - 빠르지만 SNR 낮으면 error 발생 확률 ↑

### ◆ Coding


- Error Correcting Code (ECC)
  - 오류를 수정할 수 있는 코드
- Coding rate : 일반 코드 / 전체 코드 비율 (ECC를 얼마나 넣음?)
![](/assets/images/notion/[network]-case-study:-wi-fi/img_5.png)

  - Sender 가 32 개 중에 하나 선택해서 전송 (0 ~ 31)
    - SNR 높음 (송신 good) → 높은 index 선택
    - SNR 낮음 (송신 bad) → 낮은 index 선택
    - Rate Adaptation
  - Type : 몇 bit 수신
  - Coding rate : ECC 얼마나?
  - Spatial Streams : TX, RX 안테나 사용 갯수

### ◆ MIMO (Multiple Input Multiple Output)


- 여러 TX 안테나 → 여러 RX 안테나
- 안테나 사용 갯수에 따른 분류
![](/assets/images/notion/[network]-case-study:-wi-fi/img_6.png)

- MIMO 장점
  - Spatial multiplexing gain
    - TX 에서 서로 다른 데이터를 보냄
    - RX 가 서로 다른 데이터 보낸 TX 만큼 있으면 복원 가능
![](/assets/images/notion/[network]-case-study:-wi-fi/img_7.png)

    - 안테나 갯수가 적은 쪽 만큼 spatial stream 가능
  - Diversity gain
![](/assets/images/notion/[network]-case-study:-wi-fi/img_8.png)

    - RX 가 많으면 더 잘 수신 가능 
      - 수신 상태 양호 사용 / 합쳐서 사용
  - Array gain (beamforming)
![](/assets/images/notion/[network]-case-study:-wi-fi/img_9.png)

    - 안테나 전송 타이밍 & 세기 조절 → 한쪽으로만 세게 가도록 함

### ◆ OFDM


- Orthogonal Frequency Division Multiplexing 
- 화면을 격자처럼 나눔 
  - subcarrier : 세로로 나누기
  - symbol : 가로로 나누기. guard interval 필요
- 802.11n 
  - 20MHz
    - subcarrier : 56개 (각 312.5 KHz, 총 17.5MHz)
      - 52개 → 데이터 전송에 사용
      - 4개 → pilot 전송에 사용
        - pilot : 송수신자 간 이미 알고 있는 데이터 → 근처 주파수 영역 보정
    - symbol : 3.2 μs
      - long Gi : 0.8 μs → 안좋은 환경
      - short Gi : 0.4 μs → 좋은 환경
  - 40MHz
    - 주변 채널을 몰아서 사용 → 속도 ↑
    - subcarrier : 114개 (2배보다 조금 더 큼)
      - 108개 → 데이터 전송에 사용
      - 8개 → pilot 전송에 사용 
![](/assets/images/notion/[network]-case-study:-wi-fi/img_10.png)

  - 40MHz 가 20MHz 보다 2배보다 살짝 더 많이 보냄
  - long 이 interval 이 더 기므로 short 가 더 많이 보냄
- Example
![](/assets/images/notion/[network]-case-study:-wi-fi/img_11.png)

  - 64QAM → 각 칸마다 6 bit 전송
  - Coding = \frac{5}{6} → 6 bit 중 5 bit 만 실제 데이터
  - 40MHz → channel 이 108 개
  - Short Guard Interval → 전송 3.2 μs + interval 0.4 μs 
초당 277,777 번 전송
  - Data rate = 6 \times \frac{5}{6} \times 108 \times 277,777 = 150Mbps
  - 4 spatial multiplexing → 4배 
→ 최고 속도 600Mbps

### ◆ Wi-Fi 의 발전


![](/assets/images/notion/[network]-case-study:-wi-fi/img_12.png)

- 최대 채널 넓이 증가
- Modulation 증가 : 한 칸당 더 많은 bit 전송
- Sptial stream 증가 : 안테나 수 많아야 함
