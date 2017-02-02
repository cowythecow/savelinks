
import time
import sqlite3
import pyperclip
import os

#dblocation = os.getcwd() + "\\\\files\\\\savelinks.db" 
dblocation = 'C:\\Users\\cowyt\\Desktop\\python\\text files\\savelinks.db'

conn = sqlite3.connect(dblocation)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS TODO(TITLE,LINKS)")

TITLELIST = []
LINKLIST = []

def clear():
    os.system('cls') # windows

def usage():
    clear()
    print(" USAGE ".ljust(27,"<").rjust(47,'>'))
    print("|"+"".center(45)+"|")
    print("|"+"choese the number to copy the link".center(45)+"|")
    print("|"+"quit/exit to exit".center(45)+"|")
    print("|"+"search [title]".center(45)+"|")
    print("|"+"[add] to add links".center(45)+"|")
    print("|"+"[Delete] To Delete links".center(45)+"|")
    print("|"+"".center(45)+"|")
    print('-'.ljust(24,"<").rjust(47,'>'))

def showlist():
    global TITLELIST
    global LINKLIST
    TITLELIST = []
    LINKLIST = []
    cur.execute("select * from TODO")
    TEMPLIST = cur.fetchall()
    for i in range(len(TEMPLIST)):
        TITLELIST.append(TEMPLIST[i][0])
        LINKLIST.append(TEMPLIST[i][1])
        
    for i in range(len(TITLELIST)):
        print("["+str(i+1)+"] " + TITLELIST[i])

def delete(LINK):
    print("are you sure? y/n")
    inp = input()
    if inp == "y":
        cur.execute("delete * from todo where LINKS = ?",(LINK,))
    print("----DELETED----")

    
def search(TITLE):

    TITLELIST2= []
    LINKLIST2 = []
    TITLE = " ".join(TITLE)
    TITLE2 = "%"+ TITLE +"%"
    print("searching for "+ TITLE + "...")
    cur.execute("select * from todo where TITLE like ?", (TITLE2,))
    TEMPLIST = cur.fetchall()

    for i in range(len(TEMPLIST)):
        TITLELIST2.append(TEMPLIST[i][0])
        LINKLIST2.append(TEMPLIST[i][1])


    for i in range(len(TITLELIST2)):
        print("["+str(i+1)+"] " + TITLELIST2[i])
    if TITLELIST2 == []:
        print("[-]" + TITLE + " not found!")

    else:
        INP = input()
        if INP != "":
            INP = int(INP)-1
            pyperclip.copy(LINKLIST2[INP])
        
    
def addlinks():
    print("TITLE: ")
    TITLE = input()
    print("LINK(just enter will copy from clipboard): ")
    LINKS = input()
    if LINKS == "":
        LINKS = pyperclip.paste() 
    cur.execute("INSERT INTO TODO(TITLE,LINKS) VALUES(?,?)", (TITLE,LINKS))
    conn.commit()

def updatelink(oldtitle,oldlink):
    clear()
    newlink = pyperclip.paste()
    print(oldlink)
    
    print("New Link: " + newlink)
    print("update?[Y]")
    inp = input()
    if inp.lower() == "y":
        #cur.execute("UPDATE TODO SET(TITLE = ?,LINKS = ?) WHERE TITLE = ?",(oldtitle,newlink,oldtitle))
        #conn.commit()
        pass
    else:
        print("Update canceled!")
    
    
def main():
    global TITLELIST
    global LINKLIST
    while(1):
        showlist()
        try:
            INP = input()
            if INP == "":
                raise AssertionError
            elif any(INP.lower() in x for x in ["quit","exit"]):
                print("Exiting...")
                break
            elif "search" in INP.lower():
                clear()
                INP = INP.split()
                search(INP[1:])
            elif "delete" in INP.lower():
                clear()
                INP = INP.split()
                print("Deleting {}".format(INP[1]))
                delete(LINKLIST[int(INP[1])-1])
            elif INP.lower() == "add":
                clear()
                addlinks()
            elif INP.split()[0].lower() == "update":
                updatelink(TITLELIST[int(int(INP.split()[1])-1)],LINKLIST[int(int(INP.split()[1])-1)])
            else:
                INP = int(INP)-1
                pyperclip.copy(LINKLIST[INP])
        
        except Exception as e:
            print(e)
            usage()
            time.sleep(2)

usage()
main()
conn.commit()
conn.close()
