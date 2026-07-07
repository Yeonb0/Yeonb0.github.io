---
categories:
- Computer-Architecture
date: '2026-07-07T19:37:00.000+09:00'
layout: single
series: 컴퓨터 아키텍쳐
step: 7
tags:
- CPU
- 메모리
- Cache
- Buffer
title: '[CA] Memory System (1)'
toc: true
toc_sticky: true
---

## ✦ Introduction


### ◆ Memory Hierarchy


- Static RAM (SRAM)
  - 0.5ns ~ 2.5ns
  - GB 당 $2000 ~ $5000
- Dynamic RAM (DRAM)
  - 50ns ~ 70ns
  - GB 당 $20 ~ $75
- Magnetic disk
  - 5ms ~ 20ms 
  - GB 당 $0.20 ~ $2
→ 이상적인 메모리 : SRAM 만큼 빠르면서 disk 정도의 용량 & 가격

### ◆ Locality


- Temporal locality
  - 한 번 참조된 항목은 곧바로 다시 참조되는 경향이 있음
- Spatial locality
  - 어떤 항목이 참조되면 그 근처의 다른 항목이 곧바로 참조될 확률이 높음
→ 메모리 계층 구조 이용해 지역성 활용 가능

  - 모든 것을 disk 에 저장
  - 최근 & 그 인접 항목을 DRAM 으로 복사 → Main memory
  - 더 최근 & 인접 항목을 SRAM 으로 복사 → Cache memory

### ◆ Hit & Miss


![](/assets/images/notion/[ca]-memory-system-(1)/img_1.png)

- block : 두 계층 간 복사의 최소 단위
- Hit : 접근하려는 데이터가 상위 레벨에 존재
  - 복사할 필요 X
  - Hit ratio : \frac{hit}{total}
- Miss : 접근하려는 데이터가 없음
  - 하위 레벨에서 block 단위로 복사
  - miss penalty : 복사하는데 걸리는 시간
  - Miss ratio : 1 - hit ratio

## ✦ Cache Memory


- CPU 에 가장 가까운 memory 
- 접근 순서가 주어졌을 때
  - how 데이터 존재 여부 확인?
  - where 데이터 찾음?

### ◆ Direct Mapped Cache


- Where 의 가장 단순한 답 → 위치는 주소에 의해 결정
- 메모리의 특정 block 은 cache 의 딱 한 곳에만 들어갈 수 있음
- cache index = (block 주소) mod (cache 안의 block 수)
![](/assets/images/notion/[ca]-memory-system-(1)/img_2.png)

→ 앞의 2 bit 뗀 cache 주소에 저장

  - block 수는 2의 거듭제곱
  - 하위 비트 주소 사용 
→ 같은 슬롯 매핑 두 주소 번갈아 접근 시 conflict 발생 가능

### ◆ Tags and Valid Bits


- How 의 답 → Tag bit & Valid bit 두기
- Tag bit : block 주소의 상위 비트 저장
- Valid bit : 해당 칸에 data 가 있는지 표시 
  - 초기 : 0
  - 데이터 저장 후 : 1

### ◆  Example


![](/assets/images/notion/[ca]-memory-system-(1)/img_3.png)

- 하위 3 bit 의 index 에 저장
- tag 에 상위 2 bit 저장 

### ◆ Address Subdivision



| 구분 | 비트 범위 | 비트 수 | 역할 |
|:--|:--|:--|:--|
| **Tag (t)** | 31 ~ 12 | 20비트 | 이 슬롯의 데이터가 맞는 블록인지 확인 |
| **Index (s)** | 11 ~ 2 | 10비트 | 캐시의 어느 슬롯(set)을 볼지 결정 |
| **Byte offset (b)** | 1 ~ 0 | 2비트 | 블록 내 어느 바이트인지 결정 |

![](/assets/images/notion/[ca]-memory-system-(1)/img_4.png)

→ block 크기 따라 tsb 크기 달라짐 

- Example
  - 64 block & 16 bytes/block
  - 1200번은 어디에 mapping?
  - block address = ⌊1200 / 16⌋ = 75
  - block number = 5 modulo 64 = 11

| Tag (t) | Index (s) | Offset (b) |
|:--|:--|:--|
| 31 ~ 10 | 9 ~ 4 | 3 ~ 0 |
| 22비트 | 6비트 | 4비트 |

- Block 크기 키우기
  - 장점 : miss ratio ↓ (∵ 공간 지역성)
  - 단점 
    - block 수가 줄어들며 경쟁 증가 → miss ratio ↑
    - 오염 (pollution) : 필요하지 않은 데이터까지 올러옴
    - miss penalty 증가
      - 완화 방법
        - Early restart : block 다 받기 X, CPU 가 필요한 word 도착 즉시 재개
        - Critical-word-first : CPU 가 필요한 word 를 block 에서 먼저 전송

### ◆ Cache Miss


- Cache Hit → CPU 정상적 진행 
  - Write Hit
    - cache 만 수정하면 cache / memory 불일치 발생
    1. Write-Through 
      - cache 에 쓸 때 memory 도 같이 수정
      - 단점 : memory 에 접근해야 함 → 성능저하 
    1. Write-Back
      - cache 에 변경하다가, block 이 cache 에서 쫓겨날 때 memory 에 작성
      - Dirty bit : cache 에만 최신 데이터가 있는 상태 표시
      - 내릴 block 이 dirty 하면 memory update 

|  | Write-Through | Write-Back |
|:--|:--|:--|
| 메모리 쓰기 시점 | 쓸 때마다 즉시 | 블록 교체 시에만 |
| 메모리 트래픽 | 많음 | 적음 |
| 구현 복잡도 | 단순 | dirty bit 필요 |
| 성능 | write buffer 없으면 느림 | 일반적으로 빠름 |

    - Write Buffer (둘 다 사용 가능)
      - memory 에 쓸 데이터를 buffer 에 넣어두고 CPU 다음 명령어 실행
      - background 에서 쓰기 처리. 
      - write buffer 꽉 찼을 시 → stall 발생
- Cache Miss 
  - Read miss
    - CPU pipeline stall
    - 아래 계층에서 block fetch
    - Instruction cache miss → IF 재시작
    - Data cache miss → 데이터 접근 완료
  - Write miss
    1. Write-Through
      - Allocate on miss : miss 나면 block fetch 후 쓰기
      - Write around : block 안 가져오고 바로 memory 에 쓰기
        - ex) initialization
    1. Write-Back
      - Allocate on miss : block fetch 후 쓰기

### ◆ Example : Intrinsity FastMATH


![](/assets/images/notion/[ca]-memory-system-(1)/img_5.png)

- **임베디드 MIPS 프로세서**
  - 12단계 파이프라인
  - 매 사이클마다 명령어 및 데이터 접근
- **분리 cache **: I-cache (명령어) 와 D-cache (데이터) 를 별도로 운영
  - 각각 16KB: 256 block × 16 word/block
  - D-cache: write-through || write-back 방식 사용
- **SPEC2000 miss ratio**
  - I-cache: 0.4%
  - D-cache: 11.4%
  - 가중 평균: 3.2%

## ✦ Cache Performance


### ◆ Main Memory Supporting Caches


- Main memory 로 DRAM 사용
  - 고정 width (ex. 1 word)
  - 고정 width 의 clocked bus 로 연결
    - 일반적으로 CPU clock 보다 느림
- cache → DRAM 에서 block 가져올 때
  1. 주소 전송 (1 cycle) : CPU 가 주소 요청 (한 번만)
  1. DRAM 접근 (15 cycle) : DRAM 이 데이터 준비
  1. 데이터 전송 (1 cycle) : 준비된 데이터 bus 로 전송
  - ex) 4 word 를 1 word 씩 가져오기
    - Miss panalty = 1 + (15 + 1) × 4 = 65
    - 비효율적! → bandwidth 높이자
![](/assets/images/notion/[ca]-memory-system-(1)/img_6.png)

- Increasing Memory Bandwidth
![](/assets/images/notion/[ca]-memory-system-(1)/img_7.png)

  1. bus & memory 의 bandwidth 증가 시키기
    - Miss penalty : 1 + 15 + 1 = 17
  1. Memory 를 4개의 bank 로 나눠서 병렬적 처리
    - Miss penalty : 1 + 15 + (1 × 4) = 20

### ◆ Measuring Cache Performance


- CPU Time
  - 프로그램 실행 cycle : cache hit 시간 포함
  - memory stall cycle : cache miss 인해 발생
![](/assets/images/notion/[ca]-memory-system-(1)/img_8.png)

![](/assets/images/notion/[ca]-memory-system-(1)/img_9.png)

### ◆ Example


- **주어진 조건**
  - I-cache 미스율 = 2%
  - D-cache 미스율 = 4%
  - Miss penalty = 100 사이클
  - Base CPI (이상적인 캐시) = 2
  - Load & Store 명령어 비율 = 36%
- **명령어당 미스 사이클**
  - I-cache: 0.02 × 100 = 2
  - D-cache: 0.36 × 0.04 × 100 = 1.44
- **실제 CPI = 2 + 2 + 1.44 = 5.44**
  - 이상적인 CPU는 5.44/2 = 2.72배 더 빠름

### ◆ Average Access Time


- 평균 메모리 접근 시간 = AMAT (Average Memory Access Time)
  - hit time 관련
- AMAT = Hit time + Miss rate × Miss penalty
  - Hit time      → 캐시에서 데이터를 찾는 데 걸리는 시간 (hit이든 miss든 항상 발생)
Miss rate     → miss가 나는 비율
Miss penalty  → miss 1회당 추가 대기 시간
- ex)
  - 1ns 클럭 CPU, 히트 시간 = 1사이클, Miss penalty = 20사이클, I-cache 미스율 = 5%
  - AMAT = 1 + 0.05 × 20 = **2ns**
    - 명령어당 2사이클

### ◆ Summary


- CPU 성능 ↑ → Miss penalty 중요
- Base CPI ↓ → memory stall 소요 시간 비중 ↑
- Clock 속도 ↑ → memory stall 이 더 많은 CPU cycle 차지
- 시스템 성능 평가 시 cache 동작 중요!
