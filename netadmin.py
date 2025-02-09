import nmap
import sys, os, json

#global variables 
online_hosts = [] #list of online hosts; global because for caching
sc_width = 0 #screen width

#json
json_file = 'config.json'
json_data = '' #this is also a cached value
ip_range = ''

#options for the menu
menu_options = {
    1: 'View Hosts',
    2: 'SSH to Host ',
    3: 'Ping Host',
    4: 'Add Host',
    5: 'Restore to Default',
    'r': 'Refresh Hosts & Configuration',
    'q': 'Exit'
}


def display_menu():
    """Display the menu with all the features of the application."""

    header = f"NetAdmin v1.0 \t\t | Online Hosts: {len(online_hosts.all_hosts())}"
    header = header.expandtabs() #expand tabs to get the correct length

    global sc_width #set the screen width for ui formatting
    sc_width = len(header)
    
    #Actual output
    print (header)
    print ("-"*sc_width)
    for option in menu_options:
        print(f"{option}. {menu_options[option]}")

def refresh_json():
    """Update settings from the config.json file. """

    print("Loading configuration file...")
    global json_data
    global ip_range

    with open(json_file, 'r') as file:
        json_data = json.load(file)
        ip_range = json_data["ip_range"]

def get_json_host(ip):
    """Get the saved host from the config.json file"""
    try:
        host = json_data["saved_hosts"][ip]
        return {"ip":ip, "hostname": host["hostname"], "username":host["username"]}    
    except Exception as e:
        return None
        
def scan_network(ip_range):
    """Scan the network using nmap."""
    print(f"Scanning network {ip_range}...")
    global online_hosts
    online_hosts = nmap.PortScanner()
    online_hosts.scan(hosts=ip_range, arguments='-sn')
    if(len(online_hosts.all_hosts()) == 0):
        print("\nNo hosts were found. Please edit the config.json file with a valid IP range / restore your config.json file\nAlso make sure that your hosts are online!")
        input("Press enter to continue...")

def display_hosts():
    """Display cached hosts"""
    os.system('cls')
    print('Currently Online Hosts:')
    print ("-"*sc_width)
    for index, host in enumerate(online_hosts.all_hosts(),start=1):
        hostname = get_json_host(host)
        if not hostname: #check dns hostname if there is no saved hostname
            hostname = online_hosts[host]['hostnames'][0]['name'] if online_hosts[host]['hostnames'] else 'N/A'
        else:
            hostname = hostname["hostname"] + " (saved)"
        print(f'{index}: {host} - {hostname}')

def view_hosts():
    """First menu option. Shows all the online hosts"""
    display_hosts()
    #user input: user can refresh the list, or go back to menu
    while True:
        user_input = input("\nr: Refresh hosts\nq: Go back to the main menu\n")
        if user_input == 'r':
            print ("-"*sc_width)
            scan_network(ip_range) #scan network to refresh the cached online hosts
            display_hosts()
        elif user_input == 'q':
            return
        else:
            print("Invalid option. Please try again.")
            continue
    
def ssh():
    """System call to ssh into the host. If the host is saved, it will use the username from the config.json"""
    display_hosts()
    while True:
        user_input = input(f"\n(1-{len(online_hosts.all_hosts())}): SSH into host \nr: Refresh hosts\nq: Go back to the main menu\n")
        if user_input == 'r':
            print ("-"*sc_width)
            scan_network(ip_range) #scan network to refresh the cached online hosts
            display_hosts()
        elif user_input == 'q':
            return
        elif user_input.isdigit():
            user_input = int(user_input)
            for index, host in enumerate(online_hosts.all_hosts(),start=1):
                if user_input == index:
                    username = get_json_host(host)
                    if not username:
                        username = input('Username: ')
                    else: username = username['username']
                    command = fr"Echo 'Connecting to {host}...' && ssh {username}@{host}"
                    os.system(f'start cmd /k "{command}')
                    return
        else:
            print("Invalid option. Please try again.")

def ping():
    """System call to ping a host."""
    display_hosts()
    while True:
        user_input = input(f"\n(1-{len(online_hosts.all_hosts())}): SSH into host \nr: Refresh hosts\nq: Go back to the main menu\n")
        if user_input == 'r':
            print ("-"*sc_width)
            scan_network(ip_range) #scan network to refresh the cached online hosts
            display_hosts()
        elif user_input == 'q':
            return
        elif user_input.isdigit():
            user_input = int(user_input)
            for index, host in enumerate(online_hosts.all_hosts(),start=1):
                if user_input == index:
                    os.system(fr"ping {host}")
                    input("Press enter to continue...")
                    return
        else:
            print("Invalid option. Please try again.")

def add():
    """Save a host to the config.json file"""
    display_hosts()
    #user input: user can refresh the list, or go back to menu
    while True:
        user_input = input(f"\n(1-{len(online_hosts.all_hosts())}): Add host \nr: Refresh hosts\nq: Go back to the main menu\n")
        #Refresh
        if user_input == 'r':   
            print ("-"*sc_width) #Print a line
            scan_network(ip_range) #scan network to refresh the cached online hosts
            display_hosts() #re-render the new cached hosts
        #Exit
        elif user_input == 'q':
            return
        #User selected an option
        elif user_input.isdigit():
            user_input = int(user_input)
            for index, host in enumerate(online_hosts.all_hosts(),start=1):
                if user_input == index: #if its a valid option
                    print ("-"*sc_width)
                    print(f"Host: {host}")
                    if get_json_host(host): #host already exists
                        print("The host already exists. You can try to remove it or edit it on the 'edit' menu option.")
                        input("Press enter to continue...")
                        return
                    hostname = input("Enter a hostname: ")
                    username = input("Enter your username for this host (Leave empty if none): ")
                    if hostname == '': hostname = 'N/A'
                    print(f"\nAdded: {host} - {hostname}")
                    try:
                        json_data["saved_hosts"][host] = {'hostname': hostname, 'username':username}
                        with open(json_file,'w') as file:
                            json.dump(json_data, file, indent = 4)
                        refresh_json()
                    except Exception as e:
                        print("There is a problem with the JSON file. You can try to fix it manually (config.json) or restore to default on the 'edit' menu option.")
                    input("Press enter to continue...")
                    return
        else:
            print("Invalid option. Please try again.")
            continue

def refresh():
    """Full refresh of the configuration and online hosts cache"""
    os.system('cls')
    print("Refreshing configuration...")
    print ("-"*sc_width) #Print a line

    refresh_json()
    scan_network(ip_range)

    input("\nCompleted. Press enter to continue...")


def init_config():
    """Initial configuration for clean installations and restoring to default"""
    #set ip range
    user_ip_range = input("Please set the desired IP range (xxx.xxx.xxx.xxx/xx): ")
    template = {
        "ip_range":user_ip_range,
        "saved_hosts":{}
    }
    with open(json_file, 'w') as file:
        json.dump(template, file, indent=4)
    
    print("Initial configuration was loaded.")

def restore():
    """Restore to default menu option."""
    #restore to default
    print("WARNING: Continuing will remove all the configuration saved onthe config.json file!")
    confirmation = input("Do you wish to continue? (y/n): ").lower()
    if (confirmation != 'y' and confirmation != 'yes'):
        input("Returning to menu. Press enter to continue...")
        return
    init_config()
    refresh()
    
def exit_program():
    sys.exit(0)

if __name__ == "__main__":
    os.system('cls')
    print("Loading NetAdmin v1.0...")
    refresh_json() #get config data
    if (ip_range == ''):init_config()
    scan_network(ip_range) #initial scan
    while True:
        os.system('cls')
        display_menu()
        option = input("\nSelect your option: ").lower()
        option_handle = {
            '1': view_hosts,
            '2': ssh,
            '3': ping,
            '4': add,
            '5': restore,
            'r': refresh,
            'q': exit_program
        }
        try:
            option_handle[option]()
        except Exception as e:
            print ("-"*sc_width)
            print("Please select a valid option.")
            continue