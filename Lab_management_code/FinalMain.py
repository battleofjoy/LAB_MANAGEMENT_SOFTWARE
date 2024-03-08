from multiprocessing import Process
from datetime import datetime

from FinalGUI import main
from ServerNew import Server

def GUI_Function():
    try:
        main()
    except Exception as e:
        with open("ErrorLogs.txt", "a") as f:
            f.write(f"{str(datetime.now())}: GUI_Function: {str(e)}")

def Server_Function():
    try:
        server = Server()
    except Exception as e:
        with open("ErrorLogs.txt", "a") as f:
            f.write(f"{str(datetime.now())}: Server_Function: {str(e)}")

def CleanFiles():
    try:
        with open('OnPCs.txt', 'w') as f:
            f.write("")
        with open('ShutdownPC.txt', 'w') as f:
            f.write("")
        with open('TaskPC.txt', 'w') as f:
            f.write("")
        with open('TaskDetail.txt', 'w') as f:
            f.write("")
        with open("BrowserOnPCs.txt", "w") as f:
            f.write("")
        with open("USBConnectedPCs.txt", "w") as f:
            f.write("")
        with open('CloseBrowserPCNames.txt', 'w') as f:
            f.write("")
    except Exception as e:
        with open("ErrorLogs.txt", "a") as f:
            f.write(f"{str(datetime.now())}: CleanFiles: {str(e)}")



if __name__ == "__main__":
    CleanFiles()
    p1 = Process(target=GUI_Function)
    p2 = Process(target=Server_Function)
    p1.start()
    p2.start()
    p1.join()
    p2.join()