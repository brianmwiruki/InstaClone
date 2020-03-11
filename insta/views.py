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