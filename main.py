from ground_station_device import Ground_Station_Device
import time

# Configuration for the XBee module
PORT = "/dev/cu.usbserial-A28DMVHS"  # Serial port for local module connection
BAUD_RATE = 115200  # Baud rate for local module

DEEP_SCAN_DURATION = 20  # Duration for initial deep network discovery (in seconds)

DEVICES_WE_CARE_ABOUT = ["HPRC_Rocket"]

def main():
    device = Ground_Station_Device(PORT, BAUD_RATE, DEEP_SCAN_DURATION, DEVICES_WE_CARE_ABOUT)
    device.run()

    while True:
        print("Still going")
        time.sleep(5)

if __name__ == '__main__':
    main()
