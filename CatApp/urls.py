from django.urls import path
from . import views


urlpatterns=[
    path('',views.index,name='index'),
    path('register/user/',views.customerRegister,name='register'),
    path('login/user/',views.customerLogin,name='login'),
    path('user/create/',views.createCustomer,name='ccreate'),
    path('profile/user/',views.customerProfile,name='profile'),
    path('user/update/<int:id>/',views.updateCustomer,name='cupdate'),
    path('logout/',views.Logout,name='logout'),
    path('catering/',views.catering,name='catering'),
    path('register/catering/',views.caterRegister,name='rregister'),
    path('login/catering/',views.caterLogin,name='rlogin'),
    path('catering/create/',views.createCatering,name='rcreate'),
    path('catering/update/<int:id>/',views.updateCatering,name='rupdate'),
    path('profile/catering/',views.cateringProfile,name='rprofile'),
    path('catering/menu',views.addMenu,name='mmenu'),
    path('catering/delete/<int:pk>', views.delete_menu, name='delete_menu'),
    path('catering/<int:pk>/',views.cateringMenu,name='menu'),
    path('catering/checkout/',views.checkout,name='checkout'),
    path('orderplaced/',views.orderplaced),
    path('catering/orderlist/',views.orderlist,name='orderlist'),
    path('checkstatus/',views.checkstatus,name='checkstatus'),
]

