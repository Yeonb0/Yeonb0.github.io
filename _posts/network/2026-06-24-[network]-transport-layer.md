---
categories:
- Network
date: '2026-06-24T10:33:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 13
tags:
- 네트워크
- 전송 계층
- 프로토콜
- TCP
- UDP
title: '[Network] Transport Layer'
toc: true
toc_sticky: true
---

## ✦ Transport Layer


![](/assets/images/notion/[network]-transport-layer/img_1.png)

- layer 4 : End-to-end (process-to-process) communication
  - layer 1, 2 : hop-to-hop, single hop communication
  - layer 3 : host-to-host communication
![](/assets/images/notion/[network]-transport-layer/img_2.png)

- TCP / UDP

### ◆ Layers: Function


- Layer 1 (Physical) : 신호 만들기
- Layer 2 (Data link) : framing, ARQ, Error detect / correct
- Layer 3 (Network) : addressing, routing, host 에게 전달
- Layer 4 (Transport) : packet 세밀하게 조절 & 전달
  - flow control
  - congestion control

### ◆ Port


- 같은 host 안의 process 들 구분해주는 번호
- 16 bit : 0 ~ 65,535
- process-to-process communication
  - local host
  - local process (port number)
  - remote host
  - remote process (port number) 
→ 다음과 같은 4 가지 필요

![](/assets/images/notion/[network]-transport-layer/img_3.png)

![](/assets/images/notion/[network]-transport-layer/img_4.png)

  - IP 주소 → host 설정 (우리 집)
    - in Network Layer (IP)
  - port → process 설정 (집 구성원 중 누구의 우편?)
    - in Transport Layer (TCP, UDP)
- 종류
  - well-known port
    - 0 ~ 1023
    - 유명한 / 공식적 서비스
    - 22 (SSH), 25 (SMTP), 53 (DNS), 80 (HTTP), 443 (HTTPS)
  - registered ports
    - 1024 ~ 49151
    - 어떤 비즈니스에서 사용하는 포트
    - 등록해야 사용 가능
  - dynamic ports
    - 49152 - 65535
    - 등록하지 않는 port
    - 관리 주체 X, 자유롭게 사용
    - OS 가 port 자동 생성할 때 이 범위 사용 (NAT)

### ◆ Terms


- Socket : IP address + port number
![](/assets/images/notion/[network]-transport-layer/img_5.png)

- Multiplexing & Demultiplexing
  - Transport layer 의 역할
  - Port 생성 / 제거
![](/assets/images/notion/[network]-transport-layer/img_6.png)

## ✦ UDP (User Datagram Protocol)


- 매우 간단한 protocol
1. connection-less : 연결 설정 X
1. unreliable : error, 순서 신경 X
- 하는 일 
  - port 번호 받고 process 에게 보내기
  - checksum 으로 error detection 하기
- 특징
  - datagram : packet 의 다른 이름
  - sequence number X : 순서 X 중복 detection X
- 장점 : 쉬움, 가벼움, 빠름

### ◆ Header


![](/assets/images/notion/[network]-transport-layer/img_7.png)

- Port number (Source / Destination) : 각 16 bit
- Total length : UDP header + data 길이
- Checksum : Header 의 checksum

### ◆ Application using UDP


- 현재 : TCP 65 ~ 70% / UDP 35% ~ 30%
- 멀티 미디어 스트리밍 서비스 (유튜브)
- QUIC (layer 4) : HTTP/3 에서 새로 만든 protocol. TCP 와 유사하지만 조금 더 가벼움. UDP 에 붙여서 사용
- Multicast application : 여러 사람에게 동시 전송
- DNS, SNMP 등

## ✦ TCP (Transmission Control Protocol)


1. connection-oriented : 연결 설정 O
1. reliable : 순서 대로, error 없이 전달

### ◆ Terms


- Segment : packet 의 다른 이름. 잘라서 보내는 기준
- bi-directional : 연결 되면 쌍방으로 데이터 전송
- Buffer : sender / receiver 에 존재하는 데이터 전송 대기 공간. 운영체제 (OS) 관리
![](/assets/images/notion/[network]-transport-layer/img_8.png)

- Number
  - Byte number
    - TCP 는 각 byte 마다 numbering 해서 stream
    - 첫 번째 byte 에 0 ~ 2^{32}-1 중 random number 부여
  - TCP sequence number
    - 각 segment 의 첫 번째 byte number
![](/assets/images/notion/[network]-transport-layer/img_9.png)

    - segment number + length 통해 빠진 byte 있나 파악
  - Acknowledgement number
    - ACK 에 들어가는 순서
    - 내가 다음 받아야 할 byte number (그 이전까지는 다 받았다는 의미)

### ◆ Functions


- Flow control (흐름 제어)
  - 속도 조절
  - recevier 한테 무리를 주지 않게 전송
- Congestion control (혼잡 제어)
  - 속도 조절
  - 중간 router 에서 drop 이 발생하지 않도록 전송
- Error control (오류 제어)
  - ACK 이용 재전송
  - **◆ Error Control**
  - Layer 2 에도 error control 존재 → Router 에서 발생한 오류 검출 불가능
![](/assets/images/notion/[network]-transport-layer/img_10.png)

  - If layer 4 에서만 오류 검출? 
→ layer 4 은 end point 에만 존재. 중간 router 오류 control 불가능
  - Layer 2 & 4 둘다 Error Control 에 사용

### ◆ TCP header


![](/assets/images/notion/[network]-transport-layer/img_11.png)

- 각 줄 당 32bit
- Port number (Source / Destination) : 각 16 bit
- Sequence number : 내가 보낼 데이터의 sequence number
- Acknowledgement number : 상대 데이터의 acknowledgement number
  - bi-directional → Sequence & Acknowledgement number 둘다 필요. 
서로 다른 byte number 시작
- HLEN (4 bit) : header length (unit : 4 byte)
  - option 없으면 기본 5
  - TCP option 은 자주 사용 → 유동적으로 변경
- reserved (6 bit → 4 bit) : 사용 X 예약 bit
- Flag (6 bit → 8 bit) : 0 or 1 
![](/assets/images/notion/[network]-transport-layer/img_12.png)

  - URG (Urgent) : 1 이면 중요한 data 있음 (Ctrl + C / Esc 등)
    - urgent pointer (16 bit) 사용
![](/assets/images/notion/[network]-transport-layer/img_13.png)

      - data : urgent + normal 로 구성
      - normal data 시작 위치 표시 (이전까진 urgent data)
  - ACK : Acknowledgement 있음 → 맨 처음 빼곤 보통 1
  - PSH (Push) : 1 이면 OS 에게 buffer 에서 바로 올려달라는 의미
    - buffer 에 있는 내용 모두 전송
  - RST (Reset) : 문제 있어서 연결 종료 시 1 (Client & Server 둘 다 전송 가능)
  - SYN (Synchronize) : 처음 연결 설정 시 1 (Client 만)
  - FIN (Finish) : 장상적 연결 해제 시 1 (Client 만)
- 추가된 flag
  - ECE (ECN-Echo)
    - IP-header 의 ECN 2 bit
      - ECT (ECN-Capable) : ECN 사용 가능?
        - sender 결정
        - 중간에 congestion 있으면 marking 가능
      - CE (Congestion Experience) : 지금 Congestion 있음?
        - router 결정
        - packet drop 대신 CE 1 로 marking
        - receiver 입장에선 여러 CE 가 계속 옴
    - CE marking 된 packet receive → receiver가 ECE 1 로 설정해서 보내기
  - CWR : ECE 1 받은 sender 가 CWR 전송
    - sender : congestion 있다는 거 파악하고 CWND 줄이기
    - receiver 가 CWR = 1 인 packet 받으면 다시 ECE = 0 전송
![](/assets/images/notion/[network]-transport-layer/img_14.png)

- Window size (16 bit)
  - advertised window 의 크기
  - receiver 가 자신 window 얼마 남았는지 전송
    - sender 는 이 size 이상 전송 X
  - flow control

## ✦ TCP : connection setup/teardown


### ◆ TCP connection setup


- bi-directional : client & server 모두 정보 send & receive
- 3-way handshake
  - Client : `SYN` 안녕하세요?
  - Server : `ACK` 반갑습니다 + `SYN` 안녕하세요?
  - Client : `ACK` 반갑습니다
→ connetion 완료

![](/assets/images/notion/[network]-transport-layer/img_15.png)

  - connection 설정 시 data 전송 X → sequence number 그대로 사용 
- SYN flooding attack
  - DoS (Denial-of-Service) attacks
    - Server : `SYN` 요청 → state 만들고 `ACK` + `SYN` 보내고 wait
    - Attacker : `SYN` 요청 후 → 다른 IP 로 또다시 `SYN` 요청
    - state 만 늘어남 → 다른 유저 못 받음
  - 방어
    - initial sequence number 로 계속 오는 애들 정보 찾기
    - memory 에 state 남기지 않고 최종 연결 때만 남기기

### ◆ TCP connection teardown


- 3-way handshake
  - Client : `FIN` 
  - Server : `ACK` + `FIN`
  - Client : `ACK` 
→ connection 끝

![](/assets/images/notion/[network]-transport-layer/img_16.png)

- half-close : Client 가 `FIN` 요청 보냈는데 Server 가 아직 data 전송중
  - Server : Client 의 `FIN` 에 대한 `ACK` 전송
  - data 전송 완료 후 `FIN` 전송
  - 이 동안에는 Server 의 단방향 데이터 전송 
![](/assets/images/notion/[network]-transport-layer/img_17.png)

## ✦ TCP : sliding window


### ◆ Send Window


- sender 에 window 존재
  - window 안에 있는 data 전송
  - `ACK` 받으면 그만큼 window slide
![](/assets/images/notion/[network]-transport-layer/img_18.png)

  - Last Byte ACKed : 가장 최근에 ACK 받은 byte (window 왼쪽)
  - Last Byte Sent : 가장 최근에 보낸 byte (window 안쪽 / 아직 ACK X)
  - Last Byte Written : 가장 최근에 준비된 byte (window 오른쪽 / Application)
    - LastByteAcked ≤ LastByteSent ≤ LastByteWritten

### ◆ Receive Window


- receive window 
![](/assets/images/notion/[network]-transport-layer/img_19.png)

  - LastByteRead : 가장 최근에 ACK 보낸 byte
  - NextByteExpected : 다음으로 받아야 할 byte (그 전까진 모두 받았다 가정)
  - LastByteRcvd : 가장 최근에 받은 byte (중간에 구멍 포함)
    - LastByteRead ≤ NextByteExpected ≤ LastByteRcvd 

### ◆ Window


- Linked layer 와 차이 → window size
  - linked layer : 조건에 따라 고정
  - TCP : 상황 따라 window size 변경 
- Window size : min (rwnd, cwnd)
  - rwnd (receiver window) : receiver 가 advertise 해주는 window → buffer 에 남은 공간
  - cwnd (congestion window) : network 상태 window (중간 router)

## ✦ TCP : Sliding Window Control


- TCP → congestion & flow control
  - Reliable delivery
  - Fast delivert
- Sliding Window Size 
  - Size ↑ → 속도 ↑, drop ↑
    - drop → bandwidth 낭비
  - Size ↓ → 속도 ↓, bandwidth 낭비
⇒ 적당한 size 찾기!

### ◆ Flow control


- receiver 의 Window size 칸 보고 남은 크기 추정
  - 16 bit → 0 ~ 65535 byte
  - TCP option (Window scale) 로 배수 넣을 수 있음
    - n → 2^n 만큼 곱하기
![](/assets/images/notion/[network]-transport-layer/img_20.png)

- MSS (Maximum Segment Size)
  - MTU - IP header (20) - TCP header (20 + α)
  - 보통 1460 인 경우 多
  - 1500 안 넘도록 자르기

## ✦ Congestion Control


- Congestion? → router 에서 packet loss 발생! (`ACK` 가 오지 않음)
![](/assets/images/notion/[network]-transport-layer/img_21.png)

  - data 전송 ↑ → capacity ↑, delay ↑
  - throughput : pipe 를 꽉 채워서 보냄
→ 노란색 영역이 best!

### ◆ Slow Start Phase


- 변수 : CWND
- 단위 : MSS
- Initial CWND : 1 MSS
  - 한 번 전송 → `ACK` 받으면 CWND++
  - `ACK` 받을 때마다 CWND++ 
→ 지수승 만큼 증가!
![](/assets/images/notion/[network]-transport-layer/img_22.png)

![](/assets/images/notion/[network]-transport-layer/img_23.png)

  - 각 RTT 마다 2배 → exponential increase
  - 결국 packet drop → congestion 발생 
- Time out : Packet loss 판단 방법
  - Segment 전송 후 일정 시간 동안 안옴 → TIMEOUT ⇒ LOST
  - Timeout 발생 시
    - CWND = 1 로 초기화
    - SSThresh = \frac{\text{CWND}}{2} 로 설정 
      - drop 당시 CWND 의 절반! 
  - end-to-end 간 packet 이동 → 어느 정도의 시간을 두어야 하는가?
    - margin 을 크게 두어야 함

### ◆ Congestion Avoidance Phase


- 다시 Slow Start 시작
- SSThresh 지점 도달 → 천천히 올라감
- CWND += MSS * \frac{\text{MSS}}{\text{CWND}}
- 선형적 증가 : Additive Increase
![](/assets/images/notion/[network]-transport-layer/img_24.png)

- drop 발생 시 같은 방법으로 CWND = 1 초기화 & SSThresh 설정 후 처음부터

## ✦ Fast Retransmission and Fast Recovery


### ◆ Fast Retranssmission


- Timeout → end-to-end 라 오랜 시간 기다려야 함
  - packet loss 결정 느림
- 대안 : Three duplicate ACK
  - 같은 번호에 대한 ACK 가 3번 반복 → drop 판단
  - 바로 Segment 다시 보내기

### ◆ Fast Recovery


- Three duplicate ACK 로 인해 재전송 할 때
  - Timeout : 아예 대부분 Packet 이 제대로 전송 X
  - Three duplicate ACK : 중간에 한 Packet 빼고는 대부분 잘 전송
- CWND = SSThresh
- SSThresh = \frac{\text{CWND}}{2}
  - slow start skip 하고 바로 congestion avoidance 단계로 이동
![](/assets/images/notion/[network]-transport-layer/img_25.png)

![](/assets/images/notion/[network]-transport-layer/img_26.png)
