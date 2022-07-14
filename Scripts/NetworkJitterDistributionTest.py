import os
import subprocess as sp
import sys
import time
import csv

def init(ip):
        count = 1
        interval = 1000000/400 #400 packets per second
        filename = ip + "_distribution.txt"
        open(filename, 'w').close()
        query = "hping3 -q -i u" + str(interval) + ip
        hping = sp.Popen(query.split(" "), stdout=sp.PIPE)
        while count <=  900:
                query = "ping -q -c 1 " + ip
                result = sp.getoutput(query)
                for line in result.split("\n"):
                        if "rtt" in line:
                                avg = line.split(" ")[3].split("/")[1]

                print("TTP: " + str(avg))
                data = [str(count), str(avg)]

                with open(filename, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)

                count += 1
                time.sleep(1)

        hping.kill()


if __name__ == "__main__":
        init(str(sys.argv[1]))
