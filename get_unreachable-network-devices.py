import requests
import urllib3
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Disable warnings
urllib3.disable_warnings()

# --- CONFIGURATION ---
host = os.getenv("DNAC_HOST")
user = os.getenv("DNAC_USER")
password = os.getenv("DNAC_PASS")

# --- STEP 1: Authenticate ---
print("Logging in...")
url_auth = f"https://{host}/dna/system/api/v1/auth/token"
response = requests.post(url_auth, auth=(user, password), verify=False)
token = response.json()['Token']

# --- INTERMEDIATE STEP: Get maintenance data ---
print("Fetching maintenance list...")
url_maint = f"https://{host}/dna/intent/api/v1/networkDeviceMaintenanceSchedules"
headers = {'X-Auth-Token': token}

response_maint = requests.get(url_maint, headers=headers, verify=False)
data_maint = response_maint.json()

# Create list of IDs that are in maintenance
maintenance_ids = []
if 'response' in data_maint and data_maint['response']:
    for schedule in data_maint['response']:
        maintenance_ids.extend(schedule.get('networkDeviceIds', []))

# --- STEP 2: Query data ---
print("Fetching devices...")
url_devices = f"https://{host}/dna/intent/api/v1/network-device"

response = requests.get(url_devices, headers=headers, verify=False)
data = response.json()

# --- STEP 3: Output ---
# Iterate through the 'response' list
for device in data['response']:
    network_device_id = device.get('id', 'N/A')
    hostname = device.get('hostname', 'N/A')
    ip = device.get('managementIpAddress', 'N/A')
    mac = device.get('macAddress', 'N/A')
    status = device.get('reachabilityStatus', 'N/A')
    network_device_type = device.get('type', 'N/A')

    # Check: Is the device in maintenance?
    is_maintenance = False
    if network_device_id in maintenance_ids:
        is_maintenance = True

    # Only output if Unreachable AND NOT in maintenance
    if status == 'Unreachable' and is_maintenance == False:
        printText = f"| Hostname: {hostname} | Type: {network_device_type} | IP: {ip} | MAC: {mac} | Status: {status}  | "
        print(printText)