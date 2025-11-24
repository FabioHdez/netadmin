import json, re, nmap, subprocess

#globals
json_file = 'config.json'
json_data = '' #this is also a cached value
ip_range = ''
online_hosts = [] #list of online hosts; global because for caching



def refresh_json():
    """Update settings from the config.json file. """

    # print("Loading configuration file...")
    global json_data
    global ip_range

    with open(json_file, 'r') as file:
        json_data = json.load(file)
        ip_range = json_data["ip_range"]

def create_json():


    pass

def init_config():
    """Initial configuration for clean installations and restoring to default"""
    #set ip range
    ip_range_pattern = r'^((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\/(3[0-2]|[12]?\d)$'
    while True:
        user_ip_range = input("Please set the desired IP range (xxx.xxx.xxx.xxx/xx): ")
        if re.match(ip_range_pattern,user_ip_range):
            break
        print("IP range not valid.")
    
    template = {
        "ip_range":user_ip_range,
        "saved_hosts":{}
    }
    with open(json_file, 'w') as file:
        json.dump(template, file, indent=4)
    
    print("Initial configuration was loaded.")

def scan_network(ip_range):
    """Scan the network using nmap."""
    print(f"Scanning network {ip_range}...")
    global online_hosts
    online_hosts = nmap.PortScanner()
    try:
        online_hosts.scan(hosts=ip_range, arguments='-sn',timeout=30)
        if(len(online_hosts.all_hosts()) == 0): raise Exception    
    except Exception:
        print("\nNo hosts were found. Please edit the config.json file with a valid IP range / restore your config.json file\nAlso make sure that your hosts are online!")
        input("Press enter to continue...")
