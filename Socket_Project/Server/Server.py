import socket
import threading
from tkinter import*
import json
import requests
import urllib.request
from urllib.request import urlopen
import datetime
import time

HEADER = 64
PORT = 5050
SERVER = ''
ADDR = (SERVER, PORT)
FORMAT = "utf8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
current_date = datetime.date.today().strftime("%Y%m%d")

type_list = list()
brand_list = list()
company_list = list()
data_temp = {}
clients={}

def check_signup(n):
    with open("profile.json",'r',encoding=FORMAT) as F:
        datanew = json.load(F)
        for p in datanew["profile"]:
            if (n == p["username"]):
                return False
        return True

def check_login(n, pw):
    with open("profile.json",'r',encoding=FORMAT) as login:
        datanew = json.load(login)
        for p in datanew["profile"]:
            if n == p["username"] and pw == p["password"]:
               return True
        return False

def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent = 2)

def countdown(t):
    while t:
        time.sleep(1)
        t -= 1
def update_current_data():
    URL = 'https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now'
    data = json.loads(urlopen(URL).read())
    with open("current_data.json","w",encoding="utf8") as file_1:
        data_json['Gold_Data'].append({"Date":current_date, "Data":data})
        json.dump(data_json,file_1,indent=2,ensure_ascii=False)
    while True:
        countdown(1800)
        with open("current_data.json","w",encoding="utf8") as file_1:
            json.dump(data,file_1,indent=2,ensure_ascii=False)
            

def handle_client(conn, addr):
    list.insert(END,f"{addr} đã kết nối")
    clients[conn] = addr
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                list_2.insert(END,f"[{addr}] đã ngắt kết nối.")
                connected = False
            else:
                data = json.loads(msg)
                if data["flag"] == "1":
                    with open("profile.json") as filex:
                        if filex.readline()=="":
                            conn.send("Login0".encode(FORMAT))
                        else:
                            if check_login(data["username"], data["password"]) == True:
                                conn.send("Login1".encode(FORMAT))
                            else:
                                conn.send("Login0".encode(FORMAT))
                elif data["flag"] == "2":
                    with open("profile.json") as file:
                        if (file.readline() == ""):
                            File1 = open("profile.json", "w", encoding=FORMAT)
                            with File1 as f:
                                data2 = {}
                                data2["profile"] = []
                                data2["profile"].append({"username": data["username"], "password": data["password"]})
                                json.dump(data2, f, indent = 2,ensure_ascii=False)
                            File1.close() 
                            conn.send("Signup0".encode(FORMAT))
                        else:
                            if check_signup(data["username"]) == True:
                                with open("profile.json", 'r+', encoding=FORMAT) as file:
                                    data2 = json.load(file)
                                    y = {"username": data["username"], "password": data["password"]}
                                    data2["profile"].append(y)
                                    file.seek(0)
                                    json.dump(data2, file, indent=2,ensure_ascii=False)
                                conn.send("Signup0".encode(FORMAT))
                            else:
                                conn.send("Signup1".encode(FORMAT))        
                elif data["flag"] == "3":
                    if int(data["month"])<10:
                        if int(data["day"])<10:
                            date = data["year"]+"0"+data["month"]+"0"+data["day"]
                        else:
                            date = data["year"]+"0"+data["month"]+data["day"]
                    else:
                        date = data["year"]+data["month"]+data["day"]
                    if date == current_date:
                        with open("current_data.json", "r", encoding="utf8") as file:
                            data_check = json.load(file)
                            data_url = data_check["Gold_Data"][0]["Data"]
                    else:
                        with open("data.json","r",encoding=FORMAT) as file:
                            if file.readline()=="":
                                URL = 'https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date='+date
                                data_url = json.loads(urlopen(URL).read())
                            else:
                                if check_data(date) == False:
                                    with open("data.json", "r", encoding="utf8") as file:
                                        data_check = json.load(file)
                                        for i in data_check["Gold_Data"]:
                                            if i["Date"] == date:
                                                data_url = i["Data"]
                                else:
                                    URL = 'https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date='+date
                                    data_url = json.loads(urlopen(URL).read())
                    type_list.clear()
                    brand_list.clear()
                    company_list.clear()
                    for t in data_url['golds']:
                        for i in t['value']:
                            if i['type'] not in type_list:
                                type_list.append(i['type'])
                            if i['brand'] not in brand_list:
                                brand_list.append(i['brand'])
                            if i['company'] not in company_list:
                                company_list.append(i['company'])
                    if "" not in type_list:
                        type_list.append("")
                    if "" not in brand_list:
                        brand_list.append("")
                    if "" not in company_list:
                        company_list.append("")
                    data_gold = {
                        "type":json.dumps(type_list,ensure_ascii=False),
                        "brand":json.dumps(brand_list,ensure_ascii=False),
                        "company":json.dumps(company_list,ensure_ascii=False)
                        }
                    conn.send(json.dumps(data_gold,ensure_ascii=False).encode(FORMAT))
                    data_json["Gold_Data"].clear()
                    with open("data.json","r",encoding=FORMAT) as file:
                        if file.readline()=="":
                            if date != current_date:
                                with open("data.json","w",encoding="utf8") as file_1:
                                    data_json['Gold_Data'].append({"Date":date, "Data":data_url})
                                    json.dump(data_json,file_1,indent=2,ensure_ascii=False)
                        else:
                            if check_data(date) == True and date != current_date:
                                with open("data.json", "r+",encoding="utf8") as file_2:
                                    data_new = json.load(file_2)
                                    data_temp = {"Date":date, "Data":data_url}
                                    if check_data(data_temp["Date"]) == True:
                                        data_new["Gold_Data"].append(data_temp)
                                        file_2.seek(0)
                                        json.dump(data_new, file_2,indent=2,ensure_ascii=False)
                elif data["flag"] == "4":
                    data4={}
                    data4["golds"]=[]
                    if date == current_date:
                        with open("current_data.json","r",encoding=FORMAT) as file:
                            data_web = json.load(file)
                    else:
                        with open("data.json","r",encoding=FORMAT) as file:
                            data_web = json.load(file)
                    if data["type"]!="" and data["brand"]=="" and data["company"]=="":
                        data4["golds"].clear()
                        for s in data_web["Gold_Data"]:
                                if s["Date"] == date:
                                    for t in s["Data"]['golds']:
                                        for i in t['value']:
                                            if i["type"] == data["type"]:
                                                data4["golds"].append({
                                                    "buy": i["buy"],"sell": i["sell"],"company": i["company"],
                                                    "brand": i["brand"],"updated": i["updated"],
                                                    "brand1": i["brand1"],"day": i["day"],
                                                    "id": i["id"],"type": i["type"],"code": i["code"]
                                                    })
                        conn.send(json.dumps(data4,ensure_ascii=False).encode(FORMAT))
                        
                    elif data["type"]=="" and data["brand"]!="" and data["company"]=="":
                        data4["golds"].clear()
                        for s in data_web["Gold_Data"]:
                                if s["Date"] == date:
                                    for t in s["Data"]['golds']:
                                        for i in t['value']:
                                            if i["brand"] == data["brand"]:
                                                data4["golds"].append({
                                                    "buy": i["buy"],"sell": i["sell"],"company": i["company"],
                                                    "brand": i["brand"],"updated": i["updated"],
                                                    "brand1": i["brand1"],"day": i["day"],
                                                    "id": i["id"],"type": i["type"],"code": i["code"]
                                                    })
                        conn.send(json.dumps(data4,ensure_ascii=False).encode(FORMAT))
                        
                    elif data["type"]=="" and data["brand"]=="" and data["company"]!="":
                        data4["golds"].clear()
                        for s in data_web["Gold_Data"]:
                                if s["Date"] == date:
                                    for t in s["Data"]['golds']:
                                        for i in t['value']:
                                            if i["company"] == data["company"]:
                                                data4["golds"].append({
                                                    "buy": i["buy"],"sell": i["sell"],"company": i["company"],
                                                    "brand": i["brand"],"updated": i["updated"],
                                                    "brand1": i["brand1"],"day": i["day"],
                                                    "id": i["id"],"type": i["type"],"code": i["code"]
                                                    })
                        conn.send(json.dumps(data4,ensure_ascii=False).encode(FORMAT))
                        
                    elif data["type"]!="" and data["brand"]!="" and data["company"]=="":
                        data4["golds"].clear()
                        for s in data_web["Gold_Data"]:
                                if s["Date"] == date:
                                    for t in s["Data"]['golds']:
                                        for i in t['value']:
                                            if i["type"] == data["type"] and i["brand"] == data["brand"]:
                                                data4["golds"].append({
                                                    "buy": i["buy"],"sell": i["sell"],"company": i["company"],
                                                    "brand": i["brand"],"updated": i["updated"],
                                                    "brand1": i["brand1"],"day": i["day"],
                                                    "id": i["id"],"type": i["type"],"code": i["code"]
                                                    })
                        conn.send(json.dumps(data4,ensure_ascii=False).encode(FORMAT))
                        
                    elif data["type"]!="" and data["brand"]=="" and data["company"]!="":
                        data4["golds"].clear()
                        for s in data_web["Gold_Data"]:
                                if s["Date"] == date:
                                    for t in s["Data"]['golds']:
                                        for i in t['value']:
                                            if i["type"] == data["type"] and i["company"] == data["company"]:
                                                data4["golds"].append({
                                                    "buy": i["buy"],"sell": i["sell"],"company": i["company"],
                                                    "brand": i["brand"],"updated": i["updated"],
                                                    "brand1": i["brand1"],"day": i["day"],
                                                    "id": i["id"],"type": i["type"],"code": i["code"]
                                                    })
                        conn.send(json.dumps(data4,ensure_ascii=False).encode(FORMAT))
                        
                    elif data["type"]=="" and data["brand"]!="" and data["company"]!="":
                        data4["golds"].clear()
                        for s in data_web["Gold_Data"]:
                                if s["Date"] == date:
                                    for t in s["Data"]['golds']:
                                        for i in t['value']:
                                            if i["company"] == data["company"] and i["brand"] == data["brand"]:
                                                data4["golds"].append({
                                                    "buy": i["buy"],"sell": i["sell"],"company": i["company"],
                                                    "brand": i["brand"],"updated": i["updated"],
                                                    "brand1": i["brand1"],"day": i["day"],
                                                    "id": i["id"],"type": i["type"],"code": i["code"]
                                                    })
                        conn.send(json.dumps(data4,ensure_ascii=False).encode(FORMAT))
                        
                    elif data["type"]!="" and data["brand"]!="" and data["company"]!="":
                        data4["golds"].clear()
                        for s in data_web["Gold_Data"]:
                                if s["Date"] == date:
                                    for t in s["Data"]['golds']:
                                        for i in t['value']:
                                            if i["type"] == data["type"] and i["company"] == data["company"] and i["brand"] == data["brand"]:
                                                data4["golds"].append({
                                                    "buy": i["buy"],"sell": i["sell"],"company": i["company"],
                                                    "brand": i["brand"],"updated": i["updated"],
                                                    "brand1": i["brand1"],"day": i["day"],
                                                    "id": i["id"],"type": i["type"],"code": i["code"]
                                                    })
                        conn.send(json.dumps(data4,ensure_ascii=False).encode(FORMAT))
    conn.close()

def start():
    server.listen(5)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


data_json = {}
data_json["Gold_Data"]=[]

def check_data(date):
    with open("data.json", "r", encoding="utf8") as file:
        data_check = json.load(file)
        for i in data_check["Gold_Data"]:
            if i["Date"] == date:
                return False
        return True

def Close_Conn():
    for sock in clients:
        sock.close()

update = threading.Thread(target=update_current_data)
update.start()


Server_box=Tk()
Server_box.title("Server")
Server_box.geometry("550x600")
Label(Server_box,text="Quản lý kết nối",font=("Arial", 15)).pack(padx=10,pady=10)
Label(Server_box,text=f"IP Server: {socket.gethostbyname(socket.gethostname())}",font=("Arial", 10)).pack()
box1=LabelFrame(Server_box,text="Kết nối")
box1.pack(padx=10,pady=10,fill="both",expand="yes")
my_frame=Frame(box1)                
scrollbar = Scrollbar(my_frame, orient=VERTICAL)               
list=Listbox(my_frame,height=10,width=80,yscrollcommand=scrollbar.set)              
scrollbar.pack(side=RIGHT, fill=Y)               
scrollbar.config(command=list.yview)                
list.pack(pady=10)                
my_frame.pack() 
box2=LabelFrame(Server_box,text="Ngắt kết nối")
box2.pack(padx=10,pady=10,fill="both",expand="yes")
my_frame_2=Frame(box2)                
scrollbar = Scrollbar(my_frame_2, orient=VERTICAL)               
list_2=Listbox(my_frame_2,height=10,width=80,yscrollcommand=scrollbar.set)              
scrollbar.pack(side=RIGHT, fill=Y)               
scrollbar.config(command=list_2.yview)                
list_2.pack(pady=10)                
my_frame_2.pack()
box3=LabelFrame(Server_box)
box3.pack(padx=10,pady=10,fill="both",expand="yes")
Button(box3,text="Thoát",fg="Black",width =10,command=Server_box.destroy).grid(row=0,column=0,padx=90,pady=10)
Button(box3,text="Ngắt kết nối",fg="Black",width =10,command=Close_Conn).grid(row=0,column=1,padx=90,pady=10)
threading.Thread(target=start).start()
Server_box.mainloop()
