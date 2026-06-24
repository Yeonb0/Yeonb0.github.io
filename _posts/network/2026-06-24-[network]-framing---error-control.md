---
categories:
- Network
date: '2026-06-24T10:20:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 5
tags:
- 데이터 링크 계층
- 네트워크
title: '[Network] Framing / Error Control'
toc: true
toc_sticky: true
---

## ✦ Framing


- 데이터 끊어보내기 → 도착 시에 합치기
- error 가능성 ↓, error detection ↑

### ◆ Fixed-size Framing


- 모든 frame 길이 똑같이
- delimiter (나눔자) 필요 X
- 단점
  - inefficiency : frame 보다 보낼 양 적어도 padding 채워 보내기
  - fragmentation : frame 보다 길면 잘라내 보내기

### ◆ Variable-size Framing


- 요즘 사용하는 framing 방법
- frame 나누는 delimiter 필요
  - 시작 / 끝에 flag (`01111110`)
![](/assets/images/notion/[network]-framing---error-control/img_1.png)

### ◆ Stuffing


- Bit Stuffing
  - flag 제외, 1이 연속으로 5개 나오면 `0` stuffed bit 넣기
  - 1111110 → 11111`0`10
- Byte Stuffing
  - byte 단위로 처리되는 시스템
  - PPP (Point-to-Point)
  - marker (flag) → `7E`
  - marker 제외 `7E` → `7D 5E`
  - 원래 data 에서 `7D` → `7D 5D`
→ 수신 측에서 원래대로 복원

### ◆ Ethernet Framing


- Frame 시작 : Preamble + SFD
  - Preamble (7 byte) : 10101010
  - SFD (1 byte) : 10101011
    - 이제부터 frame 시작!
- Frame 끝 : 별도 flag / delimeter X → 물리 계층에서 판단 
  - IFG (Inter-Frame Gap) : frame 과 frame 사이에 12 byte 의 idle 시간 

|  | Flag 방식 (HDLC / PPP) | Ethernet |
| 프레임 시작 | Flag (01111110) | Preamble (10101010) + SFD (10101011 |
| 프레임 끝 | Flag (01111110) | IFG (idle 감지) |
| Stuffing 필요 | Yes (bit / byte stuffing) | No |
| 길이 정보 | 불필요 (flag 로 구분) | 불필요 (IFG 로 감지) |
| Example | HDLC, PPP | Ethernet, Wi-Fi |

# ⭐Error Control


- Automatic Repeat reQuest (ARQ)
  - 피드백을 바탕으로 재전송
  - Types 
    - Stop-and-Wait
    - Go-back-N
    - Selective Repeat

## ✦ Stop-and-Wait


### ◆ ACK


- Acknowledgement (ACK) frame
- 성공적으로 받았다는 표시
- 확인했습니다!

### ◆ Timeout


- RTT (Round Trip Time) : messsage 보내고 다시 신호 받을 때까지 걸리는 시간
  - 일정하지 않음
- timeout period = RTT + margin (delay 고려)
- Sender 는 frame 보낸 후 timer 설정
  - 너무 길어도 짧아도 안됨.

### ◆ Normal Case


![](/assets/images/notion/[network]-framing---error-control/img_2.png)

### ◆ Error Case


Case 1 : Send 과정 오류 → Receiver 가 못 받음

  - 택배가 사라짐
![](/assets/images/notion/[network]-framing---error-control/img_3.png)

Case 2 : ACK 전송 오류 → Receiver 가 보낸 걸 Sender 가 못 받음

  - 확인했습니다! 문자가 전송 안됨
![](/assets/images/notion/[network]-framing---error-control/img_4.png)

Case 3 : 전송 오류 X, timeout 발생

  - 확인했습니다! 받기 전에 택배 또 보내버림
![](/assets/images/notion/[network]-framing---error-control/img_5.png)

### ◆ Sender


- frame 보낸 후 T 초 간 기다림 
  - T : timeout period
- T 초 동안 ACK 신호
  - 도착 → next frame 전송
  - 도착 X → timeout → 같은 frame 재전송
- 모든 Case 에서 똑같이 동작

### ◆ Receiver


- 전송 받은 frame 이 같은 frame? next frame?
- Case
  - Normal Case → new frame
  - Case 1 : Send 과정 오류 → new frame (받은 적 없음)
  - Case 2 : ACK 전송 오류 → 같은 frame
  - Case 3 : timeout 발생 → 같은 frame
- Recevier 는 기존 frame & new frame 어떻게 구분?
→ Sequence Number (일련 번호)

### ◆ Sequence Number


- 보낼 frame & ACK 에 sequence number 붙여서 보냄
![](/assets/images/notion/[network]-framing---error-control/img_6.png)

- ACK sequence number
  - next expexted frame → 이거 사용
![](/assets/images/notion/[network]-framing---error-control/img_7.png)

  - 방금 받은 frame
- 1 bit (0, 1) 사용 : 0 → 1 → 0 → 1 → .. 번갈아 사용
- Error case
  - Case 1) Frame Loss 발생 → receiver 는 문제 없음 
![](/assets/images/notion/[network]-framing---error-control/img_8.png)

  - Case 2) ACK lost 시 : frame 이 ACK sequence number 와 다르면 버림
![](/assets/images/notion/[network]-framing---error-control/img_9.png)

  - Case 3) ACK 가 timeout 이후에 도착
![](/assets/images/notion/[network]-framing---error-control/img_10.png)

- 전체 예시
![](/assets/images/notion/[network]-framing---error-control/img_11.png)

  - S_n : sequence number
  - 마지막 Receiver : Out-of-Order frame 오더라도 ACK 보냄

### ◆ Performance


- Not that good.
- 보내지 않고 대기하는 시간 김
![](/assets/images/notion/[network]-framing---error-control/img_12.png)

## ✦ Go-Back-N


- ACK 오기 전까지 frame 을 계속 전송
- 문제 발생 → 그 이후로 보낸 frame 없던 것으로 치고 재전송
- Design Issue 
  - ACK 받기 전까지 몇 개의 frame 을 보내야 하는가?
  - Sequence number 몇 bit 써야 하는가?
  - Error 발생 시 어떡해야 하는가?

### ◆ Sliding Window


![](/assets/images/notion/[network]-framing---error-control/img_13.png)

- Sender 의 buffer → frame 마다 sequence number 붙여서 buffer 에 저장
- Window Size : 15
  - Window 왼쪽 : 전송 완료 & ACK 완료
  - 주황색 : 전송 완료 & ACK X 
→ outstanding frame
  - 흰색 : 전송 가능 & 데이터 준비 X
  - Window 오른쪽 : 전송 불가능
- Sequence number : 4 bit → 0 ~ 15 반복
  - S_f : 첫 outstanding frame
  - S_n : 다음 보낼 frame
  - S_{size} : send window size
- Send Window 크기 만큼 일단 frame 전송
  - ACK 돌려 받으면 그만큼 window 오른쪽으로 밀기 (size 는 그대로)
- Receive window : 1 칸
![](/assets/images/notion/[network]-framing---error-control/img_14.png)

  - 다음 도착할 frame 기다림
  - 기다리던 frame 이 아니면 discard
cf) Stop-and-Wait 는 Send 1 칸, Receive 1 칸

### ◆ Sequence Number Range


- if 범위가 [0 ~ N-1] → 사용 bit 수 : \log_2N
ex) [0 ~ 63] 이면 6 bit 사용
- 너무 작아도, 너무 커도 문제
  - 원칙 : Send window size 가 N 이면 sequence number 는 N 보다 **커야**한다 (같음 X)
    - 클 경우
![](/assets/images/notion/[network]-framing---error-control/img_15.png)

      - timeout 일어나서 다시 보내면 ACK 를 다시 보내야하나?
        - next expected frame 이 3 이니 ACK(3) 보냄
        - 근데 이미 Sender는 0,1,2 보낸 상태.
        - Receiver 가 Frame 받을 때 마다 ACK(3) 을 또 보내야 하나? 
→ 가장 정확한 경우 : 매번 보내기
    - 같을 경우
![](/assets/images/notion/[network]-framing---error-control/img_16.png)

      - ACK 가 가지 않음 → but 잘못된 accept

### ◆ Cumulative ACK


- ACK(n) : n-1 까지 frame 다 받음
![](/assets/images/notion/[network]-framing---error-control/img_17.png)

- ACK 2 는 lost, but ACK 3 는 제대로 전달
→ ACK 2 전송 안됐더라도, 1, 2 제대로 받았다는 것 확인 → window 2 칸 옮김
- Timeout case
![](/assets/images/notion/[network]-framing---error-control/img_18.png)

  - Out-of-order frame 옴 → ACK 전송 X (Stop-and-Wait 와 차이)
    - NAK 가 없음

### ◆ Timer


- 가장 처음으로 보낸 frame (S_f) 에만 timer 1 개 사용
- ACK 받으면 S_f 다음 frame 에 timer set
- timeout 발생 → window 안 frame 모두 다시 보냄 (& timer reset)

### ◆ Stop-and-Wait vs. Go-Back-N


- Stop-and-Wait : Go-Back-N 의 특별한 case
  - send window size = 1
- Go-Back-N 문제점 
  - timeout 발생 시 window 안 모든 frame 재전송
  - receiver window size = 1 → 1만 lost 고 2~5 제대로 전송 되어도 전부 재전송 해야함

## ✦ Selective Repeat


- Go-Back-N 문제 해결
  - receive window size 도 N 으로
  - Send window size = Receive window size
- Send window 는 동일
- Receive window
![](/assets/images/notion/[network]-framing---error-control/img_19.png)

  - window 안에 있는 frame → 전송 받아야 하는 frame 
  - window 를 움직이는 상황 → ACK 전송
- Sequence number 가 m bit → window 는 2^{m-1} 보다 작거나 같다
  - Example
    - sequence numer 가 [0, 15] (m = 4)
    - window size : send 8개 (2^3) / receive 8개 (2^3)

### ◆ NAK mechanism


![](/assets/images/notion/[network]-framing---error-control/img_20.png)

- 원하는 frame 외에 다른 frame 전송 받음 → send 측에 원하는 frame 알려주기
- NAK : Negative achknowledgement
  - ACK(1) : 0 번 frame 까지 전송 받음 알림
  - NAK(1) : 1 번 frame 받아야 하는데 다른 frame 이 왔다고 알림
    - NAK 를 전송하지 않으면 sender는 timeout 까지 기다려야 함
- NAK 를 보냈는데도 불구하고 해당 frame 이 오지 않으면?
  - 예시에선 한 번 만 전송
  - 또 오지 않으면 → 아무것도 안함
- sender 는 NAK 받으면 해당 frame 재전송 
- if) Out-of-order frame 도착
  1. 매번 도착마다 NAK 보낸다
  1. 같은 NAK 대해 1 번 만 전송 → Selective Repeat 사용
  1. 아예 전송 X → timeout 의존

### ◆ Timer


- outstanding frame 각각 timer 필요
  - if timer 1 개만 사용 → S_f 에 위치
![](/assets/images/notion/[network]-framing---error-control/img_21.png)

→ frame 4 에 timer 없어서 loss 된거 모름

## ✦ Hybrid ARQ


- HARQ : ARQ + FEC
  - 기존 ARQ : Error 발견 → frame 버리고 재전송 요청
  - HARQ : Error 발견 → error 난 frame 도 일단 저장. 재전송 된 frame 과 합쳐서 복원 성공률 높이기 (soft combining)
- 4G LTE, 5G NR 에 사용
