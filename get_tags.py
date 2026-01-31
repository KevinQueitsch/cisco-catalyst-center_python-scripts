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

# --- STEP 2: Query data ---
print("Fetching tags...")
url_tags = f"https://{host}/dna/intent/api/v1/tag"
headers = {'X-Auth-Token': token}
response = requests.get(url_tags, headers=headers, verify=False)
data = response.json()

# --- STEP 3: Output ---
# Iterate through the 'response' list
for tag in data['response']:
    tag_id = tag.get('id', 'N/A')
    tag_name = tag.get('name', 'N/A')

    printText = f"| Tag ID: {tag_id} | Name: {tag_name} | "
    print(printText)