import I2C_LCD_driver
from time import *
import os
import subprocess
import logging
import socket
from collections import namedtuple

lcd = I2C_LCD_driver.lcd()


def get_ip_address():  # get the local ip address
    ifconfig = os.popen('ifconfig eth0 | grep "inet 10" | cut -c 14-25')
    local_ip = ifconfig.read()
    # print (local_ip)
    return "IP: " + local_ip


def get_cpu_temp():  # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format(float(cpu)/1000) + ' C'


def check_service_status():  # check nginx system status
    status = os.system('systemctl status ' + "unifi" + ' > /dev/null')
    return status


def unifi_status():  # translate nginx status into running or stopped
    if (check_service_status() == 0):
        status = "Running"
    else:
        status = "Stopped"
    return status


def pihole_get_status():  # get pihole status
    stream = os.popen(
        'pihole status | grep "DNS" | grep -Po "(?<=DNS service is)\W*\K[^ ]*"')
    pihole = stream.read()
    stream.close()
    # print(pihole)
    return pihole


def uptime():
    uptime = os.times()[4]
    return uptime


def get_disk_usage():
    path = '/'
    st = os.statvfs(path)

    # free blocks available * fragment size
    bytes_avail = (st.f_bavail * st.f_frsize)
    gigabytes = bytes_avail / 1024 / 1024 / 1024
    return (gigabytes)


def loop():
    lcd.backlight(1)     # turn on LCD backlight
    while(True):
        lcd.lcd_clear()
        # banner display
        lcd.lcd_display_string('PiHole/UniFi', 1)
        # display CPU temperature
        lcd.lcd_display_string('CPU TMP: ' + get_cpu_temp(), 2)
        sleep(10)
        lcd.lcd_clear()
        lcd.lcd_display_string('UniFi Status', 1)
        lcd.lcd_display_string('UniFi: ' + unifi_status(), 2)
        sleep(10)
        lcd.lcd_clear()
        lcd.lcd_display_string('PiHole Status', 1)
        lcd.lcd_display_string('DNS: ' + pihole_get_status(), 2)
        sleep(10)
        lcd.lcd_clear()
        lcd.lcd_display_string(
            "DiskFree: " + str(round(get_disk_usage(), 2)) + "GB", 1)
        lcd.lcd_display_string(get_ip_address(), 2)
        sleep(10)
        lcd.lcd_clear()
        lcd.backlight(0)


def destroy():  # destory commands
    lcd.lcd_clear()
    lcd.lcd_display_string("Goodbye", 1)
    sleep(1)
    lcd.lcd_clear()
    lcd.backlight(0)


if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        print('Shutting Down')
        destroy()
