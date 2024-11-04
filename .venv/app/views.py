import tkinter as tk
import traceback
# from django.db.models import TextField
# import seaborn as sns
from tkinter import *

from tkinter import ttk

import numpy
import numpy as np

from tkinter.messagebox import showinfo

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

from app.controller import Controller
from app.model import *
from numpy.ma.core import shape


class View:
    def __init__(self):
        self.selectedsession = ''
        self.var=''
        self.ssd = ''
        self.sed =''
        self.selected_values=''
        self.txtvar=''
        self.teacherresultset =None
        self.cb={}
        self.checkbuttons_vars=''
        self.entry_var=''
        self.fig, self.axs=None,None
        self.row, self.col=0,0
        self.evid=[]
        self.root=''
        self.cbid={}
        self.selectedid={}



    def create_main_window(self):

        self.root = Tk()
        self.root.title("DEI Subject Analysis")
        self.root.geometry('550x550')

        # db=connectDatabase()
        # sessions = self.getsessions()
        self.sessions = get_session()

        # sessions = ('2021-22', '2022-23', '2023-24')
        self.var = StringVar()
        combo = ttk.Combobox(self.root, textvariable=self.var, width=20)
        print(self.sessions)

        combo['values'] = [session['unvsession'] for session in self.sessions]
        combo['state'] = 'readonly'
        combo.bind('<<ComboboxSelected>>', self.session_changed)

        self.txtvar = ''
        pgmname = ''
        coursecode = ''
        selectedsession = ''
        # Checkbutton1 = tk.IntVar();
        # Checkbutton2 = tk.IntVar();
        # Checkbutton3 = tk.IntVar();
        checkbuttons_vars = []
        cb = {}

        lbl0 = Label(self.root, text="Student Marks Analysis", width=20, font=("bold", 15))
        lbl0.place(x=150, y=60)  # Course code label
        # Course code label
        lbl1 = Label(self.root, text="Enter course code", width=20, font=("bold", 10))
        lbl1.place(x=80, y=130)

        self.entry_var = tk.StringVar()
        self.entry_var.trace("w", self.on_entry_change)  #
        entry = Entry(self.root, width=20, font=("bold", 10), state=NORMAL,textvariable=self.entry_var)
        entry.place(x=240, y=130)

        lbl2 = Label(self.root, text="Enter Session", width=20, font=("bold", 10))
        lbl2.place(x=68, y=180)

        combo.place(x=240, y=180)

        # Creating a Checkbutton
        # evid=getevaluationid(self.txtvar)
        # self.cb = {'CT1', 'CT2', 'DHA'}
        # self.cb= dict(self.evid)
        # print(self.cb)
        # self.checkbuttons_vars = [tk.BooleanVar() for value in self.cb]
        #
        # xpos, ypos = 240, 205
        # for index, value in enumerate(self.cb):
        #     l = tk.Checkbutton(root, text=value, variable=self.checkbuttons_vars[index], command=self.on_button_toggle)
        #     l.pack(side="left", anchor="center")
        #     l.place(x=xpos, y=ypos)
        #     xpos = xpos + 50

        button = tk.Button(text='SUBMIT', activebackground="blue", command=self.on_submit)
        #button = tk.Button(text='SUBMIT', activebackground="blue")
        button.place(x=240, y=250)
        self.root.mainloop()
    def session_changed(self,event=None):
        self.selectedsession=str(self.var.get())
        self.ssd=self.selectedsession[:4]
        self.sed=self.selectedsession[5:9]
        self.ssd=self.ssd+'-'+'07-01'
        self.sed=self.sed+'-'+'06-30'
        print(self.ssd)
        print(self.sed)

    def on_entry_change(self,*args):
        self.txtvar=self.entry_var.get()
        self.cb = {}
        checkbutton:Checkbutton=Checkbutton()

        if len(self.txtvar)>5:
            self.evlist = getevaluationid(self.txtvar)

            self.cb = { evobj['evaluation_id_name'] for evobj in self.evlist }
            self.cbid = { evobj['evaluation_id_name']:evobj['evaluation_id'] for evobj in self.evlist }
            print (self.cbid)
            print("Arush")

            self.checkbuttons_vars = [tk.BooleanVar() for value in self.cb]
            print(self.checkbuttons_vars[0])

            xpos, ypos = 50, 205
            checkbutton.destroy()
            for index, value in enumerate(self.cb):
                checkbutton = tk.Checkbutton(self.root, text=value, variable=self.checkbuttons_vars[index],
                                   command=self.on_button_toggle)

                checkbutton.pack(side="left", anchor="center")
                checkbutton.place(x=xpos, y=ypos)
                xpos = xpos + 50
        # print("Entry changed to:", self.entry_var.get())
            print("EV ID", self.evlist)

    def on_button_toggle(self):

        print("check button toggled")
        self.selected_values = [value for value, var in zip(self.cb, self.checkbuttons_vars) if var.get()]
        print(self.selected_values)
        print("self.cbid",self.cbid)
        self.selectedid={}

        self.selectedid={key:value for key,value in self.cbid.items() if key in  self.selected_values}
        print("selected id",self.selectedid)
    def on_submit(self):
        #start_time = time.time()
        #print(f"1 Starting button click at {start_time} secs")

        # idx: int = -1
        # fig = plt.figure()
        self.get_axes()
        if self.totaxes==1:
            e = self.teacherresultset.pop()
            self.plotgraph(e)
            #start_time = time.time()
            #print(f"2 Starting button click at {start_time} secs")
        else:

            #start_time = time.time()
            #print(f"3 Starting button click at {start_time} secs")
            fig, axs = plt.subplots(nrows=self.row, ncols=self.col)
            k = 0

            try:

                for i in range(0, self.row, 1):
                    for j in range(0, self.col, 1):
                        if k < self.totaxes:
                            k = k + 1
                            e = self.teacherresultset.pop()
                            print(i,j)
                            ax = axs[i][j]
                            self.plotgraph(e, ax)
                #start_time = time.time()
                #print(f"4 Starting button click at {start_time} secs")

            except Exception as err:

                print("End of program", err)
                print(traceback.format_exc())
            finally:
                fig.suptitle("Session:-" + self.selectedsession + " Subject " + self.txtvar)
                plt.show()

        # cont= Controller()

         # =cont.submit(self.txtvar,self.ssd,self.sed,self.selectedsession)
    def plotgraph(self,e: dict, ax=None):

        rollno = []
        marks = []
        pck = e.get('program_course_key')
        programname = e.get('program_name')
        coursecode = e.get('course_code')
        branch = e.get('brname')
        spc = e.get('spname')
        empid = e.get('creator_id')
        empname = e.get('first_name')
        gs = gridspec.GridSpec(10, 10)

        # totmark = get_total_marks(self.ssd,self.sed,coursecode,empid,pck)
        for key,value in self.selectedid.items():
            comp_marks = getevmarks(self.ssd,self.sed,value,coursecode,pck,empid)
            print('comp_marks',comp_marks)
            if(self.totaxes==1):
                self.plotcomponents(comp_marks, key, empname)

            else:
                self.plotcomponents(comp_marks,key,empname,ax)

        if (self.totaxes == 1):
            plt.show()



    def plotcomponents(self,student_marks,component,empname,ax=0):
        rollno = []
        marks = []
        for x in student_marks:
            rollno.append(x['roll_number'])
            marks.append(x['marks'])

        std = np.std(marks)
        avg = np.average(marks)
        mean = np.mean(marks)

        sdlabel = 'SD=' + str(round(std, 2))
        meanlabel = 'Mean=' + str(round(mean, 2))
        avglabel = 'Average=' + str(round(avg, 2))
        print("value of ax",ax)
        if (ax==0):

            plt.plot(rollno, marks, label=component)
            plt.text(0.1, 0.7, 'Teacher=' + empname, style='italic', horizontalalignment='left', verticalalignment='top',
                    )  # transform=ax.transAxes)
            plt.legend()
            plt.xlabel('Roll no')
            plt.ylabel('Marks')
            plt.grid(True)

        else:

            ax.plot(rollno,marks,label=component)
            ax.text(0.1, 0.7, 'Teacher=' +empname , style='italic', horizontalalignment='left', verticalalignment='top',
                    )# transform=ax.transAxes)
            ax.legend()
            ax.set_xlabel('Roll no')
            ax.set_ylabel('Marks')
            ax.grid(True)


        # ax.legend()
    def get_axes(self):
        subject = self.txtvar
        self.teacherresultset = get_evaluaters(subject, self.ssd, self.sed)
        self.totaxes = len(self.teacherresultset)
        print(self.teacherresultset)
        if self.totaxes == 0:
            showinfo(
                title='Total Records',
                message=f' No Record found'

            )
            return

        print("totaxes=", self.totaxes)
        self.col = 2
        self.row: int = 0
        if self.totaxes < 7:

            if (self.totaxes % 2 == 0):
                self.row = int(self.totaxes / 2)
            else:
                self.row = int((self.totaxes + 1) / 2)
            if self.row == 1:
                self.row = 2
        else:
            self.row = 3
            self.col = 3

        # print(totaxes)
        # print("row=", row)
        # print("col=", col)




