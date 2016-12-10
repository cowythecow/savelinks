
import time
import sqlite3
import pyperclip
import os

dblocation = os.getcwd() + "\\\\files\\\\savelinks.db" 

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
    print("|"+"[99] to add links".center(45)+"|")
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

def main():
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
            elif INP == "99":
                clear()
                addlinks()
            else:
                INP = int(INP)-1
                pyperclip.copy(LINKLIST[INP])
        
        except:
            usage()
            time.sleep(2)

usage()
main()
conn.commit()
conn.close()

