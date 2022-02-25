from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from . models import Task
from . forms import TaskForm
from django.views.generic import ListView, UpdateView, DeleteView, DetailView

class TaskListview(ListView):
    model = Task
    template_name ='home.html'
    context_object_name ='task'

class TaskDetailview(DetailView):
    model = Task
    template_name = 'display.html'
    context_object_name = 'task'

class TaskUpdateview(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk':self.object.id})

class TaskDeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

def home(request):
    task = Task.objects.all()
    if request.method == 'POST':
        name = request.POST.get('task','')
        priority = request.POST.get('priority','')
        date = request.POST.get('date','')
        print(date,'>>>>>>>>>>>>..date')
        to_do_db = Task(name=name, priority=priority,date = date)
        to_do_db.save()
    return render(request, 'home.html',{'task': task})

def delete(request,id):
    task_id = Task.objects.get(id = id)
    if request.method == 'POST':
        task_id.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task  = Task.objects.get(id=id)
    task_form = TaskForm(request.POST or None, instance=task)
    if task_form.is_valid():
        task_form.save()
        return redirect('/')
    return render(request, 'edit.html',{'task_form':task_form,'task':task})


# def display(request):
#     task = Task.objects.all()
#     return render(request,'display.html',{'task': task})
