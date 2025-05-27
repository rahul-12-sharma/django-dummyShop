import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import SimpleUserCreationForm

API_URL = "https://dummyjson.com/products"


def product_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    # Base API URL
    if category:
        url = f"{API_URL}/category/{category}"
    else:
        url = API_URL

    try:
        response = requests.get(url)
        data = response.json()
        products = data.get('products', [])
    except Exception as e:
        print("Error fetching products:", e)
        products = []

    # Local search filtering (optional)
    if query:
        products = [p for p in products if query.lower() in p['title'].lower()]

    try:
        categories = requests.get(f"{API_URL}/categories").json()
    except Exception as e:
        print("Error fetching categories:", e)
        categories = []

    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': category,
    })



def product_detail(request, product_id):
    product = requests.get(f"{API_URL}/{product_id}").json()
    return render(request, 'products/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = requests.get(f"{API_URL}/{product_id}").json()
    cart = request.session.get('cart', {})

    key = str(product_id)
    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {
            'title': product['title'],
            'price': product['price'],
            'thumbnail': product['thumbnail'],
            'quantity': 1,
        }

    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'products/cart.html', {'cart': cart, 'total': total})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')


def signup_view(request):
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
        else:
            print(form.errors)  # DEBUG: shows why form failed
    else:
        form = SimpleUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
