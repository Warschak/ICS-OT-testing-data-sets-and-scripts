#!/usr/bin/env python3

import os
import subprocess as sp
import sys
import time

import csv

def init(ip):
	count = 500000 #start delay -> 2 packets per second
	file_name = ip + ".csv"

	open(file_name, "w").close()

	while count > 0:
		interval = count
		query = ""
		query += "hping3 -q -i u" + str(int(interval)) + " " + str(ip) 	#network stress test component
		print(query)
		hping3 = sp.Popen(query.split(" "), stdout=sp.DEVNULL)
		query = ""
		query += "ping -q -c 100 " + str(ip) 				#data collection component
		result = sp.getoutput(query)
		hping3.kill()
		for line in result.split("\n"):
			if "packet loss, time" in line:
				loss = line.split(" ")[5]
			if "rtt" in line:					#record average and max TTP
				ttp = line.split(" ")[3]
				avg = ttp.split("/")[1]
				max = ttp.split("/")[2]

		print(str(1000000/count))
		data = [str(1000000/count), avg, max, loss.split("%")[0]]

		with open(file_name, "a") as f:					#write data to CSV file
			writer = csv.writer(f)
			writer.writerow(data)

		print("PACKET LOSS: " + loss)
		print("AVG TTP: " + avg)
		print("MAX TTP: " + max)
		time.sleep(10)
	
		if count > 100000:						#reduce delay between packets
			count -= 10000
		elif count > 10000:
			count -= 1000
		elif count > 1000:
			count -= 100
		elif count > 100:
			count -= 10
		else:
			count -= 1

if __name__ == "__main__":
	input("Starting this script will overwrite previous data - confirm?")
	ip_list = sys.argv[1].split(',')
	print(ip_list)
	
	for ip in ip_list:
		init(ip)
