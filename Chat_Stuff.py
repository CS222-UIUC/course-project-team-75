import time
from datetime import datetime
import socket
import requests

#take my id, other person's id and get chat id
def get_chat_id(my,other):
    if(my < other):
        return str(my)+"-"+str(other)
    return str(other)+"-"+str(my)

#get message into proper format
def compose_message(id,msg):
    return str(int(time.time()))+"§"+str(id)+"§"+str(msg)+"\n"

#TODO
#Add way to push message to server, this only works locally right now
def send_msg(other,msg):
    f = open(str(get_chat_id(msg.split(sep="§")[1],other))+".csv",mode="a")
    f.write(msg)
    f.close

#TODO
#Add way to pull messages from server, only works locally rn
def populate_chat(id,other):
    f = open(str(id)+"-"+str(other)+".csv",mode="r")
    for x in f:
        msg = x.split(sep="§")
        new_msg = str(datetime.fromtimestamp(int(msg[0])))+" | "+str(msg[1])+" | "+str(msg[2])
        print(new_msg)
    f.close()

#This pulls the client API from the server and searches for the client IP
#If the IP is found, the proper user ID is returned
#Otherwise, one is created and the new IP/ID pair is pushed to the client list
def get_id():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    r = requests.get("http://158.101.3.109:8000/clients/")
    c = str(r.content)[14:-15]
    s = c.split(sep="\\n")
    last = None
    for x in s:
        if(x != ""):
            t = x.split(sep=",")
            last = t[1]
            if(str(ip) == str(t[0])):
                return t[1]
    body = str(str(ip)+","+str(int(last)+1))
    requests.post(url="http://158.101.3.109:8000/clients/",data=body)
    return int(last)+1
