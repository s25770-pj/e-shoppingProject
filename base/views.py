from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate, get_language
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProductForm, SettingsForm
from .models import Product, Category, Comment, Settings


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "user does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    products = Product.objects.filter(
        Q(category__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    total_products = Product.objects.all().count()

    categories = Category.objects.all()
    product_count = products.count()

    current_language = get_language()

    context = {'products': products, 'categories': categories,
               'product_count': product_count,
               'current_language': current_language,
               'total_products': total_products}
    return render(request, 'base/home.html', context)


def settings_page(request):
    user_settings, created = Settings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            language_code = form.cleaned_data.get('language')
            if language_code in [lang[0] for lang in Settings.LANGUAGE_CHOICES]:
                activate(language_code)
                request.session['django_language'] = language_code
            return redirect('home')
    else:
        form = SettingsForm(instance=user_settings)
    context = {'form': form}
    return render(request, 'base/settings.html', context)


def product(request, pk):
    product_item = Product.objects.get(id=pk)
    product_comments = product_item.comment_set.all().order_by('-created')

    if request.method == 'POST':
        Comment.objects.create(
            user=request.user,
            product=product_item,
            body=request.POST.get('body'),
        )
        return redirect('product', pk=product_item.id)

    context = {'product_item': product_item, 'product_comments': product_comments}
    return render(request, 'base/product.html', context)


@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'base/product_form.html', context)


@login_required(login_url='login')
def update_product(request, pk):
    product_item = Product.objects.get(id=pk)
    form = ProductForm(instance=product_item)

    if request.user != product_item.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product_item)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/product_form.html', context)


@login_required(login_url='login')
def delete_product(request, pk):
    product_item = Product.objects.get(id=pk)

    if request.user != product_item.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        product_item.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': product_item})


@login_required(login_url='login')
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': comment})
