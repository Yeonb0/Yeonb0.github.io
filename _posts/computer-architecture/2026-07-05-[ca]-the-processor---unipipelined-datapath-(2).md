---
categories:
- Computer-Architecture
date: '2026-07-05T10:29:00.000+09:00'
layout: single
series: 컴퓨터 아키텍쳐
step: 5
tags:
- CPU
- 파이프라인
title: '[CA] The Processor - Unipipelined Datapath (2)'
toc: true
toc_sticky: true
---

## ✦ Pipelineing


### ◆ MIPS Pipeline


- 5 개의 stage
  1. IF : Memory 에서 Instruction (명령어) fetch
  1. ID : Instruction 해독 & register 읽기
  1. EX : operation 실행 or 주소 계산
  1. MEM : memory 피연산자 접근
  1. WB : 결과를 register 에 저장
- Pipeline 사용 시 → stage 수 만큼 빨라짐
- stage 별 소요 시간
  - register 읽기 (2) / 쓰기 (5) → 100ps
  - 그 외 (1, 3, 4) → 200ps
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_1.png)

  - lw 가 가장 걸리는 시간 김 
    - 200ps 기준으로 pipeline 
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_2.png)

### ◆ Pipelining


- Speed up
  - 모든 stage 가 같은 시간 → stage 수 만큼 개선
  - 그러나 stage 마다 같은 시간 X (register 100 ps, 그외 200ps)
    - 속도 향상 적어짐
  - 단위 시간당 완료되는 명령어 수 (Throughput) 증가
  - 각 명령어 처리 시간 (Latency) 은 감소 X
- MIPS ISA Design
  - 모든 명령어는 32 bit
    - 한 사이클에 명령어 fetch & decode 쉬움
  - 명령어 형식 3 가지 → 한 단계에서 decode & register 읽기 가능
  - load /store 주소 지정 방식 → 3 단계에서 주소 계산 & 4 단계에서 memory 접근
  - memory 피연산자 alignment → 메모리 접근 1 cycle 만에 가능

## ✦ Hazard


- 다음 cycle 에 다름 명령어를 시작하지 못하게 하는 상황
  - Structre Hazard : 필요한 자원이 사용중
  - Data Hazard : 이전 명령어의 data 읽기 / 쓰기 완료까지 기다려야 함
  - Control Hazard : 제어 동작 결정이 이전 명령어 결과에 달려 있음

| 구분 | 원인 | 비유 | 연관 단계 |
|:--|:--|:--|:--|
| **Structure Hazard** | 하드웨어 자원 충돌 | 화장실이 하나뿐인데 두 사람이 동시에 쓰려는 상황 | MEM |
| **Data Hazard** | 데이터 의존성 (이전 결과를 기다림) | 케이크 위에 글씨를 써야 하는데, 케이크가 아직 안 구워진 상황 | EX |
| **Control Hazard** | 분기 명령어로 인한 흐름 불확실 | 갈림길에서 어느 길로 갈지 결정되기 전에 미리 출발해버린 상황 | 분기 명령어 (beq, j) |

### ◆ Structure Hazard


- 자원 사용 충돌
- MIPS pipeline → 단일 memory
  - 이전 명령어가 load / store 로 data 접근 중
→ 명령어 fetch 지연
  - pipeline bubble 발생
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_3.png)

- 해결책 :
  - 1 cycle 기다린 후에 실행 
  - instruction memory / data memory 분리 → 동시 접근 가능
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_4.png)

### ◆ Data Hazard


- 한 명령어가 이전 명령어의 데이터 접근 완료에 의존함
→ data dependancy
{% raw %}
```assembly
add $s0, $t0, $t1   ; $t0 + $t1 결과를 $s0에 저장
sub $t2, $s0, $t3   ; $s0 - $t3 결과를 $t2에 저장 (앞에서 만든 $s0가 필요!)
```
{% endraw %}

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_5.png)

- 해결책 : Forwarding (Bypassing)
  - 결과 계산되는 즉시 이용
  - register 에 저장 기다림 X 
  - datapath 에 추가 connection 필요
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_6.png)

    - EX 에서 계산 직후 다음 명령어 EX 로 data 전송
    - 첫 번째 명령어의 MEM 과 WB 는 정상적으로 진행
  - Forwarding 의 한계 : Load-Use Hazard
    - load 한 값은 `MEM` 에 접근한 이후에나 사용 가능 
    - 1 cycle 기다린 후에 forwarding
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_7.png)

    - code 수준 해결법 → lw 명령어를 몰아 쓰자!
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_8.png)

### ◆ Control Hazard


- Branch 가 제어 흐름 결정
  - branch 결과 따라 다음 명령어 결정
  - branch 의 결과 모르면 다음 명령어 fetch 불가능
`EX` 단계 이후에야 분기 가능
- 해결책 : 
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_9.png)

  - 결정 시점 앞당기기
    - branch 결정을 `ID` 단계로 당기기 
      - 전용 comparator 추가 : `ID` 단계에서 register 비교
      - 전용 adder 추가 : `ID` 단계에서 target address 계산
→ 손실 cycle 3개 → 1개로 감소

  - branch 결정 이후 어떻게 대응?
    - branch 판단까지 기다리기 → 항상 손실 발생
    - Predict Not Taken : jump 안한다고 일단 가정
      - 진짜 jump 안할시 → delay X
→ 손실 cycle X 
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_10.png)

      - jump 실제로 발생 → 예측 실패. 1 cycle 기다려야 함
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_11.png)

### ◆ Summary


- Pipeline 은 throughput 개선 O, latency 개선 X
- Hazard 의 영향 받음
- Instruction set design 이 pipeline 구현 복잡도에 영향 미침 

## ✦ MIPS Piplelined Datapath


![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_12.png)

- Pipeline datapath 는 어떻게 생겼는가?
  - 단일 datapath 와 유사
  - 각 영역은 1 cycle 동안 1 가지 역할만 함

| 단계 | 주요 부품 | 역할 |
|:--|:--|:--|
| **IF** | PC, Instruction Memory, +4 가산기 | 명령어 가져오기, 다음 PC 계산 |
| **ID** | Register File, Sign-extend | 명령어 해석, 레지스터 값 읽기 |
| **EX** | ALU, Shift-left-2, 분기 주소 가산기 | 산술/논리 연산, 분기 주소 계산 |
| **MEM** | Data Memory | 메모리 읽기(lw) 또는 쓰기(sw) |
| **WB** | 결과 선택 MUX | 결과를 레지스터 파일에 기록 |

- 거꾸로 흐르는 신호 : `MEM` / `WB` → Control Hazard 원인 

### ◆ Pipleline registers


- stage 사이에 register 필요
  - 이전 cycle 에서 생성된 정보 보관 위해
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_13.png)

  - IF / ID : fetch 한 명령어, PC + 4
  - ID / EX : 읽은 register 2개의 값, sign extended immediate, control 신호
  - EX / MEM : ALU 결과, memory에 쓸 데이터, dest register 번호
  - MEM / WB : memory 에서 읽은 데이터, ALU 결과, dest register 번호
→ 절반씩 칠해서 표현

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_14.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_15.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_16.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_17.png)

- clock 에 동기화 되어 있음 → 매 clock 마다 모든 명령어가 오른쪽으로 이동
{% raw %}
```text
ID 단계: lw의 제어 신호 전부 생성
   ↓ (ID/EX 레지스터에 보관)
EX 단계: EX용 신호 사용, 나머지는 계속 운반
   ↓ (EX/MEM 레지스터에 보관)
MEM 단계: MEM용 신호 사용, WB용 신호는 계속 운반
   ↓ (MEM/WB 레지스터에 보관)
WB 단계: 마지막 남은 WB용 신호 사용
```
{% endraw %}

### ◆ Example


- Load
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_18.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_19.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_20.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_21.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_22.png)

- Bug : write 할 register 의 번호가 다른 명령어 (3 cycle 뒤 명령어) 
{% raw %}
```text
WB  ← lw $t0, 8($s1)     ← 우리가 추적 중인 명령어
MEM ← 다른 명령어 1
EX  ← 다른 명령어 2
ID  ← 다른 명령어 3       ← 지금 ID에 있는 건 완전히 다른 명령어!
IF  ← 다른 명령어 4
```
{% endraw %}

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_23.png)

- 원래 추적 중인 명령어의 write reigster 가 함께 여행해야 함 
→ **IF/ID → ID/EX → EX/MEM → MEM/WB** 파이프라인 레지스터를 차례로 거쳐 운반


- Store 
  - IF / ID 까진 동일
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_24.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_25.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_26.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_27.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_28.png)

- WB 과정 X 

### ◆ Pipleline Diagram


- Multi-Cycle Pipeline Diagram
  - 전체 cycle 이 어떤 식으로 일어나는지 보여줌
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_29.png)

- Single-Cycle Pipeline Diagram
  - Multi 를 수직으로 자른 단면
  - 한 cycle 에서 어떤 일이 일어나고 있는지 보여줌
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_30.png)

- Pipelined Control
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(2)/img_31.png)
