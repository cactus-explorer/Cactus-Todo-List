from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader, Context
from django.shortcuts import render
from django.shortcuts import redirect


from .models import Task
from .forms import NameForm


from datetime import *
from django.utils import timezone



def index(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        task_id = request.POST.get("key")
        edited = request.POST.get("edit")
        newText = request.POST.get("newText")

        if task_id != None:
            Task.objects.filter(pk=task_id).delete()
            return redirect('/')
        elif edited != None:
            t = Task.objects.get(id=edited)
            t.task_text = newText  # change field
            t.save() # this will update only
            print(newText)
            return redirect('/')
        else:
        # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                print(form.cleaned_data['your_name'])

                saveTask = Task(task_text=form.cleaned_data['your_name'], 
                                pub_date=timezone.now())
                saveTask.save()
                
                return redirect('/')
            else:
                return HttpResponse('Invalid')
    else:
        template = loader.get_template('startpage/index.html')
        latest_task_list = Task.objects.order_by('pub_date')
        context = {
            'latest_task_list': latest_task_list,
        }
        return render(request, 'startpage/index.html', context)