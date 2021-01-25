from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from . import models
from django_globals import globals
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
import re


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
    user = request.session.get('user')
    check = 0
    if user != '':
        check = 1
    question = get_object_or_404(models.Question, pk=pk)
    context = {'Question' : question, 'check' : check}
    return render(request, 'firstApp/detail.html', context)


def results(request, pk):
    question = get_object_or_404(models.Question, pk=pk)
    context = {'Question' : question}
    return render(request, 'firstApp/results.html', context)


def vote(request, pk):
    user = request.session.get('user')
    if user == '':
        return HttpResponseRedirect(reverse('firstApp:login'))
    else:
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
    user = request.session.get('user')
    if user == '':
        return HttpResponseRedirect(reverse('firstApp:login'))
    else:
        question = get_object_or_404(models.Question, pk=pk)
        context = {'Question' : question}
        return render(request, 'firstApp/setChoice.html', context)


def create_choice(request, pk):
    textc = str(request.POST['choice_text'])
    question = get_object_or_404(models.Question, pk = pk)
    question.choice_set.create(text = textc, vote=0)
    return HttpResponseRedirect(reverse('firstApp:detail', args=(question.id,)))


def register(request):
    user = request.session.get('user')
    if user != '':
        return HttpResponseRedirect(reverse('firstApp:index'))
    else:
        return render(request, 'firstApp/register.html')

@csrf_exempt
def register_set(request):
    username = request.POST['username']
    email = request.POST['email']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    password = request.POST['password']
    repassword = request.POST['repassword']
    status = True

    if len(password) >= 8 and len(password) <= 64:
        if len(username) >= 5 and len(username) <= 30:
            if password == repassword:
                if re.fullmatch('(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))',email):
                    if re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,30})?', firstname):
                        if re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,30})?', lastname):

                            try:
                                print('khar')
                                usercheck = models.Username.objects.get(username = username)
                                print('khar2')
                                obj = {
                                    'ok': False,
                                    'status' : 'This username is available'
                                }
                                status = False
                                print('khar3')
                            except:
                                pass

                            try:
                                emailcheck = models.Username.objects.get(email = email)
                                obj = {
                                    'ok': False,
                                    'status' : 'This email is available'
                                }
                                status = False
                            except:
                                pass

                            if status:
                                user = models.Username(username = username, email = email, firstname = firstname,
                                lastname = lastname, password = password )
                                user.save()
                                obj = {
                                'ok': True,
                                'status' : 'sucssecful'
                                }
                        else:
                            obj = {
                                'ok': False,
                                'status' : 'Invalid Lastname'
                            }
                    else:
                        obj = {
                            'ok': False,
                            'status' : 'Invalid Firstname'
                        }
                else:
                    obj = {
                        'ok': False,
                        'status' : 'Invalid Email'
                    }
            else:
                obj = {
                    'ok': False,
                    'status' : 'A password is not the same as repeating a passworde'
                }
        else:
            obj = {
                'ok': False,
                'status' : 'The number of characters in the username is not allowed'
            }
    else:
        obj = {
            'ok': False,
            'status' : 'The number of characters in the password is not allowed'
        }
    return JsonResponse(obj)


def login(request):
    user = request.session.get('user')
    if user != '':
        return HttpResponseRedirect(reverse('firstApp:index'))
    else:
        return render(request, 'firstApp/login.html')


def login_set(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = models.Username.objects.get(username= username, password= password)
        obj = {
            'ok': True,
            'values': {
                'id' : user.id,
                'username' : user.username
            }
        }
        request.session['user'] = user.username
        request.session['id'] = user.id
    except:
        obj = {
            'ok': False,
            'values': {
                'error' : 'naiomad dige'
            }
        }

    return JsonResponse(obj)


def logout(request):
    request.session['user'] = ''
    request.session['id'] = ''
    return HttpResponseRedirect(reverse('firstApp:index'))
