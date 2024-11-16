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
from numpy.ma.core import shape

# from app.controller import Controller
from model import *
# from numpy.ma.core import shape





class View:
    def __init__(self):
        # self.checkbutton = None
        self.pgm_result = None
        self.branch = None
        self.checkbuttons = None
        self.checkbutton: Checkbutton = None
        self.spc = None
        self.selected_branchid = None
        self.selectedpgmid = None
        self.okbutton = None
        self.button = None
        self.pgmlbl = None
        self.brnlbl = None
        self.lbl2 = None
        self.entry = None
        self.session_combo = None
        self.pgm_combo = None
        self.branch_combo = None
        self.branchselected = None
        self.selectedsession = ''
        self.session_var=''
        self.pgm_var=''
        self.branch_var=''
        self.ssd = ''
        self.sed =''
        self.selected_values=''
        self.txtvar=''
        self.teacherresultset =None
        self.cb={}
        self.checkbuttons_vars=[]
        self.entry_var=''
        self.fig, self.axs=None,None
        self.row, self.col=0,0
        self.evid=[]
        self.root=''
        self.cbid={}
        self.selectedid={}
        self.plist_unq=[]
        self.blist_unq=[]



    def create_main_window(self):

        self.root = Tk()
        self.root.title("DEI Subject Analysis")
        self.root.geometry('550x550')
        self.sessions = get_session()
        self.txtvar = ''

        checkbuttons_vars = []
        cb = {}

        lbl0 = Label(self.root, text="Student Marks Analysis" , width=20, font=("bold", 15))
        lbl0.place(x=150, y=60)  # Course code label
        # Session Combo########################################
        lbl2 = Label(self.root, text="Enter Session", width=20, font=("bold", 10))
        lbl2.place(x=68, y=130)

        self.session_var = StringVar()
        self.session_combo = ttk.Combobox(self.root, textvariable=self.session_var, width=20)
        self.session_combo['values'] = [session['unvsession'] for session in self.sessions]
        self.session_combo['state'] = 'readonly'
        self.session_combo.bind('<<ComboboxSelected>>', self.session_changed)

        self.session_combo.place(x=240, y=130)

        # Course code label
        lbl1 = Label(self.root, text="Enter course code", width=20, font=("bold", 10))
        lbl1.place(x=80, y=180)

        self.entry_var = tk.StringVar()
        self.entry_var.trace("w", self.on_entry_change)  #
        self.entry = Entry(self.root, width=20, font=("bold", 10), state=NORMAL, textvariable=self.entry_var)
        self.entry.place(x=240, y=180)

        # OK button
        self.okbutton = tk.Button(text='OK', activebackground="blue", command=self.on_clickok)
        self.okbutton.place(x=240, y=210)

        # Create a program combo
        self.pgmlbl = Label(self.root, text="Select Program", width=20, font=("bold", 10))
        self.pgmlbl.place(x=68, y=250)
        self.pgmlbl.place_forget()
        self.pgm_var = StringVar()
        self.pgm_combo = ttk.Combobox(self.root, textvariable=self.pgm_var, width=20)

        self.pgm_combo['state'] = 'readonly'
        self.pgm_combo.bind('<<ComboboxSelected>>', self.get_pgm_selected)
        self.pgm_combo.place(x=240, y=250)
        self.pgm_combo.place_forget()

        # Create a Branch combo
        # self.brnlbl = Label(self.root, text="Select Branch", width=20, font=("bold", 10))
        # self.brnlbl.place(x=68, y=310)
        # self.brnlbl.place_forget()



        # self.branch_var = StringVar()
        # self.branch_combo = ttk.Combobox(self.root, textvariable=self.branch_var, width=20)
        # self.branch_combo['values'] = [branch for branch in self.blist_unq]
        # self.branch_combo['state'] = 'readonly'
        #
        # self.branch_combo.bind('<<ComboboxSelected>>', self.get_branch_selected)
        # self.branch_combo.place(x=240, y=310)
        # self.branch_combo.place_forget()

        #Submit button
        self.button = tk.Button(text='SUBMIT', activebackground="blue", command=self.on_submit)
        self.button.place(x=240, y=400)
        self.button.place_forget()

        self.root.mainloop()


    def on_clickok(self,event=None):
        print("OK clicked")
        subject =self.entry.get()
        print("subject=",subject)
        self.okbutton.place(x=240, y=210)
        if len(self.entry.get())>5 and self.session_combo.get():

            self.getpgmandbranch(subject, self.ssd, self.sed)
            if len(self.pgm_result)>0:
              # self.brnlbl.place(x=68, y=310)
        # self.branch_combo.place(x=240, y=310)
                self.pgmlbl.place(x=68, y=250)
                self.pgm_combo.place(x=240, y=250)
                self.button.place(x=240, y=400)
                self.okbutton.place_forget()



    # def get_branch_selected(self,event):
    #     print("branch selected",self.branch_combo.get())
    #     self.selected_branchid=self.branch_combo.get()


    def get_pgm_selected(self,event):
        print("program selected",self.pgm_combo.get())
        self.selectedpgmid=''
        if self.checkbuttons is not None:
            self.destroy_checkbutton()
        selected_value=self.pgm_combo.get()
        # Find the dictionary that has this value
        selected_dict = next((item for item in self.plist_unq if item["value"] == selected_value), None)
        # Print or use the key
        if selected_dict:
            print("Selected Key:", selected_dict["key"])
            self.selectedpgmid=selected_dict["key"]
            self.create_checkboxes()


    def session_changed(self,event=None):


        self.selectedsession =str(self.session_combo.get())

        self.ssd=self.selectedsession[:4]
        self.sed=self.selectedsession[5:9]
        self.ssd=self.ssd+'-'+'07-01'
        self.sed=self.sed+'-'+'06-30'
        print(self.ssd)
        print(self.sed)



    def on_entry_change(self,*args):
        self.txtvar=self.entry.get()

        # self.branch_combo.place_forget()
        self.pgm_combo.place_forget()
        self.pgmlbl.place_forget()
        # self.brnlbl.place_forget()
        self.button.place_forget()
        self.okbutton.place(x=240, y=210)

        self.pgm_combo.set("")
        # self.branch_combo.set("")
        self.selectedid={}
        if self.checkbuttons is not None:
            self.destroy_checkbutton()






        # print("Entry changed to:", self.entry_var.get())




    def create_checkboxes(self):

        self.cb = {}
        self.cbid = {}
        self.checkbutton: Checkbutton = Checkbutton()
        self.checkbutton.destroy()

        if len(self.txtvar) > 5:
            self.evlist = getevaluationid(self.txtvar, self.selectedpgmid)
            print("EV ID", self.evlist)

            self.cb = {evobj['evaluation_id_name'] for evobj in self.evlist}
            self.cbid = {evobj['evaluation_id_name']: evobj['evaluation_id'] for evobj in self.evlist}
            print(self.cbid)
            print("Arush")

            self.checkbuttons_vars = [tk.BooleanVar() for value in self.cb]
            # print(self.checkbuttons_vars[0])

            xpos, ypos = 50, 350
            self.checkbuttons=[]
            for index, value in enumerate(self.cb):
                self.checkbutton = tk.Checkbutton(self.root, text=value, variable=self.checkbuttons_vars[index],
                                             command=self.on_button_toggle)
                self.checkbuttons.append(self.checkbutton)
                # self.checkbuttons_vars[index].trace("write", self.check_var_changed)



                self.checkbutton.pack(side="left", anchor="center")
                self.checkbutton.place(x=xpos, y=ypos)
                xpos = xpos + 50

    def destroy_checkbutton(self):
        # Get the Checkbutton associated with this variable and destroy it
        for cb in self.checkbuttons:
            cb.destroy()
            # Clear the array after destroying
        self.checkbuttons = []

    def getpgmandbranch(self, subject, ssd, sed):

        self.pgm_result = get_programs(subject, ssd, sed)
        if len(self.pgm_result)==0:
            showinfo(
                title='Error',
                message=f' No Record found')
            return



        plist= [{"key":pgm['program_course_key'][0:7],"value":pgm['program_name']} for pgm in  self.pgm_result ]

        self.plist_unq = []
        for item in plist:
            if item not in self.plist_unq:
                self.plist_unq.append(item)

        print("plist_unq",self.plist_unq)



        # blist=[pgm['branch_id'] for pgm in  rs ]
        # self.blist_unq=list(set(blist))
        # self.branch_combo['values'] = self.blist_unq

        self.pgm_combo['values'] = [pgm['value'] for pgm in self.plist_unq]
        # self.pgm_combo['key'] = [pgm['key'] for pgm in self.plist_unq]


        # print("blist", blist)
        # print("blist_unq", self.blist_unq)


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
        if  self.validate():
            self.get_axes()
            print("into submit")
            if self.totaxes==1:
                e = self.teacherresultset.pop()
                plt.figure()
                self.plotgraph(e)
                #start_time = time.time()
                #print(f"2 Starting button click at {start_time} secs")
            elif self.totaxes==2:

                #start_time = time.time()
                #print(f"3 Starting button click at {start_time} secs")
                fig, axs = plt.subplots(nrows=self.row, ncols=self.col)
                e = self.teacherresultset.pop()
                ax = axs[0]
                self.plotgraph(e, ax)
                e = self.teacherresultset.pop()
                ax = axs[1]
                self.plotgraph(e, ax)
                fig.suptitle("Session:-" + self.selectedsession +
                             " Subject " + self.txtvar.upper() + "-"
                             + self.pgm_combo.get())
                plt.show()
            else:
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
                    fig.suptitle("Session:-" + self.selectedsession +
                                 " Subject " + self.txtvar.upper() +"-"
                                 +self.pgm_combo.get())
                    plt.show()

    def plotgraph(self,e: dict, ax=None):



        pck = e.get('program_course_key')

        coursecode = e.get('course_code')
        self.branch = e.get('brname')
        self.spc = e.get('spname')
        # empid = e.get('creator_id')
        empname = e.get('first_name')
        gs = gridspec.GridSpec(10, 10)
        print("selected items",self.selectedid.items())

        # totmark = get_total_marks(self.ssd,self.sed,coursecode,empid,pck)
        for key,value in self.selectedid.items():
            comp_marks = getevmarks(self.ssd,self.sed,value,coursecode,pck)
            print('comp_marks',comp_marks)
            if self.totaxes==1:
                self.plotcomponents(comp_marks, key)

            else:
                self.plotcomponents(comp_marks,key,ax)

        if self.totaxes ==1:
            plt.suptitle("Session:-" + self.selectedsession +
                         " Subject " + self.txtvar.upper() + "-"
                         + self.pgm_combo.get() )
            plt.show()



    def plotcomponents(self,student_marks,component,ax=None):
        rollno = []
        marks = []
        sno=1
        for x in student_marks:
            # rollno.append(x['roll_number'])
            rollno.append(sno)
            marks.append(x['marks'])
            sno=sno+1

        std = np.std(marks)
        avg = np.average(marks)
        mean = np.mean(marks)

        sdlabel = 'SD=' + str(round(std, 2))
        meanlabel = 'Mean=' + str(round(mean, 2))
        avglabel = 'Average=' + str(round(avg, 2))
        print("value of ax",ax)
        if ax is None:


            plt.plot(rollno, marks, label=component)
            plt.text(0.1, 0.7,'Branch=' +self.branch, style='italic', horizontalalignment='left', verticalalignment='top')

            plt.legend()
            plt.xlabel('Students')
            plt.ylabel('Marks')
            plt.grid(True)


        else:

            ax.plot(rollno,marks,label=component)
            ax.text(0.1, 0.7, 'Branch=' +self.branch  , style='italic', horizontalalignment='left', verticalalignment='top')

            ax.legend()
            ax.set_xlabel('Students')
            ax.set_ylabel('Marks')
            ax.grid(True)


        # ax.legend()
    def get_axes(self):
        subject = self.txtvar
        self.teacherresultset = get_evaluaters(subject,self.selectedpgmid,self.ssd, self.sed)
        self.totaxes = len(self.teacherresultset)
        print("total axes",self.totaxes)
        print("teacher result",self.teacherresultset)
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
            if self.totaxes==2:
                self.row=1

            if self.totaxes==3 or self.totaxes==4 :
                self.row=2
                self.col = 2

            if self.totaxes==5 or self.totaxes==6 :
                self.row=3
                self.col = 2


        else:
            self.row = 3
            self.col = 3

        # print(totaxes)
        # print("row=", row)
        # print("col=", col)

    def validate(self):
        if len(self.txtvar) < 6:
            showinfo(
                title='Error',
                message=f' Invalid Subject')
            return  False

        if  self.pgm_combo.get()=='':
            showinfo(
            title = 'Error',
            message = f' program not selected')
            return False
        # if  self.branch_combo.get()=='':
        #     showinfo(
        #     title = 'Error',
        #     message = f' Branch not selected')
        #     return  False
        if  len(self.selectedid)==0:
            showinfo(
            title = 'Error',
            message = f' select evaluation component')
            return  False
        return True






