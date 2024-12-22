from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import AddRecordForm, SignUpForm
from .models import Record


# Create your views here.
def home(request):
    records = Record.objects.all()
    # Check to see if logging in
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect("home")
        else:
            messages.success(request, "There was an error logging in")
            return redirect("home")
    else:
        return render(request, "home.jinja2", {"records": records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "register.jinja2", {"form": form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.jinja2", {"customer_record": customer_record})
    else:
        messages.success(request, "You must be logged in to view that page.")
        return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        customer_record.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect("home")
    else:
        messages.success(request, "You must be logged in to delete records.")
        return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added")
                return redirect("home")
        return render(request, "add_record.jinja2", {"form": form})
    else:
        messages.success(request, "You have to be logged in to create a new record.")
        return redirect("home")

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated.")
            return redirect('home')
        return render(request, "update_record.jinja2", {'form':form})
    else:
        messages.success(request, "You have to be logged in to modify a record.")