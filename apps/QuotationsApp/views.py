from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Users, Quotes
import bcrypt
import datetime
import time


def index(request):

    return render(request, 'QuotationsApp/index.html')

def login(request):
    if request.method == "POST":
        if not Users.objects.filter(email = request.POST['email']):
            messages.info(request, 'EMAIL DOES NOT EXISTS',fail_silently=True, extra_tags='login')
            return redirect('/')
        user =  Users.objects.get(email = request.POST['email'])
        hashed = user.password;

        if not Users.objects.pwMatch(request.POST['password'], hashed):
            messages.info(request, 'Incorrect PW',fail_silently=True, extra_tags='login')
            return redirect('/')

        user = Users.objects.get(email = request.POST['email'])

        request.session['userId'] = Users.objects.get(email = request.POST['email']).pk
        request.session['firstName'] = user.first_name
        request.session['lastName'] = user.last_name
        request.session['loginType'] = 'Logged In'

        return redirect('/quotes')

def register(request):
    if request.method == "POST":
        if not Users.objects.emailIsValid(request.POST['email']):
            messages.info(request, 'EMAIL IS NOT VALID',fail_silently=True, extra_tags='register')
            return redirect('/')

        if Users.objects.filter(email = request.POST['email']):
            messages.info(request, 'EMAIL ALREADY EXISTS',fail_silently=True, extra_tags='register')
            return redirect('/')

        if not Users.objects.ckFirstName(request.POST['firstName']):
            messages.info(request, 'First Name IS NOT VALID',fail_silently=True, extra_tags='register')
            return redirect('/')

        if not Users.objects.ckLastName(request.POST['lastName']):
            messages.info(request, 'Last Name IS NOT VALID',fail_silently=True, extra_tags='register')
            return redirect('/')

        if not Users.objects.pwIsValid(request.POST['password'], request.POST['confirmPassword']):
            messages.info(request, 'PASSWORD IS NOT VALID',fail_silently=True, extra_tags='register')
            return redirect('/')
        # inputs are valid create new user
        pw = request.POST['password']
        password = pw.encode('utf-8')
        hashedPW = bcrypt.hashpw(password, bcrypt.gensalt())

        user = Users.objects.create( first_name=request.POST['firstName'], last_name=request.POST['lastName'], email=request.POST['email'], password=hashedPW)
        request.session['userId'] = user.pk
        request.session['firstName'] = user.first_name
        request.session['lastName'] = user.last_name

        request.session['loginType'] = 'Registered'
        return redirect('/quotes')

def userQuotes(request, user_id):
    thisUser = Users.objects.get(pk=user_id)
    quoteList = Quotes.objects.filter(user__pk = user_id).order_by('created_at')
    quoteListCt = Quotes.objects.filter(user__pk = user_id).count()

    context = {
     'thisUser': thisUser,
     'quoteListCt': quoteListCt,
     'quoteList': quoteList,
    }
    return render(request, 'QuotationsApp/userQuotes.html', context)

def quotes(request):
    thisUser = Users.objects.get(pk=request.session['userId'])
    quoteList = Quotes.objects.all().order_by('created_at')

    #cant figure out how to exclude users favs in this list

    usersFavorites = Quotes.objects.filter(favorites = thisUser)

    context = {
     'quoteList': quoteList,
     'usersFavorites': usersFavorites,
     'user_id': request.session['userId']
    }

    return render(request, 'QuotationsApp/quotes.html', context)

def createQuote(request):
    if request.method == "POST":
        #check for empty post
        print request.session['userId']
        print request.POST['message']
        print request.POST['quotedBy']
        user = Users.objects.get(id = request.session['userId'])
        quote = Quotes.objects.create( message=request.POST['message'], quotedBy = request.POST['quotedBy'] ,user=user)
        print quote
        return redirect('/quotes')

def addFavorite(request, fav_id, user_id):
    user = Users.objects.get(pk = user_id)
    fav = Quotes.objects.get(pk = fav_id)
    fav.favorites.add(user)
    return redirect('/quotes')

def delFavorite(request, fav_id, user_id):
    #Cant figure out how to delete a specific fav
    theUser = Users.objects.get(pk = user_id)
    fav = Quotes.objects.get(pk = fav_id)
    fav.favorites.filter(allFavs = theUser).delete()

    return redirect('/quotes')
