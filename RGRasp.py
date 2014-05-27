#!/bin/env/python

import time
import config
import socket
import multiprocessing
import os
import select


def read(data):
	print "starting parse"
	values = { } 
	#args = dict(item.split(":") for item in data.split(";"))
	dat = data.split(";")
	print dat
	for i in range(0,7):
		values[i]=dat[i].split(":")
	H1 = "sudo echo " + str(config.H1motor) + "=" + values[2][1] + " > /dev/servoblaster"
	print H1
	H2 = "sudo echo " + str(config.H2motor) + "=" + values[3][1] + " > /dev/servoblaster"
	print H2
	V1 = "sudo echo " + str(config.V1motor) + "=" + values[0][1] + " > /dev/servoblaster"
	print V1
	V2 = "sudo echo " + str(config.V2motor) + "=" + values[1][1] + " > /dev/servoblaster"
	print V2
	F = "sudo echo " + str(config.Fmotor) + "=" + values[4][1] + " > /dev/servoblaster"
	print F
	led1 = "sudo echo " + str(config.ledDwn) + "=" + values[5][1] + " > /dev/servoblaster"
	print led1
	led2 = "sudo echo " + str(config.ledStr) + "=" + values[6][1] + " > /dev/servoblaster"
	print led2
	os.system(H1)
	os.system(H2)
	os.system(V1)
	os.system(V2)
	os.system(F)
	os.system(led1)
	os.system(led2)
	print "all data sent"


def send(CONNECTION_LIST1, RaspServer,  sock, message):
	for socket in CONNECTION_LIST1:
		if socket != RaspServer:
			try:
				message = message.encode(encoding='UTF-8')
				socket.sendall(message)
			except:
				socket.close()
				CONNECTION_LIST1.remove(socket)

class RaspServer1:
	def __init__(self):
		CONNECTION_LIST1 = []
		RaspServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		RaspServer.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM, 1)
		RaspServer.bind((config.HOST, config.RPiPort))
		print "Starting RaspServer..."
		RaspServer.listen(10)

		CONNECTION_LIST1.append(RaspServer)

		while 1:
			read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST1, [], [])

			for sock in read_sockets:
				if sock == RaspServer:
					sock, addr = RaspServer.accept()
					CONNECTION_LIST1.append(sock)
					#send(CONNECTION_LIST1, RaspServer, sock, "Connected: Horizontal and Rear Thrusters")
				else:
					try:
						data = sock.recv(config.RECV_BUFFER)
						read(data)

					except:
						#send(CONNECTION_LIST1, RaspServer, sock, "Kicking from OCUserver")
						sock.close()
						CONNECTION_LIST1.remove(sock)
						continue
