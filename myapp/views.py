from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from .models import Category, Photo
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout
from django.contrib import messages

# Create your views here.

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)

        # if user exists in the database then redirect the user to the gallery app
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.info(request, 'Invalid credentials! Please try again')
            return redirect('loginUser')
    else:
        return render(request, 'loginUser.html')

def logoutUser(request):
    logout(request)
    return redirect('loginUser')
    pass

def main(request):
    category = request.GET.get('category')

    # if category is not selected return all category
    if category == None:
        photos = Photo.objects.all()
    # else return or filter specific selected category
    else:
        photos = Photo.objects.filter(category__name = category)

    categories = Category.objects.all()
    return render(request, 'main.html', {'categories': categories, 'photos': photos})

def photo(request, pk):
    photos = Photo.objects.get(id=pk)

    return render(request, 'photo.html', {'photos': photos})

def deletephoto(request, pk):
    photo = get_object_or_404(Photo, id=pk)
    photo.delete()
    return redirect('main')

def addphoto(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        # checks if the category is none and selects the existing category to the specific selected id
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        # creates a new category 
        elif data['new_category'] != '':
            category = Category.objects.get_or_create(name=data['new_category'])
        else:
            category=None

        #retrieve the Category instance first and then assign it to the Photo object. 
        if isinstance(category, tuple):
            category = category[0]

        #creats a new photo object
        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image
        ) 

        # redirects to the home page after submiting the details 
        return redirect('main')
    
    else:
        return render(request, 'addphoto.html', {'categories': categories})