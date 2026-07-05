---
categories:
- Computer-Architecture
date: '2026-07-05T10:28:00.000+09:00'
layout: single
series: 컴퓨터 아키텍쳐
step: 4
tags:
- CPU
title: '[CA] The Processor - Unipipelined Datapath (1)'
toc: true
toc_sticky: true
---

## ✦ Introduction


### ◆ Instruction Execution


- 명령어 실행 단계
  1. PC (Program Counter) → 명령어 memory 로부터 명령어 fetch
    - 이때 명령어에 register 번호 포함
  1. 명령어 필드 사용해 register 읽기
  1. 명령어 실행하기 → 어떤 멍령어 인지 따라 다른 행동
    - ALU 사용 (jump 제외 모든 명령어)
      - Arithmetic
      - load / store 
      - Branch targer address
    - data memory 접근 (load / store 위해)
  1. PC update → PC + 4 또는 target addreess

### ◆ CPU Overview


![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_1.png)

- MUX 1 → PC 의 다음 주소 결정
  - PC + 4
  - Branch Address
- MUX 2 → register 의 data 값 결정
  - ALU 된 값 (rs & rt) 
  - Memory 값
- MUX 3 → ALU 의 두 번째 입력 결정
  - register 값
  - 명령어 수치 (immediate)

## ✦ Logic Design Basics


- low voltage = 0 / high voltage = 1
- 1 wire 당 1 bit

### ◆ Combinational element


- 데이터 값에 대해 연산 수행
- 현재 입력에 의해서만 출력 결정 (memory component X)
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_2.png)

- 같은 입력 → 같은 출력 
- ex) ALU

### ◆ State element


= sequential element 

- memory component 지님 (내부 기억 장소 O)
  - 2 input
    - 기록할 data
    - clock
  - 1 output
    - 이전 clock cycle 에 기록된 값
- ex) D filp-flop
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_3.png)

- Register : data 를 기록 
  - Clk 이 0 → 1 로 바뀔 때 update
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_4.png)

  - write control 이 있으면
    - write control = 1 && Clk 0 → 1 일때만 update
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_5.png)

### ◆ Store element


- Register 에 저장
  - 1 input 
    - rd (write data)
  - 2 output
    - Read data 1 ← select by rs
    - Read data 2 ← select by rt
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_6.png)

  - 한 Clk 안에 2 register read & 1 register write 동시에 가능 
    - How? memory 에서 load 하는 것이 아닌 이전 operation (rs & rt) 결과 바로 사용
- Memory 에 저장
  - 1 input
    - write data (store)
  - 1 output
    - read data (load) 
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_7.png)

  - Address : read / write 될 memory 주소
    - MemRead = 1 → load 될 위치
    - MemWrite = 1 → store 할 위치
  - CLK → write 에만 사용 (to synchronize)

### ◆ Clocking Methodology


- Clock → 언제 값을 저장할지 결정
- Combinational logic 은 clock 과 무관하게 즉시 계산 → clock edge 중간에 계산 끝

## ✦ Building a Datapath


- Datapath : CPU 에서 data 나 addreess 연산하는 elements 
  - ex) register, ALU, MUX, memory
  - 기본 요소
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_8.png)

### ◆ Instruction Fetch


- 명령어 가져오기
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_9.png)

### ◆ R-format Instructions


- `add rd, rs, rt`
- `sub rd, rs, rt`
→ register 3 개 사용

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_10.png)

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_11.png)



### ◆ I-format Instructions


- `lw rt, imm(rs)` 
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_12.png)

  - 1 cycle 만에 load
- `sw rt, imm(rs)`
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_13.png)

- `beq rs, rt, L1`
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_14.png)

- `ori, rt, rs, imm`
→ register 2 개 + imm / mem 사용

- Branch 는 PC 상대적으로 addressing 
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_15.png)

### ◆ J-format Instruction


- `j target`
![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_16.png)

- 고정 주소 사용 (target × 4)

| 2 | address |
| 31 : 26 | 25 : 0 |

- PC update → 총 32 bit
  - (PC + 4) + (jump addr * 4)

| PC + 4 | jump << 2 |
| 31 : 28 | 27 : 0 |

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_17.png)

### ◆ Address


- PC 에 저장되는 값은 항상 4의 배수
  - Sequential
    - PC [31:0] = PC[31:0] + 4
  - Branch operation
    - PC [31:0] = PC[31:0] + 4 + SignExtension(imm) * 4
- PC 의 끝 2 bit (LSB) 는 항상 0 → 사용 X
  - Sequential
    - PC [31:2] = PC[31:2] + 1
  - Branch operation
    - PC [31:2] = PC[31:2] + 1 + SignExtension(imm) 

### ◆ Full Datapath


![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_18.png)

## ✦ Control


### ◆ ALU Control


- ALU 가 어떤 연산을 할 건지 결정 → 4 bit
- Load / Store : add (0010)
- Branch : subtract (0110) → 비교 위해
- R-type : 어떤 명령어인지에 따라 function 결정 

| opcode | ALUOp (2bit) | Operation | funct | ALU function | ALU control (4bit) |
| lw | 00 | load word |  | add | 0010 |
| sw | 00 | store word |  | add | 0010 |
| beq | 01 | branch equal |  | subtract | 0110 |
| R-type | 10 | add | 100000 | add | 0010 |
|  |  | subtract | 100010 | subtract | 0110 |
|  |  | AND | 100100 | AND | 0000 |
|  |  | OR | 100101 | OR | 0001 |
|  |  | set-on-less-than | 101010 | set-on-less-than | 0111 |

![](/assets/images/notion/[ca]-the-processor---unipipelined-datapath-(1)/img_19.png)

### ◆ Instruction Control


- X → 0 / 1 아무거나 상관 없음
- read / write 는 명시적으로 disable 해야 함

| Signal | 선택 | Value `0` | Value `1` |
| RegDst | write 할 register | `rt` 선택 | `rd` 선택 |
| RegWrite | register 에 write | write X | write O |
| ALUSrc | ALU 두 번째 피연산자 | register `rt` | immediate |
| ALUOp | 어떤 연산 → OP code |  |  |
| MemWrite | memory 에 write | write X | write O |
| MemRead | memory 에서 read | read X | read O |
| MemtoReg | reg에 저장할 데이터 | ALU output | memory output |
| PCSrc | 다음 PC | PC + 4 | PC + 4 + offset * 4 |
| Jump | Jump? |  | Jump O |

- R-format instruction control

| Signal | 선택 |
| RegDst | 1 |
| RegWrite | 1 |
| ALUSrc | 0 |
| ALUOp | OP (명령어 따라) |
| MemWrite | 0 |
| MemRead | 0 |
| MemtoReg | 0 |
| PCSrc | 0 |

- Ioad word 

| Signal | 선택 |
| RegDst | 0 |
| RegWrite | 1 |
| ALUSrc | 1 |
| ALUOp | add (0010) |
| MemWrite | 0 |
| MemRead | 1 |
| MemtoReg | 1 |
| PCSrc | 0 |

- store word

| Signal | 선택 |
| RegDst | X |
| RegWrite | 0 |
| ALUSrc | 1 |
| ALUOp | add (0010) |
| MemWrite | 1 |
| MemRead | 0 |
| MemtoReg | X |
| PCSrc | 0 |

- branch

| Signal | 선택 |
| RegDst | X |
| RegWrite | 0 |
| ALUSrc | 0 |
| ALUOp | sub (0110) |
| MemWrite | 0 |
| MemRead | 0 |
| MemtoReg | X |
| PCSrc | 1 |

- jump

| Signal | 선택 |
| RegDst | X |
| RegWrite | 0 |
| ALUSrc | X |
| ALUOp | X |
| MemWrite | 0 |
| MemRead | X |
| MemtoReg | X |
| PCSrc | X |
| Jump | 1 |

- Summary

| Signal | R-format | lw | sw | beq | j |
| RegDst | 1 | 0 | X | X | X |
| RegWrite | 1 | 1 | 0 | 0 | 0 |
| ALUSrc | 0 | 1 | 1 | 0 | X |
| ALUOp | OP (명령어 따라) | add (0010) | add (0010) | sub (0110) | X |
| MemWrite | 0 | 0 | 1 | 0 | 0 |
| MemRead | 0 | 1 | 0 | 0 | X |
| MemtoReg | 0 | 1 | X | X | X |
| PCSrc | 0 | 0 | 0 | 1 | X |
| Jump | 0 | 0 | 0 | 0 | 1 |

### ◆ 성능 이슈


- lw 는 여러 명령어 중 실행 시간이 가장 김 → clock 기준 
→ pipelining 으로 개선
