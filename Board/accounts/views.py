import random
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import RegisterUserForm, CodeForm, LoginUserForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView
from .models import UserCode
from django.core.mail import send_mail
from .utils import DataMixin


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вход")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('ads')


def LogoutUser(request):
    logout(request)
    return redirect('login')


def s_mail(obj, user):
    loginer = User.objects.get(username=user)
    to_email = loginer.email
    send_mail(
        subject='Код подтверждения',
        message=f'{getattr(obj, "code")}',
        from_email='79854550554@mail.ru',
        recipient_list=[to_email, ]
    )


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        UserCode.objects.create(user=user, code=random.randint(10000, 99999))
        obj = UserCode.objects.get(user=user)
        s_mail(obj, user)
        return redirect('code')


# def check_code(request):
#     user = request.user
#     obj = UserCode.objects.get(user=user)
#     if getattr(obj, 'valid'):
#         return redirect('ads')
#     form = CodeForm(request.POST or None)
#     error = ''
#     if request.method == 'POST':
#         if '_check' in request.POST and form.is_valid():
#             code2 = form.cleaned_data.get('code', None)
#             if UserCode.objects.filter(user=user, code=code2):
#                 _usercode = UserCode.objects.get(user=user, code=code2)
#                 _usercode.valid = True
#                 _usercode.save()
#                 return redirect('ads')
#             else:
#                 error = 'Неверный код'
#         elif '_send' in request.POST:
#             UserCode.objects.filter(user=request.user).update(code=random.randint(10000, 99999))
#             s_mail(obj, user)
#     context = {'form': form, 'error': error}
#     return render(request, 'registration/code.html', context)

def check_code(request):
    user = request.user
    obj = UserCode.objects.get(user=user)

    if obj.valid:
        return redirect('ads')

    form = CodeForm(request.POST or None)
    error = ''

    if request.method == 'POST':
        if 'check_code' in request.POST:
            if form.is_valid():
                code2 = form.cleaned_data.get('code', None)
                try:
                    user_code = UserCode.objects.get(user=user, code=code2)
                except UserCode.DoesNotExist:
                    error = 'Неверный код'
                else:
                    user_code.valid = True
                    user_code.save()
                    return redirect('ads')
        elif 'send_code' in request.POST:
            new_code = random.randint(10000, 99999)
            UserCode.objects.update_or_create(user=user, defaults={'code': new_code})
            s_mail(obj, user)

    context = {'form': form, 'error': error}
    return render(request, 'registration/code.html', context)
