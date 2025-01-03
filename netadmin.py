import textwrap

def main():
    print("")

def display_menu(online_hosts):
    print(textwrap.dedent(
        f"""
        NetAdmin v1.0 \t\t | Online Hosts: {online_hosts}
        ------------------------------------------------
        1. Display Hosts
        2. SSH to Host 
        3. Ping Host
        4. Trace Route
        5. Shutdown / Restart Host
        6. Edit Settings (IP range, DNS)
        7. Exit
        ------------------------------------------------
        """
))

if __name__ == "__main__":
    main()
    display_menu(10)
