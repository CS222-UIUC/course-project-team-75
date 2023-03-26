import time
from datetime import datetime
import socket
import requests
import os

#take my id, other person's id and get chat id
def get_chat_id(my,other):
    if(int(my) < int(other)):
        return str(my)+"-"+str(other)
    return str(other)+"-"+str(my)

#get message into proper format
def compose_message(username,msg):
    return str(int(time.time()))+"§"+str(username)+"§"+str(msg)+"\n"

def send_msg(my,other,msg):
    body = {"chat_file":get_chat_id(my,other)+".csv","message":compose_message(my,msg)}
    file_req = requests.post(url="http://158.101.3.109:8000/chats/",json=body,headers={"header1":"SEND MESSAGE"})

def populate_chat(id,other,othername):
    global username

    filename = get_chat_id(id,other)+".csv"
    file_req = requests.post(url="http://158.101.3.109:8000/chats/",data=filename,stream=True,headers={"header1":"REQUEST CHAT"})
    with open("client_files/"+filename, "wb") as handle:
        for data in file_req:
            handle.write(data)

    f = open("client_files/"+filename,mode="r")
    for x in f:
        msg = x.split(sep="§")
        new_msg = str(datetime.fromtimestamp(int(msg[0][:-1])))+" | "+str(username if int(msg[1][:-1]) == int(id) else othername)+" | "+str(msg[2])
        print(new_msg[:-1])
    f.close()

#This pulls the client API from the server and searches for the client IP
#If the IP is found, the proper user ID is returned
#Otherwise, one is created and the new IP/ID pair is pushed to the client list
# def get_id():
#     hostname = socket.gethostname()
#     ip = socket.gethostbyname(hostname)
#     r = requests.get("http://158.101.3.109:8000/clients/")
#     c = str(r.content)[14:-15]
#     s = c.split(sep="\\n")
#     last = None
#     for x in s:
#         if(x != ""):
#             t = x.split(sep=",")
#             last = t[1]
#             if(str(ip) == str(t[0])):
#                 return t[1]
#     body = str(str(ip)+","+str(int(last)+1))
#     requests.post(url="http://158.101.3.109:8000/clients/",data=body,headers={"header1":"GETTING ID"})
#     return int(last)+1

username = ""
def log_in():
    global username
    c = ""
    while(c.lower() != "l"):
        c = input("(L)ogging in or (C)reating account?: ")
        if(c.lower() == "c"):
            create_account()
            return -2

    user = input("Input username: ")
    pw = input("Input password: ")

    username = user

    body = str(user)+","+str(pw)
    try:
        response = requests.post(url="http://158.101.3.109:8000/auth/",data=body)
    except:
        print("Something went wrong on our end, please try again.")
        exit()
    if(str(response.content)[2:-1] != "you suck"):
        return int(response.content)
    return -1

def chat(name):
    global user_id
    partner_id = str(requests.post(url="http://158.101.3.109:8000/clients/",data=name,headers={"header1":"GETTING NAME"}).content)[2:-1]
    while(1):
        os.system("cls")
        print("Chatting with "+str(name)+" | Type #EXIT to exit the chat. Be respectful.")
        print("_______________________________")
        populate_chat(user_id,partner_id,name)
        next_chat = input("Enter message: ")
        if(next_chat == "#EXIT"):
            os.system("cls")
            break
        send_msg(user_id,int(partner_id),next_chat)

def create_account():
    user = input("Choose a username: ")
    c = input(user+" is your chosen username. This cannot be changed. Are you sure?: ")
    if(c.lower() != "y" and c.lower() != "yes"):
        create_account()
        return
    p = ""
    while(1):
        p = input("Choose a password: ")
        a = input("Type password again: ")
        if(p == a):
            break
        else:
            print("Passwords do not match. Please try again.")
    try:
        r = requests.post(url="http://158.101.3.109:8000/clients/",json={"username":user,"password":p},headers={"header1":"ACCOUNT CREATION"})
    except:
        print("Something went wrong. Please try again.")
        return

users = None
def get_users(dummy):
    global users
    if(users == None):
        response = requests.get(url="http://158.101.3.109:8000/clients/")
        users = response.json()
    print("Current users:")
    for i in users:
        print(i)
    print()

user_id = -1
user_id = log_in()
while(user_id < 0):
    if(user_id == -2):
        print("Account creation successful.")
    else:
        print("Authentication failed. Please try again")
    user_id = log_in()
#get_users()

#options:
#view users
#chat with a user
#exit a chat
#exit the app

def help(dummy):
    global m
    k = m.keys()
    print("Available commands:")
    for i in k:
        print(i)
    print()

def ex(dummy):
    global running
    running = 0

m = {
    "help":help,
    "exit":ex,
    "users":get_users,
    "chat":chat,

}


running = 1
while(running):
    choice = input("Please use a command, or type \"help\" for more info: ")
    toks = choice.split(sep=" ")
    if(toks[0] in m):
    #try:
        m[toks[0]](toks[len(toks)-1])
    else:
        print("Unknown command. Try help for a list of commands.")
    #except:
    #    print("Command not found")