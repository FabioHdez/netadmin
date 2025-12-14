# NetAdmin v2.0 🎉
Updated the User interface from a standard CMD application to a [textual](https://textual.textualize.io/) user interface.

### Version 1 vs Version 2
The new updated version offers a more detailed user interface with a view of the hosts at all times. Now the host selection does not pull you away from the main menu screen. If a new input is required from the user or a new message needs to be displayed a modal window shows up. The new version also removes the need for text inputs in order to access the features. Overall the NetAdmin v2.0 offers a more fluid experience without giving up on the familiarity of the terminal.
![Version 1 vs Version 2](images/v1%20and%20v2%20comparison.png)

# NetAdmin v1.0

**NetAdmin v1.0** is a Python-based command-line tool designed to manage and interact with devices on a local network. NetAdmin allows users to scan networks, view online hosts, SSH into devices, ping hosts, and manage configurations seamlessly.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Main Menu](#main-menu)
  - [Options](#options)
    - [1. View Hosts](#1-view-hosts)
    - [2. SSH to Host](#2-ssh-to-host)
    - [3. Ping Host](#3-ping-host)
    - [4. Add Host](#4-add-host)
    - [5. Restore to Default](#5-restore-to-default)
    - [r. Refresh Hosts & Configuration](#r-refresh-hosts--configuration)
    - [q. Exit](#q-exit)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **View Hosts**: Display a list of currently online hosts on the network.
- **SSH to Host**: Initiate an SSH session with a selected host.
- **Ping Host**: Send ping requests to a selected host to check connectivity.
- **Add Host**: Save host details (IP, hostname, username) to the configuration for easy access.
- **Restore to Default**: Reset the configuration to its default state.
- **Refresh Hosts & Configuration**: Update the list of online hosts and reload configuration settings.
- **Exit**: Safely exit the application.

## Prerequisites

Before installing and running NetAdmin, ensure that the following prerequisites are met:

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.6 or higher
- **nmap**: Network scanning tool

### Installing nmap

#### Windows

1. Download the [nmap installer](https://nmap.org/download.html) for Windows.
2. Run the installer and follow the on-screen instructions.
3. Ensure that the installation path (e.g., `C:\Program Files (x86)\Nmap`) is added to the system's PATH environment variable.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/FabioHdez/netadmin.git
   cd netadmin
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```


## Configuration

NetAdmin uses a `config.json` file to store configuration settings such as the IP range to scan and saved hosts.

### Initial Configuration

Upon the first run, if `config.json` does not exist or is empty, the application will prompt you to set the desired IP range in the format `xxx.xxx.xxx.xxx/xx` (e.g., `192.168.1.0/24`).

### Manually Editing `config.json`

The `config.json` file has the following structure:

```json
{
    "ip_range": "192.168.1.0/24",
    "saved_hosts": {
        "192.168.1.10": {
            "hostname": "Server01",
            "username": "admin"
        },
        "192.168.1.15": {
            "hostname": "Workstation01",
            "username": "user"
        }
    }
}
```

- **ip_range**: Specifies the range of IP addresses to scan.
- **saved_hosts**: A list of hosts with their IP addresses, hostnames, and SSH usernames.

### Restoring Default Configuration

To reset the configuration to its default state:

1. Navigate to the main menu.
2. Select the **Restore to Default** option.
3. Confirm the action when prompted.

*Warning: This will erase all saved host configurations.*

## Usage

Run the NetAdmin script using Python:

```bash
python netadmin.py
```

### Main Menu

Upon launching, the main menu displays the following options:

```
NetAdmin v1.0           | Online Hosts: X
-----------------------------------------
1. View Hosts
2. SSH to Host
3. Ping Host
4. Add Host
5. Restore to Default
r. Refresh Hosts & Configuration
q. Exit
```

- **Online Hosts**: Shows the number of currently detected online hosts.


## Troubleshooting

- **No Hosts Found**
  - Ensure that the IP range in `config.json` is correct.
  - Verify that the devices you expect to see are powered on and connected to the network.
  - Check firewall settings that might block `nmap` scans.

- **nmap Not Found**
  - Ensure that `nmap` is installed on your system.
  - Verify that the `nmap` executable is added to your system's PATH.

- **Permission Issues**
  - Some `nmap` operations may require elevated privileges. Run the script with appropriate permissions if necessary.

- **SSH Connection Failures**
  - Confirm that SSH is enabled on the target host.
  - Verify that the correct username is provided.
  - Check network connectivity and firewall settings.

