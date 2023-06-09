from django.shortcuts import render,redirect
from .models import *
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse

def home(request):
    laptops=Product.objects.filter(category='L')
    mobiles=Product.objects.filter(category='M')
    topwears=Product.objects.filter(category='TW')
    bottomwears=Product.objects.filter(category='BW')
    
    return render(request, 'app/home.html',{'laptops':laptops,'mobiles':mobiles,'topwears':topwears,'bottomwears':bottomwears})

class ProductView(View):
    def get(self,request):
        laptops=Product.objects.filter(category='L')
        mobiles=Product.objects.filter(category='M')
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        return render(request,'app/home.html',{'laptops':laptops,'mobiles':mobiles,'topwears':topwears,'bottomwears':bottomwears})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class CustomerRegisterationView(View):
   def get(self,request):
      form=CustomerRegistrationForm()
      return render(request,'app/customerregistration.html',{'form':form})
   def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation! Regestration Successfully !')
            form.save() 
        return render(request,'app/customerregistration.html',{'form':form})



class ProductDetailView(View):
   def get(self,request,pk):
      product=Product.objects.get(pk=pk)
      return render(request,'app/productdetail.html',{'product':product})

def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

def showcart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                temp_amount=(p.quantity*p.product.discounted_price)
                amount=amount+temp_amount
                total_amount=amount+shipping_amount
                
        else:
            return render(request,'app/emptycart.html')
        return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})


def plus_cart(request):
    if request.method=='GET':
        user=request.user
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity=c.quantity+1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        for p in cart_product:
            temp_amount=(p.quantity+p.product_discounted_price)
            amount=amount+temp_amount
            total_amount=amount+shipping_amount
        data={
            'quantity':c.quantity,
            'amount':amount+shipping_amount,
            'totalamount':total_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method=='GET':
        user=request.user
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity=c.quantity-1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        for p in cart_product:
            temp_amount=(p.quantity+p.product_discounted_price)
            amount=amount+temp_amount
            total_amount=amount
        data={
            'quantity':c.quantity,
            'amount':amount+shipping_amount,
            'totalamount':total_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method=='GET':
        user=request.user
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        for p in cart_product:
            temp_amount=(p.quantity+p.product_discounted_price)
            amount=amount+temp_amount
            total_amount=amount
        data={
            
            'amount':amount+shipping_amount,
            'totalamount':total_amount
        }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

class ProfileView(View):
    def get(self,request):
      form=CustomerProfileForm()
      return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulation !! Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form})
    


def address(request):
    data=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'data':data,'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if(data==None):
        mobile=Product.objects.filter(category='M')
    elif(data=='one' or data=='redmi' or data=='apple'):
        mobile=Product.objects.filter(category='M').filter(brand=data)
    elif(data=='below'):
        mobile=Product.objects.filter(category='M').filter(discounted_price__lt=20000)
    elif(data=='above'):
        mobile=Product.objects.filter(category='M').filter(discounted_price__gt=20000)
  
    return render(request,'app/mobile.html',{'mobiles':mobile})


def laptop(request,data=None):
    if(data==None):
        laptop=Product.objects.filter(category='L')
    elif(data=='Asus' or data=='Acer' or data=='Lenovo' or data=='HP'):
        laptop=Product.objects.filter(category='L').filter(brand=data)
    elif(data=='below'):
        laptop=Product.objects.filter(category='L').filter(discounted_price__lt=30000)
    elif(data=='above'):
        laptop=Product.objects.filter(category='L').filter(discounted_price__gt=30000)
  
    return render(request, 'app/laptop.html',{'laptops':laptop})


def topwear(request,data=None):
    if(data==None):
        topwear=Product.objects.filter(category='TW')
    elif(data=='siyaram' or data=='dhruvi' or data=='dennis'):
        topwear=Product.objects.filter(category='TW').filter(brand=data)
    elif(data=='below'):
        topwear=Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
    elif(data=='above'):
        topwear=Product.objects.filter(category='TW').filter(discounted_price__gt=1000)
  
    return render(request, 'app/topwear.html',{'topwears':topwear})


def bottomwear(request,data=None):
    if(data==None):
        bottomwear=Product.objects.filter(category='BW')
    elif(data=='allen' or data=='peter'):
        bottomwear=Product.objects.filter(category='BW').filter(brand=data)
    elif(data=='below'):
        bottomwear=Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
    elif(data=='above'):
        bottomwear=Product.objects.filter(category='BW').filter(discounted_price__gt=1000)
  
    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwear})



# def login(request):
#     return render(request, 'app/login.html')

#def customerregistration(request):
 #   return render(request, 'app/customerregistration.html')

def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount=tempamount+amount
        totalamount=amount+shipping_amount

    return render(request, 'app/checkout.html',{'amount':amount,'add':add,'totalamount':totalamount,'cartitems':cart_items})


