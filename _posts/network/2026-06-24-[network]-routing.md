---
categories:
- Network
date: '2026-06-24T10:29:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 10
tags:
- 알고리즘
- 네트워크
- IP
- 네트워크 계층
title: '[Network] Routing'
toc: true
toc_sticky: true
---

## ✦ Overview


### ◆ Network Layer


- OSI 7 layer
  - layer 1 - Physical → (직접적) 전송 담당
  - layer 2 - Data link → physical layer 통해 전송
  - layer 3 - Network layer → 여러 매체를 hop 해서 배달
  - layer 4 - Transport layer
  - layer 5 ~ 7 (5) - Application layer
- Computer : layer 1 ~ 7 모두 존재
- Router : layer 1 ~ 3 까지만 존재

### ◆ Network Layer Function


- Forwarding : 데이터 알맞은 곳으로 보내기
  - DATA PLANE
  - 데이터 오면 destination address & routing table 확인하고 어디로 보낼지 결정
- Routing : 어디로 보낼지 route 결정 (알고리즘 결정)
  - CONTROL PLANE
  - routing algorithm 통해 routing table 구성
  - Per-Router Control Plane
![](/assets/images/notion/[network]-routing/img_1.png)

    - router 끼리 자체적으로 routing table 구성
  - Logically Centralized Control Plane
![](/assets/images/notion/[network]-routing/img_2.png)

    - Remote Controller 로 routing table 중앙 관리

## ✦ Routing


### ◆ Routing


- packet 이 forwarding 될 경로 결정
- 어떤 곳으로 가려면 어느 방향으로 가야하는지 table 작성 
- 실제는 `163.239.0.0/16` 과 같이 IP 주소로 저장
![](/assets/images/notion/[network]-routing/img_3.png)

- ex) A → F 으로 packet 보내기
  - A → α (1) → β (2) → δ (3) → F

### ◆ Routing Algorithm


- table 을 어떻게 만들 것인가? → routing algorithm
  - packet 마다 정책이 다름 
    - fast
    - throughput
→ router 도 다양성 필요

- 기본적으로 shortest path 알고리즘 사용 (거리, cost 등)
  - intradomain : 같이 관리자가 관리하는 내에서 routing
    - Distance vector → RIP
    - Link state → OSPF
  - interdomain : 다른 관리 구역 넘어갈 때 routing (정책 영향 O)
    - Path vector → BGP
  - Autonomous System (AS) : 같은 router policy 를 가진 network group
    - 12만 개 정도 존재 (우리나라는 1187개)
    - ISP 나 조직에 의해 관리
    - 서강대도 하나의 AS

## ✦ Routing Algorithms & Protocols


- 메시지 전달 방식 
  1. 주기적으로 전달 → periodic messaging 
  1. table update 될 때 → trigger based messaging
→ 일반적으로 1 + 2 방법 합침

    - 주기 맞춰 timer 설정. timer 끝날 때 까지 정보 안오면 문제 감지

### ◆ Distance vector routing


- distance vector = (destination, distance, next node)
  - 목적지, 거리, 다음 이동
- Example : A → C shortest path?
![](/assets/images/notion/[network]-routing/img_4.png)

- Table 작성하기 → Bellman-Ford!
  - initial : 직접 연결된 정보만 작성
![](/assets/images/notion/[network]-routing/img_5.png)

  - 정보 전달 (destination, distance)
    - if 기존 정보 X
      - vector 작성
    - if 기존 정보 O
      - 거리가 줄면 vector 작성
  - 최종 table
![](/assets/images/notion/[network]-routing/img_6.png)

    - A → C
      - A → B → C (8) : X
      - A → E → D → C (5) : O 
→ 더 많이 hop 하지만 최단 거리로 이동

- 전체 최단 거리 위해 지속적으로 table update 
  - router 의 변화 가능
- Link 에 문제가 발생하면?
![](/assets/images/notion/[network]-routing/img_7.png)

  - D & E 가 link 문제 파악해서 table 업데이트
![](/assets/images/notion/[network]-routing/img_8.png)

- 문제 : Count-to-infinity problem
![](/assets/images/notion/[network]-routing/img_9.png)

  - A - B 사이 직접적 통로 막혔을 때
    - B 가 C 를 통해 A 로 갈 수 있다고 착각 (사실은 B 를 지나야함)
    - 25 까지 B, C 의 A 로 가는 cost 계속 증가
![](/assets/images/notion/[network]-routing/img_10.png)

![](/assets/images/notion/[network]-routing/img_11.png)

![](/assets/images/notion/[network]-routing/img_12.png)

    - 원인 : 목적지까지 가는 과정에 자신 (B) 이 있는지 모름
→ routing loop 발생

- 해결법
  - Split horizon
    - C → B 로 routing table 보낼 때 next 가 B 이면 빼고 보냄
  - Split horizon with posion reverse
    - C → B 로 routing table 보낼 때 next 가 B 이면 distance 를 infinity 로 해서 보내기
→ 3 개 loop 는 해결 불가능

![](/assets/images/notion/[network]-routing/img_13.png)

  - Path vector routing
    - 중간 과정 모두 제공
    - 장점 : 3 개 loop 문제 해결 가능
    - 단점 : message overhead 

### ◆ RIP (Routing Information Protocol)


- Distance Vector Routing 구현 protocol
- 30초 마다 전송 + table update 시 전송
- message format
![](/assets/images/notion/[network]-routing/img_14.png)

  - 목적지 주소 (address + mask) + distance

### ◆ Link-State routing


- 최근에 많이 사용하는 방법
- 내 옆 사람의 정보를 모두에게 전송
  - cf) distance vector : 내 모든 정보를 옆 사람에게 전송
- 나와 연결된 (ID, distance) 를 모든 node 에게 전송 → graph 만들기
- 최단 경로 → Dijkstra 알고리즘 사용
![](/assets/images/notion/[network]-routing/img_15.png)

  - D - distance / P - parent
  - 순서 : A → D (1) → E (2) → B (2) → C (3) → F (4)
    - 단계마다 최소 거리 node 한 개씩 선택
    - 동 거리일 시 아무 node
  - table 생성 후 최소 거리 맞춰 전송
- 문제점 : network-wide flooding 
  - 서로서로 모든 정보를 보내며 overhead
  - 잘못 사용 시 attack
- 해결법
  - Time To Live 통해 범위 조절
  - 내가 보낸 게 나에게 도착 → sequence number 같으면 drop

### ◆ OSPF (Open Shortest Path First)


- Link-state routing 구현 protocol
- LSA massage : 메시지 이름
- periodic + update 시 전송
- message format
![](/assets/images/notion/[network]-routing/img_16.png)

  - Link-state ID : 나
  - Link ID : 내 친구
  - Metric : 친구까지 거리
  - Link data : 두 router 사이 여러 link 구분 (≒ sequence number)

### ◆ 정리



| 항목 | Distance vector (RIP) | Link state (OSPF) |
|:--|:--|:--|
| **교환 정보** | 목적지, 목적지까지의 거리 | 이웃 ID, 이웃까지의 거리 |
| **전송 대상** | 직접 연결된 이웃만 | 네트워크의 모든 노드 (flooding) |
| **알고리즘** | Bellman-Ford (분산형) | Dijkstra |
| **장점** | 단순함, 낮은 오버헤드 | 빠른 수렴, 루프 없음 |
| **단점** | 느린 수렴, count-to-infinity 문제 | 높은 메시지/CPU 오버헤드 |

## ✦ Border Gateway Protocol (BGP)


### ◆ Networks


- Flat vs. Hierarchical Network
  - Flat
    - 모든 node 가 같은 level
    - 모든 node 가 서로에 대해 알아야 함
  - Hierarchical
    - network 가 더 작은 그룹들로 나눠짐
    - 각 그룹은 독립적으로 관리 됨
→ 인터넷은 계층적! & 각 그룹은 AS 하고 불림

- Autonomous System (AS)
  - 통합된 routing policy 가짐 
  - Tier 1 : global
  - Tier 2 : regional
  - Tier 3 : local
![](/assets/images/notion/[network]-routing/img_17.png)

  - AS 관계
    - Provider (망 제공) → Customer (망 사용)
    - Peer : 서로 망 공짜로 사용 (ex) KT / SKT / LG U+)
  - Multi-homing : 한 Customer 가 여러 Provider 사용
→ 다른 AS 에 사이에는 다른 policy 필요 ⇒ BGP 

### ◆ BGP


- BGP 의 필요성
  - Scale : AS 안 / 밖이랑 다른 scale
  - Policy : AS 밖이면 cost 도 고려해야 함
  - Trust : AS 밖으로는 내부 정보 유출 X
  - Autonomy : AS 마다 정책 다름 → 여러 AS 사이의 관리 필요
![](/assets/images/notion/[network]-routing/img_18.png)

- BGP : Border router (= Edge router) 간의 routing
  - Border router : AS 끝 쪽의 BGP 를 가진 router → 목적지 AS 로 어떻게 갈지 결정
  - eBGP : 다른 AS border router 끼리 정보 교환
  - iBGP : 같은 AS 안에서 border router 끼리 정보 교환 (intra-domain)
- BGP 의 layer? 
  - TCP 위에서 Application layer protocol 이지만 network layer 와 관련

### ◆ eBPG routing


- Distance vector (+ path) : path 까지 전체 전송하는 path vector routing 
![](/assets/images/notion/[network]-routing/img_19.png)

- ex) 30번이 123번 가고 싶을 때 -? 30 → 14 → 56 → 123 와 같이 이동
- Multi path 가능 
  - 가장 shortest 여도 정책 따라 다른 route 선택 가능
  - 123 가는 길 2개
- route advertisement : 연결된 AS 의 route router 에게 전달 
  - path 를 전송하므로 loop 발견 가능
  - path 에 전달할 router 번호 있으면 전송 X

### ◆ iBGP routing


- 같은 AS 내에서 border router 끼리 정보 전달
- 바깥쪽 AS 에서 온 정보 공유하기
- 원칙 : fully connected
  - 모두가 모두에게 연결 
  - 총 \frac{n(n-1)}{2} node 연결
  - 같은 AS 안의 router 정보는 전송 X
![](/assets/images/notion/[network]-routing/img_20.png)

- R3 
  - iBGP → R1, R2 : R4 의 정보 전달
  - eBGP → R4 : R1, R2 의 정보 전달
- Loop 방지 위해 모두 직접적 연결

### ◆ Policies


- BGP 에서 shortest 한 게 best route X
- Policy 에 따라 path 결정
  - customer > peer > provider
- traffic 
  - transit traffic : 내 customer 에게 가지 않는 traffic
![](/assets/images/notion/[network]-routing/img_21.png)

    - 100, 200 : Tier 1
    - 10, 11, 12, 13 : Tier 2
    - 1, 2, 3, 4 : Tier 3
  - 한 번 내려가기 시작하면 다시 올라가기 X
- 경로 전송
  - to Customer : 모든 link 전송
  - to Peer : Customer link 만 전송
  - to Provider : Customer link 만 전송

### ◆ BGP Path Selection Order


- Policy
  1. LOCAL_PREF ↑ → 같은 AS 에서 나갈 때 높은 Preference
![](/assets/images/notion/[network]-routing/img_22.png)

    - AS 의 관리자 의해 traffic 따라 결정
  1. AS_PATH ↓ → 지나는 AS 최소
  1. MED ↓ → 여러 입구로 들어올 수 있을 때 낮은 MED
![](/assets/images/notion/[network]-routing/img_23.png)

  1. eBGP > iBGP
  1. Lowest IGP
  1. Lowest router ID
