import json, re, nmap, subprocess

#globals
json_file = 'config.json'
json_data = '' #this is also a cached value
ip_range = ''
online_hosts = [] #list of online hosts; global because for caching



def refresh_json():
    """Update settings from the config.json file. """
    with open(json_file, 'r') as file:
        json_data = json.load(file)
        #ip_range = json_data["ip_range"]
    return json_data

def create_json():


    pass

def valid_ip(ip_range) -> bool:
    """Helper function to validate an IP"""
    ip_range_pattern = r'^((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\/(3[0-2]|[12]?\d)$'
    if re.match(ip_range_pattern,ip_range):
        return True
    return False


def init_config(user_ip_range = None):
    """Initial configuration for clean installations and restoring to default"""
    #set ip range
    while not user_ip_range:
        user_ip_range = input("Please set the desired IP range (xxx.xxx.xxx.xxx/xx): ")
        if valid_ip(user_ip_range):
            print("IP range not valid.")
            user_ip_range = None
    
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
        online_hosts.scan(hosts=ip_range, arguments='-sn',timeout=15)
        if(len(online_hosts.all_hosts()) == 0): raise Exception    
    except Exception:
        print("\nNo hosts were found. Please edit the config.json file with a valid IP range / restore your config.json file\nAlso make sure that your hosts are online!")
    return online_hosts.all_hosts()

def add_host(host: str, hostname: str, username: str):
    print(f'host: {host}')
    print(f'hostname: {hostname}')
    print(f'username: {username}')

    json_data = refresh_json()
    json_data["saved_hosts"][host] = {'hostname': hostname, 'username':username}

    # raises exception
    with open(json_file,'w') as file:
        json.dump(json_data, file, indent = 4)

    return json_data

def get_json_host(json_data, ip):
    """Get the saved host from the config.json file"""
    try:
        host = json_data["saved_hosts"][ip]
        return {"ip":ip, "hostname": host["hostname"], "username":host["username"]}    
    except Exception as e:
        return None