from tkinter import *
from tkinter import messagebox
import threading
import multiprocessing
import time
import datetime

class LabManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Management")
        
        baseWidth = 1920
        baseHeight = 1080
        ratioWidth = self.root.winfo_screenwidth() / baseWidth
        ratioHeight = self.root.winfo_screenheight() / baseHeight

        self.root.geometry(f"{int(baseWidth*ratioWidth)}x{int(baseHeight*ratioHeight)}")
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        Heading = Label(self.root, text="Lab Management", font=f"times {int(30*ratioHeight)} bold", bd = 4, relief = RIDGE)
        Heading.place(x=int(5*ratioWidth), y=int(5*ratioHeight), width=int(1835*ratioWidth), height=int(70*ratioHeight))

        self.exitButton = Button(self.root, text="X", bd=4, font=f"times {int(20*ratioHeight)} bold", relief=RIDGE, command=self.exitButton_Pressed)
        self.exitButton.place(x=int(1845*ratioWidth), y=int(5*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))

        self.SL_PC_Dict = dict()

        self.SL_PCs_ShutdownPlacing = dict()
        self.SL_PCs_TasksPlacing = dict()
        self.SL_PCs_USBPlacing = dict()
        self.SL_PCs_BrowserPlacing = dict()

        self.SL_PCs_USBPlaceAttributes = dict()
        self.SL_PCs_BrowserPlaceAttributes = dict()

        self.ShutDownButton = Button()
        self.getTasksButton = Button()

        self.SL1_FrameCreate(ratioWidth, ratioHeight)
        self.SL2_FrameCreate(ratioWidth, ratioHeight)
        self.SL3_FrameCreate(ratioWidth, ratioHeight)
        self.SL4_FrameCreate(ratioWidth, ratioHeight)

        self.On_PC_Update()

        
    def On_PC_Update(self):
        try:
            Dummy = Label(self.root)
            with open ('OnPCs.txt', 'r') as f:
                OnPCs = f.read().splitlines()
            
            PCs = self.SL_PC_Dict.keys()
            OffPCs = list(set(PCs) - set(OnPCs))
            for OffPC in OffPCs:
                self.SL_PC_Dict[OffPC].config(bg = 'SystemButtonFace')
            for OnPC in OnPCs:
                self.SL_PC_Dict[OnPC].config(bg = '#98FB98')

            for OnPC in OnPCs:
                values = self.SL_PCs_USBPlaceAttributes[OnPC]
                self.SL_PCs_USBPlacing[OnPC].place(x=values[0], y=values[1], width=values[2], height=values[3])
                values = self.SL_PCs_BrowserPlaceAttributes[OnPC]
                self.SL_PCs_BrowserPlacing[OnPC].place(x=values[0], y=values[1], width=values[2], height=values[3])

            for OffPC in OffPCs:
                if "SL2" in str(OffPC):
                    self.SL_PCs_USBPlacing[OffPC].place_forget()
                    self.SL_PCs_BrowserPlacing[OffPC].place_forget()

            with open('BrowserOnPCs.txt', 'r') as f:
                BrowserOnPCs = f.read().splitlines()
            
            with open('USBConnectedPCs.txt', 'r') as f:
                USBOnPCs = f.read().splitlines()

            BrowserOFFPCs = list(set(OnPCs) - set(BrowserOnPCs))
            for BrowserOFFPC in BrowserOFFPCs:
                self.SL_PCs_BrowserPlacing[BrowserOFFPC].config(bg = 'SystemButtonFace')
            for BrowserONPC in BrowserOnPCs:
                self.SL_PCs_BrowserPlacing[BrowserONPC].config(bg = '#FC7676')

            USBOFFPCs = list(set(OnPCs) - set(USBOnPCs))
            for USBOFFPC in USBOFFPCs:
                self.SL_PCs_USBPlacing[USBOFFPC].config(bg = 'SystemButtonFace')
            for USBONPC in USBOnPCs:
                self.SL_PCs_USBPlacing[USBONPC].config(bg = '#FC7676')

            Dummy.after(1000, self.On_PC_Update)
        
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: On_PC_Update: {str(e)}")
            self.On_PC_Update()
            


    def ShutDownButton_Pressed(self, *args):
        try:
            Pc, LabName  = args
            Ans = messagebox.askyesno("Shut Down", f"Are you sure you want to shut down {Pc} in {LabName}?")
            if Ans == True:
                with open ('ShutdownPC.txt', 'a') as f:
                    f.write(f"{Pc}\n")

                messagebox.showinfo("Shut Down", f"{Pc} in {LabName} shut down command has been sent")
                self.SL_PCs_ShutdownPlacing[Pc].destroy()
                self.SL_PCs_TasksPlacing[Pc].destroy()
                self.SL_PCs_ShutdownPlacing.pop(Pc)
                self.SL_PCs_TasksPlacing.pop(Pc)
                self.SL_PC_Dict[Pc].config(bd = 3)
                # self.SL_PC_Dict[Pc].config(bg = 'SystemButtonFace')

            else:
                pass 
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: ShutDownButton_Pressed: {str(e)}")

    def TasksButton_Pressed(self, *args):
        try:
            Pc, LabName  = args
            with open ('TaskPC.txt', 'w') as f:
                f.write(f"{Pc}\n")

            time.sleep(2)

            with open ('TaskDetail.txt', 'r') as f:
                TasksRunning = f.read().splitlines()

            Msg = f"Tasks of {Pc} in {LabName} are being displayed\n"
            Tasks = "\n".join(TasksRunning)
            messagebox.showinfo("Tasks", Msg +"\n"+ Tasks)

            self.SL_PCs_ShutdownPlacing[Pc].destroy()
            self.SL_PCs_TasksPlacing[Pc].destroy()
            self.SL_PCs_ShutdownPlacing.pop(Pc)
            self.SL_PCs_TasksPlacing.pop(Pc)
            self.SL_PC_Dict[Pc].config(bd = 3)
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: TasksButton_Pressed: {str(e)}")

    def SL_PCs(self, *args):
        try:
            Pc, Lab, LabName, ratioWidth, ratioHeight, Side  = args

            PC_X = self.SL_PC_Dict[Pc].winfo_x()
            PC_Y = self.SL_PC_Dict[Pc].winfo_y()
            PC_Width = self.SL_PC_Dict[Pc].winfo_width()
            PC_Height = self.SL_PC_Dict[Pc].winfo_height()

            PC_BGcolor = self.SL_PC_Dict[Pc].cget('bg')

            if PC_BGcolor!='SystemButtonFace':
                if self.SL_PC_Dict[Pc]['bd'] == 3:
                    self.SL_PCs_ShutdownPlacing[Pc] = Button(Lab, text="📴", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.ShutDownButton_Pressed(Pc, LabName))
                    self.SL_PCs_TasksPlacing[Pc] = Button(Lab, text="📝", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.TasksButton_Pressed(Pc, LabName))
                    

                    if Side == 'Left':
                        self.SL_PCs_ShutdownPlacing[Pc].place(x=int(PC_X+15+PC_Width*ratioWidth), y=int(PC_Y+5*ratioHeight), width=int(50*ratioWidth), height=int(50*ratioHeight))
                        self.SL_PCs_TasksPlacing[Pc].place(x=int(PC_X+15+PC_Width*ratioWidth+50*ratioWidth+10), y=int(PC_Y+5*ratioHeight), width=int(50*ratioWidth), height=int(50*ratioHeight))
                        
                        
                    elif Side == 'Right':
                        self.SL_PCs_ShutdownPlacing[Pc].place(x=int(PC_X-10-50*ratioWidth), y=int(PC_Y+5*ratioHeight), width=int(50*ratioWidth), height=int(50*ratioHeight))
                        self.SL_PCs_TasksPlacing[Pc].place(x=int(PC_X-10-50*ratioWidth-50*ratioWidth-10), y=int(PC_Y+5*ratioHeight), width=int(50*ratioWidth), height=int(50*ratioHeight))
                        
                    self.SL_PC_Dict[Pc].config(bd = 2)
                
                else:
                    self.SL_PCs_ShutdownPlacing[Pc].destroy()
                    self.SL_PCs_TasksPlacing[Pc].destroy()
                    self.SL_PCs_ShutdownPlacing.pop(Pc)
                    self.SL_PCs_TasksPlacing.pop(Pc)

                    self.SL_PC_Dict[Pc].config(bd = 3)
        
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: SL_PCs: {str(e)}")

    def ShutdownAllPCsFunc(self, *args):
        try:
            Ans = messagebox.askyesno("Shut Down", f"Are you sure you want to shut down all PCs in {args[1]}?")
            if Ans == True:
                Lab = args[1]
                with open ('OnPCs.txt', 'r') as f:
                    OnPCs = f.read().splitlines()

                LabPcs = [Pc for Pc in OnPCs if str(Lab) in str(Pc)]

                with open ('ShutdownPC.txt', 'a') as f:
                    for Pc in LabPcs:
                        f.write(f"{Pc}\n")
            else:
                pass
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: ShutdownAllPCsFunc: {str(e)}")

    def CloseBrowser(self, *args):
        try:
            Pc, LabName  = args
            Ans = messagebox.askyesno("Close Browsers", f"Are you sure you want to close all browsers of {Pc} in {LabName}?")
            if Ans == True:
                with open("CloseBrowserPCNames.txt", "a") as f:
                    f.write(f"{Pc}\n")
                messagebox.showinfo("Close Browser", f"{Pc} in {LabName} Browsers are being closed")
            else:
                pass
        except Exception as e:
            with open("ErrorLogs.txt", "a") as f:
                f.write(f"{str(datetime.datetime.now())}: CloseBrowser: {str(e)}")


    def SL1_FrameCreate(self, ratioWidth, ratioHeight):
        SL1_Frame = Frame(self.root, bd=3, relief=RIDGE)
        SL1_Frame.place(x=int(5*ratioWidth), y=int(90*ratioHeight), width=int(470*ratioWidth), height=int(980*ratioHeight))
        LabLabel = Label(SL1_Frame, text="Software Lab 1", font=f"times {int(30*ratioHeight)} bold underline ", bd = 0, relief = None)
        LabLabel.place(x=int(5*ratioWidth), y=int(10*ratioHeight), width=int(455*ratioWidth), height=int(70*ratioHeight))

        self.SL_PC_Dict['SL1_PC1'] = Button(SL1_Frame, text="PC1", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC1', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC2'] = Button(SL1_Frame, text="PC2", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC2', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC3'] = Button(SL1_Frame, text="PC3", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC3', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC4'] = Button(SL1_Frame, text="PC4", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC4', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC5'] = Button(SL1_Frame, text="PC5", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC5', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC6'] = Button(SL1_Frame, text="PC6", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC6', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC7'] = Button(SL1_Frame, text="PC7", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC7', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC8'] = Button(SL1_Frame, text="PC8", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC8', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC9'] = Button(SL1_Frame, text="PC9", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC9', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC10'] = Button(SL1_Frame, text="PC10", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC10', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL1_PC11'] = Button(SL1_Frame, text="PC11", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC11', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL1_PC12'] = Button(SL1_Frame, text="PC12", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC12', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL1_PC13'] = Button(SL1_Frame, text="PC13", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC13', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL1_PC14'] = Button(SL1_Frame, text="PC14", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC14', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL1_PC15'] = Button(SL1_Frame, text="PC15", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC15', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL1_PC16'] = Button(SL1_Frame, text="PC16", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC16', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL1_PC17'] = Button(SL1_Frame, text="PC17", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC17', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL1_PC18'] = Button(SL1_Frame, text="PC18", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC18', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL1_PC19'] = Button(SL1_Frame, text="PC19", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC19', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL1_PC20'] = Button(SL1_Frame, text="PC20", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL1_PC20', SL1_Frame, "SL1", ratioWidth, ratioHeight, 'Right'))
        
        self.SL_PC_Dict['SL1_PC1'].place(x=int(35*ratioWidth), y=int(100*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC2'].place(x=int(35*ratioWidth), y=int(180*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC3'].place(x=int(35*ratioWidth), y=int(260*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC4'].place(x=int(35*ratioWidth), y=int(340*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC5'].place(x=int(35*ratioWidth), y=int(420*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC6'].place(x=int(35*ratioWidth), y=int(500*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC7'].place(x=int(35*ratioWidth), y=int(580*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC8'].place(x=int(35*ratioWidth), y=int(660*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC9'].place(x=int(35*ratioWidth), y=int(740*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC10'].place(x=int(35*ratioWidth), y=int(820*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC11'].place(x=int(360*ratioWidth), y=int(100*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC12'].place(x=int(360*ratioWidth), y=int(180*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC13'].place(x=int(360*ratioWidth), y=int(260*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC14'].place(x=int(360*ratioWidth), y=int(340*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC15'].place(x=int(360*ratioWidth), y=int(420*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC16'].place(x=int(360*ratioWidth), y=int(500*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC17'].place(x=int(360*ratioWidth), y=int(580*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC18'].place(x=int(360*ratioWidth), y=int(660*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC19'].place(x=int(360*ratioWidth), y=int(740*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL1_PC20'].place(x=int(360*ratioWidth), y=int(820*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))

        self.SL_PCs_USBPlacing['SL1_PC1'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC2'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC3'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC4'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC5'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC6'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC7'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC8'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC9'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC10'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC11'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC12'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC13'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC14'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC15'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC16'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC17'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC18'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC19'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL1_PC20'] = Button(SL1_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)

        self.SL_PCs_BrowserPlacing['SL1_PC1'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC1', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC2'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC2', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC3'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC3', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC4'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC4', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC5'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC5', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC6'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC6', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC7'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC7', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC8'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC8', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC9'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC9', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC10'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC10', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC11'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC11', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC12'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC12', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC13'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC13', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC14'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC14', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC15'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC15', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC16'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC16', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC17'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC17', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC18'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC18', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC19'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC19', "SL1"))
        self.SL_PCs_BrowserPlacing['SL1_PC20'] = Button(SL1_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL1_PC20', "SL1"))

        self.SL_PCs_BrowserPlaceAttributes['SL1_PC1'] = [int(40*ratioWidth-25), int(105*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC2'] = [int(40*ratioWidth-25), int(185*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC3'] = [int(40*ratioWidth-25), int(265*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC4'] = [int(40*ratioWidth-25), int(345*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC5'] = [int(40*ratioWidth-25), int(425*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC6'] = [int(40*ratioWidth-25), int(505*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC7'] = [int(40*ratioWidth-25), int(585*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC8'] = [int(40*ratioWidth-25), int(665*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC9'] = [int(40*ratioWidth-25), int(745*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC10'] = [int(40*ratioWidth-25), int(825*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC11'] = [int(435*ratioWidth), int(105*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC12'] = [int(435*ratioWidth), int(185*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC13'] = [int(435*ratioWidth), int(265*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC14'] = [int(435*ratioWidth), int(345*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC15'] = [int(435*ratioWidth), int(425*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC16'] = [int(435*ratioWidth), int(505*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC17'] = [int(435*ratioWidth), int(585*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC18'] = [int(435*ratioWidth), int(665*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC19'] = [int(435*ratioWidth), int(745*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL1_PC20'] = [int(435*ratioWidth), int(825*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]

        self.SL_PCs_USBPlaceAttributes['SL1_PC1'] = [int(40*ratioWidth-25), int(140*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC2'] = [int(40*ratioWidth-25), int(220*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC3'] = [int(40*ratioWidth-25), int(300*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC4'] = [int(40*ratioWidth-25), int(380*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC5'] = [int(40*ratioWidth-25), int(460*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC6'] = [int(40*ratioWidth-25), int(540*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC7'] = [int(40*ratioWidth-25), int(620*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC8'] = [int(40*ratioWidth-25), int(700*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC9'] = [int(40*ratioWidth-25), int(780*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC10'] = [int(40*ratioWidth-25), int(860*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC11'] = [int(435*ratioWidth), int(140*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC12'] = [int(435*ratioWidth), int(220*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC13'] = [int(435*ratioWidth), int(300*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC14'] = [int(435*ratioWidth), int(380*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC15'] = [int(435*ratioWidth), int(460*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC16'] = [int(435*ratioWidth), int(540*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC17'] = [int(435*ratioWidth), int(620*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC18'] = [int(435*ratioWidth), int(700*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC19'] = [int(435*ratioWidth), int(780*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL1_PC20'] = [int(435*ratioWidth), int(860*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]



        self.ShutdownAllPCs = Button(SL1_Frame, text="Shutdown All PCs", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.ShutdownAllPCsFunc(SL1_Frame, "SL1",ratioWidth, ratioHeight))
        self.ShutdownAllPCs.place(x=int(95*ratioWidth), y=int(905*ratioHeight), width=int(260*ratioWidth), height=int(50*ratioHeight))


    def SL2_FrameCreate(self, ratioWidth, ratioHeight):
        SL2_Frame = Frame(self.root, bd=3, relief=RIDGE)
        SL2_Frame.place(x=int(483*ratioWidth), y=int(90*ratioHeight), width=int(470*ratioWidth), height=int(980*ratioHeight))
        LabLabel = Label(SL2_Frame, text="Software Lab 2", font=f"times {int(30*ratioHeight)} bold underline", bd = 0, relief = None)
        LabLabel.place(x=int(5*ratioWidth), y=int(10*ratioHeight), width=int(455*ratioWidth), height=int(70*ratioHeight))

        self.SL_PC_Dict['SL2_PC1'] = Button(SL2_Frame, text="PC1", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC1', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC2'] = Button(SL2_Frame, text="PC2", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC2', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC3'] = Button(SL2_Frame, text="PC3", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC3', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC4'] = Button(SL2_Frame, text="PC4", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC4', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC5'] = Button(SL2_Frame, text="PC5", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC5', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC6'] = Button(SL2_Frame, text="PC6", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC6', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC7'] = Button(SL2_Frame, text="PC7", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC7', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC8'] = Button(SL2_Frame, text="PC8", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC8', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC9'] = Button(SL2_Frame, text="PC9", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC9', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC10'] = Button(SL2_Frame, text="PC10", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC10', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL2_PC11'] = Button(SL2_Frame, text="PC11", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC11', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL2_PC12'] = Button(SL2_Frame, text="PC12", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC12', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL2_PC13'] = Button(SL2_Frame, text="PC13", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC13', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL2_PC14'] = Button(SL2_Frame, text="PC14", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC14', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL2_PC15'] = Button(SL2_Frame, text="PC15", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC15', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL2_PC16'] = Button(SL2_Frame, text="PC16", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC16', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL2_PC17'] = Button(SL2_Frame, text="PC17", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC17', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL2_PC18'] = Button(SL2_Frame, text="PC18", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC18', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL2_PC19'] = Button(SL2_Frame, text="PC19", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC19', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL2_PC20'] = Button(SL2_Frame, text="PC20", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL2_PC20', SL2_Frame, "SL2", ratioWidth, ratioHeight, 'Right'))

        self.SL_PC_Dict['SL2_PC1'].place(x=int(35*ratioWidth), y=int(100*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC2'].place(x=int(35*ratioWidth), y=int(180*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC3'].place(x=int(35*ratioWidth), y=int(260*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC4'].place(x=int(35*ratioWidth), y=int(340*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC5'].place(x=int(35*ratioWidth), y=int(420*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC6'].place(x=int(35*ratioWidth), y=int(500*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC7'].place(x=int(35*ratioWidth), y=int(580*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC8'].place(x=int(35*ratioWidth), y=int(660*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC9'].place(x=int(35*ratioWidth), y=int(740*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC10'].place(x=int(35*ratioWidth), y=int(820*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC11'].place(x=int(360*ratioWidth), y=int(100*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC12'].place(x=int(360*ratioWidth), y=int(180*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC13'].place(x=int(360*ratioWidth), y=int(260*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC14'].place(x=int(360*ratioWidth), y=int(340*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC15'].place(x=int(360*ratioWidth), y=int(420*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC16'].place(x=int(360*ratioWidth), y=int(500*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC17'].place(x=int(360*ratioWidth), y=int(580*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC18'].place(x=int(360*ratioWidth), y=int(660*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC19'].place(x=int(360*ratioWidth), y=int(740*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL2_PC20'].place(x=int(360*ratioWidth), y=int(820*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))

        self.SL_PCs_USBPlacing['SL2_PC1'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC2'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC3'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC4'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC5'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC6'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC7'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC8'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC9'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC10'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC11'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC12'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC13'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC14'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC15'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC16'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC17'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC18'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC19'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL2_PC20'] = Button(SL2_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)

        self.SL_PCs_BrowserPlacing['SL2_PC1'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC1', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC2'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC2', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC3'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC3', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC4'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC4', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC5'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC5', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC6'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC6', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC7'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC7', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC8'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC8', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC9'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC9', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC10'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC10', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC11'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC11', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC12'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC12', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC13'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC13', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC14'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC14', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC15'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC15', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC16'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC16', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC17'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC17', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC18'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC18', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC19'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC19', "SL2"))
        self.SL_PCs_BrowserPlacing['SL2_PC20'] = Button(SL2_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL2_PC20', "SL2"))

        self.SL_PCs_BrowserPlaceAttributes['SL2_PC1'] = [int(40*ratioWidth-25), int(105*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC2'] = [int(40*ratioWidth-25), int(185*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC3'] = [int(40*ratioWidth-25), int(265*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC4'] = [int(40*ratioWidth-25), int(345*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC5'] = [int(40*ratioWidth-25), int(425*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC6'] = [int(40*ratioWidth-25), int(505*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC7'] = [int(40*ratioWidth-25), int(585*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC8'] = [int(40*ratioWidth-25), int(665*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC9'] = [int(40*ratioWidth-25), int(745*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC10'] = [int(40*ratioWidth-25), int(825*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC11'] = [int(435*ratioWidth), int(105*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC12'] = [int(435*ratioWidth), int(185*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC13'] = [int(435*ratioWidth), int(265*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC14'] = [int(435*ratioWidth), int(345*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC15'] = [int(435*ratioWidth), int(425*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC16'] = [int(435*ratioWidth), int(505*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC17'] = [int(435*ratioWidth), int(585*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC18'] = [int(435*ratioWidth), int(665*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC19'] = [int(435*ratioWidth), int(745*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL2_PC20'] = [int(435*ratioWidth), int(825*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]


        self.SL_PCs_USBPlaceAttributes['SL2_PC1'] = [int(40*ratioWidth-25), int(140*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC2'] = [int(40*ratioWidth-25), int(220*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC3'] = [int(40*ratioWidth-25), int(300*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC4'] = [int(40*ratioWidth-25), int(380*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC5'] = [int(40*ratioWidth-25), int(460*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC6'] = [int(40*ratioWidth-25), int(540*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC7'] = [int(40*ratioWidth-25), int(620*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC8'] = [int(40*ratioWidth-25), int(700*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC9'] = [int(40*ratioWidth-25), int(780*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC10'] = [int(40*ratioWidth-25), int(860*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC11'] = [int(435*ratioWidth), int(140*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC12'] = [int(435*ratioWidth), int(220*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC13'] = [int(435*ratioWidth), int(300*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC14'] = [int(435*ratioWidth), int(380*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC15'] = [int(435*ratioWidth), int(460*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC16'] = [int(435*ratioWidth), int(540*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC17'] = [int(435*ratioWidth), int(620*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC18'] = [int(435*ratioWidth), int(700*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC19'] = [int(435*ratioWidth), int(780*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL2_PC20'] = [int(435*ratioWidth), int(860*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]


        self.ShutdownAllPCs = Button(SL2_Frame, text="Shutdown All PCs", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.ShutdownAllPCsFunc(SL2_Frame, "SL2",ratioWidth, ratioHeight))
        self.ShutdownAllPCs.place(x=int(95*ratioWidth), y=int(905*ratioHeight), width=int(260*ratioWidth), height=int(50*ratioHeight))


    def SL3_FrameCreate(self, ratioWidth, ratioHeight):
        SL3_Frame = Frame(self.root, bd=3, relief=RIDGE)
        SL3_Frame.place(x=int(962*ratioWidth), y=int(90*ratioHeight), width=int(470*ratioWidth), height=int(980*ratioHeight))
        LabLabel = Label(SL3_Frame, text="Software Lab 3", font=f"times {int(30*ratioHeight)} bold underline", bd = 0, relief = None)
        LabLabel.place(x=int(5*ratioWidth), y=int(10*ratioHeight), width=int(455*ratioWidth), height=int(70*ratioHeight))

        self.SL_PC_Dict['SL3_PC1'] = Button(SL3_Frame, text="PC1", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC1', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC2'] = Button(SL3_Frame, text="PC2", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC2', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC3'] = Button(SL3_Frame, text="PC3", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC3', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC4'] = Button(SL3_Frame, text="PC4", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC4', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC5'] = Button(SL3_Frame, text="PC5", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC5', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC6'] = Button(SL3_Frame, text="PC6", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC6', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC7'] = Button(SL3_Frame, text="PC7", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC7', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC8'] = Button(SL3_Frame, text="PC8", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC8', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC9'] = Button(SL3_Frame, text="PC9", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC9', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC10'] = Button(SL3_Frame, text="PC10", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC10', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL3_PC11'] = Button(SL3_Frame, text="PC11", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC11', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL3_PC12'] = Button(SL3_Frame, text="PC12", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC12', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL3_PC13'] = Button(SL3_Frame, text="PC13", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC13', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL3_PC14'] = Button(SL3_Frame, text="PC14", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC14', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL3_PC15'] = Button(SL3_Frame, text="PC15", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC15', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL3_PC16'] = Button(SL3_Frame, text="PC16", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC16', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL3_PC17'] = Button(SL3_Frame, text="PC17", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC17', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL3_PC18'] = Button(SL3_Frame, text="PC18", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC18', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL3_PC19'] = Button(SL3_Frame, text="PC19", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC19', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL3_PC20'] = Button(SL3_Frame, text="PC20", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL3_PC20', SL3_Frame, "SL3", ratioWidth, ratioHeight, 'Right'))

        self.SL_PC_Dict['SL3_PC1'].place(x=int(35*ratioWidth), y=int(100*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC2'].place(x=int(35*ratioWidth), y=int(180*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC3'].place(x=int(35*ratioWidth), y=int(260*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC4'].place(x=int(35*ratioWidth), y=int(340*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC5'].place(x=int(35*ratioWidth), y=int(420*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC6'].place(x=int(35*ratioWidth), y=int(500*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC7'].place(x=int(35*ratioWidth), y=int(580*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC8'].place(x=int(35*ratioWidth), y=int(660*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC9'].place(x=int(35*ratioWidth), y=int(740*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC10'].place(x=int(35*ratioWidth), y=int(820*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC11'].place(x=int(360*ratioWidth), y=int(100*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC12'].place(x=int(360*ratioWidth), y=int(180*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC13'].place(x=int(360*ratioWidth), y=int(260*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC14'].place(x=int(360*ratioWidth), y=int(340*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC15'].place(x=int(360*ratioWidth), y=int(420*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC16'].place(x=int(360*ratioWidth), y=int(500*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC17'].place(x=int(360*ratioWidth), y=int(580*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC18'].place(x=int(360*ratioWidth), y=int(660*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC19'].place(x=int(360*ratioWidth), y=int(740*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL3_PC20'].place(x=int(360*ratioWidth), y=int(820*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))

        self.SL_PCs_USBPlacing['SL3_PC1'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC2'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC3'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC4'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC5'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC6'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC7'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC8'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC9'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC10'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC11'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC12'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC13'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC14'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC15'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC16'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC17'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC18'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC19'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL3_PC20'] = Button(SL3_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)

        self.SL_PCs_BrowserPlacing['SL3_PC1'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC1', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC2'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC2', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC3'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC3', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC4'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC4', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC5'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC5', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC6'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC6', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC7'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC7', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC8'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC8', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC9'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC9', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC10'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC10', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC11'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC11', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC12'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC12', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC13'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC13', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC14'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC14', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC15'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC15', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC16'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC16', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC17'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC17', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC18'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC18', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC19'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC19', "SL3"))
        self.SL_PCs_BrowserPlacing['SL3_PC20'] = Button(SL3_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL3_PC20', "SL3"))

        self.SL_PCs_BrowserPlaceAttributes['SL3_PC1'] = [int(40*ratioWidth-25), int(105*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC2'] = [int(40*ratioWidth-25), int(185*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC3'] = [int(40*ratioWidth-25), int(265*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC4'] = [int(40*ratioWidth-25), int(345*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC5'] = [int(40*ratioWidth-25), int(425*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC6'] = [int(40*ratioWidth-25), int(505*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC7'] = [int(40*ratioWidth-25), int(585*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC8'] = [int(40*ratioWidth-25), int(665*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC9'] = [int(40*ratioWidth-25), int(745*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC10'] = [int(40*ratioWidth-25), int(825*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC11'] = [int(435*ratioWidth), int(105*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC12'] = [int(435*ratioWidth), int(185*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC13'] = [int(435*ratioWidth), int(265*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC14'] = [int(435*ratioWidth), int(345*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC15'] = [int(435*ratioWidth), int(425*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC16'] = [int(435*ratioWidth), int(505*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC17'] = [int(435*ratioWidth), int(585*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC18'] = [int(435*ratioWidth), int(665*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC19'] = [int(435*ratioWidth), int(745*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL3_PC20'] = [int(435*ratioWidth), int(825*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]


        self.SL_PCs_USBPlaceAttributes['SL3_PC1'] = [int(40*ratioWidth-25), int(140*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC2'] = [int(40*ratioWidth-25), int(220*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC3'] = [int(40*ratioWidth-25), int(300*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC4'] = [int(40*ratioWidth-25), int(380*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC5'] = [int(40*ratioWidth-25), int(460*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC6'] = [int(40*ratioWidth-25), int(540*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC7'] = [int(40*ratioWidth-25), int(620*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC8'] = [int(40*ratioWidth-25), int(700*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC9'] = [int(40*ratioWidth-25), int(780*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC10'] = [int(40*ratioWidth-25), int(860*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC11'] = [int(435*ratioWidth), int(140*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC12'] = [int(435*ratioWidth), int(220*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC13'] = [int(435*ratioWidth), int(300*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC14'] = [int(435*ratioWidth), int(380*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC15'] = [int(435*ratioWidth), int(460*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC16'] = [int(435*ratioWidth), int(540*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC17'] = [int(435*ratioWidth), int(620*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC18'] = [int(435*ratioWidth), int(700*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC19'] = [int(435*ratioWidth), int(780*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL3_PC20'] = [int(435*ratioWidth), int(860*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]


        self.ShutdownAllPCs = Button(SL3_Frame, text="Shutdown All PCs", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.ShutdownAllPCsFunc(SL3_Frame, "SL3",ratioWidth, ratioHeight))
        self.ShutdownAllPCs.place(x=int(95*ratioWidth), y=int(905*ratioHeight), width=int(260*ratioWidth), height=int(50*ratioHeight))


    def SL4_FrameCreate(self, ratioWidth, ratioHeight):
        SL4_Frame = Frame(self.root, bd=3, relief=RIDGE)
        SL4_Frame.place(x=int(1440*ratioWidth), y=int(90*ratioHeight), width=int(470*ratioWidth), height=int(980*ratioHeight))
        LabLabel = Label(SL4_Frame, text="Software Lab 4", font=f"times {int(30*ratioHeight)} bold underline", bd = 0, relief = None)
        LabLabel.place(x=int(5*ratioWidth), y=int(10*ratioHeight), width=int(455*ratioWidth), height=int(70*ratioHeight))

        self.SL_PC_Dict['SL4_PC1'] = Button(SL4_Frame, text="PC1", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC1', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC2'] = Button(SL4_Frame, text="PC2", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC2', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC3'] = Button(SL4_Frame, text="PC3", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC3', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC4'] = Button(SL4_Frame, text="PC4", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC4', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC5'] = Button(SL4_Frame, text="PC5", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC5', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC6'] = Button(SL4_Frame, text="PC6", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC6', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC7'] = Button(SL4_Frame, text="PC7", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC7', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC8'] = Button(SL4_Frame, text="PC8", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC8', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC9'] = Button(SL4_Frame, text="PC9", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC9', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC10'] = Button(SL4_Frame, text="PC10", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC10', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Left'))
        self.SL_PC_Dict['SL4_PC11'] = Button(SL4_Frame, text="PC11", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC11', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL4_PC12'] = Button(SL4_Frame, text="PC12", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC12', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL4_PC13'] = Button(SL4_Frame, text="PC13", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC13', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL4_PC14'] = Button(SL4_Frame, text="PC14", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC14', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL4_PC15'] = Button(SL4_Frame, text="PC15", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC15', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL4_PC16'] = Button(SL4_Frame, text="PC16", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC16', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL4_PC17'] = Button(SL4_Frame, text="PC17", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC17', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL4_PC18'] = Button(SL4_Frame, text="PC18", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC18', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL4_PC19'] = Button(SL4_Frame, text="PC19", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC19', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))
        self.SL_PC_Dict['SL4_PC20'] = Button(SL4_Frame, text="PC20", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.SL_PCs('SL4_PC20', SL4_Frame, "SL4", ratioWidth, ratioHeight, 'Right'))

        self.SL_PC_Dict['SL4_PC1'].place(x=int(35*ratioWidth), y=int(100*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC2'].place(x=int(35*ratioWidth), y=int(180*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC3'].place(x=int(35*ratioWidth), y=int(260*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC4'].place(x=int(35*ratioWidth), y=int(340*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC5'].place(x=int(35*ratioWidth), y=int(420*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC6'].place(x=int(35*ratioWidth), y=int(500*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC7'].place(x=int(35*ratioWidth), y=int(580*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC8'].place(x=int(35*ratioWidth), y=int(660*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC9'].place(x=int(35*ratioWidth), y=int(740*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC10'].place(x=int(35*ratioWidth), y=int(820*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC11'].place(x=int(360*ratioWidth), y=int(100*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC12'].place(x=int(360*ratioWidth), y=int(180*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC13'].place(x=int(360*ratioWidth), y=int(260*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC14'].place(x=int(360*ratioWidth), y=int(340*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC15'].place(x=int(360*ratioWidth), y=int(420*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC16'].place(x=int(360*ratioWidth), y=int(500*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC17'].place(x=int(360*ratioWidth), y=int(580*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC18'].place(x=int(360*ratioWidth), y=int(660*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC19'].place(x=int(360*ratioWidth), y=int(740*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))
        self.SL_PC_Dict['SL4_PC20'].place(x=int(360*ratioWidth), y=int(820*ratioHeight), width=int(70*ratioWidth), height=int(70*ratioHeight))

        self.SL_PCs_USBPlacing['SL4_PC1'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC2'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC3'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC4'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC5'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC6'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC7'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC8'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC9'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC10'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC11'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC12'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC13'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC14'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC15'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC16'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC17'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC18'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC19'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)
        self.SL_PCs_USBPlacing['SL4_PC20'] = Button(SL4_Frame, text="U", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID)

        self.SL_PCs_BrowserPlacing['SL4_PC1'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC1', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC2'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC2', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC3'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC3', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC4'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC4', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC5'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC5', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC6'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC6', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC7'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC7', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC8'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC8', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC9'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC9', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC10'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC10', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC11'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC11', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC12'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC12', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC13'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC13', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC14'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC14', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC15'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC15', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC16'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC16', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC17'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC17', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC18'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC18', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC19'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC19', "SL4"))
        self.SL_PCs_BrowserPlacing['SL4_PC20'] = Button(SL4_Frame, text="B", bd=1, font=f"times {int(10*ratioHeight)} bold", relief=SOLID, command=lambda: self.CloseBrowser('SL4_PC20', "SL4"))

        self.SL_PCs_BrowserPlaceAttributes['SL4_PC1'] = [int(40*ratioWidth-25), int(105*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC2'] = [int(40*ratioWidth-25), int(185*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC3'] = [int(40*ratioWidth-25), int(265*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC4'] = [int(40*ratioWidth-25), int(345*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC5'] = [int(40*ratioWidth-25), int(425*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC6'] = [int(40*ratioWidth-25), int(505*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC7'] = [int(40*ratioWidth-25), int(585*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC8'] = [int(40*ratioWidth-25), int(665*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC9'] = [int(40*ratioWidth-25), int(745*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC10'] = [int(40*ratioWidth-25), int(825*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC11'] = [int(435*ratioWidth), int(105*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC12'] = [int(435*ratioWidth), int(185*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC13'] = [int(435*ratioWidth), int(265*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC14'] = [int(435*ratioWidth), int(345*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC15'] = [int(435*ratioWidth), int(425*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC16'] = [int(435*ratioWidth), int(505*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC17'] = [int(435*ratioWidth), int(585*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC18'] = [int(435*ratioWidth), int(665*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC19'] = [int(435*ratioWidth), int(745*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_BrowserPlaceAttributes['SL4_PC20'] = [int(435*ratioWidth), int(825*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]


        self.SL_PCs_USBPlaceAttributes['SL4_PC1'] = [int(40*ratioWidth-25), int(140*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC2'] = [int(40*ratioWidth-25), int(220*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC3'] = [int(40*ratioWidth-25), int(300*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC4'] = [int(40*ratioWidth-25), int(380*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC5'] = [int(40*ratioWidth-25), int(460*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC6'] = [int(40*ratioWidth-25), int(540*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC7'] = [int(40*ratioWidth-25), int(620*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC8'] = [int(40*ratioWidth-25), int(700*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC9'] = [int(40*ratioWidth-25), int(780*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC10'] = [int(40*ratioWidth-25), int(860*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC11'] = [int(435*ratioWidth), int(140*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC12'] = [int(435*ratioWidth), int(220*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC13'] = [int(435*ratioWidth), int(300*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC14'] = [int(435*ratioWidth), int(380*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC15'] = [int(435*ratioWidth), int(460*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC16'] = [int(435*ratioWidth), int(540*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC17'] = [int(435*ratioWidth), int(620*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC18'] = [int(435*ratioWidth), int(700*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC19'] = [int(435*ratioWidth), int(780*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]
        self.SL_PCs_USBPlaceAttributes['SL4_PC20'] = [int(435*ratioWidth), int(860*ratioHeight), int(20*ratioWidth), int(25*ratioHeight)]

        self.ShutdownAllPCs = Button(SL4_Frame, text="Shutdown All PCs", bd=3, font=f"times {int(18*ratioHeight)} bold", relief=RAISED, command=lambda: self.ShutdownAllPCsFunc(SL4_Frame, "SL4",ratioWidth, ratioHeight))
        self.ShutdownAllPCs.place(x=int(95*ratioWidth), y=int(905*ratioHeight), width=int(260*ratioWidth), height=int(50*ratioHeight))


    def exitButton_Pressed(self):
        self.root.destroy()

def main():
    root = Tk()
    LabManagement(root)
    root.overrideredirect(True)
    root.mainloop()

if __name__ == '__main__':
    main()