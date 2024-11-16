from database import Database
import mysql.connector
from mysql.connector import Error
from model import getallsubject_batch,insert_marks_batch,getevaluationid_batch
from datetime import datetime
import numpy as np

# Example date string
date_string = "2023-11-12"


class SubjectAnalysis :

    def __init__(self):
        self.ssd = ["2023-07-01", "2024-01-01"]

    def mymain(self):
        # rs = getallsubject()
        rs = getallsubject_batch()
        print(rs)

        for rsobj in rs:
            print(rsobj['semester_start_date'])
            ssd=rsobj['semester_start_date']
            pck=rsobj['program_course_key']
            pgmid=pck[0:7]
            print(pgmid)

            subject=rsobj['course_code']
            evids=getevaluationid_batch(subject,pgmid)
            for item in evids:
                id=item['evaluation_id']
                idname=item['evaluation_id_name']
                print(evids)
                rs1=insert_marks_batch(subject,ssd,pck,id)
                print(rs1)
                # print(rs1)
                # marks = []
                # marks=[mark['marks'] for mark in rs1]
                # sd=np.std(marks)
                # avg=np.average(marks)
                # print(marks)
                # print("sd=",sd)
                # print("average=",avg)

        # for sdate in self.ssd:
        #     print(type(sdate))
        #     # date_object = datetime.strptime(sdate, "%Y-%m-%d").date()
        #     # print(date_object)
        #
        #     rs=getallsubject()
        #
        #     print(rs);
# sa=SubjectAnalysis()
# sa.mymain()




