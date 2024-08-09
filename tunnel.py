import subprocess

type_of_server = input("Enter server type: kharej = 2, iran = 1: ")

ipv6iran = "fde8:b030:25cf::de01"
ipv6kharej = "fde8:b030:25cf::de02"

# مقداردهی اولیه به متغیرها
ipv4localkh = ""
ipv4localir = ""
ipv6local = ""
ipv6remote = ""
ipv4local = ""
ipv4remote = ""

if type_of_server == "1":
    ipv4localkh = "172.20.20.2"
    ipv6local = ipv6iran
    ipv6remote = ipv6kharej
    ipv4local = input("Enter IPv4 local: ")
    ipv4remote = input("Enter IPv4 remote: ")

elif type_of_server == "2":
    ipv4localir = "172.20.20.1"
    ipv6local = ipv6kharej
    ipv6remote = ipv6iran
    ipv4local = input("Enter IPv4 local: ")
    ipv4remote = input("Enter IPv4 remote: ")

else:
    print("Invalid server type entered.")
    exit(1)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Command succeeded: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {command}\nError: {e}")

# دستورات برای 6to4 tunnel
commands = [
    f"ip tunnel add 6to4_To_KH mode sit remote {ipv4remote} local {ipv4local}",
    f"ip -6 addr add {ipv6local}/64 dev 6to4_To_KH",
    "ip link set 6to4_To_KH mtu 1480",
    "ip link set 6to4_To_KH up",

    # دستورات برای GRE6 tunnel
    f"ip -6 tunnel add GRE6Tun_To_KH mode ip6gre remote {ipv6remote} local {ipv6local}",
    f"ip addr add {(ipv4localkh if type_of_server == '1' else ipv4localir)}/30 dev GRE6Tun_To_KH",
    "ip link set GRE6Tun_To_KH mtu 1436",
    "ip link set GRE6Tun_To_KH up"
]

for command in commands:
    run_command(command)
