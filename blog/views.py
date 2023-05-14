from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .models import Blog, Tag, Category, Comment, Reply
from .forms import TextForm, AddBlogForm 
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from .models import User
from .slugs import generate_unique_slug

def home(request):
    blogs = Blog.objects.order_by('-created')
    tags = Tag.objects.order_by('-created')
    context = {"blogs": blogs,"tags": tags}
    return render(request,'home.html',context)

def blogs(request):
    queryset = Blog.objects.order_by('-created')
    tags = Tag.objects.order_by('-created')
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,2)

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {"blogs": blogs,"tags": tags, "paginator": paginator}
    return render(request, 'blogs.html',context)

def category_blogs(request,slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blogs.all()
    tags = Tag.objects.order_by('created')[:4]
    page = request.GET.get('page',1)
    paginator = Paginator(queryset, 2)
    recentblogs = Blog.objects.order_by('-created')[:5]

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {"blogs": blogs, "tags": tags, "recentblogs": recentblogs}
    return render(request, 'category_blogs.html',context)

def tag_blogs(request,slug):
    tags = get_object_or_404(Tag, slug=slug)
    queryset = tags.tag_blogs.all()
    tags = Tag.objects.order_by('created')[:4]
    page = request.GET.get('page',1)
    paginator = Paginator(queryset, 2)
    recentblogs = Blog.objects.order_by('-created')[:5]

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {"blogs": blogs, "tags": tags, "recentblogs": recentblogs}
    return render(request, 'tag_blogs.html',context)

def blog_details(request,slug):
    form = TextForm()
    blog = get_object_or_404(Blog, slug=slug)
    liked_by = request.user in blog.likes.all()
    category = Category.objects.get(id = blog.category.id)
    related_blogs = category.category_blogs.all()
    tags = Tag.objects.order_by('created')[:4]

    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(user = request.user, blog_comment = blog, text = form.cleaned_data.get('text'))
            return redirect('blog_details', slug=slug)        

    context = {"blog": blog, "related_blogs": related_blogs, "tags": tags, "form": form, "liked_by" : liked_by}
    return render(request, 'blog_details.html', context)

@login_required(login_url='login_user')
def add_reply(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                blog_reply=comment,
                text=form.cleaned_data.get('text')
            )
    return redirect('blog_details', slug=blog.slug)

@login_required(login_url='login_user')
def likeblog(request,pk):
    blog = get_object_or_404(Blog,pk=pk)
    context = {}

    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] = False
        context['like_count'] = blog.likes.all().count()
    else:
        blog.likes.add(request.user)
        context['liked'] = True
        context['like_count'] = blog.likes.all().count()
    
    return JsonResponse(context, safe = False)

def search_blogs(request):
    search_key = request.GET.get('search',None)
    recent_blogs = Blog.objects.order_by('-created')
    tags = Tag.objects.order_by('-created')

    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains = search_key) |
            Q(category__title__icontains = search_key) |
            Q(user__username__icontains = search_key) |
            Q(tags__title__icontains = search_key)
        ).distinct()

        context = {"blogs": blogs, "recent_blogs": recent_blogs, "tags": tags, "search_key": search_key}
        return render(request, 'search.html',context)
    
    else :
        return redirect('home')

@login_required(login_url='login_user')    
def myblogs(request):
    queryset = request.user.user_blogs.all() 
    page = request.GET.get('page',1)
    paginator = Paginator(queryset, 6)
    delete = request.GET.get('delete',None)

    if delete:
        blog = get_object_or_404(Blog,pk = delete)
        if request.user.pk != blog.user.pk:
            return redirect('home')
        blog.delete()
        messages.success(request, "blog has been deleted")
        return redirect('myblogs')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {"blogs": blogs,  "paginator": paginator}
    return render(request, 'myblogs.html', context)

@login_required(login_url='login')
def addblogs(request):
    form = AddBlogForm()

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)      
           
            messages.success(request, "Blog added successfully")
            return redirect('blog_details', slug=blog.slug)
        else:
            print(form.errors)

    context = {
        "form": form
    }
    return render(request, 'addblogs.html', context)

def updateblogs(request,slug):
    blog =  get_object_or_404(Blog, slug = slug)
    form = AddBlogForm(instance = blog)

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES, instance = blog)
        if form.is_valid():
            if request.user.pk != blog.user.pk:
                return redirect('home')
            
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                title__iexact=tag.strip(),
                slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                     if tag != '':
                        new_tag = Tag.objects.create(
                        title=tag.strip(),
                        slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)      
                
            messages.success(request, "Blog Updated successfully")
            return redirect('blog_details', slug=blog.slug)
        else:
            print(form.errors)

    context = {"form": form, "blog": blog}
    return render(request, 'updateblogs.html',context)
