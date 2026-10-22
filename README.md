# Raspberry Pi I2C Dual Display Control

라즈베리 파이의 I2C 버스를 공유하여 16x2 Text LCD(0x27)와 128x64 OLED(0x3C)를 하나의 파이썬 프로그램에서 동시 제어하는 프로젝트입니다.

## 1. 하드웨어 핀 연결
- Pin 1 (3.3V) -> OLED VCC
- Pin 2 (5V) -> Text LCD VCC
- Pin 3 (SDA) -> LCD SDA / OLED SDA (공유)
- Pin 5 (SCL) -> LCD SCL / OLED SCL (공유)
- Pin 6 (GND) -> LCD GND / OLED GND (공유)

## 2. 주요 기능
- 16x2 Text LCD: 기본 텍스트 메시지 출력
- 128x64 OLED: PIL 라이브러리를 활용한 128x64 그래픽 비트맵 이미지 출력

## 3. 실행 방법
```bash
sudo apt update
sudo apt install -y python3-pil python3-smbus
pip3 install smbus2 adafruit-circuitpython-ssd1306

python3 main_display_control.py
