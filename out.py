# This scxript just sets Pin 0. Use for debugging.
from machine import Pin

lock = Pin(0, Pin.OUT)

# Set Pin 0 output value
lock.value(0);
