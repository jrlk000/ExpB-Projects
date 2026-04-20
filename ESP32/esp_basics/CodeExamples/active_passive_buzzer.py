from machine import Pin

buzzer_pin = Pin(13, Pin.OUT)

#default reads low
button = Pin(4, Pin.IN, Pin.PULL_DOWN)

#loop version

while True:
    #if button pressed, turn on the buzzer pin
    if button.value():
        buzzer_pin.value(1)
    else:
        #turn off buzzer pin if on
        if buzzer_pin.value():
            buzzer_pin.value(0)

#interrupts version