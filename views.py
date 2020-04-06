from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



# Create your views here.


def home(request):
   content = {
                'posts': Post.objects.all() 
             }
   #return HttpResponse("This is home page of Django Project")
   return render(request, 'blog/home.html', content)
   
# To List out all the post in home page  
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' # to list out all the post in home page
    ordering =  ['-date_posted'] # to order the post from newest to oldest

#To go to the detail of the post/blog    
class PostDetailView(DetailView):
    model = Post

#To create a new blog post 
#'LoginRequiredMixin' mixin is used to check if the user is logged in then only can create a post/blog 
# The paramets to the class has be in the same order
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
 
#To update an existing post 
#'LoginRequiredMixin' mixin is used to check if the user is logged in then only can update a post/blog
#'UserPassesTestMixin' mixin is used to see if the user is author of the post before modifying the post.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    # Create a function to check if the current login user is the author of the post/blog
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        else:
            return False
    

#To delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post 
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        else:
            return False
    
def about(request):

   #return HttpResponse("This is about a new Django Project")
   return render(request, 'blog/about.html', {'title': 'About'})