import requests
import urllib3
from dotenv import load_dotenv
import os
import json

load_dotenv()
urllib3.disable_warnings()

host = os.getenv("DNAC_HOST")
user = os.getenv("DNAC_USER")
password = os.getenv("DNAC_PASS")

# 1. Login
print("Logging in...")
url_auth = f"https://{host}/dna/system/api/v1/auth/token"
resp = requests.post(url_auth, auth=(user, password), verify=False)
token = resp.json()['Token']
print("Login OK.")

# 2. Fetch data
print("Fetching all maintenance schedules...")

# CORRECTION: We remove "/${id}" at the end.
# We retrieve the list of all schedules. This prevents the 400 error.
url = f"https://{host}/dna/intent/api/v1/networkDeviceMaintenanceSchedules"

headers = {
    'X-Auth-Token': token,
    'Content-Type': 'application/json'
}

response = requests.get(url, headers=headers, verify=False)

# 3. Check result
data = response.json()

for device in data['response']:
    description = device.get('description', 'N/A')
    network_device = device.get('networkDeviceIds', 'N/A')
    print(f"Maintenance Schedule: {description}, Affected Device IDs: {network_device}\n")