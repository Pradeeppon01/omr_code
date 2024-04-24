import time
import csv
import mysql.connector
import random
from random import randint
from pprint import pprint
from datetime import datetime

#constants
BARCODE_LENGTH=14
DB_USER="rootuser"
DB_PASSWORD="1234"
DB_DATABASE="chrome_extension"
DB_HOST="localhost"
PLACEHOLDER_RECORD_TABLE = "studentsPlaceholderData"
BARCODE_RECORD_TABLE = "barcodeData"
BARCODE_GENERATION_COUNT=10
CSV_FILE_PATH = "studentData.csv"
BATCH="24"
BARCODE_TEMPLATE="1{barcode_no}"
SERIAL_NO_RECORD_TABLE="serialNoData"

def db_connector():
    print(">> Into the function of db connector")
    try:
        db = mysql.connector.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE,
                host=DB_HOST
                )
        return {"db":db,"status":"success"}
    except Exception as err:
        print("ERROR : Error occured in the db connector function : ",err)
        return {"db":None,"status":"error"}


def dbSelector(query,cursor):
    print(">> Into the function of dbSelector")
    try:
        selector_start = datetime.now()
        cursor.execute(query)
        print(cursor.statement)
        result = cursor.fetchone()
        selector_end = datetime.now()
        print("select difference in seconds : ",(selector_end-selector_start).total_seconds()*1000, "Query : ",cursor.statement)
        return result
    except Exception as err:
        print("ERROR : Error occured int the dbSelector function : ",err)
        return None


def dbExecutor(query,values,cursor):
    print(">> Into the function of dbExecutor")
    try:
        executor_start = datetime.now()
        cursor.execute(query,values)
        executor_end = datetime.now()
        print("Execute difference in seconds : ",(executor_end - executor_start).total_seconds()*1000," Query : ",cursor.statement)
        print("Query Executed : ",cursor.statement)
    except Exception as err:
        print("ERROR : Error occured int the dbExecutor function : ",err)


def check_barcode_existence(barcode,cursor):
    print(">> Into the check barcode existence function")
    try:
        query = f"SELECT * FROM {BARCODE_RECORD_TABLE} WHERE barcode = {barcode}"
        results = dbSelector(query,cursor)
        return results
    except Exception as err:
        print("ERROR : Error occured in the check barcode existence ",err)
        return None


def generate_barcode_number():
    print(">> Into the generate Barcode function")
    try:
        return randint(0,10**BARCODE_LENGTH)
    except Exception as err:
        print("ERROR : Error occured in the generate barcode number function : ",err)


def generate_barcode_new_logic(barcode_no):
    print(">> Into the generate barcode new logic")
    try:
        barcode_batch = str(random.randint(10, 99)) + str(random.randint(10, 99))
        random_number = ''.join(str(random.randint(0, 9)) for _ in range(9))
        number = BARCODE_TEMPLATE.format(barcode_no=barcode_no) + BATCH + random_number
        checksum = sum(int(digit) for digit in number) % 10
        number += str(checksum)
        return number
    except Exception as err:
        print("ERROR : Error occured in the generate barcode new logic : ",err)


def record_barcode_data(barcode,sno,label,cursor):
    print(">> Into the record barcode data function")
    try:
        insert_query = f"INSERT INTO {BARCODE_RECORD_TABLE} (barcode,barcodeUsedSno,barcodeLabel) VALUES (%s,%s,%s)"
        dbExecutor(insert_query,(barcode,sno,label),cursor)
    except Exception as err:
        print("ERROR : Error occured in the record barcode data function : ",err)


def record_placeholder_data(data,current_record_id,cursor):
    print(">> Into the record placeholder data")
    try:
        insert_query = f"INSERT INTO {PLACEHOLDER_RECORD_TABLE} (sno,slno,degreeWithBranch,candidateName,registerNumber,examDateAndSession,examCentreCode,subjectCode,subjectTitle,questionCode,barCode1,barCode2,barCode3,barCode4,barCode5,barCode6,barCode7,barCode8,barCode9,barCode10) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        insert_values = (current_record_id,data.get("SL.NO"),data.get("DEGREE_WITH_BRANCH"),data.get("CANDIDATE_NAME"),data.get("REGISTER_NUMBER"),data.get("EXAM_DATE_&_SESSION"),data.get("EXAM_CENTER_CODE"),data.get("SUBJECT_CODE"),data.get("SUBJECT_TITLE"),data.get("QUESTION_CODE"),data.get("BARCODE1"),data.get("BARCODE2"),data.get("BARCODE3"),data.get("BARCODE4"),data.get("BARCODE5"),data.get("BARCODE6"),data.get("BARCODE7"),data.get("BARCODE8"),data.get("BARCODE9"),data.get("BARCODE10"))
        dbExecutor(insert_query,insert_values,cursor)
    except Exception as err:
        print("ERROR : Error occured in the record placeholder data : ",err)


def initiate_barcode_generation():
    print(">> Into the initiate barcode generation function")
    try:
        f = open(CSV_FILE_PATH,"r+") 
        csv_reader = csv.DictReader(f)
        index = 0
        start_time = datetime.now()
        print("Start time : ",start_time)
        db_response = db_connector()
        if db_response.get("status") == "success":
            db = db_response.get("db")
            cursor = db.cursor(dictionary=True)
            print("Database connection time :: ",(datetime.now()-start_time).total_seconds()*1000)
            last_record_data = dbSelector(f"SELECT MAX(sno) AS LAST_ID FROM {PLACEHOLDER_RECORD_TABLE}",cursor)  #to get from another table
            #last_record_data = dbSelector(f"SELECT serialNo as LAST_ID FROM {SERIAL_NO_RECORD_TABLE} WHERE id=1)
            if last_record_data:
                print("last record data : ",last_record_data)
                last_record_id = last_record_data.get("LAST_ID")
                if last_record_id:
                    current_record_id = int(last_record_id)+1
                else:
                    current_record_id = 1
            for index,row in enumerate(csv_reader):
                print("\n"*1)
                print("INDEX : //////// ",index)
                print("\n"*1)
                loop_start = datetime.now()
                pprint(row)
                #db.start_transaction()
                slno = row.get("SL.NO")
                print("Before slno records search ://////////// ",(datetime.now()-loop_start).total_seconds()*1000)
                slno_records = dbSelector(f"SELECT * FROM {PLACEHOLDER_RECORD_TABLE} WHERE slno = {slno}",cursor)  #created index for it
                print("after slno records search ://////////// ",(datetime.now()-loop_start).total_seconds()*1000)
                if slno_records:
                    continue
                print("After slno records")
                barcode_generated_count = 0
                barcode_insert_start = datetime.now()
                print("difference before while barcode start /////// : ",(datetime.now()-loop_start).total_seconds()*1000)
                while barcode_generated_count < BARCODE_GENERATION_COUNT:
                    barcode = generate_barcode_new_logic(barcode_generated_count)
                    barcode_existence = check_barcode_existence(barcode,cursor)
                    print("BARCODE : ",barcode)
                    while barcode_existence:
                        barcode = generate_barcode_number()
                        barcode_existence = check_barcode_existence(barcode,cursor)
                    barcode_label = f"BARCODE{barcode_generated_count+1}"
                    print(barcode_label, " : ",barcode)
                    row[barcode_label]=barcode
                    barcode_generated_count += 1
                    record_barcode_data(barcode,current_record_id,barcode_generated_count,cursor)
                barcode_insert_end = datetime.now()
                print("Barcode insert difference : ",(barcode_insert_end - barcode_insert_start).total_seconds()*1000)
                print("Total time difference till barcode insert difference : ",(datetime.now()-loop_start).total_seconds()*1000)
                after_barcode_insert_start = datetime.now()
                pprint(row)
                record_placeholder_data(row,current_record_id,cursor)
                current_record_id+=1
                after_barcode_insert_end = datetime.now()
                print("After barcode :: ",(after_barcode_insert_end-after_barcode_insert_start).total_seconds()*1000)
                commit_start = datetime.now()
                db.commit()
                commit_end = datetime.now()
                print("Commit difference : ",(commit_end-commit_start).total_seconds()*1000)
                loop_end = datetime.now()
                print("Loop difference :: ",(loop_end-loop_start).total_seconds()*1000)
                #dbExecutor(f"UPDATE {SERIAL_NO_RECORD_TABLE} SET serialNo = {barcode_generated_count} WHERE id = 1")
            f.close()
        end_time = datetime.now()
        difference = end_time - start_time
        print("Difference for whole process : ",difference.seconds)
    except Exception as err:
        print("ERROR :: Error occured in the initiate barcode generation Function : ",err)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()
            

if __name__ == "__main__":
    initiate_barcode_generation()

