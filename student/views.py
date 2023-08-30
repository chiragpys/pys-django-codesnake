import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware
from django.views.decorators.cache import never_cache
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.contrib import messages

from mysite.settings import BASE_DIR
from .forms import StudentForm, StudentModel, ContactForm, SubscribeForm, SubscribeModel, CreateUserForm, LoginForm, \
    ContactDataForm
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import ContactModel

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import timedelta
from datetime import timezone
import pytz
from django.db.models import Q
from openpyxl import Workbook
from openpyxl.styles import Alignment


# Create your views here.
@method_decorator([never_cache, login_required], name='dispatch')
class StudentFormView(TemplateView):
    # Create view
    template_name = 'student/newform.html'

    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your form submitted Successfully")
            return redirect('StudentFormView')
        else:
            pass
            # messages.error(request, "Please fill required fields..")

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        form = StudentForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context


@method_decorator([never_cache, login_required], name='dispatch')
class StudentDetailView(TemplateView):
    # Read View
    template_name = 'student/StudentDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = StudentModel.objects.all()
        return context


@method_decorator([never_cache, login_required], name='dispatch')
class StudentUpdateView(TemplateView):
    # Update View
    template_name = 'student/newupdate.html'

    def post(self, request, pk, *args, **kwargs):
        student = StudentModel.objects.get(pk=pk)
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            messages.success(request, f"{name} {last_name} data updated Successfully")
            return redirect('StudentList')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, pk, **kwargs):
        student = StudentModel.objects.get(pk=pk)
        form = StudentForm(instance=student)
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context


@method_decorator([never_cache, login_required], name='dispatch')
class StudentDelete(TemplateView):
    # Delete View
    template_name = 'student/StudentDelete.html'

    def post(self, request, pk, *args, **kwargs):
        student = StudentModel.objects.get(pk=pk)
        name = student.first_name
        last_name = student.last_name
        student.delete()
        messages.success(request, f"{name} {last_name} delete Successfully.")
        return redirect('StudentList')

        # context = self.get_context_data(**kwargs)
        # context['data'] = StudentModel.objects.all()
        # return context

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = StudentModel.objects.get(pk=pk)
        return context


@method_decorator([never_cache, login_required], name='dispatch')
class StudentIndex(TemplateView):
    template_name = 'student/index.html'


@method_decorator([never_cache, login_required], name='dispatch')
class Courses(TemplateView):
    template_name = 'student/Courses.html'


@method_decorator([never_cache, login_required], name='dispatch')
class Home(TemplateView):
    # Newsletter Subscribe
    template_name = 'student/home.html'

    def post(self, request, *args, **kwargs):
        news_form = SubscribeForm(request.POST, )
        if news_form.is_valid():
            email = news_form.cleaned_data['email']
            news_form.save()

            # Email Sending
            send_mail(
                'NewsLetter Subscription to CodeSnake',
                f'Hey there,\n'
                f'Thank you for Subscribing to CodeSnake! We are so excited to welcome you.Have a good day.',
                settings.EMAIL_HOST_USER,
                [email, ]
            )
            messages.success(request, 'Thanks Subscribed Successfully!')
            return redirect('home')

        context = self.get_context_data(**kwargs)
        context['news_form'] = news_form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        news_form = SubscribeForm()
        context = super().get_context_data(**kwargs)
        context['news_form'] = news_form
        return context


@method_decorator([never_cache, login_required], name='dispatch')
class Privacy(TemplateView):
    template_name = 'student/Privacy-Policy.html'


@method_decorator([never_cache, login_required], name='dispatch')
class About(TemplateView):
    template_name = 'student/about.html'


@method_decorator([never_cache, login_required], name='dispatch')
class ContactView(TemplateView):
    template_name = 'student/contact.html'

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            form.save()

            # Email Sending
            send_to_user = (
                'Thank you for contact CodeSnake',
                f'Hello {first_name} {last_name}, \n'
                f'Thank you for contact CodeSnake. It will be contact for you as soon as posible. Have a good day.',
                settings.EMAIL_HOST_USER,
                [email, ]
            )

            send_to_owner = (
                'CodeSnake inquire',
                f'Contact person details, \n'
                f'Name: {first_name} {last_name},\n'
                f'Email Id: {email},\n'
                f'Message: {message}.',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER, ]
            )
            send_mass_mail((send_to_user, send_to_owner), )

            messages.success(request, 'Your message was sent, thank you!')
            return redirect('contact')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        form = ContactForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context


@method_decorator([never_cache, login_required], name='dispatch')
class NewsLetterView(TemplateView):
    template_name = 'student/news.html'

    def post(self, request, *args, **kwargs):
        news_form = SubscribeForm(request.POST, )
        if news_form.is_valid():
            email = news_form.cleaned_data['email']
            check_email = SubscribeModel.objects.get(email=email)
            print(check_email)
            if email == check_email:
                messages.warning(request, "This email already Subscribe.")
            news_form.save()

        context = self.get_context_data(**kwargs)
        context['news_form'] = news_form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        news_form = SubscribeForm()
        context = super().get_context_data(**kwargs)
        context['news_form'] = news_form
        return context


# Django Login

@method_decorator([never_cache, login_required], name='dispatch')
class RegisterUser(TemplateView):
    template_name = 'student/register.html'

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('home', )
    #     else:
    #         return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            print("yes")
            # import pdb
            # pdb.set_trace()
            form.save()
            user = form.cleaned_data['username']
            print(user)
            messages.success(request, f"Account was create for {user} successfully.!")
            return redirect('login-page')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        form = CreateUserForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context


class login_user(LoginView):
    template_name = 'student/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


@method_decorator([never_cache, login_required], name='dispatch')
class logout_user(LogoutView):
    next_page = 'login'


@method_decorator([never_cache], name="dispatch")
class LoginView(View):
    template_name = 'student/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.session.get('user') is None:
            return render(request, self.template_name, {'form': self.form_class})
        else:
            return redirect('home')

    def post(self, request):
        # import pdb
        # pdb.set_trace()
        if request.session.get('user') is None:
            form = self.form_class(request.POST)
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['user'] = username
                login(request, user)
                return redirect('home', )
            print(request.session.get('user'))
            messages.error(request, "Username OR password is incorrect")
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('home')


@method_decorator([login_required], name="dispatch")
class LogoutView(View):
    def get(self, request):
        if request.session.get('user') is None:
            return redirect('login')
        else:
            del request.session['user']
            logout(request)
            print("logout done")
            return redirect('login')


@method_decorator([never_cache, login_required], name='dispatch')
class EmailView(TemplateView):
    template_name = 'student/SendEmail_ContactData.html'

    def post(self, request, *args, **kwargs):
        form = ContactDataForm(request.POST)
        if form.is_valid():
            email_id = form.cleaned_data['send_email']
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            filters_data = form.cleaned_data['filters']
            interested_data = form.cleaned_data['interested']
            called_data = form.cleaned_data['called']
            unit_data = int(form.cleaned_data['max_data'])

            import pdb
            pdb.set_trace()

            if from_date and to_date:
                to_date = to_date + timedelta(minutes=59, hours=23, )

                # to convert UTC
                from_date_utc = from_date.astimezone(timezone.utc)
                to_date_utc = to_date.astimezone(timezone.utc)

                # start_date = make_aware((form_date, '%Y-%m-%d'))
                # end_date = make_aware((to_date, '%Y-%m-%d'))
                # MyModel.objects.filter(Q(flag=True) & Q(model_num__gt=15))

                email_data = ContactModel.objects.filter(created__range=[from_date_utc, to_date_utc])
                filters_by_bool_values = Q()

                if filters_data == 'Ascending':
                    email_data = email_data.order_by('created')

                elif filters_data == 'Descending':
                    email_data = email_data.order_by('-created')

                else:
                    email_data = email_data.order_by('first_name', '-created')

                if interested_data:
                    filters_by_bool_values &= Q(interested=True)

                if called_data:
                    filters_by_bool_values &= Q(called=True)

                email_data = email_data.filter(filters_by_bool_values)[:unit_data]
                # email_data = reversed(email_data)

                # else:
                #     email_data = ContactModel.objects.filter(created__range=[from_date_utc, to_date_utc]).order_by(
                #         'first_name', '-created')

                html_content = render_to_string('student/email.html', {'data': email_data})
                email = EmailMultiAlternatives(
                    f"{from_date.date()} to {to_date.date()} data "
                    f"ContactUs CodeSnake",
                    html_content,
                    settings.EMAIL_HOST_USER,
                    [email_id]
                )
                email.attach_alternative(html_content, 'text/html')
                email.send()

                # Excel write:
                wb = Workbook()
                ws = wb.active
                ws.title = "Contact Data"

                headers = ['Id', 'First', 'Last', 'Email', 'Message', 'Date']
                ws.append(headers)

                for data in email_data:
                    ws.append([data.id, data.first_name, data.last_name, data.email, data.message,
                               data.created.strftime('%d, %b, %Y, %I:%M %p')])
                save_data = os.path.join(BASE_DIR, 'media/sample.xlsx')
                wb.save(save_data)

                messages.success(request, 'Your Contact Record data send successfully.')
                return redirect('datasend-contact')

            else:
                email_data = ContactModel.objects.all().order_by('-id')[:10]
                html_content = render_to_string('student/email.html', {'data': email_data})
                email = EmailMultiAlternatives(
                    "Last 10 data ContactUs CodeSnake",
                    html_content,
                    settings.EMAIL_HOST_USER,
                    [email_id]
                )
                email.attach_alternative(html_content, 'text/html')
                email.send()

                # Excel write:
                wb = Workbook()
                ws = wb.active
                ws.title = "Contact Data"

                alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

                headers = ['Id', 'First', 'Last', 'Email', 'Message', 'Date']
                ws.append(headers)

                for data in email_data:
                    ws.append([data.id, data.first_name, data.last_name, data.email, data.message,
                               data.created.strftime('%d, %b, %Y, %I:%M %p')])

                save_data = os.path.join(BASE_DIR, 'media/sample.xlsx')
                wb.save(save_data)

                messages.success(request, 'Your Contact Record data send successfully.')
                return redirect('datasend-contact')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        form = ContactDataForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context
