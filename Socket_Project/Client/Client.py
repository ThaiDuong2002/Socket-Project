import socket
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import json


DISCONNECT_TEXT="!DISCONNECT"

type_list = list()
brand_list = list()
company_list = list()

def IP_in():
    if IP_Entry.get()=="":
        pass
    else:
        def send(msg):
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
        def write_json(data, filename):
            with open(filename, "w") as f:
                json.dump(data, f, indent = 2)

        def login(signup_window):
            signup_window.destroy()
            window=Tk()
            window.title("Đăng nhập")
            window.geometry("600x400")
            login_frame=LabelFrame(window)
            login_frame.pack(padx=10,pady=10,fill="both",expand="yes")
            heading = Label(login_frame,text="Đăng Nhập",font=("Arial", 10))
            heading.grid(row=1,column=1,padx=10,pady=10)

            username = Label(login_frame,text="Tên đăng nhập",font=("Arial", 10))
            username.grid(row=3,column=0,padx=10,pady=10)

            name_text = StringVar()
            entry_name = Entry(login_frame,textvariable=name_text)
            entry_name.grid(row=3,column=1,ipadx="100")

            password = Label(login_frame,text="Mật khẩu",font=("Arial", 10))
            password.grid(row=4,column=0,padx=10,pady=10)

            pass_text = StringVar()
            entry_pass = Entry(login_frame,textvariable=pass_text)
            entry_pass.grid(row=4,column=1,ipadx="100")

            def login_info():
                if (entry_name.get() == "" and entry_pass.get()== ""):
                    warning = Label(login_frame, text="Vui lòng nhập tên đăng nhập và mật khẩu", font = ("Arial", 10))
                    warning.grid(row=11,column=1,padx=10,pady=10)
                elif (entry_name.get() == ""):
                    warning = Label(login_frame, text="          Vui lòng nhập tên đăng nhập          ", font = ("Arial", 10))            
                    warning.grid(row=11,column=1,padx=10,pady=10)
                elif (entry_pass.get()== ""):
                    warning = Label(login_frame, text="             Vui lòng nhập mật khẩu             ", font = ("Arial", 10))            
                    warning.grid(row=11,column=1,padx=10,pady=10)
                else:
                    profile = {
                        "flag":"1",
                        "username":entry_name.get(),
                        "password":entry_pass.get()
                        }
                    try:
                        send(json.dumps(profile))
                    except socket.error:
                        messagebox.showwarning("WARNING", "Máy chủ đã ngắt kết nối!")
                    if client.recv(2048).decode(FORMAT) == "Login1":
                        window.destroy()
                        search_by_data=Tk()
                        date_search(search_by_data)
                    else:
                        warning = Label(login_frame, text="        Tên đăng nhập hoặc mật khẩu sai!       ", font = ("Arial", 10))
                        warning.grid(row=11,column=1,padx=10,pady=10)
            login = Button(login_frame, text="Đăng Nhập",fg="Black",width=10,command=login_info)
            login.grid(row=5,column=1,padx=10,pady=10)

            ask = Label(login_frame,text="You don't have an account ?",font=("Arial", 10))
            ask.grid(row=8, column=1,padx=10,pady=10)

            def signup1():
                signup(window)
            def exit_login():
                window.destroy()
                send(DISCONNECT_TEXT)
                
            entry_ask = Button(login_frame, text="Đăng ký",fg="Black",width=10,command=signup1)
            entry_ask.grid(row=9,column=1,padx=10,pady=10)
            out=Button(login_frame,text="Thoát",fg="Black",width=10,command=exit_login)
            out.grid(row=10,column=1,padx=10,pady=10)
            window.mainloop()


        def signup(window):
    
            window.destroy()
            signup_window=Tk()
            signup_frame=LabelFrame(signup_window)
            signup_frame.pack(padx=10,pady=10,fill="both",expand="yes")
            signup_window.title("Đăng ký")
            signup_window.geometry("600x350")

            signup_heading = Label(signup_frame,text="Đăng ký",font=("Arial", 10))
            signup_heading.grid(row=1,column=1,padx=10,pady=10)

            signup_name = Label(signup_frame,text="Tên đăng nhập",font=("Arial", 10))
            signup_name.grid(row=2,column=0,padx=10,pady=10)

            name_text_1 = StringVar()
            entry_name_1 = Entry(signup_frame,textvariable=name_text_1)
            entry_name_1.grid(row=2,column=1,ipadx="100")

            signup_pass = Label(signup_frame,text="Mật khẩu",font=("Arial", 10))
            signup_pass.grid(row=3,column=0,padx=10,pady=10)

            name_text_1 = StringVar()
            entry_pass_1 = Entry(signup_frame,textvariable=name_text_1)
            entry_pass_1.grid(row=3,column=1,ipadx="100")

            signup_pass_again = Label(signup_frame,text="Nhập lại mật khẩu",font=("Arial", 10))
            signup_pass_again.grid(row=4,column=0,padx=10,pady=10)

            name_text_2 = StringVar()
            entry_pass_2 = Entry(signup_frame,textvariable=name_text_2)
            entry_pass_2.grid(row=4,column=1,ipadx="100")

            def insert():
                if entry_name_1.get()=="" or entry_pass_1.get()=="" or entry_pass_2.get()=="":
                    pass
                else:
                    if entry_pass_1.get() != entry_pass_2.get():
                        warning = Label(signup_frame, text="  Mật khẩu xác nhận không đúng  ", font = ("Arial", 10))
                        warning.grid(row=7,column=1,padx=10,pady=10)
                        pass
                    else:
                        profile = {
                            "flag":"2",
                            "username":entry_name_1.get(),
                            "password":entry_pass_1.get()
                        }
                        try:
                            send(json.dumps(profile))
                        except socket.error:
                            messagebox.showwarning("WARNING", "Máy chủ đã ngắt kết nối!")
                        if client.recv(2048).decode(FORMAT) == "Signup1":
                            warning = Label(signup_frame, text="Tên đăng nhập đã có người dùng", font = ("Arial", 10))
                            warning.grid(row=7,column=1,padx=10,pady=10)
                        else:
                            login(signup_window)
            signup = Button(signup_frame, text="Đăng ký",fg="Black",width=10,command=insert)
            signup.grid(row=5,column=1,padx=10,pady=10)

            def back():
                login(signup_window)
            def exit_signup():
                signup_window.destroy()
                send(DISCONNECT_TEXT)
            back1=Button(signup_frame,text="Quay lại",fg="Black",width=10,command=back)
            back1.grid(row=6,column=0,padx=10,pady=10)
            out=Button(signup_frame,text="Thoát",fg="Black",width=10,command=exit_signup)
            out.grid(row=6,column=2,padx=10,pady=10)
            signup_window.mainloop()

        def data_search(search_by_date,dayx,monthx,yearx):
            def data_out():
                if type_combo.get()=="" and brand_combo.get()=="" and company_combo.get()=="":
                    pass
                else:
                    result_list.delete(0,END)
                    data = {
                            "flag": "4",
                            "type": type_combo.get(),
                            "brand": brand_combo.get(),
                            "company": company_combo.get()
                        }
                    try:
                        send(json.dumps(data))
                    except socket.error:
                        messagebox.showwarning("WARNING", "Máy chủ đã ngắt kết nối!")
                    data_out=json.loads(client.recv(500000).decode(FORMAT))
                    for i in range(len(data_out["golds"])):
                        result_list.insert(END,"   Giá mua: "+data_out["golds"][i]['buy'])
                        result_list.insert(END,"   Giá bán: "+data_out["golds"][i]['sell'])
                        result_list.insert(END,"   Công ty: "+data_out["golds"][i]['company'])
                        result_list.insert(END,"   Thương hiệu: "+data_out["golds"][i]['brand'])
                        result_list.insert(END,"   Cập nhật: "+data_out["golds"][i]['updated'])
                        result_list.insert(END,"   Mã thương hiệu: "+data_out["golds"][i]['brand1'])
                        result_list.insert(END,"   Ngày: "+data_out["golds"][i]['day'])
                        result_list.insert(END,"   Id: "+data_out["golds"][i]['id'])
                        result_list.insert(END,"   Loại vàng: "+data_out["golds"][i]['type'])
                        result_list.insert(END,"   Mã: "+data_out["golds"][i]['code'])
                        result_list.insert(END,"_____________________________________________________________________________")
                    if result_list.size()==0:
                        result_list.insert(END,"                                            Không có dữ liệu!")
            type_list.sort()
            brand_list.sort()
            company_list.sort()
            search_by_date.destroy()
            search_by_data=Tk()
            search_by_data.title("Tra cứu Tỷ giá vàng")
            search_by_data.geometry("600x580")
            Tille = Label(search_by_data,text="TRA CỨU TỶ GIÁ VÀNG",font=("Arial", 25))
            Tille.pack(padx=10,pady=10)
            Date_tille = Label(search_by_data,text=f"{yearx} - {monthx} - {dayx}",font=("Arial",10))
            Date_tille.pack(padx=10,pady=10)
            wrapper = LabelFrame(search_by_data, text="Thông tin tra cứu")
            wrapper.pack(padx=10,pady=10,fill="both",expand="yes")
            wrapper_result = LabelFrame(search_by_data, text="Kết quả tra cứu")
            wrapper_result.pack(padx=10,pady=10,fill="both",expand="yes")
            detail_type=Label(wrapper, text="Loại vàng:")
            detail_type.grid(row=1,column=0,padx=20,pady=10)
            type_combo = ttk.Combobox(wrapper, value=type_list,width=20)
            type_combo.grid(row=1,column=1,padx=10,pady=10)

            detail_brand=Label(wrapper, text="Thương Hiệu:")
            detail_brand.grid(row=2,column=0,padx=20,pady=10)
            brand_combo = ttk.Combobox(wrapper, value=brand_list,width=20)
            brand_combo.grid(row=2,column=1,padx=10,pady=10)
            detail_company=Label(wrapper, text="Công ty sản xuất:")               
            detail_company.grid(row=3,column=0,padx=20,pady=10)                
            company_combo = ttk.Combobox(wrapper, value=company_list,width=20)                
            company_combo.grid(row=3,column=1,padx=10,pady=10)
                
            Button(wrapper,text="Tìm kiếm",fg="Black",width=10,command=data_out).grid(row=2,column=3,padx=40,pady=10)               
            my_frame=Frame(wrapper_result)                
            scrollbar = Scrollbar(my_frame, orient=VERTICAL)               
            result_list=Listbox(my_frame,height=11,width=60,yscrollcommand=scrollbar.set)              
            scrollbar.pack(side=RIGHT, fill=Y)               
            scrollbar.config(command=result_list.yview)                
            result_list.pack(pady=10)                
            my_frame.pack()                
            wrapper_option = LabelFrame(search_by_data)                
            wrapper_option.pack(padx=10,pady=10,fill="both",expand="yes")               
            def back():
                date_search(search_by_data)
            def search_exit():
                search_by_data.destroy()
                send(DISCONNECT_TEXT)
            def login_form():
                search_by_data.destroy()
                signup_window=Tk()
                login(signup_window)
            Button(wrapper_option,text="Quay lại",fg="Black",width=10,command=back).grid(row=1,column=1,padx=50,pady=10)     
            Button(wrapper_option,text="Thoát",fg="Black",width=10,command=search_exit).grid(row=1,column=2,padx=50,pady=10)                
            Button(wrapper_option,text="Đăng xuất",fg="Black",width=10,command=login_form).grid(row=1,column=3,padx=50,pady=10)                
            search_by_data.mainloop()                
            


        def date_search(search_by_data):
            search_by_data.destroy()
            search_by_date = Tk()
            search_by_date.title("Tỷ giá vàng")
            search_by_date.geometry("360x390")

            day = list(range(1,32))
            month = list(range(1,13))
            year = list(range(1968,2022))

            def checkYear(year):
                if (year % 4) == 0:
                    if (year % 100) == 0:
                        if (year % 400) == 0:
                            return True
                        else:
                            return False
                    else:
                         return True
                else:
                    return False
        
            Label(search_by_date,text="\n\nNHẬP NGÀY CẦN TRA CỨU\n").grid(row=2,column=2,padx=10,pady=10)
            Label(search_by_date,text="Ngày:").grid(row=3,column=1,padx=10,pady=10)
            my_day = ttk.Combobox(search_by_date, value=day)
            my_day.bind("<<ComboboxSelected>>")
            my_day.grid(row=3,column=2,padx=10,pady=10) 
            Label(search_by_date,text="Tháng:").grid(row=4,column=1,padx=10,pady=10)
            my_month = ttk.Combobox(search_by_date, value=month)
            my_month.bind("<<ComboboxSelected>>")
            my_month.grid(row=4,column=2,padx=10,pady=10)
            Label(search_by_date,text="Năm:").grid(row=5,column=1,padx=10,pady=10)
            my_year = ttk.Combobox(search_by_date, value=year)
            my_year.bind("<<ComboboxSelected>>")
            my_year.grid(row=5,column=2,padx=10,pady=10)
            def login_form():
                search_by_date.destroy()
                signup_window=Tk()
                login(signup_window)
            def check_date():
                if my_day.get()=="" or my_month.get()=="" or my_year.get()=="":
                    pass
                else:
                    if my_month.get() == '2' and checkYear(int(my_year.get()))==True and int(my_day.get())>29:
                        pass
                    elif my_month.get() == '2' and checkYear(int(my_year.get()))==False and int(my_day.get())>28:
                        pass
                    elif (my_month.get()=='4'or my_month.get()=='6'or my_month.get()=='9'or my_month.get()=='11') and int(my_day.get())>30:
                        pass
                    else:
                        type_list.clear()
                        brand_list.clear()
                        company_list.clear()
                        date ={
                                "flag": "3",
                                "day":my_day.get(),
                                "month":my_month.get(),
                                "year":my_year.get()
                            }
                        try:
                            send(json.dumps(date))
                        except socket.error:
                            messagebox.showwarning("WARNING", "Máy chủ đã ngắt kết nối!")
                        data_gold=json.loads(client.recv(100000).decode(FORMAT))
                        for p in json.loads(data_gold["type"]):
                            type_list.append(p)
                        for p in json.loads(data_gold["brand"]):
                            brand_list.append(p)
                        for p in json.loads(data_gold["company"]):
                            company_list.append(p)
                        data_search(search_by_date,my_day.get(),my_month.get(),my_year.get())
            def date_exit():
                search_by_date.destroy()
                send(DISCONNECT_TEXT)
            Button(search_by_date, text="Tiếp theo",fg="Black",bg="Light Blue",width=10,command=check_date).grid(row=6,column=2,padx=10,pady=10)
            Button(search_by_date, text="Thoát",fg="Black",bg="Light Blue",width=10,command=date_exit).grid(row=8,column=1,padx=10,pady=10)
            Button(search_by_date, text="Đăng xuất",fg="Black",bg="Light Blue",width=10,command=login_form).grid(row=8,column=3,padx=0,pady=10)
            search_by_date.mainloop()
        PORT=5050
        HEADER=64
        FORMAT = "utf8"
        SERVER = IP_Entry.get()
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ADDR = (str(SERVER), PORT)
            client.connect(ADDR)
            client_box.destroy()
            signup_window=Tk()
            login(signup_window)
        except socket.error:
            messagebox.showwarning("WARNING", "Không tìm thấy máy chủ!")


client_box=Tk()
client_box.title("Enter IP Address")
client_box.geometry("400x180")
IP_frame = LabelFrame(client_box)
IP_frame.pack(padx=10,pady=10,fill="both",expand="yes")
IP = Label(IP_frame,text="Nhập IP",font=("Arial", 10))
IP.pack(padx=10,pady=10)
IP_text=StringVar()
IP_Entry=Entry(IP_frame,textvariable=IP_text,width=30)
IP_Entry.pack(padx=10,pady=10)
Button_frame = LabelFrame(client_box)
Button_frame.pack(padx=10,pady=10,fill="both",expand="yes")
next=Button(Button_frame,text="Tiếp theo",fg="Black",width=10,command=IP_in)
next.grid(row=3,column=2,padx=50,pady=10)
exit=Button(Button_frame,text="Thoát",fg="Black",width=10,command=client_box.destroy)
exit.grid(row=3,column=1,padx=50,pady=10)
client_box.mainloop()
