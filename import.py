# from openpyxl import load_workbook
import sqlite3
# import mysql.connector

# #excel
# workbook = load_workbook('รายงานสินค้า.xlsx')
# sheet = workbook.active

# values = []
# #loop ทีละแถว
# for row in sheet.iter_rows(min_row = 2,values_only = True):
#     print(row)
#     values.append(row) 

con = sqlite3.connect('stockdb.db')
cursur = con.cursor()
def status_update():
    search_sql = '''SELECT product_id , amount , status_id FROM app_home_details;'''
    cursur.execute(search_sql)
    result = cursur.fetchall()
    for a in result:
        amount = a[1]
        if amount > 0 :
            update_sql = '''
            UPDATE app_home_details
            set status_id = 1
            WHERE product_id = "{0}";'''.format(a[0])
        if amount <= 0 :
            update_sql = '''
            UPDATE app_home_details
            set status_id = 0
            WHERE product_id = "{0}";'''.format(a[0])
        cursur.execute(update_sql)
        con.commit()
# data = '''
#     INSERT INTO app_home_details (id,product_id,product_name,amount,unit_id)
#     VALUES(?,?,?,?,?);
#     '''
status_update()