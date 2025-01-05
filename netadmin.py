import nmap


menu_options = {
    1: 'Display Hosts',
    2: 'SSH to Host ',
    3: 'Ping Host',
    4: 'Trace Route',
    5: 'Shutdown / Restart Host',
    6: 'Edit Settings (IP range, DNS)',
    7: 'Exit'
}

def display_menu(online_hosts):
    header = f"\nNetAdmin v1.0 \t\t | Online Hosts: {online_hosts}"
    header = header.expandtabs() #expand tabs to get the correct length
    print (header)
    print ("-"*len(header))
    for option in menu_options:
        print(f"{option}. {menu_options[option]}")
    print ("-"*len(header))

def scan_network(ip_range):
    print(f"Scanning network {ip_range}...")
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')
    return nm

def display_hosts():
    #use setting file in the future
    #use cache in the future
    #use threading in the future
    nm = scan_network('10.0.0.0/29') 
    for host in nm.all_hosts():
        hostname = nm[host]['hostnames'][0]['name'] if nm[host]['hostnames'] else 'N/A'
        print(f'IP: {host} - {hostname}')
    #future display offline hosts too
    input("Press Enter to continue...")
    
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
    exit(0)

if __name__ == "__main__":
    while (True):
        display_menu(10)
        option = input("Select your option: ")
        option_handle = {
            1: display_hosts,
            2: ssh,
            3: ping,
            4: traceroute,
            5: shutdown,
            6: edit,
            7: exit_program
        }
        option_handle[int(option)]()

        
