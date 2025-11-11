from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')
def menu(request):
    return render(request, 'landing_menu.html')
from django.shortcuts import render, redirect
from .models import Reservation
from django.contrib import messages
from django.utils import timezone

def reservation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')

        if name and phone and date and time and guests:
            Reservation.objects.create(
                customer_name=name,
                phone=phone,
                date=date,
                time=time,
                guests=guests,
                status='Pending'
            )
            messages.success(request, "Reservation submitted successfully!")
            return redirect('landing_reservation')

        else:
            messages.error(request, "Please fill all the fields.")

    return render(request, 'landing_reservation.html')

def contact(request):
    return render(request, 'contact.html')










from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not an admin user.")
    return render(request, 'admin_login.html')  # ✅ Must pass request here

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date
from django.db.models import Sum
from .models import MenuItem, Order, Reservation
from .forms import MenuItemForm

# ------------------------
# ADMIN DASHBOARD
# ------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from .models import MenuItem, Order, Reservation

@login_required(login_url='admin_login')
def admin_dashboard(request):
    # Analytics Data
    orders_today = Order.objects.filter(order_date__date=date.today()).count()
    upcoming_reservations = Reservation.objects.filter(date__gte=date.today()).count()
    total_menu_items = MenuItem.objects.count()

    total_revenue = (
        Order.objects.filter(status='Processed')
        .aggregate(Sum('total_price'))['total_price__sum'] or 0
    )

    context = {
        'orders_today': orders_today,
        'upcoming_reservations': upcoming_reservations,
        'total_menu_items': total_menu_items,
        'total_revenue': total_revenue,
    }
    return render(request, 'admin/admin_dashboard.html', context)

# ------------------------
# MENU MANAGEMENT (Modal)
# ------------------------
@login_required(login_url='admin_login')
def menu_list(request):
    items = MenuItem.objects.all().order_by('name')
    return render(request, 'admin/menu_list.html', {'items': items})

@login_required(login_url='admin_login')
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    # Always redirect to menu_list
    return redirect('menu_list')

@login_required(login_url='admin_login')
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
    # Always redirect to menu_list
    return redirect('menu_list')

@login_required(login_url='admin_login')
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.delete()
    return redirect('menu_list')


# ------------------------
# ORDER MANAGEMENT
# ------------------------
@login_required(login_url='admin_login')
def view_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'admin/view_orders.html', {'orders': orders})

@login_required(login_url='admin_login')
def process_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Processed'
    order.save()
    return redirect('view_orders')

@login_required(login_url='admin_login')
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Cancelled'
    order.save()
    return redirect('view_orders')


# ------------------------
# RESERVATION MANAGEMENT
# ------------------------
@login_required(login_url='admin_login')
def view_reservations(request):
    reservations = Reservation.objects.all().order_by('-date', '-time')
    return render(request, 'admin/view_reservations.html', {'reservations': reservations})

@login_required(login_url='admin_login')
def confirm_reservation(request, res_id):
    reservation = get_object_or_404(Reservation, id=res_id)
    reservation.status = 'Confirmed'
    reservation.save()
    return redirect('view_reservations')

@login_required(login_url='admin_login')
def cancel_reservation(request, res_id):
    reservation = get_object_or_404(Reservation, id=res_id)
    reservation.status = 'Cancelled'
    reservation.save()
    return redirect('view_reservations')


# ------------------------
# LOGOUT
# ------------------------

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('admin_login')  # redirect to your login page









from .models import MenuItem, Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from django.db.models import Q
from django.core.paginator import Paginator

def menu_items_view(request):
    """
    Display all menu items with live search and pagination
    """
    # Get all available items for live search dropdown
    all_items = MenuItem.objects.filter(available=True).order_by('name')
    
    # Filter for main display
    menu_items = all_items
    
    # Search functionality for main results
    search_query = request.GET.get('q', '').strip()
    if search_query:
        menu_items = menu_items.filter(
            Q(name__icontains=search_query) | 
            Q(category__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination - 6 items per page
    paginator = Paginator(menu_items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'menu_items': page_obj,
        'all_items': all_items,  # For live search
    }
    return render(request, 'menu_items_view.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import MenuItem, Order
from decimal import Decimal

# 🍽 MENU PAGE
def menu_page(request):
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'menu_items_view.html', {'menu_items': menu_items})


# ➕ ADD TO CART
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    else:
        cart[str(item_id)] = {
            'name': item.name,
            'price': float(item.price),
            'quantity': 1,
        }

    request.session['cart'] = cart
    messages.success(request, f"{item.name} added to your order.")
    return redirect('menu_items_view')


# 🧾 ORDER SUMMARY
def order_summary(request):
    cart = request.session.get('cart', {})
    order_items = []
    total = Decimal('0.00')

    for item_id, details in cart.items():
        subtotal = Decimal(details['price']) * details['quantity']
        total += subtotal
        order_items.append({
            'id': item_id,
            'name': details['name'],
            'price': details['price'],
            'quantity': details['quantity'],
            'subtotal': subtotal
        })

    context = {
        'order_items': order_items,
        'order_total': total
    }
    return render(request, 'order_summary.html', context)


# 🔼 INCREASE QUANTITY
def increase_quantity(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1
    request.session['cart'] = cart
    return redirect('order_summary')


# 🔽 DECREASE QUANTITY
def decrease_quantity(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        if cart[str(item_id)]['quantity'] > 1:
            cart[str(item_id)]['quantity'] -= 1
        else:
            del cart[str(item_id)]
    request.session['cart'] = cart
    return redirect('order_summary')


# 🗑 REMOVE ITEM FROM CART
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
        messages.info(request, "Item removed from your order.")
    return redirect('order_summary')


# ✅ PLACE ORDER
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your order is empty.")
        return redirect('menu_page')

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    # Customer info (simple)
    customer_name = request.POST.get('customer_name', 'Guest')
    phone = request.POST.get('phone', 'N/A')

    # Create order
    order = Order.objects.create(
        customer_name=customer_name,
        phone=phone,
        order_date=timezone.now(),
        total_price=total,
        status='Pending'
    )

    # Add related menu items
    for item_id in cart.keys():
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            order.items.add(menu_item)
        except MenuItem.DoesNotExist:
            pass

    order.save()
    request.session['cart'] = {}
    messages.success(request, "Your order has been placed successfully!")
    return render(request, 'order_success.html', {'order': order})


# 🧾 ADMIN ORDERS VIEW
def admin_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'admin/admin_orders.html', {'orders': orders})
