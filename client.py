import time
from datetime import datetime
import socket
import requests
import os
import bcrypt
import hashlib
from gooey import Gooey
from getpass import getpass

from rich.tree import Tree
from rich import print

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

username = ""
def log_in():
    global username
    c = ""
    while(c.lower() != "l"):
        c = input("(L)ogging in or (C)reating account?: ")
        if(c.lower() == "c"):
            create_account()
            return -2
    os.system("cls")
    user = input("Input username: ")
    pw = getpass("Input password: ")+"cringe"
    pw = hashlib.md5(pw.encode()).hexdigest()

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
    if(name == "chat"):
        print("To chat, type \"chat\" followed by a valid username.")
        return 0
    global user_id
    try:
        partner_id = str(requests.post(url="http://158.101.3.109:8000/clients/",data=name,headers={"header1":"GETTING NAME"}).content)[2:-1]
        while(1):
            os.system("cls")
            print("Chatting with "+str(name)+" | Type #R to refresh and #EXIT to exit the chat. Be respectful.")
            print("_______________________________")
            populate_chat(user_id,partner_id,name)
            next_chat = input("Enter message: ")
            if(next_chat == "#EXIT"):
                os.system("cls")
                break
            elif(next_chat == "#R"):
                populate_chat(user_id,partner_id,name)
            else:
                send_msg(user_id,int(partner_id),next_chat)
    except:
        print("Something went wrong. Please try again.")

def create_account():
    while 1:
        user = input("Choose a username: ")
        try:
            test = requests.post(url="http://158.101.3.109:8000/clients/",data=user,headers={"header1":"GETTING NAME"})
            if(test.status_code == 200):
                print("Username already taken.")
            else:
                break
        except:
            print("Something went wrong. Please try again.")
            return -2

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
        p+="cringe"
        p = hashlib.md5(p.encode()).hexdigest()
        r = requests.post(url="http://158.101.3.109:8000/clients/",json={"username":user,"password":p},headers={"header1":"ACCOUNT CREATION"})
    except:
        print("Something went wrong. Please try again.")
        return -2

users = None
def get_users(dummy):
    global users
    if(users == None):
        response = requests.get(url="http://158.101.3.109:8000/clients/")
        users = response.json()
    tree = Tree("Current users")
    for i in users:
        tree.add(i)
    print(tree)

user_id = -1
user_id = log_in()
while(user_id < 0):
    if(user_id == -2):
        print("Account creation successful.")
    else:
        print("Authentication failed. Please try again")
    user_id = log_in()


if not os.path.exists("client_files"):
   os.makedirs("client_files")

def help(dummy):
    global m
    tree = Tree("Available commands")
    k = m.keys()
    for i in k:
        tree.add(i)
    print(tree)

def ex(dummy):
    global running
    running = 0

m = {
    "help":help,
    "users":get_users,
    "chat":chat,
    "exit":ex
}

os.system("cls")
running = 1
while(running):
    choice = input("Please use a command, or type \"help\" for more info: ")
    os.system("cls")
    toks = choice.split(sep=" ")
    if(toks[0] in m):
    #try:
        m[toks[0]](toks[len(toks)-1])
    else:
        print("Unknown command. Try help for a list of commands.")
