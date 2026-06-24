---
categories:
- Network
date: '2026-06-24T10:21:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 6
tags:
- 데이터 링크 계층
- 네트워크
title: '[Network] Medium Access Control'
toc: true
toc_sticky: true
---

## ✦ Multiple-access resolution


### ◆ Multiple access 란?


- 네트워크 구성 방법
  - point-to-point : 직접적으로 유선 연결
    - ex) bus, switch, hub
  - Shared Medium : Wi-Fi 같이 무선 매체로 공유
    - 한 번에 한 user 만 전송 가능
→ control 필요
- 목표 : 여러 명이 동시에 모여서 대화 혼잡 안 생기도록

### ◆ Multiple Access Protocols


![](/assets/images/notion/[network]-medium-access-control/img_1.png)

- Random access protocols : 랜덤하게 말하기
- Controlled-access protocols : 사회자가 순서 지정
- Channelization protocols : 채널 나눠 따로따로 이야기

### ◆ Vulnerable time


- 어떤 frame 이 취약한 시간
![](/assets/images/notion/[network]-medium-access-control/img_2.png)

- Pure ALOHA 
  - 2 \times T_{\text{fr}} : 그 frame + 그 frame 이전 frame → Time slot 2배
- Slotted ALOHA
  - T_{\text{fr}} : 보내는 중인 frame
- Example
![](/assets/images/notion/[network]-medium-access-control/img_3.png)

  - T_{\text{fr}} = \frac{200\ \text{bits}}{200\times 10^3\ \text{bps}} = 1ms
  - 2 × 1ms = 2ms 동안 다른 전송 없어야 함

### ◆ Throughput


- Time Slot 시간 동안 성공적으로 수신되는 frame 확률 (충돌 제외)
- Pure ALOHA
  - S = G \times e^{-2G}
    - S : 성공적 수신 frame 수
    - G : 한 T_{\text{fr}} 마다 평균 frame 생성 수
- if G = 1, S = 0.135 → 1 time slot 마다 평균 0.135 frame 전송
- Example
![](/assets/images/notion/[network]-medium-access-control/img_4.png)

  - T_{\text{fr}} = \frac{200\ \text{bits}}{200\times 10^3\ \text{bps}} = 1ms
  - 1초에 500 frame 생성 → G = 0.5
  - S = G × e^{-2G} = 0.184
  - 500 × 0.184 = 92 frame 만 성공적 전송
- 식 proof
  - poisson 분포
<div class="equation-box">

$$
P(k) = \frac{\lambda^k \times e^{-\lambda}}{k!}
$$

</div>

  - k = 0 대입, λ = 2G 대입
<div class="equation-box">

$$
P(0) = \frac{e^{-2G}}{0!} = e^{-2G}
$$

</div>

    - 따라서 S = G \times e^{-2G}
- G 를 얼마로 해야 최대 output?
  - Pure ALOHA : G = \frac{1}{2} (2 T_\text{fr} 마다 1개)
  - Slotted ALOHA : G = 1 (1 T_\text{fr} 마다 1개)

# ⭐Random Access Protocols


- 비효율적으로 보이지만 많이 사용
- 전송할 시간 random 설정
  - 동시 가능성 有 → 충돌 해결 방법?

## ✦ ALOHA


- Hawaii 대학에서 개발
- 보낼 것이 있으면, 보낸다
- 충돌이 나면, random 한 시간 기다렸다가 다시 보낸다.

### ◆ Pure ALOHA


- Sender 가 보낼 frame 이 있으면, 즉시 보낸다.
- Receiver 가 frame 을 받으면, ACK 를 보낸다.
- ACK 가 timeout period 동안 오지 않으면, sender 가 frame 을 재전송 한다
  - 이때 random delay 만큼 기다린다
- 만약 두 개 이상의 frame 이 같은 시간에 보내지면, collision 발생
![](/assets/images/notion/[network]-medium-access-control/img_5.png)

  - Collision (충돌) : 2명 이상의 sender 가 동시에 전송, receiver 가 아무것도 받지 못함
  - frame 전송 多 → 성공률 ↑
  - frame 전송 少 → 성공률 ↓
- Random Time 설정 방법
![](/assets/images/notion/[network]-medium-access-control/img_6.png)

  - 0 \sim 2^k-1 중 하나 뽑기 → R
  - T × R 초 기다리기 (T : time slot)
  - 충돌 발생 시 K++
→ binary exponential backoff (2^x 만큼 기다림)
  - K_{max} = 15 지정
    - 넘으면 포기 → 상위 layer 에 맡김
    - 이 정도면 ACK 전달 X 문제 → K 증가로 해결 불가
  - Time Slot T → 시스템 마다 다름
    1. Transmission Time (packet size, 갯수)
    1. Propagation Time (거리, 빛의 속도)
→ 둘 중 큰 쪽으로 time slot 설정

    - Example
      - Wi-Fi : 9\mu s
      - Ethernet : 512 bit times

### ◆ Slotted ALOHA


- 시간을 slot 으로 나눠서 관리
  - 가정 : slot 은 frame 들어가기 충분한 크기
![](/assets/images/notion/[network]-medium-access-control/img_7.png)

  - Slot 간의 시작 시간 맞추기 → time synchronization
- Vulnerable time = T_{\text{fr}} 
  -  Pure ALOHA = 2T_{\text{fr}} → \frac{1}{2} 배
  - 중간 시점에서 전송 시작하는 Frame X → 앞쪽 vulnerable time 없어짐
- Throughput : S = G \times e^{-G} 
  - Pure ALOHA = S = G \times e^{-2G} → -2G 에서 -G 로

## ✦ CSMA (Carrier Sense Multiple Access)


- ALOHA : 보내고 충돌 안나길 바람 → 효율 ↓ 
- Listen before you talk : 보내고자 하는 channel 에 누가 이미 보내는 중인지 sense
  - hardware 에 Carrier Sense Capability 필요
- 상태 
  - idle : 유휴 상태 → 전송 
  - busy : 이미 전송 받는 중 → 기다렸다 전송
- Vulnerable time : T_p (propagation delay)
![](/assets/images/notion/[network]-medium-access-control/img_8.png)

  - busy 신호가 도착하기 전 idle 상태인 줄 알고 frame 보내기

### ◆ 종류


- 기준 : Carrier Sensing 빈도
1. 1-persistent CSMA
  - 계속 carrier sensing
  - busy → idle 변한 시점에 전송 
  - 장점 : 바로 접근 가능, 노는 시간 없음
  - 단점 : Collision 가능성 ↑ 
1. non-persistent CSMA
  - 한 번 sensing 후 busy 면 일정 시간 wait 후 sensing
  - sense 했을 때 idle 로 바뀌면 전송
  - 장점 : Collision 가능성 낮음
  - 단점 : 다 같이 놀고 있을 수 있음 → 효율성 ↓
1. p-persistent CSMA
  - 계속 carrier sensing
  - idle 상태 sense 
    - p 확률로 전송
    - 1-p 확률로 좀 기다렸다 전송
  - 1 & 2 의 장단점 보완
![](/assets/images/notion/[network]-medium-access-control/img_9.png)

## ✦ CSMA/CD (Collision Detection)


- Ethernet 에서 주로 사용 
- frame 충돌 판단?
  - frame 크기를 키움 
  - 내 frame 전송 중 다른 frame 받음 → collision 판단
![](/assets/images/notion/[network]-medium-access-control/img_10.png)

- Frame 의 크기를 몇으로 설정해야 하는가?
  - 가장 먼 얘가 receive 하기 직전에 send 한 frame 이 도착할 때까지 (여전히 전송 중이어야 detect 가능)
  - T ≥ 2 \times T_p
    - 이걸 위해 Ethernet 에는 maximum 거리 존재
    - frame size → variable 하지만 최솟값 존재
- Example
![](/assets/images/notion/[network]-medium-access-control/img_11.png)

  - T_{fr} ≥ 왕복 시간 = 51.2 \mus
  - T_{fr} = \frac{\text{Frame Size}}{\text{Link Bandwidth}} 
  - Frame Size ≥ 512 bit, 64 byte
- If Collision detected
  - Jamming signal 전송 → collision 발생 알림 & transmission 중단
    - jammming signal : 48 bit 짜리 garbage data
  - binary exponential backoff (ALOHA 유사)
    - randon 시간 기다림
  - 재전송 시작

## ✦ CSMA/CA (Collision Avoidance)


- 무선 (Wi-Fi) 에서 주로 사용
- detect 불가능 → 회피 (avoid)
- 무선 → half duflex
  - 한 채널 사용 시 송신 / 수신 동시에 하나만 가능
  - 동시에 하면 서로가 간섭 (self interference)
  - CSMA/CD 처럼 collision detect 불가능
- ACK 이용 
  - frame 전송 → ACK 기다림 → 안오면 collision 판단
  - backoff binary exponentially

### ◆ IFS (inter-frame spacing)


- Carrier Sensing 하던 중 idle 을 확인했을 때 대기하는 시간
  - 다른 frame 이 전송했을 수도 있기에
  - 시스템마다 고정
- idle 상태 확인 할때 마다 초기화

### ◆ Contention Window


- IFS 이후 더 기다리는 시간
- random 시간 * frame 만큼 기다림
- countdown 해서 0이 되면 전송 시작
  - idle 상태일 때만 감소
  - busy 상태 되면 초기화 X, pause O
  - 다시 idle 상태되면 초기화된 IFS 기다린 후 countdown 이어감
- Binary exponential backoff
  - collision 발생 → contention window * 2배 (0 ~ 31 → 0 ~ 63)
→ 충돌 감소
- Example
![](/assets/images/notion/[network]-medium-access-control/img_12.png)

![](/assets/images/notion/[network]-medium-access-control/img_13.png)

  - Window
    - A : 5
    - B : 10
    - C : 15

### ◆ CSMA/CA with ACK


- 지금까진 ACK 를 보내지 않는다고 가정 → 실제론 ACK 사용
  - SIFS (Short IFS) : DIFS 보다 짧은 IFS, ACK 보내기 전에 사용
  - DIFS (Data IFS) : Data 보내기 전에 기다리는 IFS 
![](/assets/images/notion/[network]-medium-access-control/img_14.png)

# ⭐ Controlled Access


- Random 숫자에 의존 X 
- Rule 에 기반해 직동
- ex) 5G

### ◆ Reservation


- 시스템 마다 운영 방식 조금씩 차이
![](/assets/images/notion/[network]-medium-access-control/img_15.png)

- data 슬롯 이전에 reservation 슬롯 존재. 거기서 1 인 data station 에 reservation 시간 할당
- 아무도 보낼게 없으면 다시 reservation time 돌아옴
- 장점 : 서로 간 충돌 위험 X, 매번 5개 wait X (효율적)
- 단점 : 누군가 in/out 할 때 overhead 

### ◆ Polling


- Bluetooth 에서 사용
- Master & Slave 구성
  - Master
    - 보내고 싶을 때 보냄
    - SEL : 이제부터 전송한다고 알림
    - Poll : slave 가 보낼 것 있는지 check 
  - Slave : Poll 수신 이후
    - 보낼 게 있음 → data 전송
    - 보낼 게 없음 → NAK 전송
![](/assets/images/notion/[network]-medium-access-control/img_16.png)

### ◆ Token Passing


- Token 을 가지고 있는 주체만 말할 수 있음
- 단점
  - token error → token 날라가서 작동 X
  - ACK error → token 이 2개 생김
→ 복잡해서 이제는 역사의 뒤안길로..

# ⭐Channelization


- Frequency & Time 통해 통신 channel 을 여러 개로 나눔

### ◆ FDMA (Frequency-Division Multiple Access)


- frequency 기준으로 나눔
![](/assets/images/notion/[network]-medium-access-control/img_17.png)

- Guard band : 간섭을 막기 위한 영역 간 간격
- Example
![](/assets/images/notion/[network]-medium-access-control/img_18.png)

  - 인당 1MHz + 0.1MHz (guard band) → 총 18명 가능

### ◆ TDMA (Time-Division Multiple Access)


- 시간 단위로 나눔
![](/assets/images/notion/[network]-medium-access-control/img_19.png)

- Guard interval : 간섭을 막기 위한 영역 간 간격
- FDMA 보다 flexible. Synchronization 중요

### ◆ CDMA (Code-Division Multiple Access)


- 같은 시간에 같은 주파수에서 전송 → Code division 기술로 나누기
- Code Division
![](/assets/images/notion/[network]-medium-access-control/img_20.png)

  - 각 사람에게 Code 배정
    - Code → 자기 자신이랑 곱하면 4(인원 수), 다른 얘랑 곱하면 0 (like orthogonal)
![](/assets/images/notion/[network]-medium-access-control/img_21.png)

  - 데이터 전송
    - 0 → -1 
    - 1 → +1
    - 전송 X → 0
![](/assets/images/notion/[network]-medium-access-control/img_22.png)

  - Common Channel 에선 다 더한 값이 전송됨 → 이게 각 채널에 전파
  - 각 채널이 데이터 받으면 → 나 이외 다른 얘의 code 곱하고 4 로 나누기
![](/assets/images/notion/[network]-medium-access-control/img_23.png)

- 코드 만드는 방법 : Walsh table
![](/assets/images/notion/[network]-medium-access-control/img_24.png)

  - 2 × 2
\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} → code : (1, 1), (1, -1)

  - 4 × 4
![](/assets/images/notion/[network]-medium-access-control/img_25.png)

### ◆ OFDMA


- 요즘 사용 → time & frequency 둘 다 나눠서 배정
![](/assets/images/notion/[network]-medium-access-control/img_26.png)

  - 주파수를 orthogonal 하게 나눠 Guard band 없이 나눔
  - 시간축으로는 guard interval 존재
