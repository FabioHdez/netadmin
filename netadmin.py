import nmap
import sys, os, json


#global variables 
online_hosts = [] #list of online hosts; global because for cach
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
    5: 'Shutdown / Restart Host',
    6: 'Edit Settings (IP range, DNS)',
    'q': 'Exit'
}


def display_menu():
    header = f"NetAdmin v1.0 \t\t | Online Hosts: {len(online_hosts.all_hosts())}"
    header = header.expandtabs() #expand tabs to get the correct length

    global sc_width #set the screen width for ui formatting
    sc_width = len(header)

    print (header)
    print ("-"*sc_width)
    for option in menu_options:
        print(f"{option}. {menu_options[option]}")

def refresh_json():
    print("Loading configuration file...")
    global json_data
    global ip_range
    
    with open(json_file, 'r') as file:
        json_data = json.load(file)
        ip_range = json_data["ip_range"]

def scan_network(ip_range):
    print(f"Scanning network {ip_range}...")
    global online_hosts
    online_hosts = nmap.PortScanner()
    online_hosts.scan(hosts=ip_range, arguments='-sn')

def display_hosts():
    #display cached online hosts
    os.system('cls')
    print('Currently Online Hosts:')
    print ("-"*sc_width)
    for index, host in enumerate(online_hosts.all_hosts(),start=1):
        hostname = online_hosts[host]['hostnames'][0]['name'] if online_hosts[host]['hostnames'] else 'N/A'
        print(f'{index}: {host} - {hostname}')

def view_hosts():
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
                    username = input('Username: ')
                    command = fr"Echo 'Connecting to {host}...' && ssh {username}@{host}"
                    os.system(f'start cmd /k "{command}')
                    return
        else:
            print("Invalid option. Please try again.")
def ping():
    display_hosts()
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

    input()

def add():
    display_hosts()
    #user input: user can refresh the list, or go back to menu
    while True:
        user_input = input(f"\n(1-{len(online_hosts.all_hosts())}): Add host \nr: Refresh hosts\nq: Go back to the main menu\n")
        if user_input == 'r':   ###Refresh
            print ("-"*sc_width) #Print a line
            scan_network(ip_range) #scan network to refresh the cached online hosts
            display_hosts() #re-render the new cached hosts
        elif user_input == 'q':    ###Exit 
            return
        elif user_input.isdigit():      ###User selected an option
            user_input = int(user_input)
            for index, host in enumerate(online_hosts.all_hosts(),start=1):
                if user_input == index: #if its a valid option
                    print ("-"*sc_width)
                    print(f"Host: {host}")
                    hostname = input("Enter a hostname: ")
                    username = input("Enter your username for this host (Leave empty if none): ")
                    if hostname == '': hostname = 'N/A'
                    print(f"\nAdded: {host} - {hostname}")
                    #
                    try:
                        new_host = {'ip': host, 'hostname': hostname, 'username':username}
                        json_data["saved_hosts"].append(new_host)
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

def shutdown():
    print("shutdown a host")
    input()

def edit():
    #remove, restore to default
    print("edit settings")
    input()

def exit_program():
    sys.exit(0)



if __name__ == "__main__":
    os.system('cls')
    print("Loading NetAdmin v1.0...")
    refresh_json() #get config data
    scan_network(ip_range) #initial scan
    while (True):
        os.system('cls')
        display_menu()
        option = input("\nSelect your option: ").lower()
        option_handle = {
            '1': view_hosts,
            '2': ssh,
            '3': ping,
            '4': add,
            '5': shutdown,
            '6': edit,
            'q': exit_program
        }
        try:
            option_handle[option]()
        except Exception as e:
            print ("-"*sc_width)
            print("Please select a valid option.")
            continue

        
