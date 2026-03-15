---
categories:
- Computer-Architecture
date: '2026-03-15T19:56:00.000+09:00'
tags:
- 성능
- 전력
title: '[CA] Computer Abstractions and Technology'
toc: true
toc_sticky: true
---

## ✦ 컴퓨터 혁명


- 컴퓨터 기술의 발전
  - Moore’s law (무어의 법칙) 이 뒷받침
→ 성능의 상승 : not linearly, but exponentially

![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_1.png)

- 새로운 App 을 가능하게
  - Mobile Computing : 휴대전화
  - Bioengineering : 인간 게놈 프로젝트
  - Data Mining : World Wide Web (WWW), 검색 엔진
  - Maching Learning, Deep Learning 등
- 컴퓨터는 만연하다

### ◆ Computer 의 종류


- Desktop Computer
  - 일반적 목적, 다양한 소프트웨어
  - 비용 ↔ 성능 절충 관계
- Server Computer
  - 네트워크 기반 
  - 높은 용량, 성능, 신뢰성
  - 작은 서버 ~ 건물 크기까지
- Embedded computers
  - 밖에선 안에 컴퓨터 기술 있는지 모름
  - 최소 성능, 가격 & 전력 소모 최소화

### ◆ Post PC Era


- Personal Mobile Device (PMD)
  - 배터리로 동작
  - 무선으로 인터넷 연결
  - 수백 달러
ex) 스마트폰, 태블릿, 전자 안경 등.

- Cloud Computing
  - Warehouse Scale Computers (WSC)
  - Software as a Service (SaaS)
ex) Amazon, Google

![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_2.png)

→ 최근의 Smart Phone 과 PC 생산량 비교

## ✦ Program 밑의 세계


### ◆ Program 실행 구조


![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_3.png)

- Application Software : 고급 언어로 쓰임
- System Software 
  - Compiler : 고급 언어 → 기계어로 번역
  - OS : 운영 체제
- Hardware : Processor (CPU), memory, I/O controller
→ 만약 Application Software 내부적으로 기계어로 컴파일이 가능하다면 System Software 거치지 않아도 됨.

### ◆ Program Code 의 레벨


- 고급 언어 (High-level language)
ex) C

{% raw %}
```c
Swap(int v[], int k)
{
  int temp;
  temp = v[k];
  v[k] = v[k+1];
  v[k+1] = temp;
}
```
{% endraw %}

- Assembly language : instruction 의 텍스트화
{% raw %}
```assembly
swap:
  muli $2, $5, 4
  add  $2, $4, $2
  lw   $15, 0($2)
  lw   $16, 4($2)
  sw   $16, 0($2)
  sw   $15, 4($2)
  jr   $31
```
{% endraw %}

- Hardware representation 
  - 0, 1 로 구성
  - 1줄 당 Assembly language 한 줄에 해당 (32 bit)
{% raw %}
```text
0000000010100001000000000011000
00000000000110000001100000100001
10001100011000010000000000000000
10001100111000100000000000000100
10101100011000010000000000000000
10101100111000100000000000000100
00000011111000000000000000001000
```
{% endraw %}

## ✦ 컴퓨터의 구조


### ◆ 컴퓨터 구성 요소


- 대부분의 컴퓨터에서 동일한 구성 요소 : Desktop, Server, Embedded
- 입/출력 (input/output)
  - 사용자 인터페이스 : 모니터, 키보드, 마우스
  - 저장 장치 : 하드 디스크, CD/DVD, flash 메모리
  - 네트워크 : 다른 컴퓨터와 소통
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_4.png)

- 메모리 (memory)
- 프로세서 (processor)

### ◆ Mouse & Monitor


- Optical mouse (광학 마우스) → Roller-boll 모델 대체
  - LED 가 바닥면 비춤
  - 작은 저해상도 카메라
  - Basic image processor : x, y 움직임 감지
  - 버튼, 휠
- LCD Screen 
  - frame buffer memory
  - R, G, B (각 8 bit 할당) 로 색 만듬

### ◆ 컴퓨터 & 핸드폰 뜯어보기


- 컴퓨터
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_5.png)

  - Processor (CPU) : 열 발생
  - Fan : CPU 에서 발생하는 열 식혀주는 쿨러 역할
  - Motherboard (메인보드) : 컴퓨터 부품 연결 중앙 회로 기판
  - Memory
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_6.png)

- 스마트폰 (애플)
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_7.png)

### ◆ CPU 의 구조


- Datapath : data operation 실행
- Control : datapath, memory 순서대로 제어
- Cache memory : 데이터 즉시 접근 위한 작고 빠른 SRAM 메모리
- example
  - AMD : 4 processor core
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_8.png)

  - Apple A12 processor 
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_9.png)

→ 4개의 big core (CPU), GPU, NPU, cache 등으로 구성

- Abstraction : Hardware -Software Interface 
  - Instruction Set Architecture (ISA)
    - Assembly 언어에서 사용 가능한 명령어 종류
→ 회사마다 ISA 다름 (Intel, ARM, MIPS)

    - ISA 가 다르면 CPU 구조도 다름
  - Application Binary Interface (ABI)
    - ISA + OS

### ◆ Data 저장소


- Main memory (volatile) : instruction 이나 data 가 전원이 꺼지면 사라짐
- Secondary memory (non-volatile) : 전원이 꺼져도 사라지지 않음
  - Magnatic disk
  - Flash memory
  - Optical disk (CDROM, DVD)

### ◆ Network


→ I/O device

- Communication & Resource sharing
- Local Area Network (LAN) : Ethernet
- Wide Area Network (WAN) : Internet
- Wireless network : WiFi, Bluetooth

## ✦ Technology Trend


- DRAM capacity 의 증가
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_10.png)

## ✦ Performance


### ◆ 성능은 분야마다 다르다


- Algorithm : Big - O notation
ex) O(m²) < O(n log n)

- 프로그래밍 언어 : Operation 실행에 필요한 machine instruction 수
- CPU & memory : instruction 실행 속도
- I/O system : I/O opreation 실행 속도

### ◆ CPU 성능 측정 기준


- Response Time (응답 시간) : 한 task 할 때 걸리는 시간
- Throughput : 단위 시간 동안 끝내는 task 수
→ Response Time 감소하면 자동적으로 Thoughput 감소

→ Response Time 에 집중

### ◆ Measuring Execution Time


- Elapsed time : 전체 응답 시간
  - CPU processing + OS + I/O 시간 
- CPU time = Execution time
  - CPU 를 사용한 실제 시간만 계산
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_11.png)

### ◆ Relative Performance


<div class="equation-box">

$$
\frac{\text{Performance}_x}{\text{Performance}_y} = \frac{\text{Execution time}_y}{\text{Execution time}_x} = n
$$

</div>

→ Performance 와 Execution time 은 반비례

- Example 
  - 어떤 프로그램을 실행하는데 A 는 10s, B 는 15s 걸림
→ A 는 B 보다 \frac{15}{10} = 1.5 배 빠름

### ◆ CPU Clocking


![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_12.png)

- Clock period : 한 Clock cycle 에 걸리는 시간
ex) 250ps = 0.25ns = 250 \times 10^{-12}s

- Clock rate (frequency) : 초당 Clock cycle 횟수
ex) 4.0 GHz = 4000MHz = 4.0 \times 10^9 Hz

### ◆ CPU Time


<div class="equation-box">

$$
\begin{aligned}\text{CPU Time} &= \text{CPU Clock Cycles} \times \text{Clock Cycle Time} \\                &= \frac{\text{CPU Clock Cycles}}{\text{Clock Rate}}\end{aligned}
$$

</div>

- Performance 줄이기 (CPU Time 줄이기)
  - 실행 시 필요한 Clock Cycle 줄이기
    - Code Optimization
  - Clock Rate 늘리기
→ CPU 성능 개선

- Example
  - A : 2 GHz clock, 10s CPU time
  - B 를 만들고 싶음
    - CPU time 6s 목표
    - clock cycle × 1.2
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_13.png)

### ◆ Instruction Count and CPI


<div class="equation-box">

$$
\text{Clock Cycles} = \text{Instruction Count} \times \text{Cycles per Instruction}
$$

</div>

<div class="equation-box">

$$
\begin{aligned}
\text{CPU Time} &= \text{Instruction Count} \times \text{CPI} \times \text{Clock Cycle Time} \\
&= \frac{\text{Instruction Count} \times \text{CPI}}{\text{Clock Rate}}
\end{aligned}
$$

</div>

- Instruction Count : 명령어 갯수
→ 프로그램, ISA, compiler 의해 결정

- Cycles per Instruction (CPI) : 한 명령어 실행하는 데 필요한 cycle 수
→ CPU hardware 의해 결정

  - 명령어 마다 CPI 다를 수 있음 → 평균 CPI 사용
ex) 

![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_14.png)

- Performance 높이기
  - CPI 수 줄이기
  - Instruction 수 줄이기
  - 초당 Cycle 수 늘리기 (Clock Rate)
- Example 1
  - A : Cycle Time = 250 ps, CPI = 2.0
  - B : Cycle TIme = 500 ps, CPI = 1.2
  - Same ISA (Assembly 언어, 즉 Instruction Count가 같음)
→ 어떤 컴퓨터가  더 빠른가?

![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_15.png)

- Example 2
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_16.png)

  - Avg CPI 는 보통 floating point 값
- 총 Clock Cycle : Σ 각 명령어의 필요 IC 갯수 × Instruction 마다 걸리는 Cycle 수
<div class="equation-box">

$$
\text{Clock Cycles} = \sum^n_{i=1}(\text{CPI}_i \times \text{Instruction Count}_i)
$$

</div>

- Weighted Avg.CPI (일반적 CPI)
<div class="equation-box">

$$
\text{CPI} = \frac{\text{Clock Cycles}}{\text{Instruction Count}} = \sum^n_{i=1}(\text{CPI}_i \times \frac{\text{Instruction Count}_i}{\text{Instruction Count}})
$$

</div>

→ 다른 Cycle 가진 명령어 마다 몇 번 사용하는지에 따라 다르게 계산

- 총 Execution Time : 어떤 두 가지 비교 위해서 사용
<div class="equation-box">

$$
\text{Execution Time} = \text{IC} \times \text{CPI} \times \text{CCT}
$$

</div>

### ◆ Summary


<div class="equation-box">

$$
\text{CPU Time} = \frac{\text{Instructions}}{\text{Program}} \times \frac{\text{Clock cycles}}{\text{Instruction}} \times \frac{\text{Seconds}}{\text{Clock cycle}}
$$

</div>

- Performace 는 다음에 따라 변한다.
  - Algorithm : IC. (CPI 에도 영향 미칠 수 있음)
  - 프로그래밍 언어 : IC, CPI
  - compiler : IC, CPI
  - Instruction Set Architecture : IC, CPU, T{}_c

## ✦ Power


- P = P_{dynamic} + P_{static} 
  - dynamic power : 어떤 활동하면 늘어나는 power → 조절 대상!
  - static power : 아무런 활동하지 않아도 사용하는 power 
  - tempurature (온도) 와도 관련 있음
- Power Trend
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_17.png)

### ◆ Dynamic Power


<div class="equation-box">

$$
\text{Power} = \text{Capacitive Load} \times \text{Voltage}^2 \times \text{Frequency}
$$

</div>

ex) Capacitive Load 기존의 85%
       Voltage, frequency 15% 감소

<div class="equation-box">

$$
\frac{P_{new}}{P_{old}} = \frac{C_{old} \times 0.85 \times ({V_{old}} \times 0.85)^2 \times F_{old} \times 0.85}{C_{old} \times {V_{old}}^2 \times F_{old}} = (0.85)^4 = 0.52
$$

</div>

→ voltage, heat 줄이기의 한계 도달. how improve performance?

## ✦ Processor Core


### ◆ Uniprocessor


- processor 가 1개
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_18.png)

→ 점차 발전 속도의 느려짐

### ◆ Multiprocessor


- processor 여러 개 사용

## ✦ Chip


- 반도체 칩 만드는 과정
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_19.png)

- Yield (수율) : 한 wafer 에서 working 하는 die 의 비율

### ◆ Integrated Circuit Cost


<div class="equation-box">

$$
\text{Cost per die} =\frac{\text{Cost per wafer}}{\text{Dies per wafer} \times \text{Yield}}\\
$$

</div>

<div class="equation-box">

$$
\text{Dies per wafer} =\frac{\text{Wafer area}}{\text{Die area}}
$$

</div>

<div class="equation-box">

$$
\\
\text{Yield} =\frac{1}{\left(1 + \left(\text{Defects per area} \times \frac{\text{Die area}}{2}\right)\right)^2}
$$

</div>

- Chip 크기가 커지면 Yield 낮아짐. 

## ✦ Benchmark


### ◆ SPEC CPU Benchmark


- CPU 성능 측정
- Standard Performance Evaluation (SPEC) 회사 제작
- SPEC CPU 2006 : 2006년에 개발된 벤치마크 프로그램
  - I/O 없이 CPU 성능만 check (Elapsed time 체크)
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_20.png)

- performance ratio → geometric mean (기하 평균) 으로 구하기
<div class="equation-box">

$$
\sqrt[n]{\prod_{i=1}^{n} \text{Execution time ratio}_i}
$$

</div>

  - 특정 성능 높은 것보다 골고루 일정한 성능 나오는 게 더 어려움. 그걸 반영하기 위한 기하 평균

### ◆ SPEC Power Benchmark


- 서버에서 다양한 부하 수준 (Target Load) 에서 전력 (watts) 대비 성능 (ssj_ops) 측정
  - Performance : ssj_ops (server side Java operations) / sec. 서버가 1초 동안 처리한 작업 수
  - Power : Watts 
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_21.png)

## ✦ Pitfall (함정) & Fallacy (오류)


### ◆ Pitfall : Amdahl’s law


- 프로그램에서 개선할 수 있는 부분 / 개선 불가능한 부분이 나눠져 있을 때, processor 수를 늘려도 성능 향상에 한계 생김
<div class="equation-box">

$$
\text{T}_\text{improved} = \frac{\text{T}_\text{affected}}{\text{improvement factor}} + \text{T}_\text{unaffected}
$$

</div>

  - 한계? Unaffected 부분

### ◆ Fallacy : Low Power at Idle


- CPU 가 일을 거의 하지 않으면 전력 소모가 낮다 → 오류
![](/assets/images/notion/[ca]-computer-abstractions-and-technology/img_22.png)

  - 10% 와 50% 의 전력 소모는 비슷
  - power 랑 load 는 비례하지 않는다

### ◆ Pitfall : MIPS as a Performance Metric


- MIPS : 1초에 실행할 수 있는 명령어 수
→ CPU 성능 비교 기준 X

  - 같은 기능, 속도인데 명령어 분리해 MIPS 늘리는 꼼수 가능
- MIPS 의 의미
  - MIPS (metric) → 현재 주제
  - MIPS (ISA 회사 이름) → Next Chapter
