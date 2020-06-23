import subprocess
import sys
import os
from threading import Thread

def port_scan(ip,path):
	print("[+] Check for open ports..")
	subprocess.Popen(["mkdir","-p","{}/nmap".format(path)])

	#First nmap scan, quick scan on 1000 ports.
	cmd = "/usr/bin/nmap -sC -sV -vvv -oA {}/nmap/initial {}".format(path,ip)
	subprocess.call(cmd,shell=True)

	#Second nmap scan, full scan on all tcp ports.
	cmd = "/usr/bin/nmap -T4 -p- -vvv -oA {}/nmap/allports {}".format(path, ip)
	subprocess.call(cmd, shell=True)

#Scan the webserver on port 80, including hidden directories.
def webserver_scan(ip,path):
	subprocess.Popen(["mkdir","{}/nikto".format(path)])
	print("[*] Nikto scan on the webserver..")
	cmd = '''nikto -h {} -C all -output web/nikto.txt {}/nikto '''.format(ip,path)
	subprocess.call(cmd,shell=True,stdout=None)

if __name__=="__main__":
	if len(sys.argv[1:])<1:
		print("\nUsage: python koalarecon.py <ip>\n")
	else:
		ip = sys.argv[1]
		path = os.getcwd()

		t1 = Thread(target=port_scan, args=(ip, path))
		t2 = Thread(target=webserver_scan, args=(ip, path))

		t1.start()
		t2.start()
		t1.join()
		t2.join()

		#subprocess making terminal fuzzy. Reset it for normal use
		subprocess.call(["stty","sane"])
		print("[*] Job Done")
