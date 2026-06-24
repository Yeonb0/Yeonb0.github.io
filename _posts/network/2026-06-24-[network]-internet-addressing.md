---
categories:
- Network
date: '2026-06-24T10:26:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 8
tags:
- 네트워크
- IP
- 네트워크 계층
- 라우팅
title: '[Network] Internet Addressing'
toc: true
toc_sticky: true
---

## ✦ IP address


- 모든 기계에 존재하는 주소
- 기본적으로 unique 해야 함

## ✦ IPv4


- 기본형. 4 byte (2^{32} 개)
- 이미 모두 소진함.
- Binary Notation                                               ↔      Dotted-deciaml notation
`10000000 00001011 00000011 00011111`             `128.11.3.31`
- How 배정?
  - IANA (국가 별 배정) / APNIC (아시아 국가들에 배정)
  - KRNIC : 한국 내에서 배정
  - ISP : KT, LG U+, SKT 등 → 개인에게 배정

### ◆ Class


- IPv4 를 분류하는 기준
- Network address + Host address
  - Network address : 망이 공통적으로 사용하는 주소
  - Host address : 망 안에서 unique 한 주소
- Class 따라 가능한 Host 개수 다름
![](/assets/images/notion/[network]-internet-addressing/img_1.png)

  - A : `0` 으로 시작 (0 ~ 127) → Network 당 Host 2^{24} 개
  - B : `10` 으로 시작 (128 ~ 191) → Network 당 Host 2^{16} 개
  - C : `110` 으로 시작 (192 ~ 223) → Network 당 Host 2^{8} 개
  - D : `1110` 으로 시작 (224 ~ 239)
    - Multicast 용
      - Unicast : 목적지가 하나
      - Multicast : 여러 명에게 보냄 (전체는 X) 
        - Netflex, Tving 등등
      - Broadcast : 전체에게 보냄
  - E : `1111` 으로 시작 (240 ~ 255)
    - 특수 목적으로 남겨놓음 (reserved)
![](/assets/images/notion/[network]-internet-addressing/img_2.png)

### ◆ Subnetting


- class 사이 이용 가능한 host 갯수 차이 큼 → subnet 으로 network / host 구분 표시
- `255.255.255.0` → `11111111 11111111 11111111 00000000`
  - 1 부분 : network number (24 bit)
  - 0 부분 : host number (8 bit)
- 1 / 0 갯수 조정해서 host 갯수 증가 가능 (2배씩)
  - 앞에서부터 1111, 0 & 1 섞어서 X
- Network address (망)
  - 같은 망 : gateway 안 거치고 바로 전달 가능
  - 다른 망 : gateway 거쳐서 가야함

### ◆ Address 할당


- Network address & subnet address 주기
  - host address 는 할당받은 범위 내에서 배정
  - address 배정 시 연속적으로 해야함 (배달 위해서)
- Example
  - `205.16.37.32` ~ `205.16.37.47` 할당
→ 16개의 host 할당 
![](/assets/images/notion/[network]-internet-addressing/img_3.png)

    - 첫 번째 (`205.16.37.32`) 할당 주소가 할당된 수 (16) 로 나눠 떨어져야 함.
    - if) 나눠 떨어지지 않음
→ subnetting 하면서 사용하지 않는 주소 생김
  - subnet → `11111111 11111111 11111111 11110000` (`255.255.255.224`)
- 전체 주소 : **IP 주소 / 1 갯수 **로 표현 
![](/assets/images/notion/[network]-internet-addressing/img_4.png)

  - Example) `205.16.37.39/28` 의 first address? 
    - 끝 4 bit 만 0 으로 바꾸기
→ 11001101 00010000 00100101 00100000
→ subnet masking 사용 이유? routing 배달 위해

## ✦ Routing


- Router
![](/assets/images/notion/[network]-internet-addressing/img_5.png)

  - 받은 데이터를 routing table 바탕으로 다음 방향으로 전송
  - routing table : (Destination, Next Hop) 저장
    - Next Hop : 다음으로 갈 router

### ◆ Prefix routing


- 전체 테이블 작성하면 복잡
- 같은 방향은 묶어서 표시 → subnet 와 유사
  - 지역적으로 IP 주소 유사해야 함
![](/assets/images/notion/[network]-internet-addressing/img_6.png)

- ex) 목적지가 `194.24.17.4`
→ Oxford 로 전송
- Longest matching prefix
![](/assets/images/notion/[network]-internet-addressing/img_7.png)

  - 목적지가 `194.24.14.72`
    - London : `194.24.0.0` ~ `194.24.32.255`
    - San Francisco : `194.24.12.0` ~ `194.24.16.0`
→ 두 Destination 모두 목적지 포함

  - 이런 경우 Prefix 가 긴쪽 (subnet 이 큰 쪽) 으로 이동
→ San Francisco 선택
  - 더 구체적인 주소로 이동
  - Prefix 동일 → 아무 곳으로 이동
- Rout aggregation
  - ex) 3 곳의 Next hop 이 동일 → 합치기
![](/assets/images/notion/[network]-internet-addressing/img_8.png)

  - `194.24.0.0/19` 로 합치기
    - 중간 12 ~ 15 비어 있지만 괜찮음
      - entry 없을 경우 : 이동 X
      - entry 있을 경우 : longest matching 이니까 자동으로 이동
    - 합칠 때는 prefix 가 (subnet) 모두 포함은 하되, 최소가 되도록
![](/assets/images/notion/[network]-internet-addressing/img_9.png)

  - specific 한게 좋은 router
  - `/28` 로 쓰면 0 ~ 15 로 추가 범위 포함 → XX

### ◆ Extra


- 특수 IP address
  - `127.0.0.1` → 자기 자신
  - `169.254.0.0/16` → 자동 IP 받기 실패 시
  - `255.255.255.255` → Broadcast (모두에게 전송)
  - private IP address 
![](/assets/images/notion/[network]-internet-addressing/img_10.png)

    - class A, B, C 일정 구역
    - public 아니라 local 에서 사용
