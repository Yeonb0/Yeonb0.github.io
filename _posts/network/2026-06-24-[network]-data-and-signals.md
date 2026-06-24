---
categories:
- Network
date: '2026-06-24T10:14:00.000+09:00'
layout: single
series: 컴퓨터 네트워크
step: 1
tags:
- 네트워크
- 전송
- 물리 계층
title: '[Network] Data and Signals'
toc: true
toc_sticky: true
---

## ✦ Data Communication Model


- 우리가 전송하는 data 는 bit 화 되어야만 전송될 수 있다.
![](/assets/images/notion/[network]-data-and-signals/img_1.png)

- Digital bit stream → Analog signal → Digital bit stream
→ 전달 과정에서 오류 발생 가능 (검증 필요)

### ◆ Data vs. Signal


- Data : 어떤 의미나 정보를 지닌 entity
  - Analog data : 연속적인 정보 
ex) 사람 목소리, 온도

  - Digital data : 이산적인 정보
ex) text, 정수

- Signal : data 의 electric or electromagnetic 표현
  - Analog signal : 연속적으로 변화하는 electromagnatic wave
  - Digital signal : 이산적인 전압 신호의 연속
- Data & Signal 의 조합

|  | Digital Signal | Analog Signal |
| Digital Data | Line coding (Ch. 2) | Modulation (Ch.3) |
| Analog Data | PCM, digitization (Ch. 2) | ampliture / frequency modulation (Ch.3) |

## ✦ Analog Signal


- 연속적인 신호
![](/assets/images/notion/[network]-data-and-signals/img_2.png)

### ◆ Periodic Signal


- Sine wave : sin 함수처럼 생김
- 특성
  - 진폭 (amplitude) : 얼마나 높이 움직이는가?
    - Peak amplitute : 제일 높은 신호
![](/assets/images/notion/[network]-data-and-signals/img_3.png)

  - 주파수 (Frequency) : 1초에 같은 pattern 을 몇 번 반복하는가?
    - 단위 : Hz
  - 주기 (Period) : 한 pattern 에 걸리는 시간
    - 단위 : s
→ 주파수 (Frequency) 와 주기 (Period) 는 역수 관계 (같은 feature)

<div class="equation-box">

$$
f = \frac{1}{T} \quad \text{and} \quad T = \frac{1}{f}
$$

</div>

![](/assets/images/notion/[network]-data-and-signals/img_4.png)

  - 위상 (Phase) : 0 을 기준으로 어느 위치가 들어오고 있나?
    - 각도 or radian 
  - 파장 (wavelength, \lambda) : 한 주기만큼 갈 때 얼마만큼의 거리를 이동하는가? (Distance)
    - \lambda = \frac{c}{f}
      - c = 빛의 속도 = 3 \times 10^8 (매질 따라 속도 변화)
      - f = 주파수 (frequency)
      - 주파수(frequency)와 파장(wavelength)은 반비례 (주기, period 와는 비례) → 한 pattern 이 짧으면 가는거리도 짧음
    - 4 번째 feature X
    - 밀리미터파 → 파장이 밀리미터 수준
- 특징 
  - 주파수 (Frequency) → 얼마나 빨리 진동하는지 보여줌
    - 빨리 진동 → 주파수 높음
    - 느리게 진동 → 주파수 낮음
  - 특이 케이스
    - 아주 느리다 갑자기 급격히 변하는 신호 → zero frequency, DC (Direct Current)
    - 갑자기 신호가 순간적으로 바뀜 → frequency 가 무한대
> 서로 다른 신호 구분 기준 → 진폭 (amplitude), 주파수 (frequency), 위상 (Phase)

### ◆ Time Domain vs. Frequency Domain


- Time Domain : x축이 시간. 일반적으로 생각하는 표현법
![](/assets/images/notion/[network]-data-and-signals/img_5.png)

- Frequency Domain : x축이 주파수 (1초에 진동 횟수), y축은 똑같이 진폭 (amplitude)
![](/assets/images/notion/[network]-data-and-signals/img_6.png)

→ Time Domain 보다 간단하나, 직관적이지 않다

![](/assets/images/notion/[network]-data-and-signals/img_7.png)

→ 한 신호에 여러 주파수가 겹처 나타날 때 유용하다

### ◆ Composite Signal


- 우리가 보는 신호 → 서로 다른 frequency & amplitude 가지는 signal 의 합
![](/assets/images/notion/[network]-data-and-signals/img_8.png)

  - 주기 있음 (periodic) → 이산적으로 나옴 
  - 주기 없음 (aperiodic) → 연속적으로 나옴

### ◆ Bandwidth (대역폭)


- Frequency 의 영역 = highest frequency - lowest frequency (중간은 상관 X)
![](/assets/images/notion/[network]-data-and-signals/img_9.png)

- Example
  - AM Radio 
    - 대역폭 10kHz
    - 530 ~ 1700kHz band 사용
  - FM Radio
    - 대역폭 200kHz
    - 88 ~ 108MHz band 사용
  - Wi-Fi 802.11n
    - 대역폭 20MHz | 40MHz
    - 2.4GHz, 5GHz, 6GHz band 사용
  - LTE 
    - 대역폭 10MHz | 20MHz
    - 1.8GHz band 사용

## ✦ Digital Signals


- amplitude, frequency, phase 사용해 bit (0, 1) 정보로 만든 signal
![](/assets/images/notion/[network]-data-and-signals/img_10.png)

- bit rate : 1초에 몇 bit 전송?
  - 단위 : bps (bit per second)
  - 1 Kbps = 1000 bps
  - 1 Mbps = 1000 Kbps
  - 1 Gbps = 1000 Mbps
- signal level 증가 가능 
  - bit 갯수 n 일 때, 한 번에 2^n 만큼의 bit 전송
ex) two bits

![](/assets/images/notion/[network]-data-and-signals/img_11.png)

## ✦ Transmission of Digital Signals


- 어떻게 digital signal 을 주고 받음?
![](/assets/images/notion/[network]-data-and-signals/img_12.png)

  - Time domain → Frequency domain 으로 바꾸기
  - 결국 sine wave 들의 합으로 만들어 전송
→ 무한대의 대역폭 필요. 难

### ◆ Baseband Transmission


- 유선에서의 전송 방법
- Digital Singal 은 이산적으로 생김 → Analog 로 변환해 channel 로 전달
  - channel : 데이터가 전송되는 추상적 통로
- 이상 : 0 ~ ∞ 의 bandwidth 사용해 정확하게 변환된 신호 전송
![](/assets/images/notion/[network]-data-and-signals/img_13.png)

- 현실 : 모든 bandwidth 사용 가능 X 
  - 일부 bandwidth 만 사용해 signal 전달 → signal 의 왜곡
![](/assets/images/notion/[network]-data-and-signals/img_14.png)

### ◆ Baseband Approximation


- Example : 3 bit 를 보낸다고 생각하자
![](/assets/images/notion/[network]-data-and-signals/img_15.png)

  - 8 pattern 존재
  - n 은 1초에 보내야하는 bit 수
    - 000 / 111 → 주파수 0
    - 001 / 011 / 100 / 110 → 4칸 마다 주기 반복. 주파수 \frac{n}{4}
    - 010 / 101 → 2칸마다 주기 반복. 주파수 \frac{n}{2}
  - bandwidth = 최고 주파수 - 최저 저파수 = \frac{n}{2} - 0 = \frac{n}{2}
![](/assets/images/notion/[network]-data-and-signals/img_16.png)

- bandwidth 를 넓힐수록 digital siganl 과 유사해짐.
  - 원래 digital signal 로 복원 용이
- bandwidth 를 줄이면 복원 불가
  - Nyquist Condition : 최소 \frac{n}{2} 만큼의 주파수 필요
![](/assets/images/notion/[network]-data-and-signals/img_17.png)

- bandwidth = f → 최고 transfer rate = 2f

### ◆ Bandpass Channel


- 무선에서의 전송방법
- 특정 주파수 구간에서 데이터 보내기 (f_1 \sim f_2)
![](/assets/images/notion/[network]-data-and-signals/img_18.png)

- 0 근처의 주파수는 사용하지 않음.
  - bandwidth = f_2 - f_1
- bandwidth 와 transfer rate 는 거의 비례함

### ◆ Modulation


- bandpass channel 에서 신호 전송 위해 필요
- Modem 모뎀 - modulator + demodulator
  - 변조 + 복조
- signal 구분 3 요소 : 진폭 / 주파수 / 위상
→ 이 세 가지 조절해 변조 & 복조

- 변조 : digital (0, 1) → analog 신호로 바꾸기
- 복조 : analog → digital 신호로 복구하기
  - FM (Frequency Modulation) : 주파수로 modulation
  - AM (Amplitude Modulation) : 진폭으로 modulation
→ noise 심함

### ◆ Baseband vs. Bandpass


- Baseband (low-pass channel)
  - ethernet 유선 사용
- Bandpass
  - Wi-Fi
  - LTE / 5G

## ✦ Transmission Impairment


- Signal 이 이동하면서 장애가 생김

### ◆ Attenuation (신호 감쇠)


- 신호가 출발한 곳에서 멀어질 수록 신호 세기 감소
  - 너무 거리가 멀어지면 신호 / 공기 구분 X
- 증폭기 (Amplifier) : 신호 증폭. but noise 도 같이 증폭
- 리피터 (Reapter) : digital signal 로 복원 + 재전송

### ◆ Signal strength 단위 : decidel (dB)


- dB = 10 \log_{10}(\frac{P_2}{P_1})
→ 비율을 의미. 기준점 (P_1) 대비 신호의 크기 (power)

- 10 dB → 10배 큼
- 30 dB → 1000배큼
  - dB 가 양수 → signal 을 얻음 (증폭됨)
  - dB 가 음수 → signal 이 사라짐 (감쇠됨)
- dB 의 장점 : 원래는 큰 수끼리 곱해야하는 계산을 덧셈 / 뺄셈으로 바꿔줌

### ◆ dBm


- 1 밀리와트 기준 dB 의 절댓값
- dBm = 10 \log_{10}P_m
  - 1mW = 0dBm
  - 10mW = 10dBm
  - 100mW = 20dBm
  - 0.1mW = -10dBm
- ex) 
  - 스마트폰 : 23 dBm
  - -30 ~ 40 dBm : 전송률 good (와이파이 꽉참)
  - -80 ~ 90 dBm : 전송이 끊킴 (와이파이 한 두 칸)
  - -100 dBm : 통신이 안됨 (0.0000000001 mW)

### ◆ Distortion (신호 왜곡)


- 다른 주파수가 다른 속도로 매체에 도착 
→ 찌그러진 형태의 주파수 

![](/assets/images/notion/[network]-data-and-signals/img_19.png)

- equalizer 사용해 복구 가능

### ◆ Noise (신호 간섭)


- 원하지 않는 주파수가 첨가됨
  - Thermal noise : 전자의 임의적 움직임 때문에 발생
  - Induced noise : motor, power line 의 자기장 때문에 발생
  - Crosstalk : 주변 유선 / 무선의 간섭
  - Impulse noise : 갑작스러운 일 (번개, power surges 등)
- 복원하기 어려움

### ◆ Signal-to-Noise Ratio (SNR)


- noise 에 비해 내 신호가 얼마나 큼?
- SNR = \frac{\text{signal power}}{\text{noise power}}
  - 높을 수록 → quality good
  - 낮을 수록 → signal & noise 비슷 → error 많음
![](/assets/images/notion/[network]-data-and-signals/img_20.png)

- \text{SNR}_{dB} = 10 \log_{10}(\text{SNR})
- SNR 이 너무 낮으면 신호 복구 불가능

## ✦ Data Rate Limits


### ◆ Data Transfer Rate (Bit Rate)


- data 전송 속도는 중요하다.
→ 예측 위해선 3 가지 요소 필요

  - bandwidth
  - number of signal level (몇 가지 pattern 사용?)
  - channel quality (noise level)
- Nyquist theorem → noise 고려 X
- Shannon theorem → noise 고려 O

### ◆ Nyquist Equation


- noise 고려 X
- Data rate = 2 \times B \times \log_2L
  - B : bandwidth
  - L : signal level 숫자 (사용 비트의 2의 제곱수)
- 최소 필요 bandwidth = \frac{n}{2}
- 그러나 signal level 을 많이 나누면 noise 에 취약
  - 신호가 비슷해서 구분 어려움

### ◆ Shannon Capacity


- noise 고려 O
- noise 있는 channel 에서의 maximum bit rate → upper mound
- C = B \times \log_2(1 + \text{SNR})
  - C : capacity (maximum bit rate)
  - B : bandwidth
  - SNR : signal-to-noise ration (not dB)
![](/assets/images/notion/[network]-data-and-signals/img_21.png)

    - QPSK : 4 level - 2 bit
    - 16QAM : 16 level - 4 bit
    - 64QAM : 64 level - 6 bit
    - 256QAM : 256 level - 8 bit
    - 1024QAM : 1024 level - 10 bit
- SNR 이 높아지면 (error 보다 signal 세기가 크면) → error 감소
- 같은 SNR 에서 사용하는 level 많을 수록 error 증가
- High SNR : \text{SNR}_{dB} 로 C 대략적으로 구하기
  - C = B \times \frac{\text{SNR}_{dB}}{3}

## ✦ Performance


### ◆ Bandwidth


- 의미가 2 개
  - Frequency bandwidth : channel 통과할 수 있는 frequency 의 범위 (Hz)
  - Data bandwidth : channel 이 버틸 수 있는 maximum bit rate
→ 서로 연관성 있음 : 비례한다

### ◆ Throughput


- 실제 data transfer rate (bps)
  - bandwidth : 최대의 개념
  - throughput : 순수 data transfer rate (header, overhead, 혼잡 등 제외)
    - Throughput < Bandwidth

### ◆ Delay


- 메시지의 첫 번째 bit 출발 ~ 마지막 bit 도착 까지의 시간
- Delay = transmission delay + propagation delay + queuing delay + processing delay
  - Transmission delay (전송 속도) : bit 를 channel 로 내보내는 시간
    - \frac{\text{message size}}{\text{bandwidth}}
    - 회선의 bandwidth 비례
  - propagation delay (전파 속도) : 송신 → 수신 도달까지 걸리는 시간
    - \frac{\text{distance}}{\text{propagation speed}}
    - 송-수신자 거리에 비례
![](/assets/images/notion/[network]-data-and-signals/img_22.png)

  - Queuing delay : queue 에서 줄 서는 시간
  - Processing delay : 시스템이 process 하는데 걸리는 시간

### ◆ Bandwidth-Delay Product


- bandwidth (bps) × delay (s) = bits
- 내가 얼마만큼의 데이터를 보내야 이 channel 을 다 채울 수 있나?
![](/assets/images/notion/[network]-data-and-signals/img_23.png)
