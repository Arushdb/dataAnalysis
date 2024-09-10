import tkinter
import traceback
# from django.db.models import TextField
# import seaborn as sns
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np


# name = input("What is your name?")
# num = input("What is your favorite number? ")
# thislist = ["apple", "banana", "cherry"];
# print(thislist);
# arr = np.array([1, 2, 3, 4, 5])
# print(arr);
class App():
    def __init__(self):
        self.mydb = mysql.connector.connect(

          #host="localhost",
          #database="cms_live",
          #user="appuser",
          #password="appuser",
          host="admission.dei.ac.in",
          database="cms_live",
          user="python",
          password="P~ython@2024"
          )
        self.root=Tk()
        self.root.title("DEI Subject Analysis")
        self.root.geometry('550x550')
        sessions = self.getsessions()
        #sessions = ('2021-22', '2022-23', '2023-24')
        self.var = StringVar()
        self.combo = ttk.Combobox(self.root, textvariable=self.var, width=20)
        self.combo['values'] = sessions
        self.combo['state'] = 'readonly'
        self.combo.bind('<<ComboboxSelected>>', self.session_changed)
        self.ssd=''
        self.sed=''
        self.teachercursor = self.mydb.cursor(dictionary=True)
        self.studentcursor = self.mydb.cursor()
        self.txtvar=''
        self.pgmname=''
        self.coursecode=''
        self.selectedsession=''

    def clear():
        combo.set('')
    def getsessions(self):
      sessioncursor=self.mydb.cursor()
      sessioncursor.execute(
        "select concat(substring(start_date,1,4),'-',"
        +" substring(end_date,1,4)) as unvsession "
        +" from university_master "
        +" order by start_date desc limit 5 " )
      sessionresult = sessioncursor.fetchall()
      print(sessionresult)
      return sessionresult

    def plotgraph(self,e: dict, ax):
        print("ssd",self.ssd)
        print("sed",self.sed)
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
        self.studentcursor.execute(
            " select sms.roll_number,sms.total_marks "
            "  from student_marks_summary sms "
            " join employee_master em on em.employee_code=sms.creator_id "
            " where sms.semester_start_date between %s and %s " 
            " and sms.course_code= %s and sms.creator_id = %s "
            " and sms.program_course_key= %s ;",(self.ssd,self.sed,coursecode,empid,pck))


        myresult = self.studentcursor.fetchall()
        print('testing')
        print(myresult)
        lg = empname
        #title = programname + "_" + branch + "_" + spc + "  " + coursecode
        #title = programname + "_" + branch + "_" + spc + "  " + coursecode
        #title = programname + "  " + coursecode
        for x in myresult:
            rollno.append(x[0])
            marks.append(x[1])

        std = np.std(marks)
        avg = np.average(marks)
        mean = np.mean(marks)

        sdlabel = 'SD=' + str(round(std, 2))
        meanlabel = 'Mean=' + str(round(mean, 2))
        avglabel = 'Average=' + str(round(avg, 2))
        print("SDlabel",sdlabel)

        # plt.bar(rollno,marks)
        #ax.title.set_text(title)

        # ax.hist(marks,bins=[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200],facecolor='yellow', edgecolor='blue' ,label=lg)
        ax.hist(marks, bins=range(min(marks), max(marks) + 10, 10), facecolor='cyan', edgecolor='blue', label=lg)
        # ax.set_xlabel(label)
        ax.axvline(x=np.mean(marks) - np.std(marks), ls="--", color='#2ca02c', alpha=0.7)
        ax.axvline(x=np.mean(marks) + np.std(marks), ls="--", color='#2ca02c', alpha=0.7)
        ax.axvline(x=np.mean(marks) , ls="--", color='#008080', alpha=0.7)
        #ax.axvline(x=np.std(marks), ls="-", color='#2ca02c', alpha=0.9)
        ax.text(0.5, 0.5, sdlabel, style='italic',horizontalalignment='center',verticalalignment='center',
                transform=ax.transAxes )
        ax.text(0.5, 0.4, meanlabel, style='italic', horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes)
        ax.text(0.1, 0.9, 'program=' +programname , style='italic', horizontalalignment='left', verticalalignment='top',
                transform=ax.transAxes)
        ax.text(0.1, 0.8, 'branch='+branch, style='italic', horizontalalignment='left', verticalalignment='top',
                transform=ax.transAxes)
        ax.text(0.1, 0.7, 'Spc=' + spc, style='italic', horizontalalignment='left', verticalalignment='top',
                transform=ax.transAxes)

        #ax.text(0.5, 0.3, avglabel, style='italic', horizontalalignment='center', verticalalignment='center',
        #        transform=ax.transAxes)
        #ax.annotate('SD', xy=(np.std(marks), 1), xytext=(50, 1), arrowprops=dict(facecolor='black', shrink=0.05))

        # ax.set xlabel="Standard Deviation="+std
        ax.legend()

    def create_main_window(self):
        #selected_session.trace('w', self.get_index(self.root,self.combo,selected_session))
        # Heading

        lbl0 = Label(self.root, text="Student Marks Analysis", width=20, font=("bold", 15))
        lbl0.place(x=150, y=60)  # Course code label
        # Course code label
        lbl1 = Label(self.root, text="Enter course code", width=20, font=("bold", 10))
        lbl1.place(x=80, y=130)
        self.txtvar = Entry(self.root, width=20, font=("bold", 10), state=NORMAL)
        self.txtvar.place(x=240, y=130)




        lbl2 = Label(self.root, text="Enter Session", width=20, font=("bold", 10))
        lbl2.place(x=68, y=180)

        self.combo.place(x=240, y=180)
        button =tkinter.Button(text='SUBMIT',activebackground="blue",command=self.submit)
        button.place(x=240,y=230)

        # combo.grid(column =1, row =1)
        # print(txt.get())
        self.root.mainloop()

    def session_changed(self,event=None):
        self.selectedsession=str(self.var.get())
        self.ssd=self.selectedsession[:4]
        self.sed=self.selectedsession[5:9]
        self.ssd=self.ssd+'-'+'07-01'
        self.sed=self.sed+'-'+'06-30'
        print(self.ssd)
        print(self.sed)
        '''
        showinfo(
            title='Result',
            message=f'you selected {self.var.get()}'

        )
        '''
        if event:
          print('event.widget.get():', event.widget.get())
    '''
    def get_index(self,root,combo,selected_session):

        Label(root, text="The value at index " + str(combo.current()) +
                         " is" + " " + str(selected_session.get()), font=('Helvetica 12')).pack()
    '''
    def submit(self):
      print("button clicked")
      self.main()
    def main(self):
        subject=self.txtvar.get()
        print("Course_code",self.txtvar.get())

        teacher = []
        self.teachercursor.execute(
            " select pch.program_course_key,pm.program_name, sms.course_code , "
            + " pch.branch_id,pch.specialization_id,stt1.component_description as brname ,"
            + " stt2.component_description as spname ,"
            + " sms.creator_id,first_name from student_marks_summary  sms "
            + " join program_course_header pch on pch.program_course_key  = sms.program_course_key "
            + " join program_master pm on pm.program_id= pch.program_id "
            + " join entity_master ent on ent.entity_id =sms.entity_id  "

            + " join employee_master em on em.employee_code=sms.creator_id "
            + " join system_table_two stt1 on stt1.component_code=pch.branch_id and stt1.group_code='BRNCOD' "
            + " join system_table_two stt2 on stt2.component_code=pch.specialization_id and stt2.group_code='SPCLCD' "
            + " where course_code =%s  and ent.entity_type in ('FAC','DEP') "
            + " and sms.semester_start_date between %s and %s group by sms.creator_id,sms.program_course_key order by sms.entity_id ", (subject  ,self.ssd,self.sed))

        # mycursor.execute("select * from student_master where enrollment_number = %s" %(enrolment))

        teacherresultset = self.teachercursor.fetchall()

        totaxes = self.teachercursor.rowcount
        if totaxes==0 :
            showinfo(
                title='Total Records',
                message=f' No Record found'

            )
            return


        print("totaxes=", totaxes)
        col = 2
        row: int = 0
        if totaxes <7 :

            if (totaxes % 2 == 0):
                row = int(totaxes / 2)
            else:
                row = int((totaxes + 1) / 2)
            if row==1:
                row=2
        else :
            row=3
            col=3


        print(totaxes)
        print("row=", row)
        print("col=", col)
        idx: int = -1
        # fig = plt.figure()
        fig, axs = plt.subplots(nrows=row, ncols=col)


        k=0
        # print(typeof(ax1))
        try:
            for i in range(0, row, 1):
                for j in range(0, col, 1):
                    if k < totaxes :
                      k=k+1
                      e = teacherresultset.pop()
                      print(e)
                      ax = axs[i][j]
                      self.plotgraph(e, ax)

        except Exception as err:
            print("End of program",err)
            print(traceback.format_exc())
        finally:
          fig.suptitle("Session:-"+self.selectedsession+" Subject "+str(self.txtvar.get()).upper())
          plt.show()

myapp = App()
myapp.create_main_window()
##myapp.plt.show()

