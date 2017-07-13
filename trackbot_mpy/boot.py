# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import network

webrepl.start()
gc.collect()

sta = network.WLAN(network.STA_IF)
sta.ifconfig(('192.168.1.20', '255.255.255.0', '192.168.1.1', '192.168.1.1'))