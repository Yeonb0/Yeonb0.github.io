---
categories:
- Network
date: '2026-06-24T10:31:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 11
tags:
- 네트워크
- 프로토콜
- 네트워크 계층
title: '[Network] Other Network-Layer Related Protocols'
toc: true
toc_sticky: true
---

## ✦ Address Resolution Protocol (ARP)


- When?
  - IP 주소는 아는데 MAC 주소는 모를 때
  - 어떤 MAC 주소가 찾는 IP 주소를 가지고 있나?
    - logical address : IP 주소 (연결 마다 달라짐)
    - physical address : MAC 주소 (기기 고정)
- Where? (layer)
  - layer 2? layer 3? 
- How? 
  - 모르면 broadcast 한다
    - Request : `141.23.56.23` 있나요?
    - Reply
      - 없으면 X
      - `142.23.56.23` : 제 MAC 주소는 A4:6E:F4:59:83:AB 입니다
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_1.png)

  - 전송 형태
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_2.png)

    - Hardware type : layer 2 의 type (ethernet)
    - Protocol type : layer 3 의  type (IP)
    - operation
      - 1 : request
      - 2 : replay
    - hardware address 는 6 byte / 나머지는 4 byte
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_3.png)

    - Request 할 때는 target MAC 주소 비어있음
    - Request ↔ Reply 시 Sender 와 Target 교환

### ◆ Spoofing


- ARP 는 인증 부재 → Host 는 수신한 답을 무조건 신뢰
- Man-in-the-Middle (MITM) attack : 중간자가 router 주소인 척 해서 가로채기
- 대응 방안
  - DAI (Dynamic ARP Inspection) : 관리형 스위치에서 ARP packet 검사해서 주소 달라지는거 검사
  - static ARP : 중요 호스트에 대해 ARP 테이플을 정적으로 고정

## ✦ Dynamic Host Configuration Protocol


- Application layer (layer 4) protocol
- IP 주소 가지고 있는 DHCP 서버 → 누군가 연결할 시 IP 주소 자동으로 빌려주기
- ex) 카페 Wi-Fi
  - 계속 사용 시 연장 / 안 쓰면 다른 기기에게 다시 빌려주기
- 한 DHCP server 가 여러 AS 관리 가능
  - 다른 네트워크에 있으면 broadcast 범위 안 닿음 
→ DHCP relay 가 넘어가서 전송
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_4.png)

- 과정 : DORA 
  - DISCOVER → OFFER → REQUEST → ACK
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_5.png)

## ✦ ICMP (Internet Control Message Protocol)


- layer 3 의 보조 프로토콜 → 데이터 전송 X

### ◆ Format


![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_6.png)

### ◆ 목적


- 언제 ICMP packet 이 전송되는가?
1. Error reporting
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_7.png)

  - Destination unreachable : 목적지로 가는 길이 없음
  - Source quench : router 가 full 임
→ 요즘엔 TCP 가 대체
  - Time exceeded : TTL 이 0 돼서 packet 이 버려짐
  - Parameter problem : header 에 문제 있음
  - Redirection 
    - 어떤 망에서 gateway 가 여러 개 일 때,
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_8.png)

      - A → B 로 전송해야하는 상황
      - R1 이 A에게 packet 을 받았을 때, 자신이 아닌 R2로 보내는게 나을 거라는 메세지
      - B에게 전송을 하긴 함
  - Rule
    - ICMP packet 에 error 생겼을 때의 error report ICMP packet 생성 X
      - query 에 대해서는 생성 가능
    - error report 은 fragmented 된 packet 의 첫 fragment 에만 생성
    - multicast packet 에 대해선 생성 X
    - 특별한 도착지 (127.0.0.1 or 0.0.0.0) 대해선 생성 X
1. Query
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_9.png)

  - Echo request & reply : ping 주고 받기
  - Timestamp request & reply 
    - round-trip time 계산용
→ ping 과 역할 동일, 거의 사용 X
  - Router solicitation & advertisement
    - 주변 router 알아보기 / 알려주기

### ◆ IP-level debugging tools


- ping
  - 시간 / TTL / 손실률 / 왕복 시간 (rtt) 정보 
  - ICMP Echo request & reply 사용
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_10.png)

  - 보안 상의 이유로 ICMP reply 막은 사이트도 있음
- traceroute
  - source & destination 사이의 router 들 trace\
  - Linux / MAC : UDP 전송
  - Windows : ICMP Echo request 사용
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_11.png)

![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_12.png)

  - 요청 시간 만료 → ICMP reply 막은 사이트 (drop 은 X)
  - TTL 을 점점 키워가며 (1→2→3) 목적지로 전송
    - time exceeded 받음
  - 마지막 hop → port 몰라서 drop
    - destination unreachable 받음

## ✦ Network Address Translation


- IP 주소 부족
- 공유기 (router) 는 Public IP 
  - 연결된 기기들에게는 Private IP unique 하게 배정
![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_13.png)

- 공인 server → 사설 IP 에 how 전달? **NAT**

### ◆ NAT : Network Address Translation


![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_14.png)

- router
  - 보통 주소 : `X.X.X.1` 로 시작 → 기기들에게 2, 3, 4, … 분배
  - 2개의 IP 가지고 있음 : 외부용 & 내부용
    - 외부 : `138.76.29.7`
    - 내부 : `10.0.0.4`
    - IP 주소 : layer 3 개념
    - Port : layer 4 개념 (TCP, UDP)
      - 같은 IP host 내에서 어떤 process?
- 전송 과정
  1. Host (`10.0.0.1:3345`)가 공인 server (`128.119.40.186:80`)에 packet 전달
  1. router 가 host 의 private 주소 → 자신이 만든 public port 를 table 에 쓰고 공인 server 에 public IP + 만든 Port 로 전송
    - LAN `10.0.0.1:3345` → WAN `138.76.29.7:5001`
  1. 공인 server 가 받은 주소(`138.76.29.7:5001`)로 packet 재전송 
  1. router 가 받은 주소의 port(`5001`) 확인해서 어디 host 로 온 packet 인지 파악하고 전송

### ◆ Port Forwarding


![](/assets/images/notion/[network]-other-network-layer-related-protocols/img_15.png)

- NAT : 내부 → 외부 나가는 packet 있을 때 NAT table 생성
- 내부에 서버가 있다면? ⇒ Port forwarding
- NAT router 에 수동으로 static mapping 추가

| 설정 | 내용 |
|:--|:--|
| 포트 포워딩 규칙 | TCP :80 → 192.168.0.10:80 |
| 외부 클라이언트 요청 | `Dst: 203.0.113.5 : 80` |
| NAT 라우터 변환 후 | `Dst: 192.168.0.10 : 80` |

  - 외부 서버가 공인 IP 로 요청 → router 가 공인 → 내부 서버 주소로 rewrite 해서 전달
