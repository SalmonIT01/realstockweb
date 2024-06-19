from django.urls import path
from . import views

urlpatterns = [
    path('',views.sign_in,name='sign_in'),
    path('index',views.index,name="index"),
    path('home',views.home,name='home'),
    path('insert',views.insert,name='insert'),
    path('borrow',views.borrow,name='borrow'),
    path('delete/<product_id>',views.delete,name='delete'),
    path('borrow/<product_id>',views.borrow,name='borrow'),
    path('update/<product_id>',views.update,name='update'),
    path('logging/<des>',views.logging,name='logging'),
    # path('log-out',views.sign_out,name='sign_out')
    
]