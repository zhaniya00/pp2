import json


with open("GitHub_works/pp2/practice_4/json/sample_data.json", "r") as file:
    data = json.load(file)

# Print header
print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 80)

# Parse JSON
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    
    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")
    
    print(f"{dn:50} {descr:20} {speed:8} {mtu:6}")