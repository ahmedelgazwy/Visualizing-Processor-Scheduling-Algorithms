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
  
def DrawGantt(TimeLine):
  fig, gnt = plt.subplots(figsize=(8,4))
  
# Setting Y-axis limits 
  gnt.set_ylim(0, 1) 
   
# Setting X-axis limits 
  gnt.set_xlabel('Time',fontsize=16)   
# Setting ticks on y-axis 
  gnt.set_yticks([0.5]) 
# Labelling tickes of y-axis 
  gnt.set_yticklabels([''])
  gnt.grid(True) 

  MaxTime=float(TimeLine[-1].split(":")[0].split('-')[1]) #ending time of last process 
  #gnt.set_xlim(0, MaxTime)

  terminators=list()
  for process in TimeLine:
    terminators.append(float(process.split('-')[0]))
    terminators.append(float(process.split(":")[0].split('-')[1]))

  terminators.append(MaxTime)  
  gnt.set_xticks(terminators)

  
  for process in TimeLine:
    ProcessStart=float(process.split('-')[0])
    ProcessEnd=float(process.split(":")[0].split('-')[1])
    processname=process.split(':')[1]

    size=(25/len(processname))
    gnt.text(ProcessStart+(ProcessEnd-ProcessStart)/(2+size/50),0.5 ,processname, fontsize=size)

    ProcessDuration=ProcessEnd-ProcessStart
    gnt.broken_barh([(ProcessStart,ProcessDuration)], (0.25, 0.5),facecolor ='#add8e6')
    
  
  #gnt.text(0.5,0.5 ,"sssss", fontsize=12)
  plt.savefig("gantt1.png")

  plt.show()
  
  #img = PhotoImage(file="gantt1.png").zoom(2).subsample(3)
  '''label=Label(image=img)
  label.image=img
  label.place(x=300,y=320 )'''

  
####################################
###############_FCFS_###############
#################################### 
def FCFS(Queue): #{('order' : 'name:burst')}
  
   order=sorted(Queue.keys())
   CurrentTime=float(order[0])
   TimeList=list()
   for ProcessOrder in order: #ProcessOrder==keys of Queue
     
     ProcessName=Queue[str(ProcessOrder)].split(':')[0]
     BurstTime=Queue[str(ProcessOrder)].split(':')[1]
     
     StartTime=CurrentTime
     FinishTime=CurrentTime+float(BurstTime)

     if (float(ProcessOrder)>(CurrentTime)):
       StartTime=float(ProcessOrder)
       FinishTime=StartTime+float(BurstTime)

       
     TimeList.append(str(StartTime)+'-'+str(FinishTime)+":"+ProcessName)
     
     CurrentTime=CurrentTime+float(BurstTime)

   return TimeList   #['Start-End:ProcessName','Start-End:ProcessName']
     
####################################أ
#################################### 
def MakeFcfsUI():
    DestroyAll()
    global label1,entry1,ButtonAddToQueue, label2,entry2,ButtonMakeSchedule,QueueContents,label3,entry3
    label1= Label(GUI,text="Enter Process Name: ",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label1.place(x=10,y=120)
    
    entry1=Entry(GUI , font=("Times", 16),width=15)
    entry1.place(x=20,y=160)
    #######################################
    
    label2= Label(GUI,text="Enter Arrival Time:  ",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label2.place(x=250,y=120)
  
    entry2=Entry(GUI , font=("Times", 16),width=15)
    entry2.place(x=270,y=160)
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

    ButtonMakeSchedule = Button(GUI, text ="Draw Schedule",font=("Arial", 20),command = lambda : MakeFCFS())
    ButtonMakeSchedule.configure(height=1,width=20)
    ButtonMakeSchedule.place(x=200,y=250)
    #####################################
    QueueContents = Text(GUI, height=20, width=35)
    QueueContents.insert(END,"Process      "+"Arrival Time    "+"Burst\n" )
    QueueContents.insert(END,"-----------------------------------\n" )



def AddToQueueUI(ProcessName,Arrival,BurstTime): # make initial look of queue contents (name:arrival:burst)
  entry1.delete(0, 'end')
  entry2.delete(0, 'end')
  entry3.delete(0, 'end')
  

  QueueContents.place(x=900,y=120)
  
  QueueContents.insert(END, ProcessName+space(ProcessName,18)+Arrival+space(Arrival,12)+BurstTime+"\n")



def MakeFCFS():
  QueueList=QueueContents.get("3.0",END).split("\n")[:-2]
  QueueDict=dict()

  for process in QueueList: #construct Dictionary of queue
    temp=process.split()
    QueueDict[temp[1]]=temp[0]+":"+temp[2] #{('order' : 'name:burst')}
    
    
  timeline=FCFS(QueueDict) #list of processes ['Start-End:ProcessName','Start-End:ProcessName']
  DrawGantt(timeline)




####################################أ
####################################
def round_robin(process_d,process_a,t_s):
    Burst = process_d #Burst
    Arrival =  process_a #Arrival
    readyqueue=[]
    ArrivalSorted=dict()

    for key, value in sorted(Arrival.items(), key=lambda item: item[1]):
      ArrivalSorted[key]=value


    graph = []
    flag=1

    curr_time=float(list(ArrivalSorted.values())[0])


    while flag == 1:
        flag=0

        for i in ArrivalSorted:
                  
         if(ArrivalSorted[i]!="done"):
            if (ArrivalSorted[i]<=curr_time) and (i not in readyqueue):
               readyqueue.append(i)

               
            if(ArrivalSorted[i]>curr_time) and (len(readyqueue)==0) and (curr_time>0) : # for gap
               curr_time=float(ArrivalSorted[i])
               readyqueue.append(i)

           
         if(i in readyqueue):
            if (Burst[i] >= t_s ):
 
                graph.append(str(curr_time) + '-' + str(t_s+curr_time)+':'+str(i))
                Burst[i] = Burst[i]-t_s
                curr_time = curr_time+t_s
 
 
            elif (Burst[i] < t_s) and (Burst[i] > 0):
                graph.append(str(curr_time) + '-' + str(Burst[i]+curr_time)+':'+str(i))
                curr_time=curr_time+Burst[i]
                Burst[i] = 0
                
            if (Burst[i]==0):
                ArrivalSorted[i]="done"
                readyqueue.remove(i)
 
        for i in Burst:
            if Burst[i] != 0:
                flag =1
                break
    return graph
  
def MakeRRUI():
    DestroyAll()
    global label1,entry1,ButtonAddToQueue, label2,entry2,ButtonMakeSchedule,QueueContents,label3,entry3,label4,entry4
    label1= Label(GUI,text="Enter Process Name:",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label1.place(x=10,y=200)
    
    entry1=Entry(GUI , font=("Times", 16),width=15)
    entry1.place(x=30,y=240)
    #######################################
    
    label2= Label(GUI,text="Enter Arrival Time:",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label2.place(x=250,y=200)
  
    entry2=Entry(GUI , font=("Times", 16),width=15)
    entry2.place(x=270,y=240)
    ######################################

    label3= Label(GUI,text="Enter Burst Time:",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label3.place(x=490,y=200)
  
    entry3=Entry(GUI , font=("Times", 16),width=15)
    entry3.place(x=510,y=240)
     
    #######################################
    
    label4= Label(GUI,text="Enter Time Quantum:",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label4.place(x=250,y=120)
  
    entry4=Entry(GUI , font=("Times", 16),width=15)
    entry4.place(x=270,y=160)
    ########################################
    
    ButtonAddToQueue = Button(GUI, text ="Add Process",font=("Arial", 14),command = lambda : AddToQueueUI(entry1.get(),entry2.get(),entry3.get()))
    ButtonAddToQueue.configure(height=1,width=15)
    ButtonAddToQueue.place(x=270,y=280)    

    ######################################
    ButtonMakeSchedule = Button(GUI, text ="Draw Schedule",font=("Arial", 20),command = lambda : MakeRR())
    ButtonMakeSchedule.configure(height=1,width=20)
    ButtonMakeSchedule.place(x=200,y=330)
    #####################################
    QueueContents = Text(GUI, height=20, width=35)
    QueueContents.insert(END,"Process      "+"Arrival Time    "+"Burst\n" )
    QueueContents.insert(END,"-----------------------------------\n" )


####################################

def MakeRR():
  QueueList=QueueContents.get("3.0",END).split("\n")[:-2]
  Process_Arrival=dict()
  Process_Burst=dict()
  

  for process in QueueList: #construct Dictionary of queue
    temp=process.split()
    Process_Arrival[temp[0]]=float(temp[1]) #{('name' : 'Arrival')}
    Process_Burst[temp[0]]=float(temp[2])
    
    
  TimeQuantum=float(entry4.get())
  
  timeline=round_robin(Process_Burst,Process_Arrival,TimeQuantum) #timeline=list of processes ['Start-End:ProcessName','Start-End:ProcessName']
  
  DrawGantt(timeline)

  

####################################
##############_SJF_#################
####################################
def MakeSJFUI():
    DestroyAll()
    global ButtonNonPreem,ButtonPreem

    ButtonNonPreem = Button(GUI, text ="Non Preemptive",font=("Arial", 14),command = lambda : SJFnonUI())
    ButtonNonPreem.configure(height=1,width=15)
    ButtonNonPreem.place(x=300,y=120)

    ButtonPreem = Button(GUI, text ="Preemptive",font=("Arial", 14),command = lambda : AddToQueueUI_RR(entry1.get(),entry2.get()))
    ButtonPreem.configure(height=1,width=15)
    ButtonPreem.place(x=500,y=120)

    
######################################
######################################
def SJFnonUI():
    DestroyAll()
    global label1,entry1,ButtonAddToQueue, label2,entry2,ButtonMakeSchedule,QueueContents,label3,entry3
    global ButtonNonPreem,ButtonPreem
    
    ButtonNonPreem = Button(GUI, text ="Non Preemptive",font=("Arial", 14),command = lambda : SJFnonUI())
    ButtonNonPreem.configure(height=1,width=15)
    ButtonNonPreem.place(x=300,y=120)

    ButtonPreem = Button(GUI, text ="Preemptive",font=("Arial", 14),command = lambda : AddToQueueUI_RR(entry1.get(),entry2.get()))
    ButtonPreem.configure(height=1,width=15)
    ButtonPreem.place(x=500,y=120)

    #######################################
    label1= Label(GUI,text="Enter Process Name:",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label1.place(x=10,y=200)
    
    entry1=Entry(GUI , font=("Times", 16),width=15)
    entry1.place(x=30,y=240)
    #######################################
    
    label2= Label(GUI,text="Enter Arrival Time:",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label2.place(x=250,y=200)
  
    entry2=Entry(GUI , font=("Times", 16),width=15)
    entry2.place(x=270,y=240)
    ######################################

    label3= Label(GUI,text="Enter Burst Time:",bg="LightBlue",fg="white",font=("Times", 16),width=17,relief="ridge")
    label3.place(x=490,y=200)
  
    entry3=Entry(GUI , font=("Times", 16),width=15)
    entry3.place(x=510,y=240)
     
    #######################################
    
    
    ButtonAddToQueue = Button(GUI, text ="Add Process",font=("Arial", 14),command = lambda : AddToQueueUI(entry1.get(),entry2.get(),entry3.get()))
    ButtonAddToQueue.configure(height=1,width=15)
    ButtonAddToQueue.place(x=270,y=280)    

    ######################################
    ButtonMakeSchedule = Button(GUI, text ="Draw Schedule",font=("Arial", 20),command = lambda : MakeSJF_non())
    ButtonMakeSchedule.configure(height=1,width=20)
    ButtonMakeSchedule.place(x=200,y=330)
    #####################################
    QueueContents = Text(GUI, height=20, width=35)
    QueueContents.insert(END,"Process      "+"Arrival Time    "+"Burst\n" )
    QueueContents.insert(END,"-----------------------------------\n" )

       
######################################
######################################
def sjf_non_prem(process_d,process_a):
 
    Burst = process_d
    Arrival=process_a
    readyqueue=[]
    graph = []
    
    ArrivalSorted=dict()
    BurstSorted=dict()    

    for key, value in sorted(Arrival.items(), key=lambda item: item[1]):
      ArrivalSorted[key]=float(value)

    for key, value in sorted(Burst.items(), key=lambda item: item[1]):
      BurstSorted[key]=float(value) 

       
    curr_time = float(list(ArrivalSorted.values())[0])

    flag=1
    while flag == 1:
     flag=0
     
     for i in BurstSorted:
                
         if (ArrivalSorted[i]!="done"):
            if (ArrivalSorted[i]<=curr_time) and (i not in readyqueue):
               readyqueue.append(i)
               
            if (ArrivalSorted[i]>curr_time) and (len(readyqueue)==0) and (curr_time>0) : # for gap
               curr_time=float(ArrivalSorted[i])
               readyqueue.append(i)     
                
         if (i in readyqueue):
                graph.append(str(curr_time)+'-'+str(curr_time+BurstSorted[i])+':'+str(i))
                ArrivalSorted[i]="done"
                readyqueue.remove(i)
                curr_time=curr_time+BurstSorted[i]
                
         for i in ArrivalSorted:
            if ArrivalSorted[i] != "done":
                flag =1
                break
    return graph
  
######################################
######################################
def MakeSJF_non():
  QueueList=QueueContents.get("3.0",END).split("\n")[:-2]
  Process_Arrival=dict()
  Process_Burst=dict()
  
  for process in QueueList: #construct Dictionary of queue
    temp=process.split()
    Process_Arrival[temp[0]]=float(temp[1]) #{('name' : 'Arrival')}
    Process_Burst[temp[0]]=float(temp[2])
    
  
  timeline=sjf_non_prem(Process_Burst,Process_Arrival) #timeline=list of processes ['Start-End:ProcessName','Start-End:ProcessName']
  DrawGantt(timeline)



######################################
######################################
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

 B1 = Button(GUI, text ="SJF",font=("Arial", 15), command =lambda :  MakeSJFUI())
 B1.configure(height=2,width=17)
 B1.grid(row=1,column=1)

 B2 = Button(GUI, text ="Round Robin",font=("Arial", 15), command =lambda :  MakeRRUI())
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
        QueueContents.destroy()
        label3.destroy()
        entry3.destroy()
        label4.destroy()
        entry4.destroy()
  except:
         pass
  try:  
     ButtonNonPreem.destroy()
     ButtonPreem.destroy()
     
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


'''receipt=Receipt()
receipt.AddItem("mon",12,14)
receipt.AddItem("ahmed",10,20)
receipt.AddItem("_",3,2)
receipt.printrec()
receipt.CalcSum()

for key,value in Receipt.items.items():
    print (key[0])'''
        
