import nmap
import sys, os

#global variables 
online_hosts = [] #list of online hosts; global because for cach
sc_width = 0 #screen width


#options for the menu
menu_options = {
    1: 'View Hosts',
    2: 'SSH to Host ',
    3: 'Ping Host',
    4: 'Trace Route',
    5: 'Shutdown / Restart Host',
    6: 'Edit Settings (IP range, DNS)',
    'q': 'Exit'
}


def display_menu(online_hosts):
    
    header = f"NetAdmin v1.0 \t\t | Online Hosts: {online_hosts}"
    header = header.expandtabs() #expand tabs to get the correct length

    global sc_width #set the screen width for ui formatting
    sc_width = len(header)

    print (header)
    print ("-"*sc_width)
    for option in menu_options:
        print(f"{option}. {menu_options[option]}")


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
            scan_network('10.0.0.0/28') #scan network to refresh the cached online hosts
            display_hosts()
        elif user_input == 'q':
            return
        else:
            print("Invalid option. Please try again.")
            continue
    
def ssh():
    display_hosts()
    while True:
        user_input = input("\nSelect the ID of the host you want to connect to or: \nr: Refresh hosts\nq: Go back to the main menu\n")
        if user_input == 'r':
            print ("-"*sc_width)
            scan_network('10.0.0.0/28') #scan network to refresh the cached online hosts
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
    print("ping a host")
    input()

def traceroute():
    print("traceroute a host")
    input()

def shutdown():
    print("shutdown a host")
    input()

def edit():
    print("edit settings")
    input()

def exit_program():
    sys.exit(0)



if __name__ == "__main__":
    os.system('cls')
    print("Loading NetAdmin v1.0...")
    scan_network('10.0.0.0/28') #initial scan
    while (True):
        os.system('cls')
        display_menu(len(online_hosts.all_hosts()))
        option = input("\nSelect your option: ").lower()
        option_handle = {
            '1': view_hosts,
            '2': ssh,
            '3': ping,
            '4': traceroute,
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

        
