import socket
import sys
import threading
import time
from queue import Queue
import pickle
from ip import IPdict
import datetime

class Server:
    def __init__(self):
        self.NUMBER_OF_THREADS=4
        self.JOB_NUMBER=[1,2,3,4]
        self.queue=Queue()
        self.all_connections=[]
        self.all_address=[]

        self.create_workers()
        self.create_jobs()

    def create_socket(self):
        try:
            self.host=""
            self.port=9999
            self.s=socket.socket()
        except socket.error as msg:
            # print(f"Socket creation error=> {msg}")
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: create_socket: {str(msg)}")


    def bind_socket(self):
        try:
            print(f"Binding the port => {self.port}")
            print(self.host)
            self.s.bind((self.host, self.port))
            self.s.listen(100) 
        except socket.error as msg:
            # print(f"Socket Binding error=> {msg} \n Retrying...")
            self.bind_socket()
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: bind_socket: {str(msg)}")

    def accepting_connection(self):
        try:
            for c in self.all_connections:
                c.close()
            del self.all_connections[:]
            del self.all_address[:]
            while True:
                try:
                    conn,address = self.s.accept()
                    self.s.setblocking(1)
                    self.all_connections.append(conn)
                    self.all_address.append(address)
                    print(f"Connection established: {address[0]}")
                except:
                    print("Error accepting connection")
                    with open("ErrorLogs.txt", "a") as f:
                        f.write(f"{str(datetime.datetime.now())}: accepting_connection: Error accepting connection")
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: accepting_connection: {str(e)}")
            self.accepting_connection()
            
            

    def list_connections(self):
        try:
            while True:
                results=[]
                for i,conn in enumerate(self.all_connections):
                    try:
                        conn.send(str.encode(' '))
                        conn.recv(201480)
                    except:
                        del self.all_connections[i]
                        del self.all_address[i]
                        continue

                    value = self.all_address[i][0]
                    key = list(IPdict.keys())[list(IPdict.values()).index(value)]
                    results.append(key)
                with open('OnPCs.txt', 'w') as f:
                    content = "\n".join(results)
                    f.write(content)
        
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: list_connections: {str(e)}")
            self.list_connections()
            
        
    
    def ShutDown_GetTasks_command(self):
        try:
            while True:
                with open('ShutdownPC.txt', 'r') as f:
                    PCs = f.read().splitlines()

                for PC in PCs:
                    if PC in IPdict.keys():
                        ipAddr = IPdict[PC]
                        addr = [x[0] for x in self.all_address]
                        target = addr.index(ipAddr)


                        conn = self.all_connections[target]
                        conn.send(str.encode('shutdown /s'))
                    else:
                        print("PC not found")
                
                with open('ShutdownPC.txt', 'r') as f:
                    PCsNew = f.read().splitlines()

                PCsLeft = list(set(PCsNew) - set(PCs))
                with open('ShutdownPC.txt', 'w') as f:
                    content = "\n".join(PCsLeft)
                    f.write(content)

                
                with open('TaskPC.txt', 'r') as f:
                    PCs = f.read().splitlines()
                
                for PC in PCs:
                    if PC in IPdict.keys():
                        ipAddr = IPdict[PC]
                        addr = [x[0] for x in self.all_address]
                        target = addr.index(ipAddr)


                        conn = self.all_connections[target]
                        conn.send(str.encode('powershell "gps | where {$_.MainWindowTitle} | select Description'))

                        response = str(conn.recv(20480), "utf-8")
                        response = response.splitlines()
                        response.pop()
                        response = [x.strip() for x in response]
                        response = [x for x in response if x!='']
                        with open('TaskDetail.txt', 'w') as f:
                            f.write("\n".join(response))

                        

                    else:
                        print("PC not found")
                
                with open('TaskPC.txt', 'w') as f:
                    f.write("")
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: ShutDown_GetTasks_command: {str(e)}")
            self.ShutDown_GetTasks_command()
            
        

    def Tasks_command(self):
        try:
            while True:
                with open('TaskPC.txt', 'r') as f:
                    PCs = f.read().splitlines()
                
                for PC in PCs:
                    if PC in IPdict.keys():
                        ipAddr = IPdict[PC]
                        addr = [x[0] for x in self.all_address]
                        target = addr.index(ipAddr)


                        conn = self.all_connections[target]
                        conn.send(str.encode('powershell "gps | where {$_.MainWindowTitle} | select Description'))

                        response = str(conn.recv(20480), "utf-8")
                        response = response.splitlines()
                        response.pop()
                        response = [x.strip() for x in response]
                        response = [x for x in response if x!='']
                        with open('TaskDetail.txt', 'w') as f:
                            f.write("\n".join(response))
                    else:
                        print("PC not found")
                
                with open('TaskPC.txt', 'w') as f:
                    f.write("")
        
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: Tasks_command: {str(e)}")
            self.Tasks_command()
            

    def BrowserUSB_command(self):
        try:
            while True:
                with open('OnPCs.txt', 'r') as f:
                    PCs = f.read().splitlines()
                
                BrowserOnPCs = []
                for PC in PCs:
                    if PC in IPdict.keys():
                        ipAddr = IPdict[PC]
                        addr = [x[0] for x in self.all_address]
                        target = addr.index(ipAddr)


                        conn = self.all_connections[target]
                        conn.send(str.encode('powershell "gps | where {$_.MainWindowTitle} | select Description'))
                        response = str(conn.recv(20480), "utf-8")
                        response = response.splitlines()
                        response.pop()
                        response = [x.strip() for x in response]
                        response = [x for x in response if x!='']
                        if ("Google Chrome" in response) or ("Microsoft Edge" in response) or ("Firefox" in response):
                            BrowserOnPCs.append(PC)
                
                with open('BrowserOnPCs.txt', 'w') as f:
                    f.write("\n".join(BrowserOnPCs))

                USBConnectedPCs = []
                for PC in PCs:
                    if PC in IPdict.keys():
                        ipAddr = IPdict[PC]
                        addr = [x[0] for x in self.all_address]
                        target = addr.index(ipAddr)


                        conn = self.all_connections[target]
                        conn.send(str.encode("""powershell "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' }"
                        """))

                        response = str(conn.recv(20480), "utf-8")
                        
                        if ("WPD" in response) or ("DiskDrive" in response) or ("USB Mass Storage" in response):
                            USBConnectedPCs.append(PC)
                
                with open('USBConnectedPCs.txt', 'w') as f:
                    f.write("\n".join(USBConnectedPCs))


                with open('CloseBrowserPCNames.txt', 'r') as f:
                    PCs = f.read().splitlines()
                
                for PC in PCs:
                    if PC in IPdict.keys():
                        ipAddr = IPdict[PC]
                        addr = [x[0] for x in self.all_address]
                        target = addr.index(ipAddr)


                        conn = self.all_connections[target]
                        conn.send(str.encode('powershell "gps | where {$_.MainWindowTitle} | select Description'))

                        response = str(conn.recv(20480), "utf-8")
                        response = response.splitlines()
                        response.pop()
                        response = [x.strip() for x in response]
                        response = [x for x in response if x!='']

                        CloseBrowserList = []
                        if ("Google Chrome" in response):
                            CloseBrowserList.append('powershell taskkill /im chrome.exe /t /f')
                        if ("Microsoft Edge" in response):
                            CloseBrowserList.append('powershell taskkill /im msedge.exe /t /f')
                        if ("Firefox" in response):
                            CloseBrowserList.append('powershell taskkill /im Firefox.exe /t /f')

                        for i in CloseBrowserList:
                            conn.send(str.encode(i))
                            time.sleep(0.1)

                    else:
                        print("PC not found")

                with open('CloseBrowserPCNames.txt', 'r') as f:
                    NewPCs = f.read().splitlines()
                
                RemainFiles = list(set(NewPCs) - set(PCs))
                with open('CloseBrowserPCNames.txt', 'w') as f:
                    f.write("\n".join(RemainFiles))

        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: BrowserUSB_command: {str(e)}")
            self.BrowserUSB_command()
            
                    



    def create_workers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t=threading.Thread(target=self.work)
            t.daemon=True
            t.start()

    def create_jobs(self):
        for x in self.JOB_NUMBER:
            self.queue.put(x)
        self.queue.join()

    def work(self):
        while True:
            x=self.queue.get()
            if x==1:
                self.create_socket()
                self.bind_socket()
                self.accepting_connection()
            if x==2:
                self.list_connections()
            if x==3:
                self.ShutDown_GetTasks_command()
            if x==4:
                self.BrowserUSB_command()

            self.queue.task_done()

if __name__ == "__main__":
    server = Server()
