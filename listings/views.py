from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Q

from .models import Listing, Category, Message


def home(request):
    all_listings = Listing.objects.all().order_by('-created_at')
    paginator = Paginator(all_listings, 20)
    page_obj = paginator.get_page(1)  # первая страница

    categories = Category.objects.all()
    return render(request, 'listings/home.html', {'page_obj': page_obj, 'categories': categories})


def listings_ajax(request):
    all_listings = Listing.objects.all().order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_listings, 20)

    try:
        listings_page = paginator.page(page)
    except:
        return JsonResponse({'listings_html': '', 'has_next': False})

    listings_html = render_to_string('listings/listings_partial.html', {'listings': listings_page})

    data = {
        'listings_html': listings_html,
        'has_next': listings_page.has_next()
    }
    return JsonResponse(data)


def add_listing(request):
    if not request.user.is_authenticated:
        return redirect('login')  # или куда у тебя логин

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')
        contact_phone = request.POST.get('contact_phone')

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


@login_required
def conversations_list(request):
    user = request.user
    conversations = Message.objects.filter(Q(sender=user) | Q(recipient=user)).order_by('-timestamp')

    interlocutors = {}
    for msg in conversations:
        if msg.sender == user:
            other = msg.recipient
        else:
            other = msg.sender
        if other.id not in interlocutors:
            interlocutors[other.id] = msg

    return render(request, 'listings/conversations_list.html', {
        'interlocutors': interlocutors.values(),
    })


@login_required
def conversation_detail(request, user_id):
    user = request.user
    other = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            listing_id = request.POST.get('listing_id')
            listing = get_object_or_404(Listing, id=listing_id) if listing_id else None
            Message.objects.create(sender=user, recipient=other, text=text, listing=listing)
            return redirect('conversation_detail', user_id=other.id)

    messages = Message.objects.filter(
        (Q(sender=user) & Q(recipient=other)) | (Q(sender=other) & Q(recipient=user))
    ).order_by('timestamp')

    return render(request, 'listings/conversation_detail.html', {
        'messages': messages,
        'other': other,
        'listing': messages.first().listing if messages.exists() else None,
    })


@login_required
def delete_conversation(request, user_id):
    other = get_object_or_404(User, id=user_id)
    Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other)) |
        (Q(sender=other) & Q(recipient=request.user))
    ).delete()
    return redirect('conversations_list')
