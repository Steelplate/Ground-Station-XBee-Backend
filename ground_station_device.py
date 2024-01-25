from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress, NeighborDiscoveryMode, XBeeException, XBeeMessage
import time

class Ground_Station_Device:

    def send_data_to_device(self, remote_device: RemoteXBeeDevice, data: str) -> None:
        """
        Send data to a specific remote device asynchronously.
        Args:
        remote_device (RemoteXBeeDevice): The remote XBee device to send data to.
        data (str): The data to send.
        """

        try:
            self.local_device.send_data_async(remote_device, data.encode())
            print(f"Data sent to {remote_device.get_node_id()}")

        except XBeeException as e:
            print(f"Error sending data to {remote_device.get_node_id()}: {e}")

    def device_discovered_callback(self, device: RemoteXBeeDevice):
        print(f"Device discovered: {device.get_node_id()}")

    def modem_status_callback(self, status):
        """ Callback for modem status updates. """

        print(f"Modem Status Update: {status}")

    def data_received_callback(self, message: XBeeMessage):
        """ Callback for received data. 
            Args:
            message (XBeeMessage): The message
        
        """
        data = message.data.decode("utf8")

        print(f"Received data from {message.remote_device.get_node_id()}: {data}")

        if data == "unsubscribed":
            print(f"Device {message.remote_device.get_node_id()} is unsubscribed, sending subscription request")
            self.send_data_to_device(message.remote_device, "subscribe")

        elif data == "subscribed":
            print(f"Device {message.remote_device.get_node_id()} is now subscribed")
            self.subscribed_devices.append(message.remote_device)

            if len(self.subscribed_devices) == len(self.devices_we_care_about):
                print("All devices are subscribed!")

        else:
            self.send_data_to_backend(data)

    def send_data_to_backend(self, data: str):
        pass

    def __init__(self, port: str, baud_rate: int, deep_scan_duration: int, devices_we_care_about: [str]):
        # Constants
        self.port = port
        self.baud_rate = baud_rate
        self.deep_scan_duration = deep_scan_duration
        self.devices_we_care_about = devices_we_care_about

        self.discovered_devices = {}
        self.subscribed_devices = []

        self.local_device = None
        self.network = None

    def run(self):
        self.setup_device()
        if self.local_device == None:
            print("Unable to open the local device")
            return

        self.setup_network()
        if self.network == None:
            print("Unable to setup the network")
            return
        
        all_devices_found = self.deep_network_discovery()
        if not all_devices_found:
            print("Failed to find all devices")
            return
        
        print("All devices were found")

        self.local_device.add_data_received_callback(self.data_received_callback)


    def setup_device(self) -> None:

        self.local_device = XBeeDevice(self.port, self.baud_rate)

        try:
            self.local_device.open()
            self.local_device.add_modem_status_received_callback(self.modem_status_callback)

        except XBeeException as e:
            self.local_device = None
            print(f"XBee Exception opening local device: {e}")
        
        except Exception as e:
            print(f"Exception opening XBee Device: {e}")
            self.local_device = None
    
    def setup_network(self) -> None:
        network = self.local_device.get_network()
        network.add_device_discovered_callback(self.device_discovered_callback)
        network.set_deep_discovery_options(NeighborDiscoveryMode.FLOOD)
        network.set_deep_discovery_timeouts(node_timeout=self.deep_scan_duration, time_bw_requests=1, time_bw_scans=0)

    def do_deep_discovery_process(self) -> bool:
        self.network.start_discovery_process(deep=True, n_deep_scans=1)

        print(f"Discovery running...")
        while self.network.is_discovery_running():
            time.sleep(1)

        print(f"Discovery finished...")

        nodes = self.network.get_devices()

        for node in nodes:
            node_id = node.get_node_id()
            if node_id in self.devices_we_care_about:
                self.discovered_devices[node_id] = node

        # Check whether every device we care about has been found
        return all(device in self.discovered_devices for device in self.devices_we_care_about)

    def deep_network_discovery(self) -> bool:
        all_devices_found = False
        num_attempts = 0

        while num_attempts < 3 and not all_devices_found:
            print(f"Attempt {num_attempts + 1} of deep network discovery...")
            try:
                all_devices_found = self.do_deep_discovery_process()

            except XBeeException as e:
                print(f"Exception in deep discovery: {e}")

            print(f"{'A' if all_devices_found else 'Not a'}ll devices were found in attempt {num_attempts + 1}, {'' if num_attempts < 3 else 'not '}retrying")

        if not all_devices_found:
            return False
        
        for node_id, device in self.discovered_devices.items():
            print(f"Found device: {node_id} - {device}")

        return True




