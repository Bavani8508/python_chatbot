import bs4
from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup 
import re

url="http://cse.pec.edu/pages/facility.html"
client=request(url)
page_html=client.read()
client.close()
page_soup=soup(page_html,"html.parser")
containers=page_soup.findAll("div",{"class":"clear"})

cont_list=[]
#cont_list=[elem.findAll("div",{"class":"row4"}).get_text().rstrip() for elem in containers[1:]]
for container in containers:
    #print(container.text)
    #container.text.strip()    
    data = re.sub(r'[\t\n ]+', ' ', container.text).strip()
    #con_string=str(container.text)
    #con_string=con_string.replace("\n","")
    #con_string=con_string.replace("\t","")
    #con_string=con_string.replace("\xa0","")
    #con_string=con_string.replace(" ","")
    cont_list.append(data)
    cont_list.append(':')
    print(data)
    print("\n")
#cont_list=con_string.split('Dr')
#print(cont_list)
    
    
    
