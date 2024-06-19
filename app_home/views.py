from django.contrib.auth import authenticate
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .models import Details,Unit,logDetails
from django.core import serializers
from django.shortcuts import get_object_or_404
from .froms import VenueFrom
from django.contrib  import messages
import datetime
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users,admin_only


# from function import*
# Create your views here.
def home(request):
    return render(request,'app_home/home.html')

@login_required()
def index(request):
    uppdata_status()
    data = Details.objects.all().select_related('unit')
    dataunit= Unit.objects.all()
    
    group = request.user.groups.all()[0].name
    if group == 'member':
        user_type = False
    if group == 'admin':
        user_type = True
    context = {
            'data': data,
            'dataunit':dataunit,
            'checkuser':user_type,
            'grouptype':group}
    return render(request, 'app_home/index.html', context)

@login_required() 
@admin_only
def insert(request):
    msg=""
    if "insert" in request.POST:
        try:
            product_id = int(request.POST.copy().get('product_id'))
            product_name = request.POST.copy().get('product_name')
            unit_name = request.POST.copy().get('unit_name')
            unit_id = unit_convert (unit_name)
            amount = int(request.POST.copy().get('amount'))
            status_id = request.POST.copy().get('status_id')
            if amount < 0 :
                msg = "กรุณากรอกจำนวนให้ถูกต้อง"
            elif product_id < 0: #เพิ่มอันนี้
                msg = "กรุณากรอกไอดีให้ถูกต้อง"
            else :
                studentcode = request.user.username
                des = f"insert the id : {product_id} ,name : {product_name} ,unit : {unit_name} ,amount : {amount} ,status : {status_id}"
                logging(studentcode,des)
                msg = "สำเร็จ"
                obj = Details()
                obj.product_id = str(product_id)
                obj.product_name = product_name
                obj.unit_id = unit_id
                obj.amount = float(amount)
                obj.status_id = status_id
                obj.save()
                
        except:
            msg = 'ไอดีสินค้าซ้ำ'
            
    
    dataunit= Unit.objects.all()
    context = {'dataunit':dataunit,
                'msg' : msg}
    return render(request, 'app_home/insert.html', context)
 

def uppdata_status():
    data = Details.objects.all()
    for x in data:
        if x.amount <= 0 :
            x.status_id = 0
            x.save()
@login_required
@admin_only
def delete (request,product_id):
    dele  = Details.objects.get(product_id=product_id)
    studentcode = request.user.username
    des = f"delete the id : {dele.product_id}, name : {dele.product_name}"
    logging(studentcode,des)
    dele.delete()
    return redirect("index")

def unit_convert (unit_name_user):
    unit_con = Unit.objects.get(unit_name = unit_name_user)
    unit_num = unit_con.unit_id
    return unit_num


@login_required()
def borrow(request,product_id):
    venue  = Details.objects.get(product_id=product_id)
    unit_title = unit_convert_num(venue.unit_id) 
    msg =""
    if "borrow" in request.POST:
        amount_borrow = float(request.POST.copy().get('amount_borrow'))
        print("test1")
        if amount_borrow > venue.amount:
            msg = "สินค้าไม่เพียงพอ"
        elif amount_borrow <= 0 :
            msg = "กรุณากรอกข้อมูลให้ถูกต้อง"
        else:
            temp_amount = venue.amount
            amount_borrow_new = venue.amount-amount_borrow
            amount_borrow_new = round(amount_borrow_new,1)
            print(amount_borrow)
            venue.amount = amount_borrow_new
            venue.save()
            studentcode = request.user.username
            des = f"borrow the id : {venue.product_id}, name : {venue.product_name} ,จากเดิม {temp_amount} ยืมไป {amount_borrow} คงเหลือ {amount_borrow_new}"
            logging(studentcode,des)
            return redirect('index')
    else:
        pass
    context = {'venue' : venue,
               'unit_title' : unit_title,
               'msg' : msg }
    return render(request, 'app_home/borrow.html',context)

def unit_convert_num (unit_num):
    unit_con = Unit.objects.get(unit_id = unit_num)
    unit_str = unit_con.unit_name
    return unit_str

@login_required()
@admin_only
def update (request,product_id):
    venue  = Details.objects.get(product_id=product_id)
    unit_title = unit_convert_num(venue.unit_id)  
    msg=""
    if "update" in request.POST:
        try:
            p  = Details.objects.get(product_id=product_id)
            tmp_product_id = p.product_id
            tmp_product_name = p.product_name
            tmp_unit_name = unit_title
            tmp_amount = p.amount
            tmp_status_id = p.status_id  # เก็บค่าเก่า
            p.product_id= request.POST.copy().get('product_id')
            p.product_name= request.POST.copy().get('product_name')
            unit_name = request.POST.copy().get('unit_name')
            p.unit_id = unit_convert (unit_name)
            p.amount= request.POST.copy().get('amount')
            p.status_id= request.POST.copy().get('status_id')
            if float(p.amount) < 0 :
                msg = "กรุณากรอกจำนวนให้ถูกต้อง"
            elif int(p.product_id) < 0: #เพิ่มอันนี้
                msg = "กรุณากรอกไอดีให้ถูกต้อง"
            elif float(p.amount) >= 0 :
                print('test3')
                studentcode = request.user.username
                des = f"update จาก id : {tmp_product_id}, name : {tmp_product_name}, unit : {tmp_unit_name}, amount : {tmp_amount}, status : {tmp_status_id} เป็น id : {p.product_id}, name : {p.product_name}, unit : {unit_name}, amount : {p.amount}, status : {p.status_id}"
                logging(studentcode,des)
                p.save()
                return redirect("index")       
        except:
            msg = "ไอดีสินค้าซ้ำ"
    dataunit= Unit.objects.all()
    context = {
        'venue' : venue,
        'unit_title':unit_title,
        'dataunit':dataunit,
        'msg' : msg       
     }
    return render(request, 'app_home/update.html',context)

def logging (studentcode,des):
    des1 = f"logging {studentcode} {des}"
    now = datetime.datetime.now()
    obj = logDetails()
    obj.time = now
    obj.descri = des1
    obj.save()
    data = logDetails.objects.all().select_related()
    context = {
            'data': data,
        }
    return(context) 

def sign_in(request):
    logout(request)
    if request.method == "POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, 
            username=username, 
            password=password
        )

        if user is not None:
            # Log user in
            login(request, user)
            return redirect('index')
        
        else:# return error message
            messages.error(request, 'Invalid login')
      
    return render(request,'app_home/sign_in.html')
 

    

    


