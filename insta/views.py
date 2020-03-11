from django.shortcuts import render, get_object_or_404
from .forms import Postform
from django.utils import timezone
from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
import datetime as dt
from .models import Image, Comment, Profile, post
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import NewImageForm, NewCommentForm, ProfileUpdateForm, RegisterForm
from django.contrib import messages
from .email import send_welcome_email

from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
)
# Create your views here.

def home(request):
    date = dt.date.today()
    images = Image.get_images()
    comments = Comment.get_comment()
    
    current_user = request.user 
    if request.method == 'POST':
        form = NewCommentForm(request.POST, auto_id=False)
        img_id = request.POST['image_id']
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = current_user
            image = Image.get_image(img_id)
            comment.image = image
            comment.save()
        return redirect(f'/#{img_id}',)
    else:
        form = NewCommentForm(auto_id=False)

    return render(request, 'index.html', {"date": date, "images":images, "comments":comments, "form": form,})

#registration

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            form.save()
            send_welcome_email(name, email)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account for {username} has been created successfully')
            return redirect('/')
        
    else:
        form = RegisterForm()
    return render(request, 'registration/registration_form.html', {'form':form})

#search functionality
login_required(login_url='/accounts/login/')
def search_images(request):
    if 'keyword' in request.GET and request.GET["keyword"]:
        search_term = request.GET.get("keyword")
        searched_images = Image.search_images(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"images": searched_images})

    else:
        message = "Your search query was empty. Type something to search."
        return render(request, 'search.html', {"message": message})

#get image functionality for display

@login_required(login_url='/accounts/login/')
def get_image(request, id):
    comments = Comment.get_comment()

    try:
        image = Image.objects.get(pk = id)
        
        
    except ObjectDoesNotExist:
        raise Http404()
    
    current_user = request.user 
    if request.method == 'POST':
        form = NewCommentForm(request.POST, auto_id=False)
        img_id = request.POST['image_id']
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = current_user
            image = Image.get_image(img_id)
            comment.image = image
            comment.save()
            return redirect(f'/image/{img_id}',)
    else:
        form = NewCommentForm(auto_id=False)
    
    return render(request, "all_images.html", {"image":image, "form":form, "comments":comments})
    
    
    # image post functionality 

    @login_required(login_url='/accounts/login/')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.Author = current_user
            image.save()
        return redirect('home')

    else:
        form = NewImageForm()
    return render(request, 'new_image.html', {"form": form})



class PostListView(ListView):
    template_name = 'insta/post_list.html'
    queryset = post.objects.all().filter(created_date__lte= timezone.now()).order_by('-created_date')
    context_object_name = 'posts'

class PostCreateView(CreateView):
    template_name = 'insta/post_create.html'
    form_class = Postform
    queryset = post.objects.all()
    success_url = '/'

    def form_valid(self, form):
        print(form.cleaned_data)
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    template_name = 'insta/post_detail.html'
    queryset = post.objects.all().filter(created_date__lte= timezone.now())
    
    def get_object(self):
        id_ = self.kwargs.get('id')

        return get_object_or_404(post, id = id_)