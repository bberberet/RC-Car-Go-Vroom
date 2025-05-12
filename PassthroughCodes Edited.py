#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# ## PWM passthrough with steering dampening (no fallback) ##

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

# Dampening settings
steering_smoothed = None  # No fallback value
alpha = 0.2  # Damping factor (0 = full dampening, 1 = no dampening)

# Store start ticks for input pulses
def passthrough_cb(gpio_in, level, tick, out_pin):
    global steering_smoothed
    if level == 1:
        # Rising edge - start of pulse
        passthrough_cb.start_ticks[out_pin] = tick
    elif level == 0:
        # Falling edge - end of pulse
        if out_pin in passthrough_cb.start_ticks:
            width = pigpio.tickDiff(passthrough_cb.start_ticks[out_pin], tick)
            
            if out_pin == PWM_OUT_SERVO:
                # Apply smoothing only if this isn't the first pulse
                if steering_smoothed is None:
                    steering_smoothed = width
                else:
                    steering_smoothed = alpha * width + (1 - alpha) * steering_smoothed
                pi.set_servo_pulsewidth(out_pin, steering_smoothed)
            else:
                # Pass through throttle directly
                pi.set_servo_pulsewidth(out_pin, width)

passthrough_cb.start_ticks = {}

# Set GPIO modes
pi.set_mode(PWM_IN_THROTTLE, pigpio.INPUT)
pi.set_mode(PWM_IN_STEERING, pigpio.INPUT)
pi.set_mode(PWM_OUT_ESC, pigpio.OUTPUT)
pi.set_mode(PWM_OUT_SERVO, pigpio.OUTPUT)

# Set up callbacks
cb1 = pi.callback(PWM_IN_THROTTLE, pigpio.EITHER_EDGE,
                  lambda g, l, t: passthrough_cb(g, l, t, PWM_OUT_ESC))
cb2 = pi.callback(PWM_IN_STEERING, pigpio.EITHER_EDGE,
                  lambda g, l, t: passthrough_cb(g, l, t, PWM_OUT_SERVO))

print("PWM passthrough with steering dampening running. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Cleanup on exit
cb1.cancel()
cb2.cancel()
pi.set_servo_pulsewidth(PWM_OUT_ESC, 0)
pi.set_servo_pulsewidth(PWM_OUT_SERVO, 0)
pi.stop()

