from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from petapp.models import Pet,Cart,Order
from django.db.models import Q
import random
import razorpay









# Create your views here.

def index(request):
    # Fetch user information
    userid = request.user.id
    uname = request.user.username
    print("User id is:", userid)
    print("Username:", uname)
    print("Result is:", request.user.is_authenticated)
    
    # Query active pets
    active_pets = Pet.objects.filter(is_active=True)
    
    # Print active pets
    print(active_pets)
    
    # Pass active pets to the template context
    context = {'products': active_pets}
    
    # Render the template with the context
    return render(request, 'index.html', context)


def catfilter(request, cv):
    q1 = Q(is_active=True)
    q2 = Q(animal_type=cv)  # Adjust this line to match the actual category field
    filtered_pets = Pet.objects.filter(q1 & q2)

    context = {'products': filtered_pets}
    return render(request, 'index.html', context)


def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        #print(userid)
        #print(pid)
        u=User.objects.filter(id=userid)
        print(u[0])
        p=Pet.objects.filter(id=pid)
        print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        print(n)
        context={}
        context['products']=p
        if n==1:
            context['msg']="Product already exists in cart!!"
            return render(request,'Pet_details.html',context)
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product successfully added to Cart!!"
            return render(request,'Pet_details.html',context)
    else:
        return redirect('/login/')



def updateqty(request, qv, cid):
    c = Cart.objects.filter(id=cid)
    if qv == '1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/viewcart') 
        



def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
    np=len(orders)
    context['items']=np
    context['total']=s
    return render(request,'placeorder.html',context)


def remove(request,uid):
    c=Cart.objects.filter(id=uid)
    c.delete()
    return redirect('/viewcart/')


def viewcart(request):
    c = Cart.objects.filter(uid=request.user.id)
    if c:
        print(c[0])
        print(c[0].pid)
        print(c[0].pid.name)
        print(c[0].pid.price)
        s = 0
        for x in c:
            print(x)
            print(x.pid.price)
            s += x.pid.price * x.qty
        print(s)
        np = len(c)
        print(np)
        context = {}
        context['items'] = np
        context['total'] = s
        context['data'] = c
        return render(request, 'viewcart.html', context)
    else:
        # Handle case where cart is empty
        context = {}
        context['items'] = 0
        context['total'] = 0
        context['data'] = []
        return render(request, 'viewcart.html', context)





def contact(request):
    if request.method =='POST':
        contact = contact(
            name = request.POST.get('name'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        contact.save()
    return render(request,'contact.html')


def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        print(uname,":",upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            #print(u.username)
            #print(u.password)
            #print(u.is_superuser)
            if u is not None:
                login(request,u)
                return redirect('/index/')
            else:
                context['errmsg']="Invalid username/password!"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')




    
def ulogout(request):
    logout(request)
    return redirect('/index/')



    
def Pet_details(request,pid):
    p=Pet.objects.filter(id=pid)

    print(p)
    context={}
    context['products']=p
    return render(request,'Pet_details.html',context)




def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        print(uname,upass,ucpass)
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="Pass and confirm pass not matching"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User registered Successfully! Please go ahead and login!"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User already Registered,use a different Id!"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')




def makepayment(request):
    orders = Order.objects.filter(uid=request.user.id)  # Change 'user_id' to 'uid'
    s = 0
    np = len(orders)
    oid = None
    for x in orders:
        s += x.pid.price * x.qty
        oid = x.order_id

    if oid is not None:
        client = razorpay.Client(auth=("rzp_test_4yv05rNMoCMWHU", "lGD9Y2ELi59ujkgr7e5jH5R5"))

        data = {"amount": s * 100, "currency": "INR", "receipt": str(oid)}  # Convert oid to string
        payment = client.order.create(data=data)
        print(payment)
        context = {}
        context['data'] = payment
        uemail = request.user.username
        context['uemail'] = uemail
        return render(request, 'makepayment.html', context)
    else:
        return HttpResponse("Error: No order ID found")




def footer(request):
    return render(request,'footer.html')


def header(request):
    return render(request,'header.html') 


def base(request):
    return render(request,'base.html')


def about(request):
    return render(request,'about.html') 


def Booking(request):
    return render(request,'Booking.html') 


def services(request):
    return render(request,'services.html')     


def Price(request):
    return render(request,'Price.html')         