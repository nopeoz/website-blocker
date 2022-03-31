import time
from datetime import datetime as dt
newline = ""

blocksites = [
    'twitter.com', 'reddit.com', 'facebook.com',
]

sites_to_block1 = list(map(lambda x: "www."+x, blocksites))
sites_to_block2 = list(map(lambda x: x, blocksites))
sites_to_block3 = list(map(lambda x: "*."+x, blocksites))  # block all variants of each site, eg. reddit.com, www.reddit.com and *.reddit.com
sites_to_block = sites_to_block1 + sites_to_block2 + sites_to_block3  # convert into one list

Linux_host = '/etc/hosts'
MacOs_host = '/private/etc/hosts'
Windows_host = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "0.0.0.0"
default_hoster = Windows_host

number = input("Time to block sites for in hours: ")
try:
    number1 = number.strip()
except AttributeError:
    # data is not a string, can't strip
    number1 = number
try:
    valid = number1.isnumeric()
except AttributeError:
    # data is an int
    valid = True

if valid is False:
    print("Please enter a positive integer!")

else:
    blocklength = int(number)

y = dt.now().hour

def block_websites(start_hour, end_hour):
    while True:
        if dt(dt.now().year, dt.now().month, dt.now().day, start_hour) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, end_hour):
            print("Sites blocked")
            with open(default_hoster, 'r+') as hostfile:
                hosts = hostfile.read()
                for site in sites_to_block:
                    if site not in hosts:
                        hostfile.seek(0, 2)  # needed in windows before a .write() call to avoid errno 0
                        hostfile.write(redirect+' '+site+'\n')
        else:
            with open(default_hoster, 'r+') as hostfile:
                hosts = hostfile.readlines()
                hostfile.seek(0)
                for host in hosts:
                    if not any(site in host for site in sites_to_block):
                        hostfile.write(host)
                hostfile.truncate()
            print('No sites blocked')
        time.sleep(60)


if __name__ == '__main__':
    block_websites(y, y+blocklength)
