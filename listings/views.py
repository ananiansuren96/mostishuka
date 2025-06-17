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
from .forms import ListingForm  # Форма для добавления/редактирования объявлений


def home(request):
    all_listings = Listing.objects.all().order_by('-created_at')
    paginator = Paginator(all_listings, 20)
    page_obj = paginator.get_page(request.GET.get('page', 1))

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


@login_required
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('home')
    else:
        form = ListingForm()

    categories = Category.objects.all()
    return render(request, 'listings/add_listing.html', {'form': form, 'categories': categories})


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
        other = msg.recipient if msg.sender == user else msg.sender
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


@login_required
def user_listings(request):
    listings = Listing.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'listings/user_listings.html', {'listings': listings})


@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, user=request.user)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('user_listings')
    else:
        form = ListingForm(instance=listing)

    return render(request, 'listings/edit_listing.html', {'form': form})

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, user=request.user)
    if request.method == 'POST':
        listing.delete()
        return redirect('user_listings')
    return render(request, 'listings/delete_listing_confirm.html', {'listing': listing})