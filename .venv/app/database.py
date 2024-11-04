import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def create_connection(self):
        """Create a database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return self.connection
                print("Successfully connected to the database")
        except Error as e:
            print(f"Error: '{e}'")
            self.connection = None

    def close_connection(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def execute_query(self, query, data=None):
        """Execute a single query."""
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            if cursor:
                cursor.close()

    # def fetch_query(self, query,params=None,dict=False):
    #     """Fetch results from a query."""
    #     cursor = None
    #     results = None
    #     try:
    #         cursor = self.connection.cursor(dictionary=dict)
    #         cursor.execute(query,params)
    #
    #         results = cursor.fetchall()
    #         print("cursor count", cursor.rowcount)
    #         return results
    #     except Error as e:
    #         print(f"Error: '{e}'")
    #         return None
    #     finally:
    #         if cursor:
    #             cursor.close()
    # def get_session(self):
    #
    #     query = """
    #         select concat(substring(start_date,1,4),'-',
    #              substring(end_date,1,4)) as unvsession
    #              from university_master
    #              order by start_date desc limit 5
    #
    #     """
    #     return self.fetch_query(query,None,True)
    #
    # def get_evaluaters(self,subject,ssd,sed):
    #
    #         query = """
    #          select pch.program_course_key,pm.program_name, sms.course_code ,
    #           pch.branch_id,pch.specialization_id,stt1.component_description as brname ,
    #          stt2.component_description as spname ,
    #          sms.creator_id,first_name from student_marks_summary  sms
    #          join program_course_header pch on pch.program_course_key  = sms.program_course_key
    #          join program_master pm on pm.program_id= pch.program_id
    #          join entity_master ent on ent.entity_id =sms.entity_id
    #
    #          join employee_master em on em.employee_code=sms.creator_id
    #          join system_table_two stt1 on stt1.component_code=pch.branch_id and stt1.group_code='BRNCOD'
    #          join system_table_two stt2 on stt2.component_code=pch.specialization_id and stt2.group_code='SPCLCD'
    #          where course_code =%s  and ent.entity_type in ('FAC','DEP')
    #          and sms.semester_start_date between %s and %s group by sms.creator_id,sms.program_course_key
    #          order by sms.entity_id
    #
    #
    #     """
    #         params=(subject,ssd,sed)
    #         return self.fetch_query(query,params,True)
    # def get_total_marks(self,ssd,sed,coursecode,empid,pck):
    #     query = """
    #     select sms.roll_number,sms.total_marks
    #     from student_marks_summary sms
    #     join employee_master em on em.employee_code=sms.creator_id
    #     where sms.semester_start_date between %s and %s
    #     and sms.course_code= %s and sms.creator_id = %s
    #     and sms.program_course_key=%s
    #     """
    #     params=(ssd,sed,coursecode,empid,pck)
    #     return self.fetch_query(query,params,False)
    #



# Example usage
#if __name__ == "__main__":
#    db = Database("localhost", "appuser", "appuser", "cms_live")
#    db.create_connection()

    # Example: Create a table
    #create_table_query = """
    #CREATE TABLE IF NOT EXISTS users (
    #    id INT AUTO_INCREMENT PRIMARY KEY,
    #    name VARCHAR(100) NOT NULL,
    #    age INT NOT NULL
    #);

    #db.execute_query(create_table_query)

    # Example: Insert a user
    #insert_user_query = "INSERT INTO users (name, age) VALUES (%s, %s)"
    #db.execute_query(insert_user_query, ("John Doe", 30))

    # Example: Fetch users


    #users = db.fetch_query(select_session_query)
    #print(users)

    #db.close_connection()
