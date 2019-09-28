'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''

from VaccumCleaner import VaccumCleaner
from Environment import Environment
from Actions import Actions
import tkinter as tk
import time
from Node import Node
from BFS import BFS, getQueueSize
import threading
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.style as style
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from scrolltextarea import scrollTxtArea

finalState = None
queueSize = []
signal = False
second = 0
seconds = []
initState = None
vc = None


def BFSThread(rootNode, goalState, path):
    global finalState
    global signal
    global queueSize
    global seconds
    finalState = BFS(rootNode, goalState, path, queueSize)
    signal = False


def generateDirtBtn(canvas,length,dotSize,e1,e2):
    global initState
    global vc
    global signal

    try:
        n = int(e1.get())
        s = int(e2.get())

        if n in range(1,11) and s in range(1,41):

            if(vc!=None):
                vc.vc.clear()
                vc.vc.reset()
                vc.vc.ht()
            del(vc)
            vc = VaccumCleaner(canvas, n, length, dotSize)

            initState = Environment(None, n, 0, 0)

            vc.drawGrid()

            initState.generateDirt(s)
            initState.print()
            vc.showState(initState)
            vc.moveToXY(0,0)

            signal=True 
               
            
        else:
             tk.messagebox.showinfo("Title", "check constraints")


    except:
        tk.messagebox.showinfo("Title", "Enter valid number")

    


def doBFS(n, a, root, vc, canvas2, textAr):
    global initState

    if signal==True:

        goalState = Environment(None, n, 0, 0)
        rootNode = Node(initState, None)

        path = []

        queueSize.clear()

        t1 = threading.Thread(target=BFSThread, args=(rootNode, goalState, path,))

        t1.start()

        t1.join()

        tk.messagebox.showinfo("Title", "Got action path")

        st = []
        for x, y, z in path[::-1]:
            st.append(str(z))

        # print(st)

        textAr.text.delete('1.0', tk.END)

        #textAr.text.config(state=tk.NORMAL)
        textAr.text.insert(tk.INSERT, "\n".join(st))
        #textAr.text.config(state=tk.DISABLED)

        a.plot(queueSize)
        canvas2.draw()

        if len(path) > 0:
            for x, y, z in path[::-1]:
                vc.moveToXY(x, y, True)
                if(z == Actions.S):
                    vc.paintDot("white")
                time.sleep(0.5)

        if finalState != None:
            vc.goHomeAftCleaning(finalState.env.vacCleanerX,
                                finalState.env.vacCleanerY)
            tk.messagebox.showinfo("Title", "Reached Home")

    else:
        tk.messagebox.showinfo("Title", "Please generate dirt")


def main():
    n = 8
    length = 40
    dotSize = 20
    w = 1280
    h = 840
    pad=15

    plt.style.use("fivethirtyeight")
    matplotlib.use("TkAgg")
    root = tk.Tk(className="AI Demo sbhdhr")
    root.geometry(str(w)+"x"+str(h))

    canvas = tk.Canvas(root, bg="red", width=w/2, height=h/2)
    canvas.grid(row=0, column=0)
    f = plt.Figure(figsize=(7.5, 4), dpi=78)
    f.suptitle('Queue Size')
    plt.xlabel('Number')
    plt.ylabel('Time')
    a = f.add_subplot(111)
    canvas2 = FigureCanvasTkAgg(f, master=root)
    canvas2.get_tk_widget().grid(row=0, column=1)
    frame3 = tk.Frame(root, bg="blue", width=w/2, height=h/2)
    frame3.grid(row=1, column=0)
    frame4 = tk.Frame(root, bg="blue", width=w/2, height=h/2)
    frame4.grid(row=1, column=1)
    txtAr = scrollTxtArea(frame3)
   # txtAr.text.config(state=tk.DISABLED)
    btn1 = tk.Button(frame4, text="Generate Dirt",
                     command=lambda: generateDirtBtn(canvas,length,dotSize,entry1,entry2))
    btn1.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X,
              expand=tk.YES, ipadx=pad, ipady=pad, padx=pad, pady=pad)
    btn2 = tk.Button(frame4, text="Run BFS !!",
                     command=lambda: doBFS(n, a, root, vc, canvas2, txtAr))
    btn2.pack(side=tk.RIGHT, anchor=tk.W, fill=tk.X,
              expand=tk.YES, ipadx=pad, ipady=pad, padx=pad, pady=pad)
    btn3 = tk.Button(frame4, text="Analyze",
                     command=lambda: doBFS(n, a, root, vc, canvas2, label1))
    btn3.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=tk.YES,
              ipadx=pad, ipady=pad, padx=pad, pady=pad)
    btn4 = tk.Button(frame4, text="Constraints",
                     command=lambda: doBFS(n, a, root, vc, canvas2, label1))
    btn4.pack(side=tk.BOTTOM, anchor=tk.W, fill=tk.X,
              expand=tk.YES, ipadx=pad, ipady=pad, padx=pad, pady=pad)
    label1 = tk.Label(frame4)
    label1.config(text="Enter N: ")
    label1.pack(side=tk.TOP)
    entry1 = tk.Entry(frame4)
    entry1.pack(side=tk.TOP,ipadx=pad, ipady=pad, padx=pad, pady=pad)
    label2 = tk.Label(frame4)
    label2.config(text="Enter dirt % : ")
    label2.pack(side=tk.TOP)
    entry2 = tk.Entry(frame4)
    entry2.pack(side=tk.BOTTOM,ipadx=pad, ipady=pad, padx=pad, pady=pad)
    
    

   

    root.mainloop()


if __name__ == "__main__":
    main()


'''
    rPane = tk.PanedWindow(root)
    rPane.pack(fill=tk.BOTH, expand=1)
    left = tk.PanedWindow(rPane, orient=tk.VERTICAL)
    rPane.add(left)
    right = tk.PanedWindow(rPane, orient=tk.VERTICAL)
    rPane.add(right)
    leftTop = tk.Frame(left,bg="red")
    left.add(leftTop)
    leftBtm = tk.Frame(left,bg="blue")
    left.add(leftBtm)
    rtTop = tk.Frame(right,bg="green")
    right.add(rtTop)
    rtBtm = tk.Frame(right,bg="yellow")
    right.add(rtBtm)

'''


'''


    canvas = tk.Canvas(root, width=1280/2, height=7pad/2)
    canvas.grid(row=0, column=0, sticky=tk.W+tk.N)

   

    
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=0, column=1, sticky=tk.E+tk.N)

    frame1 = tk.Frame(root, bg="grey", width=1280*2/3, height=7pad/2)
    frame1.grid(row=1, column=0, sticky=tk.W+tk.N,
                columnspan=2, padx=0, pady=0, ipadx=0, ipady=0)

    frame2 = tk.Frame(root, width=1280/3, height=7pad/2)
    frame2.grid(row=1, column=1, padx=0, pady=0, ipadx=0, ipady=0)

    

    btn2 = tk.Button(frame2, text="Start BFS",
                     command=lambda: doBFS(n, a, root, vc, canvas2,label1))
    btn2.grid(row=4, padx=30, pady=30)

    label1 = tk.Label( frame1,wraplength=600)
    label1.grid(row=0)
    label1.config(text='change the value')

    '''
