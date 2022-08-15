from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from . import models 

# Create your views here.

def home(request):
    return render(request,'home.html')

def register(request):
    msg=None
    form = forms.RegisterUser
    if request.method=='POST':
        form = forms.RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            msg='User registration data has been saved'
    return render(request,'registration/register.html',{'form':form,msg:'msg'})


def all_categories(request):
    data = models.QuizCategory.objects.all()
    return render(request,'all-category.html',{'data':data})

@login_required
def category_questions(request,cat_id):
    category = models.QuizCategory.objects.get(id=cat_id)
    questions = models.QuizQuestions.objects.filter(category=category).order_by('id').first()
    return render(request,'category-questions.html',{'question':questions,'category':category})

@login_required
def submit_answer(request,cat_id,question_id):
    category = models.QuizCategory.objects.get(id=cat_id)
    questions = models.QuizQuestions.objects.filter(category=category,id__gt=question_id).order_by('id').first()
    if request.method=="POST":
        if 'skip' in request.POST:
            quest = models.QuizQuestions.objects.get(id=question_id)
            user = request.user
            answer='Not Submitted'
            models.UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)

            if questions:
                return render(request,'category-questions.html',{'question':questions,'category':category})
            else:
                result = models.UserSubmittedAnswer.objects.filter(user=request.user)
                skipped = models.UserSubmittedAnswer.objects.filter(user=request.user,right_answer="Not Submitted").count()
                attempted = models.UserSubmittedAnswer.objects.filter(user=request.user).exclude(right_answer="Not Submitted").count()
                correct=0
                incorrect=0
                for row in result:
                    if row.right_answer == row.question.right_opt:
                        correct=correct+1
                    elif row.right_answer != "Not Submoitted":
                        incorrect=incorrect+1
                marks = correct - incorrect
            
                return render(request,'result.html',{'result':result,'skipped':skipped,'attempted':attempted,'correct':correct,'incorrect':incorrect,'marks':marks})

        else:
            quest = models.QuizQuestions.objects.get(id=question_id)
            user = request.user
            answer=request.POST['answer']
            models.UserSubmittedAnswer.objects.create(user=user,question=quest,right_answer=answer)
       
            if questions:
                return render(request,'category-questions.html',{'question':questions,'category':category})
            else:
                result = models.UserSubmittedAnswer.objects.filter(user=request.user)
                skipped = models.UserSubmittedAnswer.objects.filter(user=request.user,right_answer="Not Submitted").count()
                attempted = models.UserSubmittedAnswer.objects.filter(user=request.user).exclude(right_answer="Not Submitted").count()
                correct=0
                incorrect=0
                for row in result:
                    if row.right_answer == row.question.right_opt:
                        correct=correct+1
                    elif row.right_answer != "Not Submoitted":
                        incorrect=incorrect+1
                marks = correct - incorrect
                return render(request,'result.html',{'result':result,'skipped':skipped,'attempted':attempted,'correct':correct,'incorrect':incorrect,'marks':marks})
                
    else:
        return HttpResponse('Invalid Method')
