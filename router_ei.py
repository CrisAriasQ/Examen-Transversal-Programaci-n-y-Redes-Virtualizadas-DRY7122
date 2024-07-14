from netmiko import ConnectHandler


router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
}


net_connect = ConnectHandler(**router)
net_connect.enable()


eigrp_config = [
    'router eigrp EIGRP_TEST',
    'address-family ipv4 unicast autonomous-system 1',
    'network 10.0.0.0 0.0.0.255',
    'network 192.168.56.0 0.0.0.255',
    'passive-interface default',
    'no passive-interface GigabitEthernet1',
    'exit-address-family',
    'address-family ipv6 unicast autonomous-system 1',
    'network 2001:db8::/32',
    'passive-interface default',
    'no passive-interface GigabitEthernet1',
    'exit-address-family'
]

net_connect.send_config_set(eigrp_config)


output = net_connect.send_command('show running-config | section eigrp')
print("EIGRP Configuration:\n", output)


output = net_connect.send_command('show ip interface brief')
print("IP Interface Brief:\n", output)

output = net_connect.send_command('show ipv6 interface brief')
print("IPv6 Interface Brief:\n", output)


output = net_connect.send_command('show running-config')
print("Running Config:\n", output)


output = net_connect.send_command('show version')
print("Version Information:\n", output)


net_connect.disconnect()
