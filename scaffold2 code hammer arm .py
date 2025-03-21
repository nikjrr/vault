import uasyncio
from machine import Pin, TouchPad, PWM
from neopixel import NeoPixel

np = NeoPixel(Pin(12), 10)


touch = TouchPad(Pin(13))

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
OFF = (0, 0, 0)

# Touch threshold (adjust based on testing)
TOUCH_THRESHOLD = 350

# Motor Control (HW-095)
IN1 = Pin(14, Pin.OUT)  # Motor direction 1
IN2 = Pin(27, Pin.OUT)  # Motor direction 2
ENA = PWM(Pin(18), freq=1000)  # Speed control (PWM)

# Function to set motor speed (0 to 100%)
def set_speed(speed):
    ENA.duty_u16(int(speed * 655.35))  # Convert 0-100% to 0-65535

def motor_forward():
    IN1.value(0)
    IN2.value(1)
    set_speed(80)


def motor_backward():
    IN1.value(1)
    IN2.value(0)
    set_speed(80)

def motor_stop():
    IN1.value(0)
    IN2.value(0)
    set_speed(0)

async def motor_loop():
    while True:

        motor_forward()
        await uasyncio.sleep(0.5)
        motor_stop()
        await uasyncio.sleep(1)

        motor_backward()
        await uasyncio.sleep(0.5)
        motor_stop()
        await uasyncio.sleep(1)

async def animate_lights(strength):
    for i in range(strength):
        np[i] = RED
        np.write()
        await uasyncio.sleep(0.3)

    if strength == 10:
        np[9] = YELLOW
        np.write()
        await uasyncio.sleep(0.3)

    for i in range(strength - 1, -1, -1):
        np[i] = OFF
        np.write()
        await uasyncio.sleep(0.3)

async def main():
    while True:
        value = touch.read()
        print("Touch value:", value)

        if value > TOUCH_THRESHOLD:
            for i in range(10):
                np[i] = OFF
            np.write()
        else:
            strength = max(0, min(10, (800 - value) // 40))

            if strength > 0:
                uasyncio.create_task(animate_lights(strength))

        await uasyncio.sleep(0.1)
uasyncio.create_task(motor_loop())
uasyncio.run(main())
