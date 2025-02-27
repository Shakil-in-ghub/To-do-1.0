from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.all()
    completed_tasks = tasks.filter(complete=True).count()
    total_tasks = tasks.count()
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('task_list')
    else:
        form = TaskForm()
        context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context) 

def delete_task(request, task_id):
    from django.shortcuts import get_object_or_404
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/delete.html', {'task': task})

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.complete = not task.complete
    task.save()
    return redirect('task_list')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit.html', {'form': form, 'task': task})
    