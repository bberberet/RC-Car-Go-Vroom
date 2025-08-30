#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# ## PWM passthrough with 75% throttle dampening ##

import pigpio
import time

# GPIO pins
PWM_IN_THROTTLE = 23  # Pin 16
PWM_IN_STEERING = 24  # Pin 18
PWM_OUT_ESC = 13      # Pin 33
PWM_OUT_SERVO = 19    # Pin 35

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon!")
    exit()

# Dampening factor for throttle (0.75 dampening = 25% response)
throttle_dampening_factor = 0.25
neutral_pulse = 1500  # Neutral throttle (µs)

# Callback function with throttle dampening
def passthrough_cb(gpio_in, level, tick, out_pin):
    if level == 1:
        # Rising edge - record start time
        passthrough_cb.start_ticks[out_pin] = tick
    elif level == 0:
        # Falling edge - compute pulse width
        if out_pin in passthrough_cb.start_ticks:
            width = pigpio.tickDiff(passthrough_cb.start_ticks[out_pin], tick)
            
            if out_pin == PWM_OUT_ESC:
                # Apply throttle dampening
                dampened = neutral_pulse + throttle_dampening_factor * (width - neutral_pulse)
                pi.set_servo_pulsewidth(out_pin, dampened)
            else:
                # Pass through steering directly
                pi.set_servo_pulsewidth(out_pin, width)

passthrough_cb.start_ticks = {}

# Set GPIO modes
pi.set_mode(PWM_IN_THROTTLE, pigpio.INPUT)
pi.set_mode(PWM_IN_STEERING, pigpio.INPUT)
pi.set_mode(PWM_OUT_ESC, pigpio.OUTPUT)
pi.set_mode(PWM_OUT_SERVO, pigpio.OUTPUT)

# Register callbacks
cb1 = pi.callback(PWM_IN_THROTTLE, pigpio.EITHER_EDGE,
                  lambda g, l, t: passthrough_cb(g, l, t, PWM_OUT_ESC))
cb2 = pi.callback(PWM_IN_STEERING, pigpio.EITHER_EDGE,
                  lambda g, l, t: passthrough_cb(g, l, t, PWM_OUT_SERVO))

print("PWM passthrough with 75% throttle dampening running. Press Ctrl+C to stop.")
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

