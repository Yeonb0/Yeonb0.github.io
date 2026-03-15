---
categories:
- Computer-Graphics
date: '2026-03-15T20:02:00.000+09:00'
tags:
- RGBA
- RGB
- Buffering
title: '[CG] Raster Graphics'
toc: true
toc_sticky: true
---

## ✦ GPU (Graphics Processing Unit)


### ◆ 용도


- Real-Time 3D Rendering / 2D 이미지 생성
- GPGPU (general-purpose high-performance parallel computing) 
- 인공지능
→ 요즘 GPU 많이 사용

ex) NVIDIA, AMD, Intel 등

### ◆ GPU 의 장점


- SIMD 병렬성 처리
  - Single Instruction Stream : 동일 프로그램 명령어 순차적으로
  - Multiple Data Stream : 서로 다른 데이터 스트림에 대해
  - 동기화하면서 수행하며 계산
→ 행렬 계산 등에 유용하게 사용

## ✦ Color Model


### ◆ Color Model


- 컴퓨터에서 색 (color) 을 어떻게 표현할 것인가?
  - RGB color model → 주 사용 모델
![](/assets/images/notion/[cg]-raster-graphics/img_1.png)

  - CMY color model
![](/assets/images/notion/[cg]-raster-graphics/img_2.png)

  - HSV color model

### ◆ RGB Color Model


- 빨간색 (Red), 초록색 (Green), 파란색 (Blue) 의 세 원색 적절히 더해 색 표현
→ Additive color model

  - Color tuple (r, g, b) 로 표현
    - 0.0 (미포함) ~ 1.0 (원색) 사이
ex) (0.765, 0.471, 0.686)

- RGBA 모델 : RGB + Alpha Channel
ex) `glClearColor(1.0, 1.0, 1.0, 1.0);` → 화면을 하얗게 만듬

- Additive primary color
  - 빨 Red (1, 0, 0)
  - 초 Green (0, 1, 0)
  - 파 Blue (0, 0, 1)
- Subtractive primary color
  - 시안 Cyan (0, 1, 1)
  - 자홍 Megenta (1, 0, 1)
  - 노랑 Yellow (1, 1, 0)
- Neutral color (무채색)
  - 검정 Black (0, 0, 0)
  - 흰 White (1, 1, 1)
  - 회색 Gray (a, a, a) 
→ 직관적 X, but 디스플레이, 그래픽스 분야 근간 모델

### ◆ RGB Representation


- R, G, B 각 8-bit → 한 color 당 24-bit 사용
  - 0과 1 사이 값을 256 단계로 나눠 표현 (0 ~ 255)
  - 약 1640만 개 색 표현 가능
- 전문가용 : R, G, B 각 16-bit, 한 color 당 48-bit 사용
- 채널 당 bit 수 증가 → 메모리 요구량 ↑
ex) 해상도 1280 * 1024 / 24비트 색깔 사용

→ 1280 * 1024 * 24 / 8B = 3.75MB 메모리 필요

## ✦ Raster Graphics System


### ◆ Raster Graphics


- 래스터 이미지를 만들고, 화면에 띄우는 시스템
- 래스터 이미지 (raster image) : 직사각형 형태의 이미지를 화소 (pixel) 로 나눠서 각 화소를 색으로 칠한 이미지
  - Pixel = Picture element
cf) 벡터 이미지 : 또 다른 이미지 표현법. 현재는 잘 사용하지 않음

- 해상도 (resolution)
  - pixel dimension
  - 1280 × 1024, 1920 × 1080 (Full HD), 2560 × 1440 (QHD), 3840 × 2160 (4K)
  - 해상도 ↑ → 정밀도 ↑ 저장에 필요한 메모리 양 ↑
  - 현실 세계 → 연속적, but 유한 개 화소 사용 ‘이산적’ 표현 
→ 표현 오차 발생 (aliasing)

### ◆ Raster Graphics System


- 화면에 띄울 이미지 → raster image (해상도를 가지는 이미지) 사용
  - 화면에 raster image 뜨기 위해선 이미지 데이터가 그래픽 메모리에 있어야 함
  - RGB 각각 8 bit 가 frame buffer 에 떠있어야 함
![](/assets/images/notion/[cg]-raster-graphics/img_3.png)

  - 화면에서 → ↓ 순서로 데이터 읽어 색 표현 
    - 화면의 한 줄 : scan line
    - 전체 화면 한 번 다시 표시 → refresh 했다
      - refresh rate : 1초에 refresh 하는 횟수 (120 Hz, 60 Hz) 

### ◆ Frame Buffer


- Buffer : 임시 데이터 저장하는 곳
- Frame Buffer : 화면에 디스플레이 할 데이터를 임시 저장하는 곳
→ 이미지 생성에 필요한 여러 정보 저장 (색 + α)
  - Color buffer : 색 저장
    - Double buffer
    - Stereo buffer
    - Alpha buffer
  - Depth Buffer (Z-buffer) : 물체가 나한테 얼만큼 떨어져 있는가?
  - Stencil buffer : rendering 영역 제한에 사용
- Framebuffer Object (OpenGL)

## ✦ Buffering


### ◆ Single Buffering


- Rendering : Processor 가 장면 구성 요소들을 하나씩 그림
- Color buffer 1개 사용
  - Processor : new 이미지의 내용을 계산해 frame buffer 에 차례대로 그림
→ frame rate (fps) : 30 fps ~ 90 fps

  - 비디오 제어기는 frame buffer 내용 스캔하면서 화면에 나타냄
→ refresh rate (Hz) : 60 Hz

→ if 계산 중 스캔하면? 불규칙한 이미지 나타남 : flickering

![](/assets/images/notion/[cg]-raster-graphics/img_4.png)

### ◆ Double Buffering


- Color buffer 2개 사용
  - 비디오 제어기 : front buffer (FB) 에서 데이터 읽어 화면에 나타냄
  - GPU : back buffer (BB) 에 렌더링 계산수행
→ BB 렌더링 종료 시 FB ↔ BB 역할 바꾸기 : buffer swaping or presentation

    - page flip : 두 buffer 지칭 포인터 서로 바꿈
    - copy (or blit) : BB 메모리를 FB 메모리 영역에 복사
- 비디오 제어기가 매순간 완성된 이미지 도시 → flickering 현상 X, 훨씬 부드러움
→ but Tearing 현상 발생 가능
- Screen Tearing : GPU 의 frame rate & 비디오 제어기 monitor refresh rate 일치 X
  - Rendering : frame rate → 가변 (30 fps ~ 90 fps)
  - Display : refresh rate → 고정 (60 Hz)
![](/assets/images/notion/[cg]-raster-graphics/img_5.png)

- VSync (수직 동기화) → Tearing 해결 방법
  - GPU : back buffer (BB) 에 다음 프레임 렌더링 → buffer writing
  - 비디오 제어기 : front buffer (FB) 에서 데이터 읽어 화면에 디스플레이 → buffer reading
  - how work? GPU 가 BB 에 렌더링 마친 후에만 buffer swaping 일어나도록 함
→ 온전한 이미지만 화면에 나타남
![](/assets/images/notion/[cg]-raster-graphics/img_6.png)

→ rendering 이 빨리 되면 다음 refresh 까지 GPU 가 놀고 있음

  - 문제점
    - 1 refresh rate 동안 rendering 이 끝나지 않으면
→ 동일한 이미지가 여러 번 디스플레이 됨 

    - stuttering : 화면이 변하는 속도가 달라짐 
어떤 때는 1 frame 만에, 어떤 때는 2 frame 후에 바뀜
    - VSync lag : 1.2 frame 정도만에 rendering 끝내면 나머지 0.8 frame 동안 GPU 자원 낭비
![](/assets/images/notion/[cg]-raster-graphics/img_7.png)

### ◆ Triple Buffering


- Color Buffer 3개 사용 
  - FB 1개 + BB 2개
- 방법
  1. VSync 시점에 렌더링 끝난 BB X → FB 이미지 한 번 더 디스플레이 (stuttering)
  1. VSync 시점에 렌더링 끝난 BB 1 개 → 가장 최근 렌더링 한 BB 와 buffer swaping
→ Most-recent buffer swapping 방식

  1. VSync 이전에 두 BB 렌더링 모두 끝나면
    - 먼저 렌더링이 끝난 buffer 에 새로 렌더링
→ VSync lag 줄일수 있음
    - 시간이 남을 때마다 new 이미지 BB 에 그리고 있음
→ VSync 시점 되면 가장 나중에 완성된 이미지 사용
- 장점
  - 렌더링 시점 & 디스플레이 시점간 지연 (VSync lag) 줄일수 있음
![](/assets/images/notion/[cg]-raster-graphics/img_8.png)

  - Stuttering 문제 줄일수 있음 → frame rate stabilization
![](/assets/images/notion/[cg]-raster-graphics/img_9.png)
