import random
import  re
import sqlite3
import data
import bs4
from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup 
import datetime
import operator
from tkinter import *
import time
import tkinter.messagebox
import pyttsx3
import threading
import speech_recognition as sr 
from PIL import ImageTk as itk, Image
user_response=['0']
window_size="400x400"
class Bot(Frame):
    
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.master = master   
        
        # sets default bg for top level windows
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE" #message box background colour
        self.tl_fg = "#000000"  #message box foreground colour
        self.font = "Verdana 10"
        
        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5) #bd is for specifying the width around the menu options
# Menu bar

    # File
        file = Menu(menu, tearoff=0) #tearoff is used to position the menu options, 1 is default.
        menu.add_cascade(label="File", menu=file)
       # file.add_command(label="Save Chat Log", command=self.save_chat)
        file.add_command(label="Clear Chat", command=self.clear_chat)
      #  file.add_separator()
        file.add_command(label="Exit",command=self.chatexit)

    # Options
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options)

        # username     

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default",command=self.font_change_default)
        font.add_command(label="Times",command=self.font_change_times)
        font.add_command(label="System",command=self.font_change_system)
        font.add_command(label="Helvetica",command=self.font_change_helvetica)
        font.add_command(label="Fixedsys",command=self.font_change_fixedsys)

        # color theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_command(label="Default",command=self.color_theme_default) 
       # color_theme.add_command(label="Night",command=self.) 
        color_theme.add_command(label="Grey",command=self.color_theme_grey) 
        color_theme.add_command(label="Blue",command=self.color_theme_dark_blue) 
       
        color_theme.add_command(label="Torque",command=self.color_theme_turquoise)
        color_theme.add_command(label="Hacker",command=self.color_theme_hacker)
       # color_theme.add_command(label='Mkbhd',command=self.MKBHD)

        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        #help_option.add_command(label="Features", command=self.features_msg)
        help_option.add_command(label="About PyBot", command=self.msg)
        help_option.add_command(label="Developers", command=self.about)

        self.text_frame = Frame(self.master, bd=6) # the space surrounding the text box
        self.text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # contains messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        #self.entry_field.place(x=10,y=10,width=1000,height=30)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        # self.users_message = self.entry_field.get()

        image=Image.open('voice.png')
        image = image.resize((40, 40), Image.ANTIALIAS)
        self.my_img = itk.PhotoImage(image)
        self.roundedbutton = Button(self.master, image=self.my_img,command=lambda: self.voice_message_insert(None))
        self.roundedbutton["bg"] = "white"
        self.roundedbutton["border"] = "0"
        self.roundedbutton.place(x=20,y=10)
        self.roundedbutton.pack(side="top")

        # frame containing send button and emoji button
        #self.send_button_frame = Frame(self.master, bd=0)
        #self.send_button_frame.pack(fill=BOTH)

        

        # send button
        '''self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message_insert(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")'''
        #self.send_button.place(x=10,y=40)
        #self.send_button.pack(side=LEFT, ipady=8)
        self.master.bind("<Return>", self.send_message_insert)
        
        self.last_sent_label(date="No messages sent.")
        #t2 = threading.Thread(target=self.send_message_insert(, name='t1')
        #t2.start()
        welcome="Zara:Hi I am a chatbot developed for college enquiry system. How may I help you\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, welcome)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        
        #text to speech part

    def playResponce(self,responce):
        x=pyttsx3.init()
        #print(responce)
        li = []
        if len(responce) > 100:
            if responce.find('--') == -1:
                b = responce.split('--')
                #print(b)
                 
        x.setProperty('rate',120)
        x.setProperty('volume',100)
        x.say(responce)
        x.runAndWait()
        #print("Played Successfully......")
        
        
    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)
    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

    def chatexit(self):
        exit()

    def msg(self):
        tkinter.messagebox.showinfo("Zara v1.0",'Zara is a chatbot for answering queries related to Pondicherry Engineering College.\nIt is developed with the help of Python.\nGUI is based on Tkinter\nIt is mainly designed to answer questions regarding our college for the first year students')

    def about(self):
        tkinter.messagebox.showinfo("Zara Developers","T.BAVANI \n 3RD YEAR CSE DEPARTMENT \n PONDICHERRY ENGINEERING COLLEGE")
    
    

    


        
        
    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def font_change_times(self):
        self.text_box.config(font="Times")
        self.entry_field.config(font="Times")
        self.font = "Times"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def font_change_helvetica(self):
        self.text_box.config(font="helvetica 10")
        self.entry_field.config(font="helvetica 10")
        self.font = "helvetica 10"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys")
        self.entry_field.config(font="fixedsys")
        self.font = "fixedsys"

    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        #self.emoji_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.sent_label.config(bg="#EEEEEE", fg="#000000")

        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

    # Dark
    def color_theme_dark(self):
        self.master.config(bg="#2a2b2d")
        self.text_frame.config(bg="#2a2b2d")
        self.text_box.config(bg="#212121", fg="#FFFFFF")
        self.entry_frame.config(bg="#2a2b2d")
        self.entry_field.config(bg="#212121", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#2a2b2d")
        self.send_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
       # self.emoji_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#2a2b2d", fg="#FFFFFF")

        self.tl_bg = "#212121"
        self.tl_bg2 = "#2a2b2d"
        self.tl_fg = "#FFFFFF"

    # Grey
    def color_theme_grey(self):
        self.master.config(bg="#444444")
        self.text_frame.config(bg="#444444")
        self.text_box.config(bg="#4f4f4f", fg="#ffffff")
        self.entry_frame.config(bg="#444444")
        self.entry_field.config(bg="#4f4f4f", fg="#ffffff", insertbackground="#ffffff")
        self.send_button_frame.config(bg="#444444")
        self.send_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        #self.emoji_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.sent_label.config(bg="#444444", fg="#ffffff")

        self.tl_bg = "#4f4f4f"
        self.tl_bg2 = "#444444"
        self.tl_fg = "#ffffff"


    def color_theme_turquoise(self):
        self.master.config(bg="#003333")
        self.text_frame.config(bg="#003333")
        self.text_box.config(bg="#669999", fg="#FFFFFF")
        self.entry_frame.config(bg="#003333")
        self.entry_field.config(bg="#669999", fg="#FFFFFF", insertbackground="#FFFFFF")
        #self.send_button_frame.config(bg="#003333")
        #self.send_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        #self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#003333", fg="#FFFFFF")

        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"    

    # Blue
    def color_theme_dark_blue(self):
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        #self.send_button_frame.config(bg="#263b54")
        #self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        #self.emoji_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#263b54", fg="#FFFFFF")

        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF"

 
    

    # Torque
    def color_theme_turquoise(self):
        self.master.config(bg="#003333")
        self.text_frame.config(bg="#003333")
        self.text_box.config(bg="#669999", fg="#FFFFFF")
        self.entry_frame.config(bg="#003333")
        self.entry_field.config(bg="#669999", fg="#FFFFFF", insertbackground="#FFFFFF")
        #self.send_button_frame.config(bg="#003333")
        #self.send_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        #self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#003333", fg="#FFFFFF")

        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"

    # Hacker
    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        #self.send_button_frame.config(bg="#0F0F0F")
        #self.send_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        #self.emoji_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#0F0F0F", fg="#33FF33")

        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"

    

    # Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_default()  

    def mail_id(self,faculty_name):
        #faculty_name=input("Bot: Please enter the faculty name as per the record:")
        
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        cursor.execute("select email from faculty where name =?",(faculty_name,))
        mail_id=cursor.fetchone()
        #print("Bot:",end=" ")
        #print(mail_id[0])
        
        conn.commit()
    def news(self):
        news_lst=[]
        url="http://www.pec.edu/"
        client=request(url)
        page_html=client.read()
        client.close()
        page_soup=soup(page_html,"html.parser")
        containers=page_soup.findAll("div",{"class":"newsbox"})
        for container in containers:
            print(container.text)
            news_lst.append(container.text)
            link=container.find("a")
            if(link):
                if(link["href"]):
                    if(" " in link["href"]):
                        
                        link["href"].replace(" ","%20")
                        
                    if("https:" in link["href"]):
                        print(link["href"])
                        print("\n")
                    elif("http" in link["href"]):
                        news_lst.append(link["href"])
                        #print(link["href"])
                        #print("\n")

                    else:
                        pec_link="http://www.pec.edu/"+link["href"]
                        news_lst.append(pec_link)
                        #print(pec_link)
                        #print("\n")                       
                    
                else:
                    pass
        return news_lst
    def ccgc(self):
        ccgc_lst=[]
        url="http://ccgc.pec.edu/"
        client=request(url)
        page_html=client.read()
        client.close()
        page_soup=soup(page_html,"html.parser")
        containers=page_soup.findAll("p",{"class":["MsoNormal","MsoNormalCxSpMiddle"]})
        del containers[0:7]
        print("Bot:",end=" ")
        for container in containers:
            if containers.index(container)%6!=0:
                ccgc_lst.append(container.text)
                print(container.text,end=" ")
            else:
                ccgc_lst.append(container.text)
                print("\n")
                print(container.text)
        return ccgc_lst
    def send_message_insert(self, message):
        
        user_input = self.entry_field.get()
        pr1 = "User : " + user_input + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr1)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        t1 = threading.Thread(target=self.playResponce, args=(user_input,))
        t1.start()
        time.sleep(1)
        #ob=chat(user_input)
        ob=self.userresponse(user_input)
        pr="Zara : " + ob + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        self.last_sent_label(str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        self.entry_field.delete(0,END)
        #time.sleep(0)
        #t2 = threading.Thread(target=self.playResponce, args=(ob,))
        #t2.start()
        return ob

    def voice_message_insert(self,message):
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak anything")
            r.adjust_for_ambient_noise(source) 
            audio=r.listen(source)

            try:
                text=r.recognize_google(audio)
                vb=self.userresponse(text)
                pr1 = "Human : " + text + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr1)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                print('you said:{}'.format(text))
                pr="PyBot : " + vb + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                self.last_sent_label(str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
                self.entry_field.delete(0,END)
                '''time.sleep(0)
                t2 = threading.Thread(target=self.playResponce, args=(vb,))
                t2.start()
                return vb'''
                
                
            except:
                print("Sorry could not recognize your voice")
        
        
    tag_name=" "
    def userresponse(self,pr1):
        #print("hello")
        e_list=['😀','😃','😄','😁','🔥','⚡','👏','😎','🎇','✨','😲','😊','💙','🙌','❤️','💟','😍','😻','💓','💗','♥️','❣️','💕','👼','💝','🥰','💖','😘','🖤','💜','💚','💛','🙇‍♂️','🙇‍♀️','🧡','🤎','🤍','💞','🤝','👌','🤓','🙂','🤠','😉','🤩','🤗','🥳','🙈','💋','💯','✌','🤞','🤙','🤟','🤘','👍','🙏','🦾','👀','💃','🕺','🎉','🎊','🎖','🏆','💎','🤐','🤨','😐','😑','😶','😏','😒','🙄','😬','🤥','😔','😪','😴','😷','🤕','🤢','🤮','🤧','🥴','😵','🤦','🤦‍♂️','🤯','😕','😟','🙁','☹','😞','😤','😡','😠','🤬','💦','🖕','👎']
        response=pr1.lower()
        if len(response)>1:
            res = [ele for ele in e_list if(ele in response)]
            if len(res)!=0:
                print(res[0])
                response=response.replace(res[0],"")
                print(response)
        flag=True
        value=1
        #tag_name=""
        #response=" "
        while(flag==True):
            
            #print(response)
            #print("User:", end=" ")
            #response = input().lower()
            if(response!='bye'):
                exp=re.compile("dr.\D+.\D")
                match=exp.search(response)
                if(response=='thanks' or response=='thank you' ):
                    flag=False
                    u_res="You are welcome.."
                    return u_res
                    break
                elif any(regex in response for regex in ['📅','📆','🗓','⏰','⌚','⏲','🕰','⌛','⌛',"today's date","current date","current time","time now","time","date"]):
                    u_res=str(datetime.datetime.now())
                    return u_res
                    break
            
                else:
                    tag=1
                    u_res=" "
                    if re.search("news of pec*",response) or re.search("happenings of pec*",response):
                        value = 1
                        new=self.news()
                        for news in new:
                            u_res+=news
                            u_res+='\n'                        
                        return u_res
                    
                    elif match:
                        faculty_name=match.group()
                        conn = sqlite3.connect("chatbot.db")
                        cursor = conn.cursor()
                        cursor.execute("select name,email,designation,department from faculty3 where name =?",(faculty_name,))
                        mail_id=cursor.fetchall()
                        u_res="The faculty details for "+faculty_name+" is:\n"
                        for faculty in mail_id:
                            for string in faculty:
                                u_res+=str(string)
                                u_res+='\n'
                        return u_res
                        break                       
                    
                    while value==1:
                        for intent in data.intents["intents"]:
                            for entity in intent["entities"]:
                                tag_result=any(tag_lst in response for tag_lst in ["pec","dsc","women's cell","nss","hostel","first year","cultural club","iis","tnp","ccgc","cse","grreting","bot"])
                                if tag_result:
                                    pass
                                    
                                else:
                                    response+=" of " 
                                    response+=self.tag_name
                                if re.search("members of ccgc*",response):
                                    ccg=self.ccgc()
                                    for news in ccg:
                                        u_res+=news
                                        u_res+='\n'
                                    return u_res
                                    self.userresponse()
                                if re.search("email*",response) or re.search("mail id*",response):
                                    match=["pec","dsc","women's cell","nss","hostel","first year","cultural club","iis","tnp","ccgc","cse","grreting","bot"]
                                    if any(x in response for x in match):
                                        pass
                                    else:
                                        faculty_name="Please enter the faculty name as per the record:"
                                        fn=self.entry_field.get()
                                        print(fn)
                                        self.mail_id(fn)
                                        return faculty_name
                                       
                                for pattern in entity["patterns"]:
                                    #print(tag_name,end=" ")
                                    #print(response)                                    
                                    if pattern in response:
                                        
                                        user_response.append(random.choice(entity["responses"]))
                                        self.tag_name=intent["tag"]
                                        value=0
                                        continue
                                       
                                    else:
                                                                               
                                        continue
                        if user_response[-1]!='0' :
                            #print(user_response)
                            fl=1
                            if fl==1:

                                #print(user_response[-1])
                                u_res=user_response[-1]
                                #print("Bot:"+ u_res )
                                value=0
                                user_response.clear()
                                user_response.append('0')
                                return u_res
                                break
                        else:
                            u_res="Sorry!!! I can't understand this query"
                            #print("Sorry!!! I can't understand this query")
                            value=0
                            return u_res
                            break
                        break
                    
            else:
                flag=False
                for intent in data.intents["intents"]:
                    for entity in intent["entities"]:
                        for pattern in entity["patterns"]:
                            if pattern in response:
                                #print("Bot:"+ random.choice(entity["responses"]))
                                u_res=random.choice(entity["responses"])
                                value=1
                                return u_res
                                break

root=Tk()


a = Bot(root)
#a.userresponse()
root.geometry(window_size)
root.title("PyBot")
#root.iconbitmap('i.ico')
root.mainloop()
