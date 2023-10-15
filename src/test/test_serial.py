import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the TX and RX GPIO pins
TX_PIN = 14  # BCM GPIO number for TX (Transmit)
RX_PIN = 15  # BCM GPIO number for RX (Receive)

# Set the TX pin as an output and RX pin as an input
GPIO.setup(TX_PIN, GPIO.OUT)
GPIO.setup(RX_PIN, GPIO.IN)

# Short the TX and RX pins
GPIO.output(TX_PIN, GPIO.HIGH)

try:
    while True:
        # Read the state of the RX pin
        rx_state = GPIO.input(RX_PIN)

        if rx_state == GPIO.HIGH:
            print("Loopback detected: RX is HIGH")
        else:
            print("No loopback detected: RX is LOW")

        # Wait for a moment
        time.sleep(1)

except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C
    GPIO.cleanup()
