from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


# ********** functions that render page **********


def index(request):
    if request.session.get('email_session_id') != None:
        print('email_session_id already logged in')
        return redirect('/quotes')
    return render(request, 'index.html')


def quote_dashboard(request):
    # only allow user into dashboard if they have session id
    if request.session.get('email_session_id') == None:
        print('no session in email_session_id')
        return redirect('/')

    user_in_session = User.objects.get(
        email=request.session['email_session_id'])
    # print('***************')
    # print(User.objects.all().get(email=request.session['email_session_id']))
    context = {
        'user': user_in_session,
        'user_quotes': Author.objects.all(),
    }
    return render(request, 'quote_dashboard.html', context)


def user_quote(request, user_id):
    if request.session.get('email_session_id') == None:
        print('no session in email_session_id')
        return redirect('/')
    user = User.objects.get(id=user_id)
    context = {
        'user': user,
        'quote_info': Author.objects.filter(user=user),
    }

    return render(request, 'user_quote.html', context)


def edit_account(request, user_id):
    if request.session.get('email_session_id') == None:
        print('no session in email_session_id')
        return redirect('/')

    user_in_session = User.objects.get(
        email=request.session['email_session_id'])
    context = {
        'user': user_in_session
    }

    return render(request, 'edit_account.html', context)


# ******* functions that redirect to render page ******


def register(request):
    user_errors = User.objects.user_validator(request.POST)
    if len(user_errors) > 0:
        for key, value in user_errors.items():
            messages.error(request, value)
        return redirect("/")

    user_in_db = User.objects.filter(email=request.POST['email'])
    if len(user_in_db) > 0:
        print('Email already exists')
        messages.error(request, "That email already exists.")
        return redirect('/')

    else:
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
    print('hashed_pw:', hashed_pw)
    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw
    )
    request.session['email_session_id'] = new_user.email
    return redirect('/quotes')


def login(request):
    user_list = User.objects.filter(email=request.POST['email'])
    if len(user_list) < 1:
        print('no user found')
        messages.error(request, 'User email was not found.')
        return redirect('/')
    else:
        print('user found -> logging in user')
        if bcrypt.checkpw(request.POST['password'].encode(), user_list[0].password.encode()):
            print('password match')
            request.session['email_session_id'] = user_list[0].email
            return redirect('/quotes')

        else:
            print('failed password')
            messages.error(request, 'Incorrect Password')
        return redirect('/')


def logout(request):
    print('loggin out user')
    print('clearing session email_session_id')
    request.session.clear()
    return redirect('/')


def add_author(request):
    author_errors = Author.objects.author_validator(request.POST)
    if len(author_errors) > 0:
        for key, value in author_errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        Author.objects.create(
            name=request.POST['name'],
            quote=request.POST['quote'],
            user=User.objects.get(email=request.session['email_session_id'])
        )
    return redirect('/quotes')


def update(request, user_id):
    if len(request.POST['first_name']) < 3:
        messages.error(request, 'First name should be at least 3 characters.')
    if len(request.POST['last_name']) < 3:
        messages.error(request, 'Last name should be at least 3 characters.')
    if len(request.POST['email']) < 3:
        messages.error(request, 'Email is too short')

    error_messages = messages.get_messages(request)
    error_messages.used = False
    if len(error_messages) > 0:
        return redirect(f'/myaccount/{user_id}')
    emails_in_db = User.objects.filter(email=request.POST['email'])
    user_to_edit = User.objects.get(id=user_id)
    if request.POST['email'] == user_to_edit.email:
        user_to_edit.last_name = request.POST['last_name']
        user_to_edit.first_name = request.POST['first_name']
        user_to_edit.save()
        return redirect('/quotes')
    if len(emails_in_db) < 1:
        user_to_edit.last_name = request.POST['last_name']
        user_to_edit.first_name = request.POST['first_name']
        user_to_edit.email = request.POST['email']
        user_to_edit.save()
        request.session['email_session_id'] = request.POST['email']
        return redirect('/quotes')
    else:
        print('Email already exists')
        messages.error(request, "That email already exists.")
        return redirect(f'/myaccount/{user_id}')


def like_quote(request, user_id):
    user_to_like = User.objects.get(
        email=request.session['email_session_id'])
    quote_to_like = Author.objects.get(id=user_id)
    quote_to_like.users_who_liked.add(user_to_like)
    return redirect('/quotes')


def delete(request, user_id):
    quote_to_delete = Author.objects.get(id=user_id)
    quote_to_delete.delete()
    return redirect('/quotes')
