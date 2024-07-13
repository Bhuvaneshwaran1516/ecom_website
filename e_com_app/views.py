from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
import json
import paypalrestsdk
from e_com_app.models import Category,Product,Cart,CartItem,Favorite,Order,OrderItem,ShippingAddress
from e_com_app.forms import CustomUserForm,ShippingAddressForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import e_com_app.paypal_config

def profile_view(request):
    # Example user data
    user_data = {
        
    }
    return render(request, 'nav.html', {'user': user_data})
# myapp/views.py


def login(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method=='POST':
            user=request.POST.get('user')
            pwd=request.POST.get('password')
            user=authenticate(request,username=user,password=pwd)
            if user is not None:
                auth_login(request,user)
                messages.success(request,'Login Successfully')
                return redirect('/home')
            else:
                messages.error(request,'Invalid user name and password.')
                
        return render(request,'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logout Successfully')
    return redirect('/home')

def reg(request):    
    if request.method=='POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            name=request.POST["username"]
            email=request.POST["email"]
            password1=request.POST["password1"]
            password2=request.POST["password2"]
            if password1==password2:
                user=User.objects.create_user(username=name,email=email,password=password1)
                # user.is_staff=True
                # user.is_superuser=True
                user.save()
                messages.success(request,"Register Successfully and you can login...")
                return redirect('/login')
            else:
                messages.warning(request,'Password Mismatch...')
    else:
        form=CustomUserForm()
        
    return render(request,'reg.html',{'forms':form})


def home(request):
    products=Product.objects.filter(trending=1)   
    return render(request,'home.html',{'view':products})


def category(request):
    category=Category.objects.filter(status=0)
    return render(request,'product/category.html',{'category':category})

def categoryview(request,name):
    if(Category.objects.filter(name=name,status=0)):
        
        products=Product.objects.filter(category__name=name)
        return render(request,'product/product.html',{'product':products,'category':name})
    else:
        return redirect('/category')
    


def product_details(request,cname,pname):
   
        if(Category.objects.filter(name=cname,status=0)):
          if(Product.objects.filter(name=pname,status=0)):
              products=Product.objects.filter(name=pname,status=0).first()
              return render(request,'product/product_details.html',{'product':products,'category':cname })
          else:
              
              return redirect('/category')
        else:
            messages.warning(request,'No such Category found..')
            return redirect('/category')
   

        


def addtocart(request,product_id):
    if request.user.is_authenticated:
        product=get_object_or_404(Product,id=product_id)
        cart,created=Cart.objects.get_or_create(user=request.user)
        cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product)         

            
        
        if not created:
            if cart_item.product_quantity < product.quantity:
                cart_item.product_quantity += 1
                cart_item.save()
                messages.success(request, f"{product.name} Successfully added to cart.") 
            else:
                messages.error(request,'Not enough stock')
        else:
            if product.quantity >0:
                cart_item.product_quantity=1
                cart_item.save()
                messages.success(request, f"{product.name} Successfully added to cart.")
            else:
                messages.success(request,'Product out of stock')
        return redirect('/view_cart')
    else:
        
        messages.success(request,'LOGIN AND ADD TO CART..')        
        return redirect('/login')
    
def remove_cart(request,product_id):
    
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.product_quantity > 1:
        cart_item.product_quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    messages.success(request, f"{product.name} removed from cart.")

    return redirect('/view_cart')


def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'nav.html', {'cart': cart})

    
    

def view_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.total_price() for item in cart_items)   

        for item in cart_items:
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                quantity = int(quantity)
                if 1 <= quantity <= item.product.quantity:
                    item.product_quantity = quantity
                    item.save()
                
                else:
                    messages.error(request, 'Invalid quantity for item: {item.product.name}')
    else:
        messages.success(request,'Login and see Cart')
        return redirect('/login')      
    return render(request,'cart/view_cart.html',{'cart': cart,'cart_items': cart_items,'total':total,})

def show_cart(request,product_id):
    product = get_object_or_404(Product, id=product_id)  
    return render(request,'cart/show_cart.html',{'product':product})





def add_to_favorites(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if created:
            messages.success(request, 'Product added to favorites list.')
        else:
            messages.error(request, 'Product is already in favorites list.')
        return redirect('/favorites')
    else:
        messages.success(request,'Login and add to favorite.')
        return redirect('/login')

def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite = Favorite.objects.filter(user=request.user, product=product).first()
    if favorite:
        favorite.delete()
        messages.success(request, 'Product removed from favorites list.')
    else:
        messages.info(request, 'Product is not in favorites list.')
    return redirect('/favorites')

def view_favorites(request):
    if request.user.is_authenticated:
    
        favorites = Favorite.objects.filter(user=request.user)
        return render(request,'favorites/view_favorites.html',{'favorites': favorites})
    else:
        messages.success(request,'Login and see favorites')
        return redirect('/login')

   
  

def show_favorites(request,product_id):
    product = get_object_or_404(Product, id=product_id)  
    return render(request,'favorites/show_favorites.html',{'product':product})


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.quantity < 1:
        messages.error(request, 'This product is out of stock.')
        return redirect('/product_details')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > product.quantity:
            messages.error(request, 'Not enough stock for the quantity requested.')
            return redirect('/product_details')       
       

        # Create the order
        order = Order.objects.create(user=request.user,total_price=product.selling_price * quantity)        
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.selling_price)

        # Update product stock
        product.quantity -= quantity
        product.save()

         # Create PayPal payment
        payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": request.build_absolute_uri(f'/payment-success/?order_id={order.id}'),
                    "cancel_url": request.build_absolute_uri('/payment_cancel')
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": product.name,
                            "sku": "item",
                            "price": str(order.total_price),
                            "currency": "USD",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(order.total_price),
                        "currency": "USD"
                    },
                    "description": f"Order for {product.name}"
                }]
            })

        if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        # Redirect the user to PayPal for payment approval
                        approval_url = link.href
                        return redirect(approval_url)
        else:
                print(payment.error)


        

    return render(request, 'order/buy_now.html', {'product':product})




def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    order_id = request.GET.get('order_id')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Payment was successful
        order = get_object_or_404(Order, id=order_id)
        order.status = 'Paid'
        order.save()
        messages.success(request,'Payment Successfully,Order Placed')        
        return redirect('order_summary', order_id=order.id)
    else:
        # Payment failed
        messages.error(request,'The payment error...')
        return render(request, 'order/buy_now.html')


def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    return render(request, 'order/order_summary.html', {'order': order})

def order_summary_pdf(request, order_id):
    # Get the order object
    order = get_object_or_404(Order, id=order_id)
    addresses = order.user.shippingaddress_set.all()
    address = addresses[0] if addresses else None
    
    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.id}_summary.pdf"'
    
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    
    # Set title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, f"Order Summary for Order ID: {order.id}")
    
    # Set font for order details
    p.setFont("Helvetica", 12)
    
    # Order details
    p.drawString(50, 730, f"Customer Name: {order.user.username}")
    p.drawString(50, 710, f"Order Date: {order.order_date}")
    p.drawString(50, 690, f"Delivery Date: {order.delivery_date}")
    p.drawString(50, 670, f"Created At: {order.created_at}")

    if address:
        p.drawString(50, 640, "Shipping Address:")        
        p.drawString(50, 620, f"{address.address_line_1} {address.address_line_2},")
        p.drawString(50, 600, f"{address.city}, {address.state}, ({address.postal_code})")
        p.drawString(50, 580, f"Phone No: {address.phone_number}")
    
    
    
    # Add additional order information here if needed
    # e.g., p.drawString(100, 630, f"Additional Info: {order.additional_info}")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 500, f" Product Details")
    p.setFont("Helvetica", 12)

    
    for item in order.items.all():
        p.drawString(50, 480, f" Total Quantity : {item.quantity}")
        p.drawString(50, 460, f" Product Name: {item.product.name}")
        p.drawString(50, 440, f" Original price:  { item.product.original_price } ")
        p.drawString(50, 420, f" Discount: { item.product.discount } ")
        p.drawString(50, 400, f" After Discount Price: { item.product.selling_price} ")
        
    
    p.drawString(200, 370, f"Total Amount: {order.total_price }")
    p.setFont("Helvetica-Bold", 14)
    p.drawString(170, 300, f"THANK YOU FOR PURCHASING...")
    
    
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    
    return response

def payment_cancel(request):
    messages.error(request,'Payment Cancel,Try Again...')
    return redirect('/view_cart')




def order_list(request):
    if request.user.is_authenticated:

        orders = Order.objects.filter(user=request.user)
        return render(request, 'order/order_list.html', {'orders':orders})
    else:
        messages.success(request,'Login and see order')
        return redirect('/login')


def search(request): 
    if request.method=='POST':
        searched=request.POST['searched']
        searched=Product.objects.filter( Q(name__icontains=searched) |  Q(description__icontains=searched) )
        if not searched:
            messages.success(request,'That product does not exist... please try again..')
            return render(request,'search/search.html')
        else:
            return render(request,'search/search.html',{'searched':searched})

    else:
        return render(request,'search/search.html')
    
def view_search(request,product_id):
    product = get_object_or_404(Product, id=product_id)  
    return render(request,'search/view_search.html',{'product':product})  

    

def add_shipping_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            messages.success(request,'Shipping Address Added')
            return redirect('/home')  # Redirect to a profile page or any other page
    else:
        form = ShippingAddressForm()
    return render(request, 'order/add_shipping_address.html', {'form': form})

def edit_shipping_address(request, address_id):
    shipping_address = ShippingAddress.objects.get(id=address_id)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            form.save()
            messages.success(request,'Shipping Address Update')
            return redirect('/home')  # Redirect to a profile page or any other page
    else:
        form = ShippingAddressForm(instance=shipping_address)
    return render(request, 'order/edit_shipping_address.html', {'form': form})


