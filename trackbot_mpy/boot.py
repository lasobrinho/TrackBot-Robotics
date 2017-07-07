# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import network
webrepl.start()
gc.collect()
# sta_if, ap_if = network.WLAN(network.STA_IF), network.WLAN(network.AP_IF)