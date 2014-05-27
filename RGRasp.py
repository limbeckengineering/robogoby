#!/bin/env/python

import time
import config
import socket
import multiprocessing
import os
import select
import RPi.GPIO as GPIO

def led(dutyDwn, dutyStr, signal):
	if signal==1:
		GPIO.setmodea(GPIO.BOARD)
		GPIO.setup(config.ledDwn, GPIO.OUT)
		GPIO.setup(config.ledStr, GPIO.OUT)
		ledD = GPIO.PWM(config.ledDwn, 60)
		ledS = GPIO.PWM(config.ledStr, 60)
		ledD.start(0)
		leds.start(0)
	else:
		ledD.ChangeDutyCycle(dutyDwn)
		ledS.ChangeDutyCycle(dutyStr)

def read(data):
	print "starting parse"
	values = { } 
	dat = data.split(";")
	print dat
	for i in range(0,len(dat)):
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
	os.system(H1)
	os.system(H2)
	os.system(V1)
	os.system(V2)
	os.system(F)
	leds = multiprocessing.Process(name="LEDS", target=led, args=(values[5][1], values[6][1], 0))
	led.start()
	led.terminate()
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
						led(50, 50, 1)
						read(data)

					except:
						#send(CONNECTION_LIST1, RaspServer, sock, "Kicking from OCUserver")
						sock.close()
						CONNECTION_LIST1.remove(sock)
						continue
