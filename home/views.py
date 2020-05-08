from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')  

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form Correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Message Sent Successfully")
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query) # icontains is the django search feature to get the posts which has the title matching with query
        allPostsContent = Post.objects.filter(content__icontains=query) # shows the results if the query matches in content of post too
        allPosts = allPostsTitle.union(allPostsContent) # merged title and content querysets
    if allPosts.count() == 0:
        messages.warning(request, "No search results matching your query")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for wrong inputs
        if len(username) > 15:
            messages.error(request, "Username must be less then 15 characters")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username should have letters and numbers only")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1) # Django inbuilt model
        myuser.first_name = fname # We will add these 2 things
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password, Please try again")
            return redirect('home')
    else:
        return HttpResponse("404 - Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')