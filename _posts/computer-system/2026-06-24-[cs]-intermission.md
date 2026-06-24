---
categories:
- Computer-System
date: '2026-06-24T10:51:00.000+09:00'
layout: single
series: 컴퓨터 시스템 개론
step: 7
tags:
- CS
- 프로세스
title: '[CS] Intermission'
toc: true
toc_sticky: true
---

## ✦ What we have learned


- Data 표현
  - 컴퓨터는 정보를 bit 로 표현
- x86-64 assembly
  - 프로그램 → assembly 명령어로 번역
  - assembly 명령어가 컴퓨터의 CPU 에 의해 실행됨
- Array & Struct
  - assembly level 에서 어떻게 표현되는가?
  - 프로그램에서 잘못 사용되면 buffer overflow 발생 가능

### ◆ Memory vs. File Storage


- Main Mamory (RAM) : 컴퓨터 종료 시 사라짐 (휘발성)
- Secondary Storage (SSD) : 컴퓨터 종료해도 유지 

### ◆ Loader


- .exe 파일 실행 시 OS 는 loader 실행
  - executable 파일을 memory 공간으로 load 
  - PC 를 프로그램 시작점으로 intialize
![](/assets/images/notion/[cs]-intermission/img_1.png)

### ◆ Context Switching


- CSPRO 서버에 수많은 학생이 동시에 접속해서 각자 프로그램을 실행하고 있는데, 어떻게 모두가 "동시에" 사용하는 것처럼 느껴질까?
{% raw %}
```text
Time ──────────────────────────────────────────────►
A's program :  ████      ████      ████
B's program :      ████      ████      ████
C's program :          ████      ████      ████
```
{% endraw %}

- 여러 개의 execution 이 서로 interleaving 중 
{% raw %}
```assembly
  mov %rax, %rcx
  ...
  add $0x10, %rdi
  ...
```
{% endraw %}

- Context : 프로그램이 CPU 에서 실행되던 그 순간의 모든 상태
  1. 범용 register
  1. PC 
  1. flag register
  1. stack 정보
  1. memory 매핑 정보
- OS 에 의해서 관리
  - 메모리 주소 충돌? virtual memory 사용
    - virtual address : 프로그램에서 사용하는 주소
    - physical address : 실제 메모리에서 물리적 주소
  - virtual address → 각각의 프로그램이 CPU 를 온전히 점유한다고 느끼게 만듬
