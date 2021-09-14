import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.1.201", 9347))

# --------------------------Header-------------------------------
protocol_identifier1 = '47'
protocol_identifier2 = '74'
cmd = '17'  # Command 0x17 means PTC_COMMAND_SET_SPIN_RATE
return_code = '00'  # Useless
payload_length = '00000002'

# --------------------------Payload------------------------------
# payload = '0258'  # 600rpm
payload = '04b0'  # 1200rpm

# --------------------------str to bytes-------------------------
message_str = protocol_identifier1 + protocol_identifier2 + cmd + return_code + payload_length + payload
message_bytes = bytes.fromhex(message_str)

# --------------------------s------------------------------------
bytes_sent = sock.send(message_bytes)
return_message = sock.recv(8)
re_payload_length = int.from_bytes(return_message[4:8], byteorder='big')

print(type(return_message), return_message.hex())
print(type(re_payload_length), re_payload_length)