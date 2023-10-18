from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.defaults import permission_denied
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .forms import *
from .models import *


class AdList(ListView):
    model = Ad
    ordering = '-creation_time'
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 10


class AdDetail(FormMixin, DetailView):
    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'
    form_class = ResponseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        pk = self.kwargs.get('pk')
        if form.is_valid():
            self.response_submitted = True
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.resp_author = self.request.user
            self.object.resp_ad = self.get_object()
            self.object.save()
            return super().form_valid(form)
        except IntegrityError:
            return redirect('/')


    def get_success_url(self, **kwargs):
        return reverse_lazy('ad', kwargs={'pk': self.get_object().id})


class CreateAdView(LoginRequiredMixin, CreateView):

    template_name = 'create_ad.html'
    raise_exception = True

    def get(self, request):
        form = AdForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:

            form = AdForm(request.POST)
            if form.is_valid():
                ad = form.save(commit=False)
                ad.author = request.user
                ad.save()
                return redirect('ads')
            return render(request, self.template_name, {'form': form})
        else:
            return reverse_lazy('login')



class AdEdit(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'edit_ad.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)

    def get_success_url(self):
        return reverse('ads')

class ResponseList(ListView):
    model = Response
    ordering = '-creation_time'
    template_name = 'responses.html'
    context_object_name = 'responses'
    form_class = ResponseFilterForm
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResponseFilterForm(
            user=self.request.user, data=self.request.GET
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        ad_id = self.request.GET.get('ad')
        if ad_id:
            queryset = queryset.filter(resp_ad__author=user, resp_ad=ad_id)
        else:
            queryset = queryset.filter(resp_ad__author=user)
        return queryset


def accept_response(request, response_id):
    if request.method == 'POST':
        response = Response.objects.get(id=response_id)
        response.accepted = True
        response.save()
        _ad = response.resp_ad
        owner = _ad.author
        player = response.resp_author
        to_email = player.email
        send_mail(
            subject='Ваш отклик принят!',
            message=f'{owner} принял Ваш отклик на свое объявление {response.resp_ad.title}',
            from_email="79854550554@mail.ru",
            recipient_list=[to_email, ],
        )
        action_completed = True

        return HttpResponseRedirect(reverse('responses'))
    else:
        return HttpResponseBadRequest("Вы не можете выполнить это действие.")


def reject_response(request, response_id):
    if request.method == 'POST':
        response = Response.objects.get(id=response_id)
        response.delete()
        action_completed = True

        return HttpResponseRedirect(reverse('responses'))
    else:
        return HttpResponseBadRequest("Вы не можете выполнить это действие.")


def mailing(request):
    _user = request.user
    if _user.is_superuser:

        template_name = 'mailing.html'
        players = User.objects.all()
        to_email = [player.email for player in players]
        form = MailingForm(request.POST)
        if form.is_valid():
            subject = f'Рассылка новостей нашей Доски объявлений'
            message = form.cleaned_data['text']
            from_email = '79854550554@mail.ru'
            recipient_list = to_email

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
            )
        context = {
            'form': form,
        }
        return render(request, template_name, context)
    else:
        return permission_denied(request, exception=None)










