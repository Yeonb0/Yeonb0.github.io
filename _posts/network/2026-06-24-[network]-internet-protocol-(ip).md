---
categories:
- Network
date: '2026-06-24T10:28:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 9
tags:
- 네트워크
- 프로토콜
- IP
- 네트워크 계층
title: '[Network] Internet Protocol (IP) '
toc: true
toc_sticky: true
---

## ✦ Internet Protocol (IP)


### ◆ IP : A Network Layer Protocol


- Protocol : 규약. 절차. 메세지 규정
- Layer 1 & 2 : 직접적으로 연결 (유선 / 무선)
- Layer 3 : 여러 개 거쳐야하는 목적지까지 데이터 전송해야할 때
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_1.png)

- H → Host
  - 데이터 송신 / 수신 주체
- R → Router 
  - 직접적 기능 X 
  - Packet 전달 역할만
- 802.11 (Wi-Fi) / Ethernet (유선) / PPP → layer 1 & 2
  - 통신 위해선 양쪽에 모두 Protocol 있어야 함
- IP → layer 3
  - 다음 번 목적지로 가게 함
  - Multi hop 을 가능하게 함
  - Hourglass Model
    - layer 3 의 IP 는 만국 공통 → layer 1, 2, 4 의 여러 protocol 공통으로 모으는 역할

### ◆ IP : Service Model


- IP 가 어떤 기능을 해줌? (layer 4 입장)
- Packet delivery
  - Connectionless : 연결 설정 안하고 보냄 (like 우편)
→ 받았는지 안받았는지 모름
    - cf) Connection-oriented : 연결 설정하고 보냄 (like 전화)
→ layer 4 TCP
  - Best-effort (unreliable)
    - Packet 이 없어질수도, 순서 안맞을수도, copy 될 수도, 오래 걸릴수도 있지만 일단 최선을 다해서 보냄 
    - 그 이상의 서비스는 layer 4 에서
- Global Addressing Scheme : 세계 만국 공통

## ✦ Packet


### ◆ Frame


- Header 
  - 목적지 주소 (MAC / 물리적 주소)
    - layer 2 : 내 주소인지 판단 → 일단 받고 목적지 주소가 내가 아니면 버리
    - layer 3 : AP → 목적지 주소로 forwarding 해줌
- Address
  - MAC 주소 (물리적 주소)
    - 기기에 할당된 주소
    - 한 기기에 여러 개 가능 → 5G, Wi-Fi MAC 주소 다름
    - 48 bit 주소
    - 기기를 이동해도 고정인 주소
  - IP 주소 (논리적 주소)
    - IPv4 : 32 bit 주소33
    - 기기를 이동할 때마다 달라짐
  - packet : 데이터 조각 (general)
  - frame : layer 1,2 에 사용하는 데이터 조각
  - datagram : layer 3, 4 (UDP)
  - segment : layer (TCP)

### ◆ Packet format


- Layer 내려올 수록 점점 앞 뒤로 붙음

| Header (L2) | Header (L3) | Payload | Trailer (L3) | Trailer (L2) |

- Header 에 어떤 내용이 들어있는가?
1. 첫 번째 줄
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_2.png)

  - 20 byte (+ option 40 byte, 거의 사용 X) → 총 80 bit
  - VER (4 bit) : IP version
    - IPv4 `0100` / IPv6 `0110`
  - HLEN (4 bit) : Header 의 길이 (단위 4 byte)
    - ex) `0101` → 5 * 4 byte = 20 byte
  - Service (8 bit)
    - 과거 : 우선순위 + 서비스 정의
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_3.png)

      - Precedence 3 bit → priority 0 ~ 7
      - TOS (Type of Service) 4 bit
        - D : delay 최소화
        - T : throughput 최대화
        - R : reliability 최대화
        - C : cost 최소화
→ Precedence & TOS 따라 어떻게 처리할 지 router 정책 정함
ex) 버리는 우선순위 정하기 / 보낼 순서 정하기

    - 현재 
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_4.png)

      - DSCP 6 bit → Precedence 와 유사
        - 4가지로 class 나눠 중요 순서 정함 (source 바탕)
EF → AF → CS → Default
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_5.png)

      - ECN 2 bit → Congestion Notification
        - 막힌다 라는 신호
        - 중간 router 가 바꿔서 보내는 값
        - 알림만. 해결은 TCP 가
  - Total length (16 bit) : header + data 전체 길이
    - 최대 65535 byte 까지
1. 세 번째 줄
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_6.png)

  - Time to live (TTL) (8 bit) : 0 ~ 255 
    - router 간 이동마다 -1
    - 0 되면 forwarding 멈추고 drop
      - 빙빙 도는 경우 막기 위해 router 이동 범위 제한
    - 전세계 어디도 보통 20 hop 안넘음
  - Protocol (8 bit) : layer 4 의 protocol 이 무엇인가?
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_7.png)

1. 나머지
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_8.png)

  - 보내는 사람 / 받는 사람 IP 주소
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_9.png)

  - 최대 40 byte 까지 추가로 붙을 수 있음 (거의 사용 X)

### ◆ Example


![](/assets/images/notion/[network]-internet-protocol-(ip)/img_10.png)

- 패킷 길이가 2 (8 byte) → 5 이상이어야 함
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_11.png)

- 총 8 * 4 = 32 byte 
- 기본 20 byte. option 12 byte
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_12.png)

- Header 20 byte. 총 길이 32 + 8 = 40
- Data 20 byte
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_13.png)

- TTL = `01`

## ✦ Fragmentation


### ◆ MTU (Maximum Transfer Unit)


- Protocol 마다 MTU 다름
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_14.png)

- 보낼 때 maximum packet size
- payload 에 들어갈 수 있는 최대량
  - 위 layer 가 맞춰서 보냄
  - 이 이상으로 보냈을 시 → fragmentation
  - packet : 데이터 조각 (general)
  - frame : layer 1,2 에 사용하는 데이터 조각
  - datagram : layer 3, 4 (UDP)
  - segment : layer (TCP)

### ◆ Fragmentation


- IP Header 를 각 나눠진 frame 마다 붙임
- Fragment 조립 → 최종 destination 에서
  - MTU 작아져서 중간에 fragmentation 되고 다시 MTU 커져도 조립 X
  - 합치려면 모든 fragmentation 다 도착해야함.
→ 하나라도 도착 X 면 버림

### ◆ Exercise


![](/assets/images/notion/[network]-internet-protocol-(ip)/img_15.png)

- fragment O & 마지막 fragment
- fragment X
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_16.png)

- fragment O & 다음 fragment 존재
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_17.png)

- fragment O & fragment offset 0
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_18.png)

- Total length = header size 20 + payload 80 byte
- start 800 byte ~ end 879 byte

### ◆ Path MTU Discovery


- 요즘은 fragmentation 하지 않도록 미리 나누어서 전송
- 중간 MTU 가 어떤지 알아보기 위해 D = 1 로 설정하고 전송
  - 문제 생길 시 ICMP 가 “Fragmentation Needed” 보냄
  - fragment size 줄여서 check
→ 모두 통과하는 size 로 잘라서 보냄
- 요즘 가장 많이 사용하는 protocol → Ethernet
→ Source 에서 1480 씩 보내는 경우 多
![](/assets/images/notion/[network]-internet-protocol-(ip)/img_19.png)
