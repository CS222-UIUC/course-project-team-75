from django.http import HttpResponse
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import email
from io import StringIO
import pandas as pd
from django.http import JsonResponse
from django.http import FileResponse
import os

from .forms import NameForm



def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:
        form = NameForm()
    return render(request, 'name.html', {'form': form})

@csrf_exempt
def get_clients(request):
     data = pd.read_csv("/home/opc/dating/user_database.csv")
     if(request.method == "POST"):
          if(request.headers["Header1"] == "ACCOUNT CREATION"):
               m = pd.read_csv("/home/opc/dating/user_database.csv")["userid"].max()+1
               data = json.loads(request.body.decode())
               f = open("/home/opc/dating/user_database.csv","a")
               f.write(str(m)+","+str(data["username"])+","+str(data["password"])+'\n')
               return HttpResponse("a-ok")
          name = str(request.body)[2:-1]
          return HttpResponse(data.loc[data["username"] == name].iloc[0]["userid"])
     return JsonResponse(data["username"].tolist(),safe=False)

@csrf_exempt
def authenticate(request):
    if(request.method == "POST"):
        f = open("/home/opc/dating/user_database.csv","r")
        s = request.body.decode().split(sep=",")
        if(s[0]+","+s[1]+"\n" in f.read()):
            f.close()
            data = pd.read_csv("/home/opc/dating/user_database.csv")
            info = data.loc[data["username"] == s[0]]
            return HttpResponse(str(info.iloc[0]["userid"]))
        else:
            return HttpResponse("you suck")

@csrf_exempt
def request_chat(request):
    if(request.method == "POST"):
        if(request.headers and request.headers["Header1"] == "SEND MESSAGE"):
            content = json.loads(request.body.decode())
            f = open("/home/opc/dating/chats/"+content["chat_file"],"a")
            f.write(content["message"])
            f.close()
            return HttpResponse("a-ok")
        path = ("/home/opc/dating/chats/"+str(request.body)[2:-1])
        print(path)
        if(os.path.exists(path)):
                print(path)
                return FileResponse(open(path,"rb"))
        else:
            f = open(path,"w")
            f.close()
            return FileResponse(open(path,"rb"))
