from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse,HttpResponseRedirect
from . import models

def index(request,):
    list_Question = models.Question.objects.order_by('-pub_date')
    context = {'list_Question' : list_Question}
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
