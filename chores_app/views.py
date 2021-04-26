from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Chore
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            full_name = request.POST['full_name'],
            email_address = request.POST['email_address'],
            password = hashed_pw
        )
        request.session['user_id'] = user.id
        return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_list = User.objects.filter(email_address = request.POST['login_email'])
        if len(user_list) == 0:
            messages.error(request, 'A user with that email address cannot be found.')
            return redirect('/')
        else:
            user = user_list[0]
            print(user.password)
            if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/dashboard')
            else:
                messages.error(request, 'Incorrect password or email entered.')
                return redirect('/')

def dashboard(request):
    user = User.objects.get(id = request.session['user_id'])
    chores = Chore.objects.all()
    context = {
        'user': user,
        'chores': chores
    }
    return render(request, 'dashboard.html', context)

def chores_new(request):
    user = User.objects.get(id = request.session['user_id'])
    all_users = User.objects.all()
    context = {
        'user': user,
        'all_users': all_users
    }
    return render(request, 'chore_form.html', context)

def chores_add(request):
    errors = Chore.objects.chore_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/chores/new')
    else:
        user = User.objects.get(id = request.session['user_id'])
        assignee = User.objects.get(id = request.POST['assignee_id'])
        chore = Chore.objects.create(
            name = request.POST['name'],
            creator = user
        )
        chore.assignees.add(assignee)
        return redirect('/dashboard')

def chores_edit(request, chore_id):
    user = User.objects.get(id = request.session['user_id'])
    all_users = User.objects.all()
    context = {
        'user': user,
        'chore': Chore.objects.get(id=chore_id),
        'all_users': all_users
    }
    return render(request, 'chores_edit.html', context)

def chores_update(request, chore_id):
    errors = Chore.objects.chore_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/chores/{chore_id}/edit')
    else:
        user = User.objects.get(id = request.session['user_id'])
        assignee = User.objects.get(id = request.POST['assignee_id'])
        chore = Chore.objects.get(id = chore_id)
        chore.name = request.POST['name']
        chore.creator = user
        chore.assignees.add(assignee)
        chore.save()
        return redirect('/dashboard')

def chores_delete(request, chore_id):
    chore = Chore.objects.get(id = chore_id)
    chore.delete()
    return redirect('/dashboard')