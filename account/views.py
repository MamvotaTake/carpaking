from django.contrib import messages, auth
from django.contrib.auth.tokens import default_token_generator
# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from account.forms import RegistrationForm
from account.models import Account
# Create your views here.
from employees import forms
from employees.forms import EmployeeForm
from employees.models import Employee


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = first_name.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string("account/account_verification_email.html", {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        # messages.error(request, 'error!')
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'account/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'You are logged in successfully.')
            if user.is_manager:
                return redirect('manager')
            else:
                return redirect('employee')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'account/login.html')


def manager(request):
    employee = Employee.objects.all()
    employee_count = employee.count()
    context = {
        'employee': employee,
        'employee_count': employee_count,
    }
    return render(request, 'manager/manager.html', context)


def employee(request):
    employee = Employee.objects.all()
    employee_count = employee.count()
    if request.method == 'POST':
        form = forms.EmployeeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            actual_entry_time = form.cleaned_data['actual_entry_time']
            number_plate = form.cleaned_data['number_plate']
            choice_category = form.cleaned_data['choice_category']
            employee = Employee(name=name, number_plate=number_plate, actual_entry_time=actual_entry_time,
                                choice_category=choice_category)
            employee.save()
            messages.success(request, 'Your space has been successfully reserved.')

    form = EmployeeForm()
    context = {
        'form': form,
        'employee_count': employee_count,
    }
    return render(request, 'employee/employee.html', context)


def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        time = request.POST.get('time')
        plate = request.POST.get('plate')
        choice = request.POST.get('choice')

        employee = Employee(
            name=name,
            actual_entry_time=time,
            number_plate=plate,
            choice_category=choice,
        )
        employee.save()
        return redirect('manager')
    return render(request, 'manager/manager.html')


def remove_employee(request, employee_id):
    employee_id = int(employee_id)
    try:
        employee_list = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return redirect('manager')
    employee_list.delete()
    return redirect('manager')


def update_employee(request, pk):
    emp = Employee.objects.get(id=pk)
    if request.method == 'POST':
        emp.name = request.POST['name']
        emp.actual_entry_time = request.POST['time']
        emp.number_plate = request.POST['plate']
        emp.choice_category = request.POST['choice']
        employee = Employee(
            name=emp.name,
            actual_entry_time=emp.actual_entry_time,
            number_plate=emp.number_plate,
            choice_category=emp.choice_category,
        )
        employee.save()
        return redirect('manager')
    else:
        messages.error(request, 'User not updated please try again')
    return render(request, 'manager/manager.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_staff = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def forgot_password(request):
    if request.method == 'POST':

        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string("account/reset_password_email.html", {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')

        else:
            messages.error(request, 'Account Does not exist')
            return redirect('forgot_password')
    return render(request, 'account/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'account/resetPassword.html')
