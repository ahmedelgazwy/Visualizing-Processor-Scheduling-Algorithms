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


#####################################
def buttonselected(button, buttons):
    global selectedbutton
    selectedbutton = button
    for i in buttons:
        if (i == button):
            i.configure(bg="lightblue")
        else:
            i.configure(bg='SystemButtonFace')


#####################################
def space(word, numofspaces):
    space = ""
    for i in range(0, numofspaces - len(word)):
        space = space + " "
    return space


#####################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


#####################################
def min_a(arr, num):
    try:
        minx = arr[0]
        index = 0
        for i in range(1, num):
            if arr[i] < minx:
                minx = arr[i]
                index = i
        return index
    except:
        pass


#####################################
def DrawGantt(TimeLine):
    fig, gnt = plt.subplots(figsize=(12, 4), dpi=120)

    # Setting Y-axis limits
    gnt.set_ylim(0, 1)

    # Setting X-axis limits
    gnt.set_xlabel('Time', fontsize=16)
    # Setting ticks on y-axis
    gnt.set_yticks([0.5])
    # Labelling tickes of y-axis
    gnt.set_yticklabels([''])
    gnt.grid(True)

    MaxTime = float(TimeLine[-1].split(":")[0].split('-')[1])  # ending time of last process
    # gnt.set_xlim(0, MaxTime)

    terminators = list()
    for process in TimeLine:
        terminators.append(float(process.split('-')[0]))
        terminators.append(float(process.split(":")[0].split('-')[1]))

    terminators.append(MaxTime)
    gnt.set_xticks(terminators)

    for process in TimeLine:
        ProcessStart = float(process.split('-')[0])
        ProcessEnd = float(process.split(":")[0].split('-')[1])
        processname = process.split(':')[1]

        size = (20 / len(processname))
        gnt.text(ProcessStart + (ProcessEnd - ProcessStart) / (2 + size / 50), 0.5, processname, fontsize=size)

        ProcessDuration = ProcessEnd - ProcessStart
        gnt.broken_barh([(ProcessStart, ProcessDuration)], (0.25, 0.5), facecolor='#add8e6')

    # gnt.text(0.5,0.5 ,"sssss", fontsize=12)
    plt.savefig("gantt.png")

    # plt.show()
    GanttImage = PhotoImage(file="gantt.png").zoom(2).subsample(3)
    global labelimg
    try:
        labelimg.destroy()
    except:
        pass
    labelimg = Label(image=GanttImage)
    labelimg.image = GanttImage
    labelimg.place(x=250, y=470)


#####################################
def AvgWaitingTime(Arrival, Timeline):
    waiting = dict()
    NumOfProcess = 0
    for process in Arrival:  # {('name' : Arrival)}
        ProcessWaiting = 0
        FirstTime = 1
        for i in Timeline:  # ['Start-End:ProcessName','Start-End:ProcessName']
            ProcessName = i.split(':')[1]
            if (ProcessName == process):
                ProcessStart = float(i.split('-')[0])
                if (FirstTime == 1):
                    ProcessEnd = float(Arrival[process])
                    FirstTime = 0

                ProcessWaiting += ProcessStart - ProcessEnd
                ProcessEnd = float(i.split('-')[1].split(':')[
                                       0])  # time of previous end for next process burst to make CurrentStart-PreviousEnd

        waiting[process] = ProcessWaiting
        NumOfProcess += 1

    Sum = 0
    for process in waiting:
        Sum = Sum + waiting[process]

    AvgWaiting = float(Sum) / float(NumOfProcess)

    return float("{:.2f}".format(AvgWaiting))


#####################################
def ShowWaitingTime(AvgWaiting):
    global label6
    try:
        label6.destroy()
    except:
        pass
    label6 = Label(GUI, text="Average Waiting: \n" + str(AvgWaiting), bg='#d2d2d2', fg="red", font=("Times", 16),
                   width=15, relief="ridge")
    label6.place(x=10, y=610)


####################################
#############_FCFS_#################
####################################
def FCFS(Queue):  # {('order' : 'name:burst')}

    print(Queue.keys())
    order = sorted(Queue.keys())
    print(order)
    CurrentTime = float(order[0])
    TimeList = list()
    for ProcessOrder in order:  # ProcessOrder==keys of Queue

        ProcessName = Queue[str(ProcessOrder)].split(':')[0]
        BurstTime = Queue[str(ProcessOrder)].split(':')[1]

        StartTime = CurrentTime
        FinishTime = CurrentTime + float(BurstTime)

        if (float(ProcessOrder) > (CurrentTime)):
            StartTime = float(ProcessOrder)
            FinishTime = StartTime + float(BurstTime)

        TimeList.append(str(StartTime) + '-' + str(FinishTime) + ":" + ProcessName)

        CurrentTime = CurrentTime + float(BurstTime)

    return TimeList  # ['Start-End:ProcessName','Start-End:ProcessName']


####################################
def MakeFcfsUI():
    DestroyAll()
    global label1, entry1, ButtonAddToQueue, label2, entry2, ButtonMakeSchedule, QueueContents, label3, entry3

    buttons = [B0, B1, B2, B3]
    buttonselected(B0, buttons)

    label1 = Label(GUI, text="Enter Process Name:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label1.place(x=10, y=200)

    entry1 = Entry(GUI, font=("Times", 16), width=15)
    entry1.place(x=30, y=240)
    #######################################

    label2 = Label(GUI, text="Enter Arrival Time:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label2.place(x=250, y=200)

    entry2 = Entry(GUI, font=("Times", 16), width=15)
    entry2.place(x=270, y=240)
    ######################################

    label3 = Label(GUI, text="Enter Burst Time:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label3.place(x=490, y=200)

    entry3 = Entry(GUI, font=("Times", 16), width=15)
    entry3.place(x=510, y=240)

    #######################################

    ButtonAddToQueue = Button(GUI, text="Add Process", font=("Arial", 14),
                              command=lambda: AddToQueueUI(entry1.get(), entry2.get(), entry3.get()))
    ButtonAddToQueue.configure(height=1, width=15)
    ButtonAddToQueue.place(x=270, y=280)

    ######################################
    ButtonMakeSchedule = Button(GUI, text="Draw Schedule", font=("Arial", 20), command=lambda: MakeFCFS(),
                                bg="lightblue")
    ButtonMakeSchedule.configure(height=1, width=18)
    ButtonMakeSchedule.place(x=205, y=330)
    #####################################
    QueueContents = Text(GUI, height=20, width=35)
    QueueContents.insert(END, "Process      " + "Arrival Time    " + "Burst\n")
    QueueContents.insert(END, "-----------------------------------\n")


#############################################
def AddToQueueUI(ProcessName, Arrival, BurstTime):  # make initial look of queue contents (name:arrival:burst)
    error = 0
    if (ProcessName == '' or Arrival == '' or BurstTime == ''):
        ShowError("Please Fill All Fields!")
        error = 1

    if (is_number(Arrival) == 0 and Arrival != ''):
        ShowError("Arrival Must Be Numeric!")
        error = 1

    if (is_number(BurstTime) == 0 and BurstTime != ''):
        ShowError("Burst Must Be Numeric!")
        error = 1

    if (error == 0):
        QueueContents.place(x=900, y=120)
        QueueContents.insert(END,
                             ProcessName + space(ProcessName, 18) + Arrival + space(Arrival, 12) + BurstTime + "\n")
        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
        entry3.delete(0, 'end')


#############################################

def MakeFCFS():
    QueueList = QueueContents.get("3.0", END).split("\n")[:-2]
    QueueDict = dict()
    Process_Arrival = dict()

    for process in QueueList:  # construct Dictionary of queue
        temp = process.split()
        QueueDict[temp[1]] = temp[0] + ":" + temp[2]  # {('order' : 'name:burst')}
        Process_Arrival[temp[0]] = float(temp[1])  # {('name' : Arrival)}

    timeline = FCFS(QueueDict)  # list of processes ['Start-End:ProcessName','Start-End:ProcessName']

    AvgWaiting = AvgWaitingTime(Process_Arrival, timeline)
    ShowWaitingTime(AvgWaiting)
    DrawGantt(timeline)


####################################أ
####################################
def round_robin(process_d, process_a, t_s):
    Burst = process_d.copy()  # Burst
    Arrival = process_a.copy()  # Arrival
    readyqueue = []
    ArrivalSorted = dict()

    for key, value in sorted(Arrival.items(), key=lambda item: item[1]):
        ArrivalSorted[key] = value

    graph = []
    flag = 1

    curr_time = float(list(ArrivalSorted.values())[0])

    while flag == 1:
        flag = 0

        if (len(readyqueue) == 0) and (curr_time > 0):  # for gap, make current_time= closest arrival time of process,so in next while iteration we can append to readyqueue
            for i in ArrivalSorted:
                if (ArrivalSorted[i] != "done"):
                    curr_time = float(ArrivalSorted[i])

        for i in ArrivalSorted:

            for x in Burst:
                if Burst[x] != 0:
                    flag = 1
                    break
            for z in ArrivalSorted:
                if (ArrivalSorted[z] != "done"):
                    if (ArrivalSorted[z] <= curr_time) and (z not in readyqueue):
                        readyqueue.append(z)

            if (i in readyqueue):
                if (Burst[i] >= t_s):
                    graph.append(str(curr_time) + '-' + str(t_s + curr_time) + ':' + str(i))
                    Burst[i] = Burst[i] - t_s
                    curr_time = curr_time + t_s
                    if (Burst[i] == 0):
                        ArrivalSorted[i] = "done"
                        readyqueue.remove(i)

                elif (Burst[i] < t_s) and (Burst[i] > 0):
                    graph.append(str(curr_time) + '-' + str(Burst[i] + curr_time) + ':' + str(i))
                    curr_time = curr_time + Burst[i]
                    Burst[i] = 0
                    if (Burst[i] == 0):
                        ArrivalSorted[i] = "done"
                        readyqueue.remove(i)


    return graph


########################################
def MakeRRUI():
    DestroyAll()
    global label1, entry1, ButtonAddToQueue, label2, entry2, ButtonMakeSchedule, QueueContents, label3, entry3, label4, entry4

    buttons = [B0, B1, B2, B3]
    buttonselected(B2, buttons)

    label1 = Label(GUI, text="Enter Process Name:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label1.place(x=10, y=200)

    entry1 = Entry(GUI, font=("Times", 16), width=15)
    entry1.place(x=30, y=240)
    #######################################

    label2 = Label(GUI, text="Enter Arrival Time:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label2.place(x=250, y=200)

    entry2 = Entry(GUI, font=("Times", 16), width=15)
    entry2.place(x=270, y=240)
    ######################################

    label3 = Label(GUI, text="Enter Burst Time:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label3.place(x=490, y=200)

    entry3 = Entry(GUI, font=("Times", 16), width=15)
    entry3.place(x=510, y=240)

    #######################################

    label4 = Label(GUI, text="Enter Time Quantum:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label4.place(x=250, y=120)

    entry4 = Entry(GUI, font=("Times", 16), width=15)
    entry4.place(x=270, y=160)
    ########################################

    ButtonAddToQueue = Button(GUI, text="Add Process", font=("Arial", 14),
                              command=lambda: AddToQueueUI(entry1.get(), entry2.get(), entry3.get()))
    ButtonAddToQueue.configure(height=1, width=15)
    ButtonAddToQueue.place(x=270, y=280)

    ######################################
    ButtonMakeSchedule = Button(GUI, text="Draw Schedule", font=("Arial", 20), command=lambda: MakeRR(), bg="lightblue")
    ButtonMakeSchedule.configure(height=1, width=18)
    ButtonMakeSchedule.place(x=205, y=330)
    #####################################
    QueueContents = Text(GUI, height=20, width=35)
    QueueContents.insert(END, "Process      " + "Arrival Time    " + "Burst\n")
    QueueContents.insert(END, "-----------------------------------\n")


####################################

def MakeRR():
    QueueList = QueueContents.get("3.0", END).split("\n")[:-2]
    Process_Arrival = dict()
    Process_Burst = dict()

    for process in QueueList:  # construct Dictionary of queue
        temp = process.split()
        Process_Arrival[temp[0]] = float(temp[1])  # {('name' : 'Arrival')}
        Process_Burst[temp[0]] = float(temp[2])

    TimeQuantum = float(entry4.get())

    timeline = round_robin(Process_Burst, Process_Arrival, TimeQuantum)  # timeline=list of processes

    AvgWaiting = AvgWaitingTime(Process_Arrival, timeline)
    ShowWaitingTime(AvgWaiting)

    DrawGantt(timeline)


####################################
##############_SJF_#################
####################################
def MakeSJFUI():
    DestroyAll()
    global label1, entry1, ButtonAddToQueue, label2, entry2, ButtonMakeSchedule, QueueContents, label3, entry3, buttonPreem, buttonNonPreem
    global ButtonNonPreem, ButtonPreem
    global Type
    Type = IntVar()  ###############

    buttons = [B0, B1, B2, B3]
    buttonselected(B1, buttons)

    buttonNonPreem = Radiobutton(GUI, text="Non Preemptive", variable=Type, value=1, bg="#d2d2d2", font=("Arial", 14))
    buttonNonPreem.place(x=300, y=120)
    buttonPreem = Radiobutton(GUI, text="Preemptive", variable=Type, value=2, bg="#d2d2d2", font=("Arial", 14))
    buttonPreem.place(x=500, y=120)

    #######################################
    label1 = Label(GUI, text="Enter Process Name:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label1.place(x=10, y=200)

    entry1 = Entry(GUI, font=("Times", 16), width=15)
    entry1.place(x=30, y=240)
    #######################################

    label2 = Label(GUI, text="Enter Arrival Time:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label2.place(x=250, y=200)

    entry2 = Entry(GUI, font=("Times", 16), width=15)
    entry2.place(x=270, y=240)
    ######################################

    label3 = Label(GUI, text="Enter Burst Time:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label3.place(x=490, y=200)

    entry3 = Entry(GUI, font=("Times", 16), width=15)
    entry3.place(x=510, y=240)

    #######################################

    ButtonAddToQueue = Button(GUI, text="Add Process", font=("Arial", 14),
                              command=lambda: AddToQueueUI(entry1.get(), entry2.get(), entry3.get()))
    ButtonAddToQueue.configure(height=1, width=15)
    ButtonAddToQueue.place(x=270, y=280)

    ######################################
    ButtonMakeSchedule = Button(GUI, text="Draw Schedule", font=("Arial", 20), command=lambda: MakeSJF(),
                                bg="lightblue")
    ButtonMakeSchedule.configure(height=1, width=18)
    ButtonMakeSchedule.place(x=205, y=330)
    #####################################
    QueueContents = Text(GUI, height=20, width=35)
    QueueContents.insert(END, "Process      " + "Arrival Time    " + "Burst\n")
    QueueContents.insert(END, "-----------------------------------\n")


######################################
######################################
def MakeSJF():
    QueueList = QueueContents.get("3.0", END).split("\n")[:-2]
    Process_Arrival = {}
    Process_Burst = dict()

    for process in QueueList:  # construct Dictionary of queue
        temp = process.split()
        Process_Arrival[temp[0]] = float(temp[1])  # {('name' : Arrival )}
        Process_Burst[temp[0]] = float(temp[2])  # {('name' : Burst )}

    error = 0
    if (Type.get() not in [1, 2]):
        ShowError("Please Select Preemption")
        error = 1
    if (error == 0):
        if (Type.get() == 1):
            timeline = sjf_non_prem(Process_Burst,
                                    Process_Arrival)  # timeline=list of processes ['Start-End:ProcessName','Start-End:ProcessName']
        if (Type.get() == 2):
            timeline = sjf_prem(Process_Burst, Process_Arrival)

        AvgWaiting = AvgWaitingTime(Process_Arrival, timeline)
        ShowWaitingTime(AvgWaiting)

        DrawGantt(timeline)


######################################
######################################
def sjf_non_prem(process_d, process_a):
    Burst = process_d.copy()
    Arrival = process_a.copy()
    readyqueue = []
    graph = []

    ArrivalSorted = dict()
    BurstSorted = dict()

    for key, value in sorted(Arrival.items(), key=lambda item: item[1]):
        ArrivalSorted[key] = float(value)

    for key, value in sorted(Burst.items(), key=lambda item: item[1]):
        BurstSorted[key] = float(value)

    curr_time = float(list(ArrivalSorted.values())[0])

    flag = 1
    print(BurstSorted)
    while flag == 1:
        flag = 0

        for i in BurstSorted:  # loop over all process and add to readyqueue the ready processes
            if (ArrivalSorted[i] != "done"):
                if (ArrivalSorted[i] <= curr_time) and (i not in readyqueue):
                    readyqueue.append(i)

        if (len(readyqueue) == 0) and (
                curr_time > 0):  # for gap, make current_time= closest arrival time of process,so in next while iteration we can append to readyqueue
            for i in ArrivalSorted:
                if (ArrivalSorted[i] != "done"):
                    curr_time = float(ArrivalSorted[i])

        for i in BurstSorted:  # loop over process sorted with burst times so we choose smallest burst that is also in readyqueue

            for x in ArrivalSorted:  # check if some still not done
                if ArrivalSorted[x] != "done":
                    flag = 1
                    break

            if (i in readyqueue and ArrivalSorted[i] != "done"):
                graph.append(str(curr_time) + '-' + str(curr_time + BurstSorted[i]) + ':' + str(i))
                ArrivalSorted[i] = "done"
                readyqueue.remove(i)
                curr_time = curr_time + BurstSorted[i]
                break

    return graph


######################################
#####################################
def sjf_prem(process_d, process_t):
    Burst = process_d.copy()
    Arrival = process_t.copy()
    val = []
    time = sorted(Arrival.values())
    key = []
    for i in time:
        for j in Arrival:
            if i == Arrival[j]:
                key.append(j)
                Arrival[j] = 'null'

    for i in key:
        for j in Burst:
            if i == j:
                val.append(Burst[j])
                Burst[j] = 'null'
    i = 0
    graph = []
    curr_time = time[0]

    while len(val) != 0:
        x = 0
        while 1:
            flag2 = 0
            for j in range(i + 1, len(time)):
              if(curr_time<=time[j]):
                if ((val[i] + curr_time - time[j] > val[j]) and ((val[i] + time[i]) > time[j])):
                    if time[i] > curr_time:
                        curr_time = time[i]

                    flag2 = 1

                    if time[j] != curr_time:
                        # print(1)
                        graph.append(str(curr_time) + '-' + str(time[j]) + ':' + key[i])

                    val[i] = val[i] + curr_time - time[j]
                    # print(val[i])
                    curr_time = time[j]

                    i = j
                    break

            if flag2 == 0:
                # print(curr_time,val[i])
                if time[i] > curr_time:  # gap
                    curr_time = time[i]
                print(curr_time, val[i])

                graph.append(str(curr_time) + '-' + str(curr_time + val[i]) + ':' + key[i])
                print(graph)
                # print(curr_time,val[i],i)
                curr_time = curr_time + val[i];
                val.remove(val[i])
                key.remove(key[i])
                time.remove(time[i])
                for i in time:
                    if i <= curr_time:
                        x = x + 1
                i = min_a(val, x)
                break

    # print(graph)
    return graph


####################################
###########_Priority_###############
####################################
def MakePrioUI():
    DestroyAll()
    global label1, entry1, ButtonAddToQueue, label2, entry2, ButtonMakeSchedule, QueueContents, label3, entry3, buttonPreem, buttonNonPreem, label4, entry4
    global ButtonNonPreem, ButtonPreem
    global Type
    Type = IntVar()  ###############

    buttons = [B0, B1, B2, B3]
    buttonselected(B3, buttons)

    buttonNonPreem = Radiobutton(GUI, text="Non Preemptive", variable=Type, value=1, bg="#d2d2d2", font=("Arial", 14))
    buttonNonPreem.place(x=300, y=120)
    buttonPreem = Radiobutton(GUI, text="Preemptive", variable=Type, value=2, bg="#d2d2d2", font=("Arial", 14))
    buttonPreem.place(x=500, y=120)

    #######################################
    label1 = Label(GUI, text="Enter Process Name:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label1.place(x=250, y=200)

    entry1 = Entry(GUI, font=("Times", 16), width=15)
    entry1.place(x=270, y=240)
    #######################################
    label2 = Label(GUI, text="Enter Burst Time:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label2.place(x=250, y=280)

    entry2 = Entry(GUI, font=("Times", 16), width=15)
    entry2.place(x=270, y=320)
    ######################################
    label3 = Label(GUI, text="Enter Arrival Time:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label3.place(x=490, y=200)

    entry3 = Entry(GUI, font=("Times", 16), width=15)
    entry3.place(x=510, y=240)

    #######################################
    label4 = Label(GUI, text="Enter Priority:", bg="LightBlue", fg="white", font=("Times", 16), width=17,
                   relief="ridge")
    label4.place(x=490, y=280)

    entry4 = Entry(GUI, font=("Times", 16), width=15)
    entry4.place(x=510, y=320)

    #######################################
    ButtonAddToQueue = Button(GUI, text="Add Process", font=("Arial", 14),
                              command=lambda: AddToQueueUI_Prio(entry1.get(), entry2.get(), entry3.get(), entry4.get()))
    ButtonAddToQueue.configure(height=1, width=15)
    ButtonAddToQueue.place(x=380, y=360)

    ######################################
    ButtonMakeSchedule = Button(GUI, text="Draw Schedule", font=("Arial", 20), command=lambda: MakePrio(),
                                bg="lightblue")
    ButtonMakeSchedule.configure(height=1, width=18)
    ButtonMakeSchedule.place(x=305, y=410)
    #####################################
    QueueContents = Text(GUI, height=20, width=46)
    QueueContents.insert(END, "Process      " + "ArrivalTime    " + "Burst    " + "Priority\n")
    QueueContents.insert(END, "----------------------------------------------\n")


######################################

def AddToQueueUI_Prio(ProcessName, BurstTime, Arrival,
                      Priority):  # make initial look of queue contents (name:arrival:burst)
    error = 0
    if (ProcessName == '' or Arrival == '' or BurstTime == '' or Priority == ''):
        ShowError("Please Fill All Fields!")
        error = 1

    if (is_number(Arrival) == 0 and Arrival != ''):
        ShowError("Arrival Must Be Numeric!")
        error = 1

    if (is_number(BurstTime) == 0 and BurstTime != ''):
        ShowError("Burst Must Be Numeric!")
        error = 1

    if (is_number(Priority) == 0 and Priority != ''):
        ShowError("Priority Must Be Numeric!")
        error = 1

    if (error == 0):
        QueueContents.place(x=850, y=120)
        QueueContents.insert(END,
                             ProcessName + space(ProcessName, 18) + Arrival + space(Arrival, 11) + BurstTime + space(
                                 BurstTime, 11) + Priority + "\n")
        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
        entry3.delete(0, 'end')
        entry4.delete(0, 'end')


######################################

def MakePrio():
    QueueList = QueueContents.get("3.0", END).split("\n")[:-2]  # name arrival burst priority

    Process_Arrival = dict()
    Process_Burst = dict()
    Process_Priority = dict()

    for process in QueueList:  # construct Dictionary of queue
        temp = process.split()
        Process_Arrival[temp[0]] = float(temp[1])  # {('name' : Arrival)}
        Process_Burst[temp[0]] = float(temp[2])  # {('name' : Burst)}
        Process_Priority[temp[0]] = float(temp[3])  # {('name' : Priority)}

        error = 0
        if (Type.get() not in [1, 2]):
            ShowError("Please Select Preemption")
            error = 1

        if (error == 0):
            if (Type.get() == 1):
                timeline = prio_nonprem(Process_Burst, Process_Arrival,
                                        Process_Priority)  # timeline=list of processes ['Start-End:ProcessName','Start-End:ProcessName']
            if (Type.get() == 2):
                timeline = prio_prem(Process_Burst, Process_Arrival, Process_Priority)

            AvgWaiting = AvgWaitingTime(Process_Arrival, timeline)
            ShowWaitingTime(AvgWaiting)

            DrawGantt(timeline)


######################################

def prio_nonprem(process_d, process_t, process_p):
    Burst = process_d.copy()
    Arrival = process_t.copy()
    Priority = process_p.copy()
    TimeList = list()
    PrioritySorted = dict()
    ArrivalSorted = dict()

    readyqueue = list()

    for key, value in sorted(Arrival.items(), key=lambda item: item[1]):
        ArrivalSorted[key] = float(value)

    for key, value in sorted(Priority.items(), key=lambda item: item[1]):
        PrioritySorted[key] = float(value)

    curr_time = float(list(ArrivalSorted.values())[0])

    flag = 1
    while flag == 1:
        flag = 0

        for i in PrioritySorted:  # loop over all process and add to readyqueue the ready processes
            if (ArrivalSorted[i] != "done"):
                if (ArrivalSorted[i] <= curr_time) and (i not in readyqueue):
                    readyqueue.append(i)

        if (len(readyqueue) == 0) and (
                curr_time > 0):  # for gap, make current_time= closest arrival time of process,so in next while iteration we can append to readyqueue
            for i in ArrivalSorted:
                if (ArrivalSorted[i] != "done"):
                    curr_time = float(ArrivalSorted[i])

        for i in PrioritySorted:

            for x in ArrivalSorted:
                if ArrivalSorted[x] != "done":
                    flag = 1
                    break

            if (i in readyqueue):
                TimeList.append(str(curr_time) + '-' + str(curr_time + Burst[i]) + ':' + str(i))
                ArrivalSorted[i] = "done"
                readyqueue.remove(i)
                curr_time = curr_time + Burst[i]

    return TimeList


##########################################

def prio_prem(process_d, process_t, process_p):
    Burst = process_d.copy()  # Duration
    Arrival = process_t.copy()  # Arrival
    Priority = process_p.copy()  # Priority

    arr_t = sorted(Arrival.values())
    pross_n = []
    pross_time = []
    pross_p = []
    for i in arr_t:
        for j in Arrival:
            if i == Arrival[j]:
                pross_n.append(j)
                Arrival[j] = 'null'
    for i in pross_n:
        for j in Burst:
            if i == j:
                pross_time.append(Burst[j])
                Burst[j] = 'null'
    for i in pross_n:
        for j in Priority:
            if i == j:
                pross_p.append(Priority[j])
                Priority[j] = 'null'
    i = 0
    graph = []
    curr_time = arr_t[0]
    while len(pross_time) != 0:
        x = 0
        while 1:
            flag2 = 0
            for j in range(i + 1, len(arr_t)):
                if ((pross_p[i] > pross_p[j]) and ((pross_time[i] + arr_t[i]) > arr_t[j])):

                    if arr_t[i] > curr_time:
                        curr_time = arr_t[i]

                    flag2 = 1
                    if arr_t[j] != curr_time:
                        graph.append(str(curr_time) + '-' + str(arr_t[j]) + ':' + pross_n[i])
                    curr_time = arr_t[j]
                    pross_time[i] = pross_time[i] + arr_t[i] - arr_t[j]
                    i = j
                    break
            if flag2 == 0:
                if arr_t[i] > curr_time:
                    curr_time = arr_t[i]
                graph.append(str(curr_time) + '-' + str(curr_time + pross_time[i]) + ':' + pross_n[i])
                curr_time = curr_time + pross_time[i];
                pross_time.remove(pross_time[i])
                pross_n.remove(pross_n[i])
                arr_t.remove(arr_t[i])
                pross_p.remove(pross_p[i])
                for i in arr_t:
                    if i <= curr_time:
                        x = x + 1
                i = min_a(pross_p, x)
                break
    return graph


######################################
######################################
def main():
    global GUI, B0, B1, B2, B3

    GUI = Tk()
    GUI.title("Process Scheduler")
    GUI.configure(bg='#d2d2d2')
    GUI.minsize(0, 800)
    GUI.resizable(0, 0)

    labelbanner = Label(GUI, text="Process Scheduler", font=("Arial", 30), bg='lightblue', relief="ridge", fg="White")
    labelbanner.grid(columnspan=4, padx=500, sticky='ew')

    B0 = Button(GUI, text="FCFS", font=("Arial", 15), command=lambda: MakeFcfsUI())
    B0.configure(height=2, width=16)
    B0.grid(row=1, column=0)

    B1 = Button(GUI, text="SJF", font=("Arial", 15), command=lambda: MakeSJFUI())
    B1.configure(height=2, width=16)
    B1.grid(row=1, column=1)

    B2 = Button(GUI, text="Round Robin", font=("Arial", 15), command=lambda: MakeRRUI())
    B2.configure(height=2, width=16)
    B2.grid(row=1, column=2)

    B3 = Button(GUI, text="Prirority", font=("Arial", 15), command=lambda: MakePrioUI())
    B3.configure(height=2, width=16)
    B3.grid(row=1, column=3)

    GUI.bind('<Return>', func)

    GUI.mainloop()


def func(event):
    try:
        if (selectedbutton == B3):
            AddToQueueUI_Prio(entry1.get(), entry2.get(), entry3.get(), entry4.get())
        else:
            AddToQueueUI(entry1.get(), entry2.get(), entry3.get())

    except:
        pass


##########################
##########################

def DestroyAll():  # make sure that area we use is clear before placing objects

    try:
        label1.destroy()  # receipt
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
        buttonPreem.destroy()
        buttonNonPreem.destroy()

    except:
        pass
    try:
        label6.destroy()
        labelimg.destroy()
    except:
        pass


##########################
##########################

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom


try:
    main()
except:
    ShowError("Error Happened, Please Check Your Inputs!")


