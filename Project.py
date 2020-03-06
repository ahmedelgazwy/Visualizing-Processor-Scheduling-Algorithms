from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt 



####################################
########_USEFUL_FUNCTIONS_##########
#################################### 
    
def ShowError(error):
  errorbox = Tk()
  errorbox.withdraw()
  messagebox.showinfo("Error", error)
  
def space(word,numofspaces):
   space = ""
   for i in range (0,numofspaces-len(word)):
     space = space + " "
   return space

def FCFS(Queue): #{('order' : 'name:burst')}
  
   order=1
   CurrentTime=0
   TimeList=list()
   for ProcessOrder in Queue: #ProcessOrder==keys of Queue
     
     ProcessName=Queue[str(order)].split(':')[0]
     BurstTime=Queue[str(order)].split(':')[1]
     
     StartTime=CurrentTime
     FinishTime=CurrentTime+int(BurstTime)
     
     TimeList.append(str(StartTime)+'-'+str(FinishTime)+":"+ProcessName)
     
     order=order+1
     CurrentTime=CurrentTime+int(BurstTime)

   return TimeList   #['Start-End:ProcessName','Start-End:ProcessName']
     
  
  

####################################أ
############_Receipt_###############
#################################### 
def MakeFcfsUI():
    DestroyAll()
    global label1,entry1,ButtonAddToQueue, label2,entry2,ButtonMakeSchedule,QueueContents,label3,entry3
    label1= Label(GUI,text="Enter Process Name: ",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label1.place(x=10,y=120)
    
    entry1=Entry(GUI , font=("Times", 16),width=15)
    entry1.place(x=20,y=160)
    #######################################
    
    label2= Label(GUI,text="Enter Process Order: : ",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label2.place(x=250,y=120)
  
    entry2=Entry(GUI , font=("Times", 16),width=15)
    entry2.place(x=270,y=160)
    #######################################

    #######################################
    
    label3= Label(GUI,text="Enter Burst Time: : ",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label3.place(x=490,y=120)
  
    entry3=Entry(GUI , font=("Times", 16),width=15)
    entry3.place(x=510,y=160)

    
     
    #######################################
    ButtonAddToQueue = Button(GUI, text ="Add Process",font=("Arial", 14),command = lambda : AddToQueueUI(entry1.get(),entry2.get(),entry3.get()))
    ButtonAddToQueue.configure(height=1,width=15)
    ButtonAddToQueue.place(x=270,y=200)
    #######################################
    


    ######################################
    ButtonMakeSchedule = Button(GUI, text ="Draw Schedule",font=("Arial", 20),command = lambda : MakeFCFS_UI())
    ButtonMakeSchedule.configure(height=1,width=20)
    ButtonMakeSchedule.place(x=200,y=250)
    #####################################
    QueueContents = Text(GUI, height=20, width=30)
    QueueContents.insert(END,"Process        "+"Order    "+"Burst\n" )
    QueueContents.insert(END,"------------------------------\n" )



def AddToQueueUI(MedName,Quantity,BurstTime): # make initial look of receipt contents
  entry1.delete(0, 'end')
  entry2.delete(0, 'end')
  entry3.delete(0, 'end')
  

  QueueContents.place(x=900,y=120)
  
  QueueContents.insert(END, MedName+space(MedName,17)+Quantity+space(Quantity,7)+BurstTime+"\n")


def MakeFCFS_UI():
  QueueList=QueueContents.get("3.0",END).split("\n")[:-2]
  QueueDict=dict()

  for process in QueueList: #construct Dictionary of queue
    temp=process.split()
    QueueDict[temp[1]]=temp[0]+":"+temp[2] #{('order' : 'name:burst')}
    
    
  TimeLine=FCFS(QueueDict) #list of processes ['Start-End:ProcessName','Start-End:ProcessName']
  



  fig, gnt = plt.subplots(figsize=(8,4))
  
# Setting Y-axis limits 
  gnt.set_ylim(0, 1) 
   
# Setting X-axis limits 
  gnt.set_xlabel('seconds')   
# Setting ticks on y-axis 
  gnt.set_yticks([0.5]) 
# Labelling tickes of y-axis 
  gnt.set_yticklabels([''])
  gnt.grid(True) 

  MaxTime=int(TimeLine[-1].split(":")[0].split('-')[1]) #ending time of last process 
  #gnt.set_xlim(0, MaxTime)

  terminators=list()
  for process in TimeLine:
    terminators.append(int(process.split('-')[0]))

  terminators.append(MaxTime)  
  gnt.set_xticks(terminators)

  PreviousEnd=0
  for process in TimeLine:
    ProcessStart=int(process.split('-')[0])
    ProcessEnd=int(process.split(":")[0].split('-')[1])
    processname=process.split(':')[1]
    gnt.text(PreviousEnd+(ProcessEnd-ProcessStart)/2,0.5 ,processname, fontsize=10)
    PreviousEnd=ProcessEnd
    
  
  gnt.broken_barh([(0,MaxTime)], (0.25, 0.5),facecolors =('tab:blue'))

  
  
  #gnt.text(0.5,0.5 ,"sssss", fontsize=12)

  plt.show()
  plt.savefig("gantt1.png")




 


####################################
####################################




def main():
 try:
   AdminGui.destroy()
 except:
   try:
     LoginScreen.destroy()
   except:
     pass
  
  
 global GUI
 GUI = Tk()
 GUI.title("Process Scheduler")
 GUI.configure(bg='#d2d2d2')
 GUI.minsize(600,650)
 GUI.resizable(0,0)

  
# LoginScreen.destroy()

 try:
   global PaymentType
   PaymentType = IntVar() ###############
   global OrderType
   OrderType = IntVar()
 except:
   pass


 
 labelbanner= Label(GUI,text="Process Scheduler",font=("Arial",30),bg='lightblue',relief="ridge",fg="White")
 labelbanner.grid(columnspan=4,padx=500,sticky='ew')

 B0 = Button(GUI, text ="FCFS",font=("Arial", 15),command = lambda : MakeFcfsUI())
 B0.configure(height=2,width=16)
 B0.grid(row=1,column=0)

 B1 = Button(GUI, text ="SJF",font=("Arial", 15), command =lambda :  MakeFcfsUI())
 B1.configure(height=2,width=17)
 B1.grid(row=1,column=1)

 B2 = Button(GUI, text ="Round Robin",font=("Arial", 15), command =lambda :  MakeFcfsUI())
 B2.configure(height=2,width=16)
 B2.grid(row=1,column=2)

 B3 = Button(GUI, text ="Prirority",font=("Arial", 15), command=lambda: ProfitButtons())
 B3.configure(height=2,width=16)
 B3.grid(row=1,column=3)



 
 GUI.mainloop()
 
 




####################################
####################################
####################################







def DestroyAll(): # make sure that area we use is clear before placing objects

  try:  
        label1.destroy() #receipt
        entry1.destroy()
        ButtonAddToQueue.destroy()
        label2.destroy()
        entry2.destroy()
        ButtonMakeSchedule.destroy()
        buttoncash.destroy()
        buttonvisa.destroy()
        labelPaymentType.destroy()
        QueueContents.destroy()
        labelOrderType.destroy()
        buttonstore.destroy()
        buttondelivery.destroy()
        labelClientID.destroy()
        entryClientID.destroy()
        labelAddress.destroy()
        EntryAddress.destroy()

  except:
         pass

  
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom
        

   

  
try:  
 main()
except:
  ShowError("Unexpected Error Happened")



