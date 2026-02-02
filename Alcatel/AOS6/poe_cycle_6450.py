from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from getpass import getpass
import time

device = {
    'device_type': 'alcatel_aos',
    'ip': '',
    'username': '',
    'password': '',
    "fast_cli": False,
    "global_delay_factor": 2
}

device['ip'] = input("Enter the device IP: ").strip()
device['username'] = input("Enter your username: ").strip()
device['password'] = getpass("Enter your password: ")

port = input("Enter port number you want to cycle: ").strip()

connection = None

try:
    connection = ConnectHandler(**device)
    print("Successfully connected to the device.")

    print(f"Disabling PoE on port {port}")
    connection.send_command_timing(f"lanpower stop {port}")

    time.sleep(5)

    print(f"Enabling PoE on port {port}")
    connection.send_command_timing(f"lanpower start {port}")

    time.sleep(3)

    print("\nPoE cycle complete.")

except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
    print(f"Connection failed: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if connection:
        connection.disconnect()
        print("\nDisconnected from the device.")
