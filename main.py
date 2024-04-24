import time
import csv
import mysql.connector
from random import randint
from pprint import pprint
from datetime import datetime

#constants
BARCODE_LENGTH=14
DB_USER="root"
DB_PASSWORD="1234"
DB_DATABASE="omr_data"
DB_HOST="localhost"
PLACEHOLDER_RECORD_TABLE = "studentsPlaceholderData"
BARCODE_RECORD_TABLE = "barcodeData"
BARCODE_GENERATION_COUNT=10

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
        cursor.execute(query)
        print(cursor.statement)
        return cursor.fetchall()[0]
    except Exception as err:
        print("ERROR : Error occured int the dbSelector function : ",err)
        return None


def dbExecutor(query,values,cursor):
    print(">> Into the function of dbExecutor")
    try:
        cursor.execute(query,values)
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


def record_barcode_data(barcode,sno,label,cursor):
    print(">> Into the record barcode data function")
    try:
        insert_query = f"INSERT INTO {BARCODE_RECORD_TABLE} (barcode,barcodeUsedSno,barcodeLabel) VALUES (%s,%s,%s)"
        dbExecutor(insert_query,(barcode,sno,label),cursor)
    except Exception as err:
        print("ERROR : Error occured in the record barcode data function : ",err)


def record_placeholder_data(data,cursor):
    print(">> Into the record placeholder data")
    try:
        insert_query = f"INSERT INTO {PLACEHOLDER_RECORD_TABLE} (slno,degreeWithBranch,candidateName,registerNumber,examDateAndSession,examCentreCode,subjectCode,subjectTitle,questionCode,barCode1,barCode2,barCode3,barCode4,barCode5,barCode6,barCode7,barCode8,barCode9,barCode10) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        insert_values = (data.get("SL.NO"),data.get("DEGREE_WITH_BRANCH"),data.get("CANDIDATE_NAME"),data.get("REGISTER_NUMBER"),data.get("EXAM_DATE_&_SESSION"),data.get("EXAM_CENTER_CODE"),data.get("SUBJECT_CODE"),data.get("SUBJECT_TITLE"),data.get("QUESTION_CODE"),data.get("BARCODE1"),data.get("BARCODE2"),data.get("BARCODE3"),data.get("BARCODE4"),data.get("BARCODE5"),data.get("BARCODE6"),data.get("BARCODE7"),data.get("BARCODE8"),data.get("BARCODE9"),data.get("BARCODE10"))
        dbExecutor(insert_query,insert_values,cursor)
    except Exception as err:
        print("ERROR : Error occured in the record placeholder data : ",err)


def initiate_barcode_generation():
    print(">> Into the initiate barcode generation function")
    try:
        csv_file_path = "studentData.csv"
        f = open(csv_file_path,"r+") 
        csv_reader = csv.DictReader(f)
        index = 0
        start_time = datetime.now()
        print("Start time : ",start_time)
        db_response = db_connector()
        if db_response.get("status") == "success":
            db = db_response.get("db")
            cursor = db.cursor(dictionary=True)
            last_record_data = dbSelector(f"SELECT MAX(sno) AS LAST_ID FROM {PLACEHOLDER_RECORD_TABLE}",cursor)  #to get from another table
            if last_record_data:
                print("last record data : ",last_record_data)
                last_record_id = last_record_data.get("LAST_ID")
                if last_record_id:
                    current_record_id = int(last_record_id)+1
                else:
                    current_record_id = 1
            for index,rows in enumerate(csv_reader):
                row = rows 
            iteration = 0 
            while iteration < 10000:
                print("Iteration : ",iteration)
                pprint(row)
                #db.start_transaction()
                slno = row.get("SL.NO")
                slno_records = dbSelector(f"SELECT * FROM {PLACEHOLDER_RECORD_TABLE} WHERE slno = {slno}",cursor)  #created index for it
                if slno_records:
                    #continue
                    pass
                print("After slno records")
                barcode_generated_count = 0
                while barcode_generated_count < BARCODE_GENERATION_COUNT:
                    barcode = generate_barcode_number()
                    barcode_existence = check_barcode_existence(barcode,cursor)
                    print("BARCODE : ",barcode)
                    while barcode_existence:
                        barcode = generate_barcode_number()
                        barcode_existence = check_barcode_existence(barcode,cursor)  #created index for it
                    barcode_label = f"BARCODE{barcode_generated_count+1}"
                    print(barcode_label, " : ",barcode)
                    row[barcode_label]=barcode
                    barcode_generated_count += 1
                    record_barcode_data(barcode,current_record_id,barcode_label,cursor)
                pprint(row)
                record_placeholder_data(row,cursor)
                iteration+=1
                current_record_id+=1
                db.commit()
            f.close()
        end_time = datetime.now()
        difference = end_time - start_time
        print("Difference is : ",difference)
        print("Difference in seconds : ",difference.seconds)
    except Exception as err:
        print("ERROR :: Error occured in the initiate barcode generation Function : ",err)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    initiate_barcode_generation()
