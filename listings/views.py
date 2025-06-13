### listings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Listing, Category

def home(request):
    listings = Listing.objects.all().order_by('-created_at')[:12]
    categories = Category.objects.all()
    return render(request, 'listings/home.html', {'listings': listings, 'categories': categories})

def add_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES.get('image')
        category_id = request.POST['category']
        contact_phone = request.POST['contact_phone']

        category = Category.objects.get(id=category_id)
        Listing.objects.create(
            title=title,
            description=description,
            price=price,
            image=image,
            category=category,
            contact_phone=contact_phone
        )
        return redirect('home')

    categories = Category.objects.all()
    return render(request, 'listings/add_listing.html', {'categories': categories})

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    listings = Listing.objects.filter(category=category).order_by('-created_at')
    return render(request, 'listings/category_list.html', {'category': category, 'listings': listings})
