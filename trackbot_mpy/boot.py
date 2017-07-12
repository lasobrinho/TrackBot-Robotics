# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import network
import machine
webrepl.start()
gc.collect()
machine.freq(160000000)