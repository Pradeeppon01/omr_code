import time
import csv
from pprint import pprint
from datetime import datetime
from database_connection import db_connector
from trigger_barcode_Gen import dbSelector,dbExecutor,dbSelectAll
from constants import *

def initiate_qr_generation():
    print(">> Into the initiate qr generation function")
    try:
        db_response = db_connector()
        if db_response.get("status") == "success":
            db = db_response.get("db")
            cursor = db.cursor(dictionary=True)
            results = dbSelectAll(f"SELECT * FROM {PLACEHOLDER_RECORD_TABLE}",cursor)
            data_dict = {}

            for index, dbData in enumerate(results):
                formatted_data = {
                    'SNO': dbData.get('sno', ''),
                    'SL_NO': dbData.get('slno', ''),
                    'DEGREE_WITH_BRANCH': dbData.get('degreeWithBranch', ''),
                    'CANDIDATE_NAME': dbData.get('candidateName', ''),
                    'REGISTER_NUMBER': dbData.get('registerNumber', ''),
                    'EXAM_DATE_&SESSION': dbData.get('examDateAndSession', ''),
                    'EXAM_CENTER_CODE': dbData.get('examCentreCode', ''),
                    'SUBJECT_CODE': dbData.get('subjectCode', ''),
                    'SUBJECT_TITLE': dbData.get('subjectTitle', ''),
                    'QUESTION_CODE': dbData.get('questionCode', ''),
                    'BARCODE1': dbData.get('barCode1', ''),
                    'BARCODE2': dbData.get('barCode2', ''),
                    'BARCODE3': dbData.get('barCode3', ''),
                    'BARCODE4': dbData.get('barCode4', ''),
                    'BARCODE5': dbData.get('barCode5', ''),
                    'BARCODE6': dbData.get('barCode6', ''),
                    'BARCODE7': dbData.get('barCode7', ''),
                    'BARCODE8': dbData.get('barCode8', ''),
                    'BARCODE9': dbData.get('barCode9', ''),
                    'BARCODE10': dbData.get('barCode10', ''),
                    'QRCODE1': dbData.get('qrCode1', ''),
                    'QRCODE2': dbData.get('qrCode2', ''),
                    'QRCODE3': dbData.get('qrCode3', ''),
                    'QRCODE4': dbData.get('qrCode4', ''),
                    'QRCODE5': dbData.get('qrCode5', ''),
                    'QRCODE6': dbData.get('qrCode6', ''),
                    'QRCODE7': dbData.get('qrCode7', ''),
                    'QRCODE8': dbData.get('qrCode8', ''),
                    'QRCODE9': dbData.get('qrCode9', ''),
                    'QRCODE10': dbData.get('qrCode10', '')
                }
                data_dict[index] = formatted_data
            print(data_dict)
    except Exception as err:
        print("ERROR :: Error occured in the initiate qr generation Function : ",err)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()
            

if __name__ == "__main__":
    initiate_qr_generation()


