from machine import Pin, ADC
from time import sleep

#initialize pin and create adc
adc_pin = Pin(32, Pin.IN)
adc = ADC(adc_pin)

#12 bits corresponds to 2**12
adc.block().init(bits=12)

#11dB allows an allowed measure spectrum of [0, 3.3] [V]
adc.init(atten=ADC.ATTN_11DB)

#ask for analog signal in loop.
while True:
    adc_val = adc.read_u16()
    print(f"Approx digit value from adc value in 16 bits: {adc_val}")
    print(f"Corresponding tension value {3.3/2**16 * adc_val} [V].")
    sleep(1)


