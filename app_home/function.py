import sqlite3
import datetime

con = sqlite3.connect('stockdb.db')
cursur = con.cursor()

def insert():
    print("INSERT")
    try :
        input_id = input('product id:')
        input_title = input('product name')
        input_unit = input('unit:')
        convert_unit = convert(input_unit)
        input_amount = float(input('amount:'))
        insert_sql = '''INSERT INTO products2 (product_id, product_name,unit_id, amount)
                        VALUES("{0}","{1}","{2}","{3}")'''.format(input_id,input_title,convert_unit,input_amount)
        cursur.execute(insert_sql)
        con.commit()
        des = f"Insert id:{input_id} name:{input_title} unit id:{input_unit} amount:{input_amount}"
        #convert_time()
        log(des)
        status_update()
    except Exception :
        print("Error inserting")
    return input_unit

def search():
    user_input = input('Search:')
    try:
        int(user_input)
        search_sql = '''SELECT p.product_id, p.product_name,  p.amount , u.title_unit, st.status
                        FROM products2 as p
                        LEFT JOIN status as st 
                        ON p.status_id = st.id
                        LEFT JOIN unit_table as u 
                        ON p.unit_id = u.id
                        WHERE p.product_id LIKE "%{0}%"
                        '''.format(user_input)
        
    except :
        search_sql = '''SELECT p.product_id, p.product_name,  p.amount , u.title_unit, st.status
                        FROM products2 as p
                        LEFT JOIN status as st 
                        ON p.status_id = st.id
                        LEFT JOIN unit_table as u 
                        ON p.unit_id = u.id
                        WHERE p.product_name LIKE "%{0}%"
                        '''.format(user_input)

    cursur.execute(search_sql)
    result = cursur.fetchall()
    for n in range(len(result)):
        print(result[n])
       
def showdb():
    db = '''SELECT * 
            FROM products2; '''
    cursur.execute(db)
    product_table = cursur.fetchall()
    print(product_table)
    
def updatedb():
    search()
    input_id = input('select data to update[product id]:')
    input_title = input('product name')
    input_unit = input('unit:')
    input_amount = float(input('amount:'))
    convert_unit = convert(input_unit)
    update_sql = '''
    UPDATE products2
    set product_name= "{0}",unit_id = "{1}", amount= "{2}"
    WHERE product_id = "{3}";
    '''.format(input_title,convert_unit,input_amount,input_id) # unit id ไปใช้ convert
    cursur.execute(update_sql)
    con.commit()
    des = f"Update id:{input_id} name:{input_title} unit id:{input_unit} amount:{input_amount}"
    log(des)
    
def delete():
        deleteuser_input = input('select data to delete[product id]:')
        try:
            userinput_sql = '''SELECT product_id FROM products2'''
            cursur.execute(userinput_sql)
            result = cursur.fetchall()
            list_infomation=[]
            for c in result :
                list_infomation.append(list(c)[0])
            str_information = str(deleteuser_input)
            if str_information in list_infomation :
                bool_input = input("Are you sure you want to delete(Y/N): ")
                if bool_input == "Y" :
                    userInfo_sql = '''SELECT product_name, unit_id, amount FROM products2
                              WHERE product_id LIKE "{0}"  
                    '''.format(deleteuser_input)
                    cursur.execute(userInfo_sql)
                    result = cursur.fetchall()
                    des = f"Delete id:{deleteuser_input} name:{result[0][0]} amount:{result[0][1]} unit_id:{result[0][2]}"
                    log(des)
                    delete_sql = '''
                    DELETE FROM products2
                    WHERE product_id = "{0}" ;
                    '''.format(deleteuser_input)
                    cursur.execute(delete_sql)
                    con.commit()
                    print("Delete complete.")

                    
                elif bool_input == "N" :
                    print("OK system isn't delete your information.")
            else :
                print("Don't have this product id.")

        except :
            print("invalid input must to be integer or don't have in order.")
            delete()
    
            
def convert(cv):

    unitID = '''select id from unit_table
         where title_unit GLOB  "{0}"'''.format(cv)
    cursur.execute(unitID)
    result = cursur.fetchall()
    x= list(result[0])
    return x[0]

def convert_time(p_id):
    sql_date = '''
            select datetime(create_date, 'localtime')
            from products2
            where product_id = "{0}";'''.format(p_id)
    cursur.execute(sql_date)
    date_list = cursur.fetchall()
    datenow = date_list[0][0]
    
    update = '''
          UPDATE products2
          set create_date = '{0}'
          where product_id = {1};
    '''.format(datenow,p_id)
    
    cursur.execute(update)
    con.commit()

def status_update():
    search_sql = '''SELECT product_id , amount , status_id FROM products2'''
    cursur.execute(search_sql)
    result = cursur.fetchall()
    for a in result:
        amount = a[1]
        if amount > 0 :
            update_sql = '''
            UPDATE products2
            set status_id = 1
            WHERE product_id = "{0}";'''.format(a[0])
        if amount <= 0 :
            update_sql = '''
            UPDATE products2
            set status_id = 0
            WHERE product_id = "{0}";'''.format(a[0])
        cursur.execute(update_sql)
        con.commit()
    
def showStatus():
    showItem_sql = ''' SELECT p.product_id, p.product_name,  p.amount , u.title_unit, st.status
                    FROM products2 as p
                    LEFT JOIN status as st 
                    ON p.status_id = st.id
                    LEFT JOIN unit_table as u 
                    ON p.unit_id = u.id
                    WHERE p.status_id = 1;
                    '''
    cursur.execute(showItem_sql)
    result = cursur.fetchall()
    for n in range(len(result)):
        print(result[n])
    
def borrow():
    input_borrow = input("Product id ที่ต้องการยืม : ")
    borrow_sql = ''' SELECT p.product_id, p.product_name,  p.amount , u.title_unit, st.status
                        FROM products2 as p
                        LEFT JOIN status as st 
                        ON p.status_id = st.id
                        LEFT JOIN unit_table as u 
                        ON p.unit_id = u.id
                        WHERE p.product_id LIKE "{0}"'''.format(input_borrow)
    cursur.execute(borrow_sql)
    borrow_list = cursur.fetchall() # list ทุกตัว
    if borrow_list[0][4] == "active" : # เช็คว่า ค่าที่ใส่มา active ไหม
        borrow_amount = float(input("ต้องการยืมเท่าไร : ")) 
        if borrow_amount <= 0: # เช็ค จำนวนที่ใส่ < 0 ไหม
            print("กรุณาใส่เลขมากกว่า 0")
            return None
        new_amount = borrow_list[0][2] - borrow_amount
        if new_amount >= 0 : # เช็ค จำนวนที่ใส่มีมากกว่าในคลังไหม
            while True :
                answer = input("คุณต้องการยืม %s เป็นจำนวน %.2f %s ใช่หรือไม่ (Y/N) : " % (borrow_list[0][1], borrow_amount, borrow_list[0][3]))
                answer = answer.capitalize()
                if answer == "Y" :
                    update_amount_sql = '''UPDATE products2
                                    set amount = "{0}" WHERE product_id = "{1}"
                                    '''.format(new_amount, input_borrow)
                    cursur.execute(update_amount_sql)
                    con.commit()
                    status_update()
                    des = f"Borrow id:{input_borrow} name:{borrow_list[0][1]} borrowed:{borrow_amount} from:{borrow_list[0][2]} remaining:{new_amount}"
                    log(des)
                    break
                elif answer == "N" :
                    print("ยกเลิกการยืม")
                    break
                else :
                    print("โปรดใส่ (Y/N)")
        else:
            print("จำนวนสินค้าไม่เพียงพอตามที่คุณต้องการ")
            
    elif borrow_list[0][4] == "inactive" :
        print("สินค้านี้ไม่พร้อมให้ใช้บริการ")
    else :
        print("ไม่มีสินค้านี้ในคลังสินค้า")
    
def log(des):
    now = datetime.datetime.now()
    des_sql = '''INSERT INTO log (time, descri)
                        VALUES("{0}","{1}")'''.format(now,des)
    cursur.execute(des_sql)
    con.commit()

    
def main():
    print("**---Warehouse management system---**")
    print("1.Search\n2.Insert\n3.Update\n4.Delete\n5.Borrow\n6.Show Status\n7.Show database")
    choose = input("Choose :")
    if choose == "1":
        search()
        main()
    elif  choose == "2":
        insert()
        main()
    elif  choose == "3":
        updatedb()
        main()
    elif  choose == "4":
        delete()
        main()
    elif  choose == "5":
        borrow()
        main()
    elif  choose == "6":
        showStatus()
        main()
    elif  choose == "7":
        showdb()
        main()
    else:
        print("Invalid choice")
        main()

# main()  
# search()  
# showdb()  
# insert()  
# updatedb()
# status_update()
# delete()
# showStatus()
# borrow()
from .models import Details
def update_status():
    dt = Details.objects.all()
    print(dt)

update_status()    
