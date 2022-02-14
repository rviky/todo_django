from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import todo
from .forms import todoform

def login(request):
    if request.session.has_key('username'):
        username = request.session['username']
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            request.session['username'] = username
            auth.login(request, user)
            return redirect('dashboard') 
        else:
            return render (request, 'login.html', {"message": "Username or Password is wrong!"})
    return render (request, 'login.html')


@login_required(login_url='/')
def logout(request):
    try:
        del request.session['username']
        auth.logout(request)
        return render (request, 'login.html', {"message": "You are logged out"})
    except:
        pass
    return redirect('login')



@login_required(login_url='/')
def dashboard(request):
    getUserInstance = User.objects.get(username=str(request.user))
    todos = todo.objects.filter(user=getUserInstance)
    todoList = []
    for todo_data in todos:
        if todo_data.status:
            status = "Completed"
            color = "color: green!important"
        else:
            status = "Not Completed"
            color = "color: red!important"
        todoDict = {
            "title": todo_data.note,
            "status": status,
            "color": color,
            "updated": todo_data.updated,
            "id": todo_data.id
        }
        todoList.append(todoDict)
    context = {
        "todoListdata": todoList
    }
    return render(request, "index.html", context)


@login_required(login_url='/')
def delItem(request, itemNo):
    try:
        getObject = todo.objects.get(id=itemNo)
        getObject.delete()
        return redirect('dashboard')

    except:
        return redirect('error')
    
def error(request):
    return render(request, "error.html")

@login_required(login_url='/')
def addItem(request):
    if request.method == "POST":
        title = request.POST['title']
        status = request.POST['status']
        if title and status:
            todoInstance = todo.objects.create(user=request.user,note=title, status=status)
            todoInstance.save()
            return render(request, "add.html", {'message': "Added to your list!"})
    return render(request, "add.html")



@login_required(login_url='/')
def updateItem(request, id):
    values = todo.objects.get(id=id)
    form = todoform(instance=values)
    if request.method == "POST":
        mform = todoform(request.POST, instance=values)
        if mform.is_valid():
            mform.save()
            return redirect('dashboard')
        else:
            return redirect('error')
    context = {'form': form}
    return render(request, "update.html", context)