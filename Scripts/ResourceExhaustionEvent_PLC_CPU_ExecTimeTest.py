import os
import subprocess as sp
import sys
import time
import csv
import snap7

def init(ip, nmap_query):
        client = snap7.client.Client() 	#snap7 client for PLC connection
        rack = 0			#PLC rack (change if required)
        slot = 2			#PLC slot (change if required)
        count = 1

        if nmap_query is None:
                filename = ip + "_default.csv"
                print("default exec time")
        else:
                print(nmap_query)
                filename = nmap_query.replace(' ', '_').replace('-', '') + "_cpu.csv"
                nmap = sp.Popen(nmap_query.split(" "), stdout=sp.PIPE)

        open(filename, 'w').close()
        while count <=  900:		#test for 15 minutes
                if nmap_query is not None:
                        if nmap.poll() is not None:
                                nmap = sp.Popen(nmap_query.split(" "), stdout=sp.PIPE)

                try:
                        client.connect(ip, rack, slot)
                        result = client.get_exec_time() #obtain CPU execution time
                        client.disconnect()
                except:
                        result = -1

                print("CPU TIME: " + str(result) + "ms")

                data = [str(count), str(result)]

                with open(filename, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)

                count += 1
                time.sleep(1)

        if nmap_query is not None:	#Kill running scans
                if nmap.poll() is None:
                        nmap.kill()


if __name__ == "__main__":
        ip = str(sys.argv[1])
        init(ip, None)
        init(ip, "sudo nmap -sS -p- " + ip)
        init(ip, "sudo nmap -sT -p- " + ip)
        init(ip, "sudo nmap -sU -p- " + ip)
        init(ip, "sudo nmap -sY -p- " + ip)
        init(ip, "sudo nmap -sN -p- " + ip)
        init(ip, "sudo nmap -sF -p- " + ip)
        init(ip, "sudo nmap -sX -p- " + ip)
        init(ip, "sudo nmap -sA -p- " + ip)
        init(ip, "sudo nmap -sW -p- " + ip)
        init(ip, "sudo nmap -sM -p- " + ip)
