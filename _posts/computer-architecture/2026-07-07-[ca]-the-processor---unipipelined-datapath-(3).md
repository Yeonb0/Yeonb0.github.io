---
categories:
- Computer-Architecture
date: '2026-07-07T19:35:00.000+09:00'
layout: single
series: 컴퓨터 아키텍쳐
step: 6
tags:
- CPU
- 파이프라인
title: '[CA] The Processor - Unipipelined Datapath (3)'
toc: true
toc_sticky: true
---

## ✦ Data Hazards in ALU Instructions


{% raw %}
```text
sub $2, $1, $3
and $12, $2, $5
or  $13, $6, $2
add $14, $2, $2
sw  $15, 100($2)
```
{% endraw %}

→ Data hazard 발생

  - 해결 : forwarding 
    - 언제 forwarding 해야하는지 how 감지?
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_1.png)

- 실제 값 저장 시점 : CC5 
  - 파란 선 : 종속적. `add` 와 `sw` 는 저장 이후에 forwarding → 올바르게 -20 전송
  - 빨간 선 : forwarding 으로 타이밍 안맞음 → how? 

### ◆ Detecting the Need to Forward


- 언제 fowarding 필요 감지 → register 번호를 pipeline register 에 
- 조건
  1. ID/EX & EX/MEM
    1. ID/EX 의 rs = EX/MEM 의 rd
    1. ID/EX 의 rt = EX/MEM 의 rd
  1. ID/EX & MEM/WB
    1. ID/EX 의 rs = MEM/WB 의 rd
    1. ID/EX 의 rt = MEM/WB 의 rd
- 앞 명령어의 목적지 (rd) ?= 현재 명령어 출처 (rs, rt)
- 예외 
  1. forwarding 명령어가 register 에 write 하는 경우만 해당 
→ `sw` 는 X
  1. rd 가 `$0` 이면 제외 
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_2.png)

- 모든 조건 & 예외 만족 시
  - 뒤쪽 register (EX/MEM or MEM/WB) → 앞쪽 ALU 로 이동
- 실제 하드웨어 제어
  - EX/MEM (10) || MEM/WB (01) → 어디서 forwarrding 되는지 표시

| 신호 | 해저드 종류 | RegWrite<br>(예외 1) | RegisterRd ≠ 0<br>(예외 2) | RegisterRd = ID/EX.RegisterRs/Rt | 값 |
|:--|:--|:--|:--|:--|:--|
| ForwardA | EX 해저드 | O (EX/MEM) | O (EX/MEM) | O (EX/MEM.Rd = ID/EX.Rs) | 10 |
| ForwardB | EX 해저드 | O (EX/MEM) | O (EX/MEM) | O (EX/MEM.Rd = ID/EX.Rt) | 10 |
| ForwardA | MEM 해저드 | O (MEM/WB) | O (MEM/WB) | O (MEM/WB.Rd = ID/EX.Rs) | 01 |
| ForwardB | MEM 해저드 | O (MEM/WB) | O (MEM/WB) | O (MEM/WB.Rd = ID/EX.Rt) | 01 |

- 한 조건이라도 어긋나면 → 00 (forwarding X)

### ◆ Double Data Hazard


{% raw %}
```text
add $1, $1, $2
add $1, $1, $3
add $1, $1, $4
```
{% endraw %}

- 두 hazard 가 동시에 발생
→ 가장 마지막 `add` : EX hazard && MEM hazard

- 우리가 원하는 것 → 가장 최신 값!
  - EX > MEM
- MEM hazard 예외 추가
  - EX hazard 가 아닐 때
  - if (MEM/WB.RegWrite and (MEM/WB.RegisterRd ≠ 0)
and **not** (EX/MEM.RegWrite and (EX/MEM.RegisterRd ≠ 0) 
and (EX/MEM.RegisterRd = ID/EX.RegisterRs))
and (MEM/WB.RegisterRd = ID/EX.RegisterRs))
→ ForwardA = 01
  - if (MEM/WB.RegWrite and (MEM/WB.RegisterRd ≠ 0)
and **not** (EX/MEM.RegWrite and (EX/MEM.RegisterRd ≠ 0) 
and (EX/MEM.RegisterRd = ID/EX.RegisterRt))
and (MEM/WB.RegisterRd = ID/EX.RegisterRt))
→ ForwardB = 0

| 신호 | 해저드 종류 | RegWrite<br>(예외 1) | RegisterRd ≠ 0<br>(예외 2) | EX hazard 아님<br>(예외 3) | RegisterRd = ID/EX.RegisterRs/Rt | 값 |
|:--|:--|:--|:--|:--|:--|:--|
| ForwardA | EX 해저드 | O (EX/MEM) | O (EX/MEM) | — | O (EX/MEM.Rd = ID/EX.Rs) | 10 |
| ForwardB | EX 해저드 | O (EX/MEM) | O (EX/MEM) | — | O (EX/MEM.Rd = ID/EX.Rt) | 10 |
| ForwardA | MEM 해저드 | O (MEM/WB) | O (MEM/WB) | O | O (MEM/WB.Rd = ID/EX.Rs) | 01 |
| ForwardB | MEM 해저드 | O (MEM/WB) | O (MEM/WB) | O | O (MEM/WB.Rd = ID/EX.Rt) | 01 |

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_3.png)

- forwarding 포함 datapath

### ◆ Load-Use Data Hazard


![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_4.png)

- `lw` 는 MEM 이 끝난 후에야 데이터 준비 가능
  - `and` 에게 forwarding 할 데이터 존재 X
  - 해결 : 1 cycle stall (멈추기)
- 조건 
  1. ID/EX MemRead = 1 
→ 현재 단계 명령어가 `lw` ?
  1. ID/EX 의 rt & IF/ID rs/rt
→ 저장할 값을 바로 사용?
→ 모두 참이면 stall + bubble 삽입

- Stall 구현
  1. bubble 삽입 : ID/EX control 신호를 `0` 으로 
→ EX/MEM/WB 단계 `nop` 상태
  1. Pipeline 동결 : PC & IF/ID update 차단
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_5.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_6.png)

→ 더 정확히

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_7.png)

- Hazard 포함 Datapath 
- Stall 의 특징
  - 성능 저하 → but 올바른 결과 위해 반드시 필요
  - compiler : hazard & stall 피하기 위해 코드 재배치 가능 
    - pipeline 구조 알아야 함 (hw & sw)

## ✦ Branch Hazards


![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_8.png)

{% raw %}
```text
36:  sub  $10, $4, $8
40:  beq  $1,  $3, 7
44:  and  $12, $2, $5
48:  or   $13, $2, $6
52:  add  $14, $4, $2
56:  slt  $15, $6, $7
     ...
72:  lw   $4,  50($7)  // branch 이동시
```
{% endraw %}

- branch 단계 → MEM 에서 결정 시 3 cycle 낭비
  - ID 단계에서 결정!
→ Data hazard 가 발생한다면?

- Example
  - Case 1) Forwarding
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_9.png)

    - `add` 결과가 `beq` ID 시점에 사용 가능 → forwarding 만으로 해결 가능
    - ALU 가 앞앞 or 앞앞앞 인 경우
  - Case 2) Forwarding + 1 stall
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_10.png)

    1. 바로 앞 명령어가 ALU 인 경우
    1. 앞앞 명령어가 `lw` 인 경우
  - Case  3) Forwarding + 2 stall
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(3)/img_11.png)

    - `lw` 바로 다음에 `beq` 오는 경우 
→ 비용 가장 높음

## ✦ Fallacies & Pitfalls


### ◆ Fallacies


- Pipelining 은 쉽다 (X)
  - 기본 개념은 쉽다
  - hazard 같은 디테일은 어렵다
- Pipelining 은 기술과 무관하다 (X)
  - transistor 가 발전할 수록 기법 향상 
  - ISA 설계는 기술 트랜드 고려

### ◆ Pitfalls


- 잘못된 ISA 설계는 Pipelining 어렵게 만듬 
  - 복잡한 명령어 집합 → pipelining overhead
  - 복잡한 주소 지정 방식 → reg update side effect, memory 간접 참조
  - delayed branches

### ◆ Concluding Remarks


- ISA ↔ Datapath : 서로 설계에 영향
- Pipelining → 병렬성으로 throughput 상향
  - 명령어 latency 자체는 감소 X
- hazard : structural, data, control
