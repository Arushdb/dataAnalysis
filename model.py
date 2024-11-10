from database import Database
import mysql.connector
from mysql.connector import Error

import time

def get_programs( subject, ssd, sed):
    query = """
         select pch.program_course_key,pm.program_name, sms.course_code , 
          pch.branch_id,pch.specialization_id,stt1.component_description as brname ,
         stt2.component_description as spname 
         from student_marks_summary  sms 
         join program_course_header pch on pch.program_course_key  = sms.program_course_key 
         join program_master pm on pm.program_id= pch.program_id 
         join entity_master ent on ent.entity_id =sms.entity_id  
         
         join system_table_two stt1 on stt1.component_code=pch.branch_id and stt1.group_code='BRNCOD' 
         join system_table_two stt2 on stt2.component_code=pch.specialization_id and stt2.group_code='SPCLCD' 
         where course_code =%s  and ent.entity_type in ('FAC','DEP') 
         and sms.semester_start_date between %s and %s group by sms.program_course_key 
         order by sms.entity_id 


    """
    params = (subject, ssd, sed)
    return fetch_query(query, params, True)
def get_evaluaters1( subject,pgmid,brnid, ssd, sed):
    query = """
         select pch.program_course_key,pm.program_name, sms.course_code , 
          pch.branch_id,pch.specialization_id,stt1.component_description as brname ,
         stt2.component_description as spname ,
         sms.creator_id,first_name from student_marks_summary  sms 
         join program_course_header pch on pch.program_course_key  = sms.program_course_key 
         join program_master pm on pm.program_id= pch.program_id 
         join entity_master ent on ent.entity_id =sms.entity_id  

         join employee_master em on em.employee_code=sms.creator_id 
         join system_table_two stt1 on stt1.component_code=pch.branch_id and stt1.group_code='BRNCOD' 
         join system_table_two stt2 on stt2.component_code=pch.specialization_id and stt2.group_code='SPCLCD' 
         where course_code =%s  and ent.entity_type in ('FAC','DEP') and pm.program_id=%s and pch.branch_id=%s
         and sms.semester_start_date between %s and %s group by sms.creator_id,sms.program_course_key 
         order by sms.entity_id 


    """
    params = (subject,pgmid,brnid, ssd, sed)
    return fetch_query(query, params, True)


def get_evaluaters( subject,pgmid, ssd, sed):
    query = """
         select pch.program_course_key,pm.program_name, sms.course_code , 
          pch.branch_id,pch.specialization_id,stt1.component_description as brname ,
         stt2.component_description as spname ,
         sms.creator_id,first_name from student_marks_summary  sms 
         join program_course_header pch on pch.program_course_key  = sms.program_course_key 
         join program_master pm on pm.program_id= pch.program_id 
         join entity_master ent on ent.entity_id =sms.entity_id  
         join employee_master em on em.employee_code=sms.creator_id 
         join system_table_two stt1 on stt1.component_code=pch.branch_id and stt1.group_code='BRNCOD' 
         join system_table_two stt2 on stt2.component_code=pch.specialization_id and stt2.group_code='SPCLCD' 
             
         where sms.course_code =%s  and ent.entity_type in ('FAC','DEP') and pm.program_id=%s 
         
         and sms.semester_start_date between %s and 
         %s group by sms.program_course_key 
         order by sms.entity_id ;

    """
    params = (subject,pgmid, ssd, sed)
    return fetch_query(query, params, True)



def get_total_marks( ssd, sed, coursecode, empid, pck):
    query = """
    select sms.roll_number,sms.total_marks 
    from student_marks_summary sms 
    join employee_master em on em.employee_code=sms.creator_id 
    where sms.semester_start_date between %s and %s 
    and sms.course_code= %s and sms.creator_id = %s 
    and sms.program_course_key=%s
    """
    params = (ssd, sed, coursecode, empid, pck)
    return fetch_query(query, params, False)

def fetch_query(query,params=None,dict=False):
    """Fetch results from a query."""
    cursor = None
    results = None
    db=connectDatabase()
    try:
        cursor = db.cursor(dictionary=dict)
        cursor.execute(query,params)

        results = cursor.fetchall()
        print("cursor count", cursor.rowcount)
        return results
    except Error as e:
        print(f"Error: '{e}'")
        return None
    finally:
        if cursor:
            cursor.close()
def get_session():

    query = """
        select concat(substring(start_date,1,4),'-',
             substring(end_date,1,4)) as unvsession 
             from university_master 
             order by start_date desc limit 5

    """
    return fetch_query(query,None,True)

def connectDatabase():
    db=Database("localhost", "appuser", "appuser", "cms_live")
    #db=Database("admission.dei.ac.in", "python", "P~ython@2024", "cms_live")
    db=db.create_connection()
    return db
def getevaluationid(subject,pgmid):
    query = """
    
     select evaluation_id,evaluation_id_name 
        from course_evaluation_component where course_code = %s 
        and  program_id =%s 
        order by  evaluation_id_name  
    
    """
    params = (subject,pgmid)
    return fetch_query(query, params, True)


def getevmarks(ssd,sed,evid,subject,pck):
    query = """

        select roll_number,marks from student_marks sm
        
        where sm.semester_start_date between %s
        and %s and  sm.evaluation_id=%s and sm.course_code=%s	
         and sm.program_course_key=%s;

    """
    params = (ssd,sed,evid,subject,pck )
    return fetch_query(query, params, True)

# def time_fetch_query(query,params=None,dict=False,tag=""):
#     start_time = time.time()
#     returnVal = fetch_query(query, params, dict)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"fetch_query {tag} runtime: {elapsed_time:.6f} seconds")
#     return returnVal