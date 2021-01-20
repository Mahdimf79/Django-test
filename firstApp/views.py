from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User
from . import models
from django_globals import globals



def index(request):
    list_Question = models.Question.objects.order_by('-pub_date')
    list_Choice = models.Choice.objects.all()
    #request.session['user'] = ''
    user = request.session.get('user')
    logout = 0
    if user != '':
        logout = 1
    context = {'list_Question' : list_Question, 'list_Choice' : list_Choice, 'user' : user, 'logout' : logout}
    return render(request, 'firstApp/index.html', context)


def detail(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    context = {'Question' : question}
    return render(request, 'firstApp/detail.html', context)


def results(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    context = {'Question' : question}
    return render(request, 'firstApp/results.html', context)


def vote(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    try:
        choice_selected = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, choice.DoesNotExist):
        context1 = {'question' : question,'error_message': 'you didnt select a choice'}
        return render(request, 'firstApp/detail.html',context1)
    else:
        choice_selected.vote += 1
        choice_selected.save()
        return HttpResponseRedirect(reverse('firstApp:results', args=(question.id,)))


def setQuestion(request):
    user = request.session.get('user')
    if user != '':
        return render(request, 'firstApp/setQuestion.html')
    else:
        return HttpResponseRedirect(reverse('firstApp:index'))




def create_question(request):
    textq = str(request.POST['question_text'])
    userid = request.session.get('id')
    username = get_object_or_404(models.Username, id= userid)
    username.question_set.create(text = textq, pub_date = timezone.now())
    return HttpResponseRedirect(reverse('firstApp:index'))


def setChoice(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    context = {'Question' : question}
    return render(request, 'firstApp/setChoice.html', context)


def create_choice(request, pk):
    textc = str(request.POST['choice_text'])
    question = get_object_or_404(models.Question, pk = pk)
    question.choice_set.create(text = textc, vote=0)
    return HttpResponseRedirect(reverse('firstApp:detail', args=(question.id,)))


def register(request):
    context = {'error' : ''}
    if request.session.get('error') != '':
        context = {'error' : request.session.get('error') }
    request.session['error'] = ''
    return render(request, 'firstApp/register.html', context)


def register_set(request):
    username = request.POST['username']
    email = request.POST['email']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    password = request.POST['password']
    repassword = request.POST['repassword']
    status = False
    if password == repassword:
        status = True
    else:
        request.session['error'] = 'Password is carnt'
        status = False
        return HttpResponseRedirect(reverse('firstApp:register'))
    if status:
        user = models.Username(username = username, email = email, firstname = firstname,
         lastname = lastname, password = password )
        user.save()
        userget = get_object_or_404(models.Username, username = username)
        request.session['user'] = username
        request.session['id'] = userget.id
    return HttpResponseRedirect(reverse('firstApp:index'))


def login(request):
    context = {'error' : ''}
    if request.session.get('error') != '':
        context = {'error' : request.session.get('error') }
    request.session['error'] = ''
    return render(request, 'firstApp/login.html', context)


def login_set(request):
    username = request.POST['username']
    password = request.POST['password']
    user = get_object_or_404(models.Username, username = username)
    if password == user.password:
        request.session['user'] = user.username
        request.session['id'] = user.id
        return HttpResponseRedirect(reverse('firstApp:index'))
    else:
        request.session['error'] = "User is not valid"
        return HttpResponseRedirect(reverse('firstApp:login'))


def logout(request):
    request.session['user'] = ''
    request.session['id'] = ''
    return HttpResponseRedirect(reverse('firstApp:index'))
