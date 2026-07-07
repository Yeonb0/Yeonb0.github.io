---
categories:
- Computer-Architecture
date: '2026-07-07T19:39:00.000+09:00'
layout: single
series: 컴퓨터 아키텍쳐
step: 9
tags:
- 메모리
- 버츄얼 메모리
- Cache
- VM
title: '[CA] Memory System (3)'
toc: true
toc_sticky: true
---

## ✦ Virtual Memory


### ◆ Virtual Memory


- CPU 의 보조 저장 → cache
- 보조저장장치 (disk) 의 cache → main memory 활용
  - CPU & OS 가 공동 관리
- 프로그램들은 main memory 공유
  - 각 프로그램은 private virtual address space 가짐
    - 자주 사용하는 코드 & 데이터 저장
  - 다른 프로그램으로부터 보호
- CPU & OS : virtual address → physical address 변환
  - VM 의 block : page
  - VM 변환 miss : page fault
![](/assets/images/notion/[ca]-memory-system-(3)/img_1.png)

![](/assets/images/notion/[ca]-memory-system-(3)/img_2.png)

- VM address : page (block) number + page (block) offset
  - 4k (4096 → 12 bit 사용)

### ◆ Page Fault


- Page Fault Penaly 
  - Page fault 발생 → disk 에서 page 가져오기
    - 수백만 clock cycle 필요
    - OS 에 의해 처리
  - page fault rate 최소화
    - Fully associative placement (S = 1)
    - 똑똑한 replacement algorithm
- Page table
  - virtual address → physical address 변환 정보 저장
  - virtual page number 를 index 로 사용해 PTE 찾기
  - page 가 memory 에 있음
    - PTE : physical page number 저장
    - 추가적 status bit : referenced, dirty, …
  - page 가 memory 에 없음
    - PTE : disk 의 swap space 참조
![](/assets/images/notion/[ca]-memory-system-(3)/img_3.png)

![](/assets/images/notion/[ca]-memory-system-(3)/img_4.png)

## ✦ Page Fault 처리 & TLB


### ◆ Replacement and Writes


- LRU (Least Recently Used) 사용
  - page 접근 시 PTE 의 reference bit (= use bit) 1로 설정
  - OS 의해 주기적으로 0 초기화
  - reference bit = 0 인 page → 최근에 사용 X
- Disk write → 수백만 cycle 소요
  - block 단위로 한번에 처리
  - Write-through (매번 즉시 반영) → 비실용적
Write-back (교체 시점 한번에 반영) → 사용
  - page write 될 때 PTE 의 dirty bit 설정

### ◆ TLB


- Virtual address 변환 → 매번 page table 접근해야 함 
  - 2번의 memory 참조 필요
    - PTE 접근
    - 실제 memory 접근
- TLB (Translation Look-aside Buffer)
  - CPU 내부의 PTE 저장 cache
  - PTE 의 locality 좋은 성질 이용
  - 16~512개의 PTE 
    - hit 시 0.5~1 cycle
    - miss 시 10~100 cycle
    - miss rate 0.01%~1%
  - miss → hardware or software 로 처리
![](/assets/images/notion/[ca]-memory-system-(3)/img_5.png)

- TLB Miss
  - page 가 memory 에 있음
    - memory 에서 PTE 불러와 재시도
    - hardware 로 처리 → 복잡한 page table 구조에서는 복장 가능
    - software 로 처리 → 최적화된 handler + special exception
  - page 가 memory 에 없음 (page fault)
    -  OS 가 page 가져오고 page table 업데이트
    - fault 발생한 명령어 재시작
- Miss Handler
  - 두 가지 miss
    - Page O PTE X
    - Page X 
  - destination register 가 덮어써지기 전에 TLB miss 감지해야 함
→ Exception 발생 
  - Handler 가 memory → TLB 로 PTE 복사
    - 명령어 재시작
    - Page 없으면 page fault 발생
- Page Fault
  1. fault 난 virtual address PTE를 찾음 → disk에서 page 위치 확인
  1. memory에서 교체할 page 선택 (dirty bit = 1 이면 disk에 write-back)
  1. disk → memory로 page 복스 & page table 갱신
  1. fault가 발생했던 명령어부터 재실행

## ✦ Memory Hierarchy


1. 데이터 어디에 배치? (block placement)
1. 데이터 어떻게 찾음? (finding a block)
1. miss  발생 시 무엇을 교체? (replacement)
1. 데이터 어떻게 write? (write policy)

### ◆ Block Placement


- by Associativity
- Direct mapped (1-way associative)
  - 배치 위치가 하나로 고정
  - E = 1
- n-way set associative
  - 하나의 set 내에서 n개의 선택지
  - S > 1 & E > 1
- Fully associative
  - 어느 위치든 가능
  - S = 1
- Associativity ↑ 
  - miss rate ↓
  - 복잡도, 비용, 접근 시간 ↑ 

### ◆ Finding a Block



| Associativity | 위치 탐색 방법 | Tag 비교 횟수 |
|:--|:--|:--|
| Direct mapped | Index | 1 |
| n-way set associative | Set index로 찾은 후 set 내 entry 탐색 | n |
| Fully associative | 모든 entry 탐색 | entry 수 |
|  | Full lookup table | 0 |

- Hardware cache
  - 비용 절감을 위해 비교 횟수 ↓
- Virtual memory
  - Full table lookup → fully associative 가능
  - Miss rate ↓

### ◆ Replacement


- Miss 발생 시 교체할 line 선택
  - LRU (Least Recently Used) : associativity 높으면 비용 ↑
  - Random : LRU 와 유사 성능, 구현 쉬움
- Virtual Memory 
  - hardware 지원으로 LRU 근사

### ◆ Write Policy


- Write-through
  - 상위 & 하위 모두 업데이트
  - Replacement가 단순, but write buffer가 필요할
- Write-back
  - 상위만 업데이트
  - Block이 교체될 때만 하위 업데이트
  - 더 많은 state를 유지 (dirty bit)
- Virtual memory → write-back 만 가능

### ◆ Miss 종류


- Compulsory miss (= cold start miss)
  - Block 첫 번째 접근 시
- Capacity miss
  - 교체된 block에 다시 접근
  - cache 크기 유한해서 발생
- Conflict miss (collision miss라고도 함)
  - Set 내 entry 경쟁으로 인해 발생
  - Fully associative 아닌 cache에서 발생
  - 동일한 총 크기의 fully associative cache에선 발생 X

| 설계 변경 | Miss rate에 대한 영향 | 부정적 성능 영향 |
|:--|:--|:--|
| Cache 크기 증가 | Capacity miss 감소 | 접근 시간 증가 가능 |
| Associativity 증가 | Conflict miss 감소 | 접근 시간 증가 가능 |
| Block 크기 증가 | Compulsory miss 감소 | Miss penalty 증가. <br>매우 큰 block 크기 → pollution으로 인해 miss rate가 증가 |
