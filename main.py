from ground_station_device import Ground_Station_Device
import time

# Configuration for the XBee module
PORT = "/dev/cu.usbserial-A28DMVHS"  # Serial port for local module connection
BAUD_RATE = 115200  # Baud rate for local module

DEEP_SCAN_DURATION = 20  # Duration for initial deep network discovery (in seconds)

DEVICES_WE_CARE_ABOUT = ["HPRC_Rocket"]

# Dictionary to store discovered devices
discovered_devices = {}

'''

def send_data_to_device(local_device: XBeeDevice, remote_device: RemoteXBeeDevice, data: str) -> None:

    """
    Send data to a specific remote device asynchronously.
    Args:
    local_device (XBeeDevice): The local XBee device.
    remote_device (RemoteXBeeDevice): The remote XBee device to send data to.
    data (str): The data to send.
    """

    try:

        local_device.send_data_async(remote_device, data.encode())
        print(f"Data sent to {remote_device.get_node_id()}")

    except XBeeException as e:

        print(f"Error sending data to {remote_device.get_node_id()}: {e}")

def deep_network_discovery(network, attempt=1, max_attempts=3) -> None:

    """
    Perform a deep network discovery. If not all devices are found, the method retries up to max_attempts.
    Args:
    network (XBeeNetwork): The XBee network for discovery.
    attempt (int): Current attempt number.
    max_attempts (int): Maximum number of attempts allowed.
    """

    try:

        network.set_deep_discovery_options(NeighborDiscoveryMode.FLOOD)
        network.set_deep_discovery_timeouts(node_timeout=DEEP_SCAN_DURATION, time_bw_requests=1, time_bw_scans=0)
        network.start_discovery_process(deep=True, n_deep_scans=1)

        print(f"Discovery attempt {attempt} running...")

        while network.is_discovery_running():
            time.sleep(1)  # Reduces CPU usage during wait

        print("Discovery finished\n")

        # Processing discovered nodes
        nodes = network.get_devices()

        for node in nodes:

            node_id = node.get_node_id()

            if node_id in DEVICES_WE_CARE_ABOUT:
                discovered_devices[node_id] = node

        all_devices_found = all(device in discovered_devices for device in DEVICES_WE_CARE_ABOUT)

        if all_devices_found:

            for node_id, device in discovered_devices.items():
                print(f"Found device: {node_id} - {device}")

        elif attempt <= max_attempts:

            print(f"Not all devices found in attempt {attempt}. Retrying...")
            deep_network_discovery(network, attempt + 1, max_attempts)

        else:

            print(f"Failed to find all devices after {max_attempts} attempts.")
            sys.exit(1)

    except XBeeException as e:

        print(f"XBeeException occurred during discovery: {e}")

        if attempt <= max_attempts:

            print(f"Retrying discovery (Attempt {attempt + 1} of {max_attempts})...")
            deep_network_discovery(network, attempt + 1, max_attempts)

        else:

            print(f"Maximum attempts reached. Unable to complete discovery.")
            sys.exit(1)

def device_discovered_callback(device: RemoteXBeeDevice):

    """ Callback for when a device is discovered. """

    print(f"Device discovered: {device.get_node_id()}")


def modem_status_callback(status):

    """ Callback for modem status updates. """

    print(f"Modem Status Update: {status}")

def received_callback(xbee_message: XBeeMessage):

    """ Callback for received data. 
        Args:
        xbee_message (XBeeMessage): The message
    
    """

    address = xbee_message.remote_device.get_64bit_addr()
    data = xbee_message.data.decode("utf8")

    print(f"Received data from {xbee_message.remote_device.get_node_id()}: {data}")

    if data == "unsubscribed":
        send_data_to_device()

def main():

    device = XBeeDevice(PORT, BAUD_RATE)

    try:

        device.open()

        network = device.get_network()
        network.add_device_discovered_callback(device_discovered_callback)

        deep_network_discovery(network)

        device.add_data_received_callback(received_callback)
        device.add_modem_status_received_callback(modem_status_callback)

        # DEVICES_WE_CARE_ABOUT.append(device)

        print("Listening for devices and ready to send data...\n")

        while True:

            data_to_send = input("Enter data to send (type 'exit' to stop): ")

            if data_to_send.lower() == 'exit':
                break

            for device_id in DEVICES_WE_CARE_ABOUT:

                if device_id in discovered_devices:

                    # Pass the local device instance as the first argument
                    send_data_to_device(device, discovered_devices[device_id], data_to_send)

                else:

                    print(f"Device '{device_id}' not found in the network.")

    except XBeeException as e:

        print(f"Critical XBeeException occurred: {e}")
        sys.exit(1)

    finally:

        if device.is_open():
            device.close()
'''

def main():
    device = Ground_Station_Device(PORT, BAUD_RATE, DEEP_SCAN_DURATION, DEVICES_WE_CARE_ABOUT)
    device.run()

    while True:
        print("Still going")
        time.sleep(5)

if __name__ == '__main__':
    main()
