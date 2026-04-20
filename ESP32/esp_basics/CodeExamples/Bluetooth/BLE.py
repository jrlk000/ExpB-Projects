# This example demonstrates a UART periperhal.

import bluetooth
import random
import struct
import time
from ble_advertising import advertising_payload
from machine import Pin

from micropython import const

# ---- Constants for events ----
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3) #GATT Generic attribute profile

#
_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

# ---- Define the specific UUID number for BLE vendor. ----
#service - mainly organizes related data
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

#characteristics - one actual data item or data endpoint inside a service
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
#service definition used by gatts_register_services to trell the BLE stack which services and characteristics exists on this device
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)
#encoded information: device hgas a UART service, has two characteristics, characteristics have certain permissions

class BLESimplePeripheral:
    def __init__(self, ble, name="ESP32"):
        self._ble = ble
        self._ble.active(True) #changes the active state of the BLE radio, and returns teh current state

        #registers a callback for events from the BLE stack.
        #The BLE itself is the software that handles all Bluetooth communication.
        self._ble.irq(self._irq)

        #configure  the server with the specified services, replacing any existing services.
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))

        self._connections = set()

        self._write_callback = None

        self._payload = advertising_payload(name=name, services=[_UART_UUID])

        self._advertise()

    # ---- private methods ----

    #interrupt request functiojn to handle BLE interrupt events
    def _irq(self, event, data) -> None:
        """
        Event handler orchestrates all possible events.

        ARGS
        ----
        event ():
        data ():
        """
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            print("\nThe BLE connection is successful.")
            self._connections.add(conn_handle)
        # Indicate disconnections from device
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            # So it announces the presewnce of the device for pairing candidates.
            self._advertise()
        #A client has written to this characteristic or descriptor.
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def _advertise(self, interval_us=500000):
        """

        ARGS
        ----
        interval_us ():
        """
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        #

    # ---- public methods ----
    def send(self, tx_data):
        """

        ARGS
        ----
        data: tx data used for communication between conversing devices.
        """
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, tx_data)

    def is_connected(self) -> bool:
        """

        RETURNS
        -------
        bool :
        """
        return len(self._connections) > 0

    def on_write(self, callback):
        """

        ARGS
        ----
        callback (Callable) : Funktion that defines what is done to the received data after an interruption.
        # to store the different requests there is a BLE stack.
        A stack is in this case a layered software system that implements the Bluetooth protocol.
        #BLE communication is complicated:
        -radio signals, packet formatting, connection handling, security,
        and the BLE object handles all of them for you

        """
        self._write_callback = callback

def demo():
    ble = bluetooth.BLE() # returns a sigelton Bluetooth Low Energy object (BLE)
    p = BLESimplePeripheral(ble)
    led = Pin(2, Pin.OUT)
    a = ['led_on:', 'led_off:', 'switch:']
    b = [val.encode() for val in a]
    overview_commands = [":".join([str(val[k]) for k in (0, 1)]) for val in zip(a, b)]

    def on_rx(rx_data):
        print("Received:", rx_data, f"type of received data: {type(rx_data)}.")
        if rx_data == b'led_on':
            led.value(1)
            print(led.value(), f"byte code: {b'led_on'}.")
        elif rx_data == b'led_off':
            led.value(0)
            print(led.value(), f"byte code: {b'led_off'}.")
        elif rx_data == b'switch':
            led.vale(not led.value())
            print(led.value(), f"byte code: {b'switch'}.")
        else:
            print("Command has no effect.")
            print(f"Allowed statements: {overview_commands}")

    p.on_write(on_rx)

    print("Please use LightBlue to connect to ESP32.")

    #receive message loop
    while True:
        if p.is_connected():
            # Short burst of queued notifications.
            tx_data = input("Enter a message: ")
            print("Send: ", tx_data)
            p.send(tx_data)

if __name__ == "__main__":
    demo()