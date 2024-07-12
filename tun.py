import os
import yaml
import subprocess

irorkharej = input("Enter the server (kharej = 1, iran = 2): ")

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run command {command}: {e}")
        exit(1)

def unmask_and_start_networkd():
    commands = [
        ['systemctl', 'unmask', 'systemd-networkd.service'],
        ['systemctl', 'enable', 'systemd-networkd.service'],
        ['systemctl', 'start', 'systemd-networkd.service']
    ]
    for command in commands:
        run_command(command)

def install_packages():
    packages = ['iproute2', 'nano', 'netplan.io']
    for package in packages:
        run_command(['apt-get', 'install', '-y', package])
    print("Packages installed successfully.")


def create_netplan_config(local, remote):
    if irorkharej == '1':
        ip6 = 'fd19:db99:3788:eded::2001/64'
    elif irorkharej == '2':
        ip6 = 'fd19:db99:3788:eded::2002/64'
    else:
        print("Invalid input for server location.")
        exit(1)
    
    netplan_config = {
        'network': {
            'version': 2,
            'tunnels': {
                'tunel01': {
                    'mode': 'sit',
                    'local': local,
                    'remote': remote,
                    'addresses': [ip6],
                    'mtu': 1500
                },
            }
        }
    }

    netplan_dir = '/etc/netplan/'
    netplan_file = os.path.join(netplan_dir, 'tun1.yaml')

    # Remove existing netplan file if it exists
    if os.path.exists(netplan_file):
        os.remove(netplan_file)

    # Create netplan directory if it doesn't exist
    if not os.path.exists(netplan_dir):
        os.makedirs(netplan_dir)

    # Write new netplan configuration
    with open(netplan_file, 'w') as file:
        yaml.dump(netplan_config, file, default_flow_style=False)

def apply_netplan():
    run_command(['netplan', 'apply'])
    print("Netplan configuration applied successfully.")

def main():
    unmask_and_start_networkd()
    install_packages()

    local = input("Enter the local IP address for tunel01: ")
    remote = input("Enter the remote IP address for tunel01: ")
    
    create_netplan_config(local, remote)
    apply_netplan()

if __name__ == "__main__":
    main()
