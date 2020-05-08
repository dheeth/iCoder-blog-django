from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from blog.models import Post, Comment

# Create your views here.

def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug = slug).first()
    # Get the comments on the post
    comments = Comment.objects.filter(post=post)
    context = {'post': post, 'comments': comments}
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == "POST":
        blogComment = request.POST.get("blogComment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)

        comment = Comment(blogComment=blogComment, user=user, post=post)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")

    return redirect(f"/blog/{post.slug}") # Redirect the user on same post after comment