from django.shortcuts import render, redirect, get_object_or_404
from .models import Listing, Category

def home(request):
    listings = Listing.objects.all().order_by('-created_at')[:12]
    categories = Category.objects.all()
    return render(request, 'listings/home.html', {'listings': listings, 'categories': categories})

def add_listing(request):
    if not request.user.is_authenticated:
        return redirect('login')  # или куда у тебя логин

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES.get('image')
        category_id = request.POST['category']
        contact_phone = request.POST['contact_phone']

        category = get_object_or_404(Category, id=category_id)
        Listing.objects.create(
            title=title,
            description=description,
            price=price,
            image=image,
            category=category,
            contact_phone=contact_phone,
            user=request.user  # если есть поле user в модели
        )
        return redirect('home')

    categories = Category.objects.all()
    return render(request, 'listings/add_listing.html', {'categories': categories})

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'listings/detail.html', {'listing': listing})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    listings = Listing.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'listings/category.html', {'listings': listings, 'category': category, 'categories': categories})


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу логиним пользователя после регистрации
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})