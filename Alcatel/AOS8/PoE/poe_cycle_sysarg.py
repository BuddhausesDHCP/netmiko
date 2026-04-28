from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import sys
import time

def usage():
    print("Usage: python script.py <ip> <username> <password> <port>")
    print("  ip        - Device IP address")
    print("  username  - Login username")
    print("  password  - Login password")
    print("  port      - Port number to PoE cycle")
    print("\nExample: python script.py 192.168.1.1 admin secretpass 1/1/1")
    sys.exit(1)

if len(sys.argv) != 5:
    print("Error: Expected 4 arguments, got", len(sys.argv) - 1)
    usage()

_, ip, username, password, port = sys.argv

device = {
    'device_type': 'alcatel_aos',
    'ip': ip,
    'username': username,
    'password': password,
    "fast_cli": False,
    "global_delay_factor": 2
}

connection = None
try:
    connection = ConnectHandler(**device)
    print("Successfully connected to the device.")
    print(f"Disabling PoE on port {port}")
    connection.send_config_set([f"lanpower port {port} admin-state disable"])
    time.sleep(5)
    print(f"Enabling PoE on port {port}")
    connection.send_config_set([f"lanpower port {port} admin-state enable"])
    time.sleep(2)
    print("\nPoE cycle complete.")
except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if connection:
        connection.disconnect()
        print("\nDisconnected from the device.")
