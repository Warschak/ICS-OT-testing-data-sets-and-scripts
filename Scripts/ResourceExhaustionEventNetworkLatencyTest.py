import os
import subprocess as sp
import sys
import time
import csv

def init(ip, nmap_query):
        count = 1

        if nmap_query is None:
                filename = ip + "_default.csv"
                print("default latency")
        else:
                print(nmap_query)
                filename = nmap_query.replace(' ', '_').replace('-', '') + "_ping.csv"
                nmap = sp.Popen(nmap_query.split(" "), stdout=sp.PIPE)

        open(filename, 'w').close()
        while count <=  900:	#test for 15 minutes
                if nmap_query is not None:
                        if nmap.poll() is not None:
                                nmap = sp.Popen(nmap_query.split(" "), stdout=sp.PIPE)

                try:
                        query = ""
                        query += "ping -q -c 1 " + str(ip)	#obtain RTT
                        rtt = -1
                        result = sp.getoutput(query)
                        for line in result.split("\n"):
                                if "rtt" in line:
                                        ttp = line.split(" ")[3]
                                        rtt = ttp.split("/")[1]
                except Exception as e:
                        print(e)
                        rtt = -1

                print("RTT: " + str(rtt) + "ms")

                data = [str(count), str(rtt)]

                with open(filename, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)

                count += 1
                time.sleep(1)

        if nmap_query is not None:
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
