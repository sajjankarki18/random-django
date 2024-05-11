from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from .models import Category, Photo
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomCreationForm
from django.contrib.auth.decorators import login_required

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

def registerUser(request):
    form = CustomCreationForm()

    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if password1 == password2:
                user = auth.authenticate(username=username, password=password1)

                if user is not None:
                    login(request, user)
                    return redirect('main') 
                else:
                    messages.info(request,' user already exists!')
                    return redirect('registerUser')
                
            else:
                messages.info(request, 'enter a valid password')    
                return redirect('registerUser')
            
    return render(request, 'registerUser.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('loginUser')
    pass

@login_required(login_url=loginUser)
def main(request):
    user = request.user
    category = request.GET.get('category')

    # if category is not selected return all category
    if category == None:
        photos = Photo.objects.filter(category__user = user)
    # else return or filter specific selected category
    else:
        photos = Photo.objects.filter(category__name = category, category__user = user)

    categories = Category.objects.filter(user=user)
    return render(request, 'main.html', {'categories': categories, 'photos': photos})

@login_required(login_url=loginUser)
def photo(request, pk):
    photos = Photo.objects.get(id=pk)

    return render(request, 'photo.html', {'photos': photos})

def deletephoto(request, pk):
    photo = get_object_or_404(Photo, id=pk)
    photo.delete()
    return redirect('main')

@login_required(login_url=loginUser)
def addphoto(request):
    user = request.user
    categories = user.category_set.all()
    # categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        # checks if the category is none and selects the existing category to the specific selected id
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        # creates a new category 
        elif data['new_category'] != '':
            category = Category.objects.get_or_create(user=user, name=data['new_category'])
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