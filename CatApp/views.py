from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from collections import Counter



# Create your views here.
def index(request):
    return render(request,'index.html',{})


def orderplaced(request):
	return render(request,'orderplaced.html',{})	    


def checkstatus(request):
	b_object = Bill.objects.all()
	return render(request,'checkstatus.html',{'b_object':b_object})
	
# Creating Customer Account	
#cleaned_data-->manually match each cleaned_data to its database place and then save the instance to the database not the form
# Creating Customer Account	
def customerRegister(request):
	form =CustomerSignUpForm(request.POST or None)
	if form.is_valid():
		user      = form.save(commit=False)
		username  =	form.cleaned_data['username']
		password  = form.cleaned_data['password']
		user.is_customer=True
		user.set_password(password)
		user.save()
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("ccreate")
	context ={
		'form':form
	}			
	return render(request,'signup.html',context)


# Customer Login
def customerLogin(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user     = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("profile")
			else:
				return render(request,'login.html',{'error_message':'Your account disable'})
		else:
			return render(request,'login.html',{'error_message': 'Invalid Login'})
	return render(request,'login.html')


# customer profile view
def customerProfile(request,pk=None):
	if pk:
		user = User.objects.get(pk=pk)
	else:
		user=request.user
	
	return render(request,'profile.html',{'user':user})


#Create customer profile 
def createCustomer(request):
	form = CustomerForm(request.POST)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		return redirect("profile")
	context={
	'form':form,
	'title':"Complete Your profile"
	}
	return render(request,'profile_form.html',context)


#  Update customer detail
def updateCustomer(request,id):
	form  	 = CustomerForm(request.POST or None,instance=request.user.customer)
	if form.is_valid():
		form.save()
		return redirect('profile')
	context={
	'form':form,
	'title':"Update Your profile"
	}
	return render(request,'profile_form.html',context)


def Logout(request):
    logout(request)
    return redirect('index')


# Showing catering list to Customer
def catering(request):
	r_object = Catering.objects.all()
	
	context={
	'r_object':r_object
	}
	
	return render(request,'catering.html',context)  



# creating catering account
def caterRegister(request):
	form = CateringSignUpForm(request.POST or None)
	if form.is_valid():
		user      = form.save(commit=False)
		username  =	form.cleaned_data['username']
		password  = form.cleaned_data['password']
		user.is_catering=True
		user.set_password(password)
		user.save()
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("rcreate")
	context ={
		'form':form
	}			
	return render(request,'catersignup.html',context)	


# catering login
def caterLogin(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user     = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("rprofile")
			else:
				return render(request,'caterlogin.html',{'error_message':'Your account disable'})
		else:
			return render(request,'caterlogin.html',{'error_message': 'Invalid Login'})
	return render(request,'caterlogin.html')


# restaurant profile view
def cateringProfile(request,pk=None):
	if pk:
		user = User.objects.get(pk=pk)
	else:
		user=request.user
	
	return render(request,'cater_profile.html',{'user':user})

# create catering  detail
@login_required(login_url='/login/catering/')
def createCatering(request):
	form=CateringForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		return redirect("rprofile")
	context={
	'form':form,
	'title':"Complete Your Catering profile"
	}
	return render(request,'cater_profile_form.html',context)

@login_required(login_url='/login/catering/')
def updateCatering(request,id):
	form  	 = CateringForm(request.POST or None,request.FILES or None,instance=request.user.catering)
	if form.is_valid():
		form.save()
		return redirect('rprofile')
	context={
	'form':form,
	'title':"Update Your Catering profile"
	}
	return render(request,'cater_profile_form.html',context)

@login_required(login_url='/login/catering/')
def addMenu(request):
	# form = MenuForm(request.POST or None,request.FILES or None,instance=request.user.catering)
	# if form.is_valid():
	# 	instance = form.save(commit=False)
	# 	catering_instance = Catering.objects.get(user=request.user)
	# 	instance.owner = catering_instance
	# 	instance.save()
	# 	return redirect("mmenu")
	# context={
	# 	'form':form,
	# 	'title':"ADD MENU"
	# }	
	if not request.user.is_authenticated:
		return redirect("rlogin") 

	if request.method == "POST":
		item_name = request.POST['item_name']
		price = request.POST['price']
		catering_instance = Catering.objects.get(user=request.user)
		menu = Menu(item_name = item_name, price=price, owner=catering_instance)
		menu.save()

		return redirect('mmenu')

	else:
		catering_instance = Catering.objects.get(user=request.user)
		menus = Menu.objects.filter(owner = catering_instance)

		return render(request, 'addmenu.html', context  = {'menus' : menus})

@login_required(login_url='/login/catering/delete/')
def delete_menu(request, pk):
     
	menu = Menu.objects.get(pk=pk)
	menu.delete()
	return redirect('mmenu')


def cateringMenu(request, pk=None):
	cater = Catering.objects.get(id=pk)
	item = Menu.objects.filter(owner = cater)
	context = {
		'items' : item,
		'rid' : pk,
		'rname' : cater.catering_name,
		'rinfo' : cater.about_info,
		'rlocation' : cater.location,
		}
	return render(request,'menu3.html',context)

# @login_required(login_url='/login/user/')
# def checkout(request, pk=None):
# 	cater = Catering.objects.get(id=pk)
# 	item = Menu.objects.filter(owner = cater)
# 	context = {
# 	    'item' : item,
# 	    'rid' : pk,
# 	}
# 	return render(request,'order.html')


	

	


	
def orderlist(request):
	if request.POST:
		oid = request.POST['orderid']
		select = request.POST['orderstatus']
		select = int(select)
		order = Bill.objects.filter(id=oid)
		if len(order):
			x = 0
			if select == 1:
				x = Bill.BOOKING_ACCEPTED
			elif select == 2:
				x = Bill.BOOKING_REJECTED
			else:
				x=0
			order[0].status = x
			order[0].save()
				
			
	
			
	orders = Bill.objects.filter(owner_id=request.user.catering.id).order_by('-time')
	corders = []

	for order in orders:

		user = User.objects.filter(id=order.orderedBy.id)
		user = user[0]
		corder = []
		if user.is_catering:
			corder.append(user.catering.catering_name)
			corder.append(user.catering.about_info)
		elif user.is_customer:
			corder.append(user.customer.customer_name)
			corder.append(user.customer.phone)
		items_list = orderItem.objects.filter(bill_id=order)

		items = []
		for item in items_list:
			citem = []
			citem.append(item.item_id)
			citem.append(item.quantity)
			menu = Menu.objects.filter(id=item.item_id.id)
			citem.append(menu[0].price*item.quantity)
			menu = 0
			items.append(citem)

		corder.append(items)
		corder.append(order.total_amount)
		corder.append(order.id)

		x = order.status
		if x == Bill.BOOKING_PENDING:
		    x=0
		elif x == Bill.BOOKING_ACCEPTED:
		    x = 1
		elif x == Bill.BOOKING_REJECTED:
			x = 2
		# else:
		# 	break

		corder.append(x)
		corder.append(order.event_location)
		corders.append(corder)

	context = {
		"orders" : corders,

	}

	return render(request,"order-list.html",context)



@login_required(login_url='/login/user/')
def checkout(request):
	if request.POST:
		addr  = request.POST['address']
		ordid = request.POST['oid']
		Bill.objects.filter(id=int(ordid)).update(event_location = addr)
                                                    
		return redirect('/orderplaced/')
	else:	
		cart = request.COOKIES['cart'].split(",")
		cart = dict(Counter(cart))
		items = []
		totalprice = 0
		uid = User.objects.filter(username=request.user)
		oid = Bill()
		oid.orderedBy = uid[0]
		for x,y in cart.items():
			item = []
			it = Menu.objects.filter(id=int(x))
			if len(it):
				oiid=orderItem()
				oiid.item_id=it[0]
				oiid.quantity=int(y)
				oid.owner=it[0].owner
				oid.save()
				oiid.bill_id =oid
				oiid.save()
				totalprice += int(y)*it[0].price
				item.append(it[0].item_name)
				it[0].quantity = it[0].quantity - y
				it[0].save()
				item.append(y)
				item.append(it[0].price*int(y))
			
			items.append(item)
		oid.total_amount=totalprice
		oid.save()
		context={
			"items":items,
			"totalprice":totalprice,
			"oid":oid.id
		}	
		return render(request,'order.html',context)





    

    	


        








        
