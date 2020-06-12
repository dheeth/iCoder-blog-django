from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from blog.models import Post, Comment
from blog.templatetags import extras

# Create your views here.

def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug = slug).first()
    post.views = post.views + 1
    post.save()
    # Get the comments on the post
    comments = Comment.objects.filter(post=post, parent=None) # To count only comments
    replies = Comment.objects.filter(post=post).exclude(parent=None) # To get the replies & used exclude because we want the comments which have some parent to be considered as replies and parent != none gives error
    repDict = {}
    # If the comment gets first reply, it's sno. won't be there in dictionary and then it will be added to the dictionary and if it's the reply after 1 already there, it will simply be added with the existing ones in the same comment no.
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments': comments, 'user': request.user, 'repDict': repDict}
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == "POST":
        blogComment = request.POST.get("blogComment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            # For Normal Comment
            comment = Comment(blogComment=blogComment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            # For Replies
            parent = Comment.objects.get(sno=parentSno)
            comment = Comment(blogComment=blogComment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}") # Redirect the user on same post after comment