#!/usr/bin/env python
# coding: utf-8

# ## basic passthrough code ##
# 

# In[ ]:


import pigpio
import time

# GPIOs
PWM_IN_THROTTLE = 23  # Pin 16
PWM_IN_STEERING = 24  # Pin 18
PWM_OUT_ESC = 13      # Pin 33
PWM_OUT_SERVO = 19    # Pin 35

pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon!")
    exit()

# Set up input capture
def passthrough_cb(gpio_in, level, tick, out_pin):
    if level == 1:
        # Rising edge - record start time
        passthrough_cb.start_ticks[out_pin] = tick
    elif level == 0:
        # Falling edge - calculate pulse width
        if out_pin in passthrough_cb.start_ticks:
            width = pigpio.tickDiff(passthrough_cb.start_ticks[out_pin], tick)
            pi.set_servo_pulsewidth(out_pin, width)

passthrough_cb.start_ticks = {}

# Set up callbacks
pi.set_mode(PWM_IN_THROTTLE, pigpio.INPUT)
pi.set_mode(PWM_IN_STEERING, pigpio.INPUT)

pi.set_mode(PWM_OUT_ESC, pigpio.OUTPUT)
pi.set_mode(PWM_OUT_SERVO, pigpio.OUTPUT)

cb1 = pi.callback(PWM_IN_THROTTLE, pigpio.EITHER_EDGE, lambda g, l, t: passthrough_cb(g, l, t, PWM_OUT_ESC))
cb2 = pi.callback(PWM_IN_STEERING, pigpio.EITHER_EDGE, lambda g, l, t: passthrough_cb(g, l, t, PWM_OUT_SERVO))

print("PWM passthrough running. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Cleanup
cb1.cancel()
cb2.cancel()
pi.set_servo_pulsewidth(PWM_OUT_ESC, 0)
pi.set_servo_pulsewidth(PWM_OUT_SERVO, 0)
pi.stop()


# ### same code but with a 50% throttle dampening effect ###

# In[3]:


import pigpio
import time

# GPIOs
PWM_IN_THROTTLE = 23  # Pin 16
PWM_IN_STEERING = 24  # Pin 18
PWM_OUT_ESC = 13      # Pin 33
PWM_OUT_SERVO = 19    # Pin 35

# Dampening factor (0 = full dampening, 1 = passthrough)
DAMPENING = 0.5

pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon!")
    exit()

# Set up input capture
def passthrough_cb(gpio_in, level, tick, out_pin, dampen=False):
    if level == 1:
        passthrough_cb.start_ticks[out_pin] = tick
    elif level == 0 and out_pin in passthrough_cb.start_ticks:
        width = pigpio.tickDiff(passthrough_cb.start_ticks[out_pin], tick)
        width = max(1000, min(2000, width))  # Clamp to 1000–2000 µs

        if dampen:
            width = int(1500 + (width - 1500) * DAMPENING)

        pi.set_servo_pulsewidth(out_pin, width)

passthrough_cb.start_ticks = {}

# Set up GPIO modes
pi.set_mode(PWM_IN_THROTTLE, pigpio.INPUT)
pi.set_mode(PWM_IN_STEERING, pigpio.INPUT)
pi.set_mode(PWM_OUT_ESC, pigpio.OUTPUT)
pi.set_mode(PWM_OUT_SERVO, pigpio.OUTPUT)

# Create callbacks
cb1 = pi.callback(
    PWM_IN_THROTTLE,
    pigpio.EITHER_EDGE,
    lambda g, l, t: passthrough_cb(g, l, t, PWM_OUT_ESC, dampen=True)
)
cb2 = pi.callback(
    PWM_IN_STEERING,
    pigpio.EITHER_EDGE,
    lambda g, l, t: passthrough_cb(g, l, t, PWM_OUT_SERVO, dampen=False)
)

print("PWM passthrough with throttle dampening running. Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Cleanup
cb1.cancel()
cb2.cancel()
pi.set_servo_pulsewidth(PWM_OUT_ESC, 0)
pi.set_servo_pulsewidth(PWM_OUT_SERVO, 0)
pi.stop()

