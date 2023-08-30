#!/usr/bin/env python3
import curses
import subprocess
import time
import re
import math
import logging

# Setup logging
logging.basicConfig(filename='/tmp/cron.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Spinner states
spinner_states = ['|', '/', '-', '\\']

# Define the get_color_for_value function
def get_color_for_value(value, scale_type):
    if scale_type == 'temperature':
        if 34 <= value <= 38:
            return 1  # Green
        elif 38 < value <= 50:
            return 2  # Yellow
        elif 50 < value <= 70:
            return 4  # Orange
        else:
            return 3  # Red
    elif scale_type == 'fan_speed':
        if 2000 <= value <= 5000:
            return 1  # Green
        elif 5000 < value <= 9000:
            return 2  # Yellow
        elif 9000 < value <= 13000:
            return 4  # Orange
        else:
            return 3  # Red

def get_fan_info():
    result = subprocess.run(["sudo", "ipmitool", "sdr", "type", "fan"], capture_output=True, text=True)
    return result.stdout.strip()

def get_temp_info():
    result = subprocess.run(["sudo", "ipmitool", "sdr", "type", "temperature"], capture_output=True, text=True)
    return result.stdout.strip()

def sigmoid(x, L=1, x0=0.5, k=1):
    return L / (1 + math.exp(-k * (x - x0)))

def calculate_fan_speed(highest_temp):
    L = 100
    x0 = 60
    k = 0.15
    min_speed = 3
    max_speed = 100
    calculated_speed = int(L / (1 + math.exp(-k * (highest_temp - x0))))
    fan_speed = max(min_speed, min(calculated_speed, max_speed))
    return fan_speed

def extract_numeric_value(s, pattern):
    match = re.search(pattern, s)
    return float(match.group(1)) if match else None

def main(stdscr):
    # Initialize spinner index
    spinner_idx = 0

    subprocess.run(["sudo", "ipmitool", "raw", "0x30", "0x30", "0x01", "0x00"])
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_RED)

    stdscr.timeout(1000)

    while True:
        stdscr.clear()

        fan_info = get_fan_info().split('\n')
        temp_info = get_temp_info().split('\n')

        highest_temp = max([extract_numeric_value(s, r"\b(\d+\.?\d*) degrees C\b") for s in temp_info if extract_nu>
        fan_speeds = [extract_numeric_value(s, r"\b(\d+\.?\d*) RPM\b") for s in fan_info if extract_numeric_value(s>
        mean_fan_speed = int(sum(fan_speeds) / len(fan_speeds)) if fan_speeds else 0

        logging.info(f"Heat of Highest Temp Sensor: {highest_temp}C")
        logging.info(f"Mean Fan Speed: {mean_fan_speed} RPM")

        temp_color = get_color_for_value(highest_temp, 'temperature')
        fan_speed_color = get_color_for_value(mean_fan_speed, 'fan_speed')

        stdscr.addstr(0, 0, f"Heat of Highest Temp Sensor: {highest_temp}C ", curses.color_pair(temp_color))
        stdscr.addstr(0, 60, f"Mean Fan Speed: {mean_fan_speed} RPM ", curses.color_pair(fan_speed_color))

        stdscr.addstr(1, 0, '-' * 120)

        for i in range(max(len(fan_info), len(temp_info))):
            stdscr.addstr(i + 2, 55, "|", curses.color_pair(1))

        for idx, temp_line in enumerate(temp_info):
            stdscr.addstr(idx + 2, 0, temp_line.ljust(55))

        # Update the spinner index and draw it
        spinner_idx = (spinner_idx + 1) % len(spinner_states)
        stdscr.addstr(len(temp_info) + 4, 0, f"Running {spinner_states[spinner_idx]}", curses.color_pair(5))

        for idx, fan_line in enumerate(fan_info):
            stdscr.addstr(idx + 2, 56, " " + fan_line.ljust(54))

        current_temp = int(highest_temp)
        fan_speed = calculate_fan_speed(current_temp)

        logging.info(f"Set fan speed to {fan_speed}%")
        fan_speed_hex = format(int(fan_speed * 255 / 100), 'x')

        subprocess.run(["sudo", "ipmitool", "raw", "0x30", "0x30", "0x02", "0xff", f"0x{fan_speed_hex}"])

        stdscr.refresh()

        c = stdscr.getch()
        if c == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)

