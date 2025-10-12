from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseServerError, Http404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from .models import Todo, Category
from .forms import TaskForm

# Custom error handlers
def handler400(request, exception, template_name='400.html'):
    """Handle 400 Bad Request errors."""
    context = {
        'error': '400 Bad Request',
        'message': 'The server cannot process the request due to a client error.',
        'status_code': 400
    }
    return render(request, '400.html', context, status=400)

def handler403(request, exception, template_name='403.html'):
    """Handle 403 Forbidden errors."""
    context = {
        'error': '403 Forbidden',
        'message': 'You do not have permission to access this page.',
        'status_code': 403
    }
    return render(request, '403.html', context, status=403)

def handler404(request, exception, template_name='404.html'):
    """Handle 404 Not Found errors."""
    context = {
        'error': '404 Not Found',
        'message': 'The page you are looking for does not exist.',
        'status_code': 404
    }
    return render(request, '404.html', context, status=404)

def handler500(request, template_name='500.html'):
    """Handle 500 Server Error."""
    context = {
        'error': '500 Server Error',
        'message': 'An error occurred while processing your request.',
        'status_code': 500
    }
    return render(request, '500.html', context, status=500)

def task_list(request):
    tasks = Todo.objects.all()
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'all')
    sort = request.GET.get('sort', 'date')  # 'title' | 'date' | 'status'
    direction = request.GET.get('dir', 'desc')  # 'asc' | 'desc'
    page_number = request.GET.get('page')
    category_id = request.GET.get('category')

    # Filtering
    if q:
        tasks = tasks.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'pending':
        tasks = tasks.filter(completed=False)
    if category_id:
        tasks = tasks.filter(category_id=category_id)

    # Sorting
    if sort == 'title':
        order_field = 'title'
    elif sort == 'status':
        order_field = 'completed'
    else:
        order_field = 'created_at'
    if direction == 'desc':
        order_field = f'-{order_field}'
    tasks = tasks.order_by(order_field)

    # Pagination (10 per page)
    paginator = Paginator(tasks, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'tasks': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'q': q,
        'status': status,
        'sort': sort,
        'direction': direction,
        'categories': Category.objects.all(),
        'category_selected': int(category_id) if category_id else None,
    }
    return render(request, 'task_list.html', context)

def task_detail(request, pk):
    task = get_object_or_404(Todo, pk=pk)
    return render(request, 'task_detail.html', {'task': task})

@login_required(login_url='/admin/login/')
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if request.user.is_authenticated:
                task.owner = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

@login_required(login_url='/admin/login/')
def task_update(request, pk):
    task = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required(login_url='/admin/login/')
def task_delete(request, pk):
    task = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
    return HttpResponseNotAllowed(['POST'])

@login_required(login_url='/admin/login/')
def task_toggle_completed(request, pk):
    task = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        messages.success(request, f"Marked as {'completed' if task.completed else 'pending'}: {task.title}")
        return redirect('task_list')
    return HttpResponseNotAllowed(['POST'])

def health(request):
    return HttpResponse('ok')

def ready(request):
    try:
        # minimal DB check
        Todo.objects.exists()
        return HttpResponse('ready')
    except Exception as e:
        return HttpResponseServerError('not ready')
