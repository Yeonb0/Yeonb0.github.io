---
categories:
- Computer-System
date: '2026-06-24T10:50:00.000+09:00'
layout: single
series: 컴퓨터 시스템 개론
step: 6
tags:
- CS
- Buffer
title: '[CS] Buffer Overflow'
toc: true
toc_sticky: true
---

## ✦ Reviews


- Byte Ordering → Little Endian (MSB 가 뒤에)
![](/assets/images/notion/[cs]-buffer-overflow/img_1.png)

  - cf) Big Endian (MSB 가 앞에)
![](/assets/images/notion/[cs]-buffer-overflow/img_2.png)

- String 의 memory 저장 → Little / Big 모두 동일 (순서대로 저장)
{% raw %}
```c
char s[6] = "AB123";
```
{% endraw %}

{% raw %}
```assembly
0x7ffd0f231872: 0x41 ; A
0x7ffd0f231873: 0x42 ; B
0x7ffd0f231874: 0x31 ; 1
0x7ffd0f231875: 0x32 ; 2
0x7ffd0f231876: 0x33 ; 3
0x7ffd0f231877: 0x00 ; null
```
{% endraw %}

- Stack Frame 
  - Stack 은 frame 이라는 부분으로 나뉨
  - 각 frame 에 저장되는 것
    - return address
    - local variable
    - callee-saved register backup
  - `call` 통해 할당
  - `ret` 하기 직전 해제
- Memory 구조
![](/assets/images/notion/[cs]-buffer-overflow/img_3.png)

  - Stack : 함수 실행 중의 Stack frame 
  - Heap : `malloc()` 또는 `new()` 로 할당되는 dynamic memory block
  - Data : 프로그램의 global 변수
  - Code (text) : Instruction

## ✦ Buffer Overflow


- Buffer
  - 잠시 data 를  저장하기 위한 배열
  - in C : 사용자 입력 string 저장 위한 character array

### ◆ Buffer Overflow (BOF)


- C 언어는 배열 boundary check X → buffer 크기를 넘어서 작성 가능 
→ memory 안의 data 손상 시킬 수 있음
  - stack frame 에 저장되어 있는 return address 변경 (control hijack)
- 주로 stack 에 위치안 buffer 에서 발생
  - stack-based buffer overflow : 다른 stack frame 공간 침범 
  - cf) stack overflow : stack 에 저장 공간 X 
- string handling function 의해 발생
  - `gets()`, `scanf("%s", ...)`, `strcpy()`, `strcat()`
  - 입력 받는 배열 size 검사 안하고 input 받음
- hacker 가 쉽게 악용 가능

### ◆ Example code


{% raw %}
```c
void echo(void) {
	char buf[8];
	gets(buf);
	puts(buf);
}

int main() {
	echo();
	return 0;
}
```
{% endraw %}

{% raw %}
```assembly
(gdb) disassemble echo
0x401136: sub  $0x18,%rsp
0x40113a: lea  0x8(%rsp),%rdi       ; stack + 8
0x40113f: mov  $0x0,%eax
0x401144: call 0x401040 <gets@plt>
0x401149: lea  0x8(%rsp),%rdi       ; stack + 8
0x40114e: call 0x401030 <puts@plt>
0x401153: add  $0x18,%rsp
0x401157: ret

(gdb) disassemble main
0x401158: sub  $0x8,%rsp
0x40115c: call 0x401136 <echo>
0x401161: mov  $0x0,%eax
0x401166: add  $0x8,%rsp
0x40116a: ret
```
{% endraw %}

![](/assets/images/notion/[cs]-buffer-overflow/img_4.png)

- 원래 예상 동작 : 8 글자 입력 → 오류 X
- 9 ~ 15 글자 입력 : 원래 예상 동작은 아니지만, 오류 발생 X
- 16 글자 이상입력 → return address 침범해서 `Segmentation fault` 발생
{% raw %}
```assembly
0123456789ABCDEF
```
{% endraw %}

![](/assets/images/notion/[cs]-buffer-overflow/img_5.png)

- Example) 입력 : 0123456789ABCDEFabc
![](/assets/images/notion/[cs]-buffer-overflow/img_6.png)

  - return address 가 `0x636261` 이 됨 → Control Hijack

### ◆ Morris Worm


- 최초로 알려진 인터넷 worm (1988)
- `finger` 유틸리티의 버퍼 오버플로우 취약점을 악용
{% raw %}
```bash
$ finger "<long string>+<new return address>"
```
{% endraw %}
