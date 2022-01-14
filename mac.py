''' Wrapper de machine, para NodeMCU e aplicações do projeto'''

from machine import Pin
import time


pn = {
    'd0': [16, False],
    'd1': [5, False],
    'd2': [4, False],
    'd3': [0, False],
    'led': [2, False],
    'd5': [14, False],
    'd6': [12, False],
    'd7': [13, False],
    'd8': [15, False]}  # corespondencia dos pinos com o NodeMCU

led = Pin(pn['led'][0], Pin.OUT)


def tgl_led():
    led(not led())
    pn['led'][1] = not pn['led'][1]
    

def blink(duration=0.1):
    tgl_led()
    time.sleep(duration)
    tgl_led()


async def async_blink(duration=0.1):
    tgl_led()
    await time.sleep(duration)
    tgl_led()


def tgl_pin(pin):
    # usando pin OUT e IN para trocar o estado dos pinos pois isso é o que funciona com relés :)
    # IN == ligado, OUT == desligado
    if pn[pin][1]:
        Pin(pn[pin][0], Pin.IN)
    else:
        Pin(pn[pin][0], Pin.OUT)
    pn[pin][1] = not pn[pin][1]  # atualiza o valor do pino

