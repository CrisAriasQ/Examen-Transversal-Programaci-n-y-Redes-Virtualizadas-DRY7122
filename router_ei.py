from netmiko import ConnectHandler

# Configuración de conexión al router
router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
}

# Conectar al router
net_connect = ConnectHandler(**router)
net_connect.enable()

# Configuración de EIGRP Nombrado
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

# Obtener configuración EIGRP
output = net_connect.send_command('show running-config | section eigrp')
print("EIGRP Configuration:\n", output)

# Obtener información de las IP y estado de las interfaces
output = net_connect.send_command('show ip interface brief')
print("IP Interface Brief:\n", output)

output = net_connect.send_command('show ipv6 interface brief')
print("IPv6 Interface Brief:\n", output)

# Obtener running-config
output = net_connect.send_command('show running-config')
print("Running Config:\n", output)

# Obtener show version
output = net_connect.send_command('show version')
print("Version Information:\n", output)

# Cerrar la conexión
net_connect.disconnect()
