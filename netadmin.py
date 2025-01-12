import nmap
import sys, os

#global variables 
online_hosts = [] #list of online hosts; global because for cach
sc_width = 0 #screen width

#options for the menu
menu_options = {
    1: 'Display Hosts',
    2: 'SSH to Host ',
    3: 'Ping Host',
    4: 'Trace Route',
    5: 'Shutdown / Restart Host',
    6: 'Edit Settings (IP range, DNS)',
    'q': 'Exit'
}
def clear_screen():
    if (os.name == 'nt'):
        os.system('cls')
    else: 
        os.system('clear')

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
    #use setting file in the future
    #display saved offline hosts too

    #display cached online hosts
    def display():
        clear_screen()
        for host in online_hosts.all_hosts():
            hostname = online_hosts[host]['hostnames'][0]['name'] if online_hosts[host]['hostnames'] else 'N/A'
            print(f'IP: {host} - {hostname}')
    display()
    #user input: user can refresh the list, or go back to menu
    while True:
        user_input = input("\n1: Refresh hosts\nq: Go back to the main menu\n")
        if user_input == '1':
            print ("-"*sc_width)
            scan_network('10.0.0.0/28') #scan network to refresh the cached online hosts
            display()
        elif user_input == 'q':
            return
        else:
            print("Invalid option. Please try again.")
            continue
    
def ssh():
    print("ssh to a host")
    input()

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
    clear_screen()
    print("Loading NetAdmin v1.0...")
    scan_network('10.0.0.0/28') #initial scan
    while (True):
        clear_screen()
        display_menu(len(online_hosts.all_hosts()))
        option = input("\nSelect your option: ").lower()
        option_handle = {
            '1': display_hosts,
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

        
