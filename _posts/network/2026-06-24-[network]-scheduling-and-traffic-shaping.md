---
categories:
- Network
date: '2026-06-24T10:32:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 12
tags:
- 네트워크
- 네트워크 계층
- 라우터
title: '[Network] Scheduling and Traffic Shaping '
toc: true
toc_sticky: true
---

## ✦ Scheduling


- Router : 다음번 host 로 전송 
  - Routing : 다음 hop 정하기
  - Scheduling : 누구 먼저 보낼지 정하기

### ◆ FIFO Queue


![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_1.png)

- First-In First-Out : 한 줄로 쌓고 앞에서부터 보내기
- 특징
  - 가장 단순한 방법
  - flow (src → dst 흐름) 모름
  - congestion control (혼잡 제어) X
  - queue 가 full 이면 새로 도착한 packet drop (tail drop)
  - 공평 (우열 X)
  - bandwidth 고려 X
- 문제점 
  - 보내는 만큼 받음
    - selfish 할 수록 이득
    - attack 으로 악용 가능
  - 더 / 덜 중요한 거 판단 불가능

### ◆ Active Queue Management (AQM)


- FIFO + tail drop : 꽉 차는 순간 우르르 drop
- 대안 : AQM → 적극적으로 Queue 관리 ⇒ TCP 에게 거의 다 찼다는 hint 주기
  - 가득 찰 거 같으면 미리 조취
  - RED (Random Early Detection)
  - CoDel / FQ-CoDel
  - ECN 마킹 
  - **◆ RED (Random Early Detection)**
  - 특정 전송률 넘어가면 random 으로 packet drop
![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_2.png)

  - Minimum thrashold 까지 점점 drop 률 높임
  - Maximum thrashold 시 모든 packet drop
  - Avglen = (1 - w) Avglen + w × SampleLen
![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_3.png)

    - 오는 Packet (SampleLen) : 100 → 200 → 50 → 250 → 100
    - Avglen? (w = 0.1)
      - 1st) 100 
      - 2nd) (1 - 0.1) × 100 + 0.1 × 200 
= 90 + 20 = 110
      - 3nd) (1 - 0.1) × 110 + 0.1 × 50
= 99 + 5 = 104
→ 이런 식으로 smoothing

### ◆ Priority Queue


![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_4.png)

- priority 별로 queue 생성 
  - high / low
- 문제점 : 높은 priority 가 계속 오면 낮은 priority 는 starvation (기아 현상)

### ◆ Round Robin


![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_5.png)

- flow 별로 queue 생성
  - src - dst pair 마다 queue 만들기
- 순서대로 하나씩 전송 → 보내는 만큼 받기 X
  - **◆ Weighted Round Robin**
  - Round Robin + Priority 도입
  - 각 queue 마다 weight 설정
    - 각 차례마다 packet 갯수 다르게 보내기 (weight 3 → 3개 / weight 1 → 1개 전송)
- 문제점 
  - Packet 마다 size 다를 시 packet 작은 애들은 오래 기다려야 할 수도

### ◆ Fair Queueing


- Round Robin 에 packet size (S_i) 추가
- packet Size S_i
  - 초기값 : 0
  - packet 전송 시 그 크기 더하기
  - 여러 S 중 작은 값 가진 queue 에서 전송 → 더하기 
![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_6.png)

- Tie break rule 정하기 : A > B > C
- 문제점
  - S 가 낮은 얘들은 한동안 혼자 보냄
→ 해결 : use it or lose it

가장 낮은 얘는 보낼 때 자신 이외 젤 작은 S 로 바꾸기

S_1  150만 / S_2  151만 / S_3 2천

    - 원래 → S_1, S_2 보낸 후 계속 S_3  보내기
    - 적용 → S_3 보낼 때 150만으로 설정

| 구분 | S_3 값 | 결과 |
|:--|:--|:--|
| 적용 전 | 2천 ( 옛날 값 유지 ) | S_3 가 150만까지 혼자 독점 |
| 적용 후 | 150만 ( S_{min} 으로 끌어올림 ) | 처음부터 공평하게 경쟁 |

### ◆ Weighted Fair Queueing (WFQ)


- 가장 많이 사용하는 Scheduling 방법
- 각 flow 마다 weight 지님
  - packet 전송 시 weight 로 나눈 값만큼만 더하기
  - weight 가 높을 수록 더 자주 기회 얻음
- S_i = S_i + \frac{P}{w_i}
![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_7.png)

![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_8.png)

## ✦ Traffic Shaping


- bursty traffic : 여러 packet 들이 몰려들어오는 상황
- traffic shaping : bursty 한 상황이 regulated flow 되도록 하는 것
![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_9.png)

### ◆ Leaky Bucket


![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_10.png)

- 구멍 뚫린 양동이
- 들어오는 packet 은 일정하지 않음
- 나가는 packet 은 일정함

### ◆ Token Bucket


- Leaky → 어떠한 burst 도 허락하지 않음 
- Token → 완전 일정 X 완화 시키는 형태
- Packet 전송 시 token 소비
  - token 은 일정한 속도로 쌓임
  - token 에는 한계 존재 (일정 이상으로 쌓이지 않음)
- token 이 쌓여있을 시 한 번에 많은 packet 전송 가능!
![](/assets/images/notion/[network]-scheduling-and-traffic-shaping/img_11.png)

  - r = token 쌓이는 속도
  - 가정) 처음 bucket 에는 token 이 꽉 차있음
  - 풀이
    - 0 ~ 10ms : 사용 X
    - 10 ~ 30ms : 40 kbps - 15kbps = 25 * 20 = 500 bit 필요
    - 30 ~ 40ms : 50 kbps - 15kbps = 35 * 10 = 350 bit 필요
    - 40 ~ 60ms : 10 kbps - 15kbps = -5 * 20 = -100 bit 필요 (얻음)
    - 60 ~ 100ms : 20 kbps - 15kbps = 5 * 40 = 200 bit 필요
→ 총 950 bits 필요
