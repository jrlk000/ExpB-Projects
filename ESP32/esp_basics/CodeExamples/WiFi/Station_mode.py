import time
import network

#1. DEfine the interface Globally
sta_if = network.WLAN(network.STA_IF)

ssidRouter     = 'TNGBOX3689703' #Enter the router name
passwordRouter = '59968779516854631142' #Enter the router password

def STA_Setup(ssidRouter,passwordRouter):
    print("Setup start")
    # put on your client hat, STA - Station, IF - Interface
    # station interface - talk to the part of the WiFi chip that handles outgoing connectoins
    #sta_if = network.WLAN(network.STA_IF)
    #check whether ESP32 (in station mode) is connected to a wifi access point and possesses a valid IP address
    if not sta_if.isconnected():
        print('connecting to',ssidRouter)
        sta_if.active(True) #activate network interface - point of interconnection between a computer and a network (virtual doorway that defines how the ESP talks to the outer world)
        sta_if.connect(ssidRouter,passwordRouter) #connect to wireless network
        #check whether it's connected to an ap or has a valid IP-address
        while not sta_if.isconnected():
            pass
    ip_adress, subnet_mask, gateway, dns_server = sta_if.config()
    #print('Connected, IP address:', sta_if.ifconfig())
    print(f"IP:Address: {ip_adress}, subnet_mask: {subnet_mask}, gateway: {gateway} and dns_server: {dns_server}")
    #1) identifier of esp32 in network provided by the router, 2)devide IPv4 address into network and host components, enabling network segmentation, 3)network node that acts as an entry/exit point between different networks, protocols or technologies 4) domain name system  translates human-readable domain names into numerical IP-address
    print("Setup End")

try:
    STA_Setup(ssidRouter,passwordRouter)
except Exception as e:
    print("Error occurred:", e)
    sta_if.disconnect()
    #or just deaktivate
    #sta_if.active(False)
    
    
    
