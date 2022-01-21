from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import ModelForm

from .models import Category, Post, PostImages
from .forms import formPost, formImage, formRegisterUser, formLoginUser

from PIL import Image
import os


# Create your views here.
def logoutUser(request):

    logout(request)
    
    page = "login"
    form = formLoginUser()
    context = {"form":form, "page":page}
    return render(request, "imagegallery/login_register.html", context)

def registerUser(request):
    page = "register"  
    
    if request.method == "POST":
    
        form = formRegisterUser(request.POST)
        if form.is_valid():
            form.save()
        
            user=authenticate(request, username=request.POST["username"], password=request.POST["password1"])
            if user is not None:
                login(request, user)
                return redirect("imagegallery:gallery")
        else:
            context = {"form": form, "page":page}
            return render(request, "imagegallery/login_register.html", context)

    
    form = formRegisterUser()
    context = {"form":form, "page":page}
    return render(request, "imagegallery/login_register.html", context)

def loginUser(request):
    page = "login"
    form = formLoginUser()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user     = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("imagegallery:gallery")
        else:
            context = {"form": form, "message":"Invalid credentials!", "page":page}
            return render(request, "imagegallery/login_register.html", context)

    return render(request, "imagegallery/login_register.html", {"form":form, "page":page})


#VIEW Multiple Images: can be filtered by category, owner
@login_required(login_url='imagegallery:login')
def gallery(request):
    category = request.GET.get('category')
    user     = request.user

    if category == None:
        photos = PostImages.objects.filter(post__category__user=user).order_by('-id')
        filterby = "All"
    else:
        photos = PostImages.objects.filter(post__category__name=category, post__category__user=user).order_by('-id')
        filterby = category
    
    categories  = Category.objects.filter(user=user).order_by('name')
    context = {"categories": categories, "photos": photos, "filter":filterby}
    return render(request, "imagegallery/gallery.html", context)

# VIEW an Image
@login_required(login_url='imagegallery:login')
def photo(request, photo_id):   
    photo = PostImages.objects.get(id=int(photo_id))
    return render(request, "imagegallery/photo.html", {"photo": photo})


# UPLOAD IMAGES
@login_required(login_url='imagegallery:login')
def add(request):
    user = request.user
    
    if request.method == "POST":
        new_category        = request.POST['category_new']
        selected_category   = request.POST['category']
        form = formPost(request.POST, request.FILES, user=request.user) 
                        
        if form.is_valid():
            #check if valid image files
            max_filesize_upload = 3 * 1024 * 1024
            images=request.FILES.getlist('images')
            for image in images:
                try:  
                    img = Image.open(image)
                    img.verify()
                except: 
                    return render(request, "imagegallery/add.html", {"form": form, "image_err_msg":"Invalid image file selected! Try again."})

                
                image.seek(0, os.SEEK_END)
                file_length = image.tell()
                    
                if file_length > max_filesize_upload:
                    return render(request, "imagegallery/add.html", {"form": form, "image_err_msg":"Large image size! Each file should be < " + str(max_filesize_upload/(1024*1024)) + " MB"})

            #retrieve or create new category object
            if selected_category == "" and new_category == "":  
                return render(request, "imagegallery/add.html", {"form": form, "message":"Select a category or type a new category!"})
            if selected_category != "":
                category = Category.objects.get(id=selected_category)
            elif new_category != "":
                category, created = Category.objects.get_or_create(name=new_category, user=request.user)
            else:
                category = None

            #update more info before actually saving to db
            new_post = form.save(commit=False) 
            new_post.owner      = request.user       
            new_post.category   = category
            new_post.save() #gives the new_post.id

            #save the images in a different form 
            if new_post.id != None:  
                for image in images:
                    photo = PostImages.objects.create(
                            post = Post.objects.get(pk=new_post.id),                    
                            images=image,            
                    )

            return redirect("imagegallery:gallery")
        
        else:
            return render(request, "imagegallery/add.html", {"form": form})


    return render(request, "imagegallery/add.html", {
        "form": formPost(user=request.user)
        })
