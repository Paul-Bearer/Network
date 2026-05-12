from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.core.paginator import Paginator

# need to be logged in to like 

def index(request):
    all_posts = Post.objects.all().order_by('-time')
    try:
        filtered_likes = Like.objects.filter(
        source = request.user
    )
    except: 
        filtered_likes = []

    liked_post = []
    for i in filtered_likes:
        post_content = i.target.id
        liked_post.append(post_content)
    

    p = Paginator(all_posts, 10)
    print(p.num_pages)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
        

    return render(request, "network/index.html", {
        "posts":page_obj,  # only worked when changed all_posts to page_obj
        "liked_posts":liked_post,
        "page_obj": page_obj
    })



def user_profile_page(request, id):
    # this is the profile of the user you're viewing
    user_profile = User.objects.get(id=id)

    followers = Following.objects.filter(target = user_profile)
    following = Following.objects.filter(source = user_profile)

    posts_by_user = Post.objects.filter(author = user_profile)
    print(posts_by_user)

    try:
        filtered_likes = Like.objects.filter(
        source = request.user
    )
    except: 
        filtered_likes = []

    liked_post = []
    for i in filtered_likes:
        post_content = i.target.id
        liked_post.append(post_content)

    p = Paginator(posts_by_user, 10)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    




    # am i following?
    # in this line here... i couldn't figure out how it would ever change to true... I've always reassigned it later
    # i see that .exists() will change the value from true to false if the relationship exists. 
    # used sopme help to figure this out.. but before I looked for help, but i was on the right track.
    # is_following = False
    # if request.user.is_authenticated:
    #     is_following = Following.objects.filter(
    #         source=request.user, 
    #         target = user_profile
    #     ).exists()




    is_following = False
    try:
        relationship = Following.objects.get(
            source=request.user,
            target = user_profile
        )
        is_following = True
    
    except:
        is_following = False

    
    return render(request, "network/user_profile_page.html", {
        "user_profile":user_profile,
        "is_following":is_following,
        "followers":len(followers),
        "following":len(following),
        "posts_by_user":page_obj,
        "page_obj": page_obj,
        "liked_posts":liked_post,
    })



def add_follow(request, target_id):
    current_user = request.user
    target_user = User.objects.get(id=target_id)


    # Maybe create a message like we did last time for commerce? Like already following?
    # if i remember correctly, we will need to add another variable to the function? def add_follow(request, target_id, message):???
    if current_user == target_user:
        return HttpResponseRedirect(reverse("user_profile_page", args=[target_id]))

    # I think chatGPT wanted another if statement here
    else:
        new_follower = Following(source = current_user, target = target_user)
        new_follower.save()

        # redirect user to profile page
        return HttpResponseRedirect(reverse("user_profile_page", args=[target_id]))



def delete_follow(request, target_id):
    current_user = request.user
    target_user = User.objects.get(id=target_id)

    if current_user == target_user:
        return HttpResponseRedirect(reverse("user_profile_page", args=[target_id]))
    
    else:
        # kept crashing, could not figure out why.. chatGPT said that i should change .get to .filter, then delete.. curious of your thoughts
        follower_to_delete = Following.objects.filter(source=current_user, target=target_user)
        follower_to_delete.delete()
        return HttpResponseRedirect(reverse("user_profile_page", args=[target_id]))



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def new_post(request):
    if request.method == "POST":
        new_content = request.POST['new_content']
        author = request.user
        # time
    
        post = Post(
            content = new_content,
            author = author,
        )
        post.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "network/index.html")
    

def following_page(request):
    my_followers = Following.objects.filter(source=request.user)
    target_list = []
    for i in my_followers:
        target_list.append(i.target)

    content_list = []
    for i in target_list:
        target_content = Post.objects.filter(author=i)
        content_list += target_content
    print(content_list)

    liked_post = []
    filtered_likes = Like.objects.filter(source=request.user)
    for i in filtered_likes:
        post_content = i.target.id
        liked_post.append(post_content)      



    p = Paginator(content_list, 10)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)



    return render(request, "network/following_page.html", {
        "content_list":page_obj,
        "page_obj": page_obj,
        "liked_posts":liked_post,
    })





@csrf_exempt
def edit_post(request, post_id): 
    single_Post = Post.objects.get(id=post_id)
    package = json.loads(request.body)
    updated_post = package['update']

    single_Post.content = updated_post
    single_Post.save()

    return JsonResponse({
        "message": "Task Updated!"
    })


@csrf_exempt
def like(request, post_id):
    # create a new row in the like table 
    new_like = Like(
        source = request.user,
        target = Post.objects.get(id=post_id)
    )
    new_like.save()

    return JsonResponse({
        "message":"Like Sucessful"
    })



@csrf_exempt
def unlike(request, post_id):
    delete_like = Like.objects.get(
        source = request.user,
        target = Post.objects.get(id=post_id)
    )
    delete_like.delete()
    return JsonResponse({
        "message":"Like Deleted"
    })



 



    