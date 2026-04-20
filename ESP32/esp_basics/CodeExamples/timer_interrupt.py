from machine import Pin, DAC
from time import sleep

MODES = [0, 1, 2, 3]

#Pins that should be used as LED
LEDs = []

#del_time = 0.1
mode=0

def handle_interrupt(button1)->None:
    global mode
    mode += 1
    mode %= 4
    print(mode)

def led_switch(leds: list, direction=1, delay=False):
    if leds is None or len(leds)<=0:
        raise ValueError("Input must be at least one element or an iterable containing on element.")

    for l in range(0, len(leds))[::direction]:
        if not isinstance(leds[l], Pin):
            raise TypeError("Pin must be a machine Pin.")
        leds[l].value(not leds[l].value())

        if delay:
            sleep(1)
"""
def adaptable_led_switch(leds, step_logic="even"):
    if leds is None or all(isinstance(l, Pin) for l in leds):
        raise ValueError(f'Given argument contains a none Pin object which is invalid.')

    value_patern = []

    #currently are just even and odd valid iteration orders.
    if step_logic != "even":
        value_patern.extend([k%2 == 1 for k in range(0, len(leds))])

    value_patern.extend([k%2 == 0 for k in range(0, len(leds))])

    for n in range(0, len(leds)):
        leds[n].value(int(value_patern[n]))"""

#Create a button object.
button1 = Pin(4, Pin.IN)
button1.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

#irq interrupt request

#Create DAC object
dac1 = DAC(Pin(25, Pin.OUT))
#dac2 = DAC(Pin(26, Pin.OUT))


#Initialize LEDs
for k in [18, 19, 21, 22, 23, 27]:
    LEDs.append(Pin(k, Pin.OUT))



#create tension bar for multicolor led
tension_bar = [255/6 * k for k in range(0, 7)] #DAC expects 8bit integer values not the actual tension values


while True:
    #led blinking patterns
    """print("Entered while loop.")
    if (mode == MODES[0]):
        for _ in range(0, 2):
            led_switch(LEDs)
            sleep(1)
    if (mode == MODES[1]):
        led_switch(LEDs, direction=1, delay=True)
        sleep(1)
        led_switch(LEDs, direction=-1, delay=True)"""
    """if (mode == MODES[2]):
        for val in ("even", "odd", "even", "odd"):
            adaptable_led_switch(LEDs, val)
            sleep(1)"""
    #different led colors
    """if (mode == MODES[3]):
        for k in tension_bar:
            dac1.write(k)
            dac2.write(k)
            sleep(5)"""
    dac1.write(int(tension_bar[mode]))
    #dac2.write(int(tension_bar[mode]))

    """dac1.deinit()
    dac2.deinit()"""




