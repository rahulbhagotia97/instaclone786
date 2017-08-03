from django.shortcuts import render, redirect
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm ,UpvotingForm , ProductForm
from models import UserModel, SessionToken, PostModel, LikeModel, CommentModel, ReviewModel, ProductModel
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from datetime import timedelta
from django.utils import timezone
from instaclone.settings import BASE_DIR
from paralleldots import set_api_key, emotion

from imgurpython import ImgurClient

CLIENT_ID = "19dd19a5793b141"
CLIENT_SECRET = "0ccfd1904a6a8707a06f9ac99df39da1072a6af5"

PARALLEL_DOTS_KEY = "3BGXwiNiSiIotjitcAogTSIDBN2wHmDqo7TtrJGqOKw"

veriifcation_code = '088145235648fs689sa56h'
user_id = '854'

# function declaration for signup

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')
            # return redirect('login/')
    else:
        form = SignUpForm()

    return render(request, 'index.html', {'form': form})

# function declaration for login

def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)

# function declaration for posts

def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + '/' + post.image.url)

                client = ImgurClient(CLIENT_ID,CLIENT_SECRET)
                post.image_url = client.upload_from_path(path,anon=True)['link']
                post.save()

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')

# function declaration for feeds

def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login/')

# function declaration for liking a post

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')


# function declaration for commenting on a post

def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')

# function declaration

def search_view(request):
    user = check_validation(request)
    if user:
        if request.method == 'GET':
    verification_code = request.GET.get('verification_code')
    user_id = request.GET.get('user_id')

    context = {
        'verification_code': verification_code,
        'user_id': verification_url,
    }
    return render_to_response('search.html', context, context_instance = RequestContext(request))

# function declaration for uploading products related post

def product_view(request):
    user = check_validation(request)
    if user:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                review = ProductModel(user=user, image=image, caption=caption)
                review.save()

                path = str(BASE_DIR + '/' + product.image.url)

                client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
                product.image_url = client.upload_from_path(path, anon=True)['link']
                product.save()

                return redirect('/products/')

            else:
                return render(request, 'feed.html', {'form': form})
        else:
            return redirect('/post/')

# function declaration for adding reviews on products post

def review_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data.get('product').id
            review_text = form.cleaned_data.get('review_text')
            review = ReviewModel.objects.create(user=user, product_id=product_id, review_text=review_text)
            review.save()
            return redirect('/products/')
        else:
            return redirect('/products/')
    else:
        return redirect('/feed/')

def review_review(reviewtext):
    req_json = none
    req_url = "https://apis.paralleldots.com/emotion"
    "text" : "reviewtext",
    "set_apikey" : "3BGXwiNiSiIotjitcAogTSIDBN2wHmDqo7TtrJGqOKw"
}
    # 1 is for positive tag and 0 is for negative tag
    try:
        req_json = requests.post(req_url, payload).json()
        if req_json is not None:
        print req_json['emotion_type']
                if req_json['emotion_type'] == "happy":
                    return 1
                else:
                    return 0

# function declaration for upvoting comment

def upvoting_view(request):
    user = check_validation(request)
    comment = None
    print "upvote"
    if user and request.method == 'POST':

        form = UpvotingForm(request.POST)
        if form.is_valid():
            print form.cleaned_data

            comment_id = int(form.cleaned_data.get('userid'))

            comment = CommentModel.objects.filter(userid=comment_id).first()
            print "isnt a upvote"

            if comment is not None:
                print "upvoted"
                comment.upvote_num += 1
                comment.save()
                print comment.upvote_num
            else:
                print 'stupid mistake'
        else:
            print "not valid"
            return redirect('/feeds/')
    else:
        return redirect('/login/')

# function declaration for logging out

def logout_view(request):
    user=check_validation(request)
    if user is not None:
        latest_sessn = SessionToken.objects.filter(user=user).last()
        if latest_sessn:
            latest_sessn.delete()
            return redirect("/login/")
        else:
            return redirect('/feeds/')

# For validating the session

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None