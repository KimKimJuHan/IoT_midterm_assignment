import time
import smbus2
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


class I2C_LCD1602:
    def __init__(self, i2c_addr=0x27, bus_num=1):
        self.addr = i2c_addr
        self.bus = smbus2.SMBus(bus_num)

        self.LCD_CLEARDISPLAY = 0x01
        self.LCD_ENTRYMODESET = 0x04
        self.LCD_DISPLAYCONTROL = 0x08
        self.LCD_FUNCTIONSET = 0x20
        self.LCD_SETDDRAMADDR = 0x80

        self.LCD_ENTRYLEFT = 0x02
        self.LCD_DISPLAYON = 0x04
        self.LCD_CURSOROFF = 0x00
        self.LCD_BLINKOFF = 0x00
        self.LCD_4BITMODE = 0x00
        self.LCD_2LINE = 0x08
        self.LCD_5x8DOTS = 0x00
        self.LCD_BACKLIGHT = 0x08
        self.ENABLE = 0b00000100

        self._init_lcd()

    def _write_word(self, data):
        temp = data | self.LCD_BACKLIGHT
        self.bus.write_byte(self.addr, temp)

    def _send_nibble(self, nibble):
        self._write_word(nibble)
        self._strobe(nibble)

    def _strobe(self, nibble):
        self._write_word(nibble | self.ENABLE)
        time.sleep(0.0005)
        self._write_word(nibble & ~self.ENABLE)
        time.sleep(0.0001)

    def _send_byte(self, cmd, mode=0):
        high = mode | (cmd & 0xF0)
        low = mode | ((cmd << 4) & 0xF0)
        self._send_nibble(high)
        self._send_nibble(low)

    def _init_lcd(self):
        self._send_nibble(0x30)
        self._send_nibble(0x30)
        self._send_nibble(0x30)
        self._send_nibble(0x20)

        self._send_byte(
            self.LCD_FUNCTIONSET
            | self.LCD_4BITMODE
            | self.LCD_2LINE
            | self.LCD_5x8DOTS
        )
        self._send_byte(
            self.LCD_DISPLAYCONTROL
            | self.LCD_DISPLAYON
            | self.LCD_CURSOROFF
            | self.LCD_BLINKOFF
        )
        self.clear()
        self._send_byte(self.LCD_ENTRYMODESET | self.LCD_ENTRYLEFT)
        time.sleep(0.2)

    def clear(self):
        self._send_byte(self.LCD_CLEARDISPLAY)
        time.sleep(0.002)

    def print_line(self, text, line=1):
        line_offsets = [0x00, 0x40]
        if line not in (1, 2):
            return
        self._send_byte(self.LCD_SETDDRAMADDR | line_offsets[line - 1])
        formatted_text = text.ljust(16)[:16]
        for char in formatted_text:
            self._send_byte(ord(char), mode=1)


def main():
    try:
        lcd = I2C_LCD1602(i2c_addr=0x27, bus_num=1)
        lcd.print_line("Hello World!", line=1)
        lcd.print_line("Raspberry Pi IoT", line=2)
    except Exception as e:
        print(f"LCD Error: {e}")

    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        oled.fill(0)
        oled.show()

        image = Image.new("1", (128, 64))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        draw.rectangle((0, 0, 127, 63), outline=255, fill=0)
        draw.ellipse((49, 10, 77, 38), outline=255, fill=0)
        draw.text((12, 44), "OLED 128x64 Image", font=font, fill=255)

        oled.image(image)
        oled.show()
    except Exception as e:
        print(f"OLED Error: {e}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()