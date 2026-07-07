---
categories:
- Computer-Architecture
date: '2026-07-07T19:39:00.000+09:00'
layout: single
series: 컴퓨터 아키텍쳐
step: 8
tags:
- 메모리
- Cache
- Buffer
title: '[CA] Memory System (2) '
toc: true
toc_sticky: true
---

## ✦ Associative Cache


- Fully associative
  - S (set) 이 1 로 고정 
  - 어떤 block 이든 cache 의 빈 곳 아무데나 들어 갈 수 있음
  - hit 확인하려면 모든 항목 동시에 비교 해야 함 → 비쌈
  - 모든 항목마다 comaparator 필요
- n-way set associative
  - E > 1 && S > 1
  - cache 를 여러 set 으로 나누고 block number 의 modulo 로 어떤 set 들어갈지 결정 
  - 현재 대부분의 cache가 사용
  - entry (line) 만큼의 comparator 필요
![](/assets/images/notion/[ca]-memory-system-(2)/img_1.png)

- Directed mapped 
  - 12 (`1100`) → block 4 에 저장
- Set associative
  - 12(`1100`) → 4로 나누면 0 → set 4 찾기
- Fully associative 
  - 모든 line (entry) 찾기 

### ◆ Spectrum of Associativity


![](/assets/images/notion/[ca]-memory-system-(2)/img_2.png)

- One-way set associative (direct mapped)
  - S = 8
  - Block, Tag, Data 구조로 0~7번 항목
- Two-way set associative
  - S = 4
  - Set 0~3, 각 set에 Tag+Data가 2개씩
- Four-way set associative
  - S = 2 
  - Set 0~1, 각 set에 Tag+Data가 4개씩
- Eight-way set associative (fully associative)
  - S = 1
  - Set 없이 Tag+Data가 8개 나란히

| 방식 | S | E | 특징 |
|:--|:--|:--|:--|
| Direct mapped | 8 | 1 | 각 block이 딱 1곳에만 들어갈 수 있음 |
| 2-way set associative | 4 | 2 | 각 block이 set 내 2곳 중 선택 가능 |
| 4-way set associative | 2 | 4 | 각 block이 set 내 4곳 중 선택 가능 |
| Fully associative | 1 | 8 | 어디든 들어갈 수 있음, S=1이므로 index bit = 0 |

### ◆ Example


 Yellow : New (Miss)

Red : Miss

Blue : Hit

- 4-block cache 비교 : 접근 순서 0 → 8 → 0 → 6 → 8
- Directed mapped
  - S = 4, E = 1
  - 0 → 0 (`00`)
  - 6 → 2 (`10`)
  - 8 → 0 (`00`)

| Block address | Cache index | Hit/miss | 0 | 1 | 2 | 3 |
|:--|:--|:--|:--|:--|:--|:--|
| 0 | 0 | miss | Mem[0] |  |  |  |
| 8 | 0 | miss | Mem[8] |  |  |  |
| 0 | 0 | miss | Mem[0] |  |  |  |
| 6 | 2 | miss | Mem[0] |  | Mem[6] |  |
| 8 | 0 | miss | Mem[8] |  | Mem[6] |  |

  - 5번 접근 모두 miss 
  - 0 과 8 이 모두 `0` 번 slot 사용 → 계속 충돌 일어남 
- 2-way set associative
  - S = 2, E = 2
  - 0 → 0 (`0`)
  - 8 → 0 (`0`)
  - 6 → 0 (`0`)

| Block address | Cache index | Hit/miss | Set 0 |  | Set 1 |  |
|:--|:--|:--|:--|:--|:--|:--|
| 0 | 0 | miss | Mem[0] |  |  |  |
| 8 | 0 | miss | Mem[0] | Mem[8] |  |  |
| 0 | 0 | hit | Mem[0] | Mem[8] |  |  |
| 6 | 0 | miss | Mem[0] | Mem[6] |  |  |
| 8 | 0 | miss | Mem[8] | Mem[6] |  |  |

  - miss 4번
- Fully associative
  - S = 1, E = 4

| Block address | Hit/miss | Line 1 | Line 2 | Line 3 | Line 4 |
|:--|:--|:--|:--|:--|:--|
| 0 | miss | Mem[0] |  |  |  |
| 8 | miss | Mem[0] | Mem[8] |  |  |
| 0 | hit | Mem[0] | Mem[8] |  |  |
| 6 | miss | Mem[0] | Mem[8] | Mem[6] |  |
| 8 | hit | Mem[0] | Mem[8] | Mem[6] |  |

  - miss 3번

### ◆ How Much Associativity


- 얼마나 많은 연관성 필요?
- Associativity ↑ (E 갯수) → miss rate ↓
  - but 효과 점점 감소
![](/assets/images/notion/[ca]-memory-system-(2)/img_3.png)

- t : 22 / s : 8 / b : 2
- index (S) 로  set 선택
- 선택된 행에서 4개의 line 을 동시에 읽음 
- 각 line 의 tag & valid 비교
  - 4-way 이므로 comparator 4개 필요
- 4 comparator 중 일치 → Hit ⇒ 해당 line data 출력
{% raw %}
```text
주소 입력
  ↓
Index → 해당 set의 행 선택
  ↓
4개 way 동시 Tag 비교 (병렬)
  ↓
Hit? → multiplexor로 해당 way의 Data 출력
Miss? → 하위 memory에서 데이터 가져옴
```
{% endraw %}

### ◆ Replacement Policy


- Direct mapped : miss 마다 바꿈
- Set associative
  - valid bit = 0 우선 선택
  - 모두 사용중이면 항목 중 선택
- 선택 방법
  - Least-recently used (LRU)
    - 가장 오랫동안 사용되지 않은 것 선택
    - 2-way → 간단 / 4-way → 관리 가능 / 그 이상은 어려움
  - Random
    - 높은 associativity (E 갯수 ↑) 에서 LRU 와 성능 비슷

### ◆ Multilevel Caches


- Primary cache → CPU 에 연결
  - 작지만 빠름
- Level-2 cache → primary cache miss 처리
  - L1 보다 크고 느림, main memory 보단 빠름
- Level-3 cache (일부)
- Main memory → L2 (& L3) miss 처리
![](/assets/images/notion/[ca]-memory-system-(2)/img_4.png)
