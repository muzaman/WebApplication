from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.views import LoginView, LogoutView
from django.template.loader import get_template
from .forms import ChangeUserInfoForm
from .models import AdvUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from .forms import RegisterUserForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from .utilities import signer
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'BAccount/delete_user.html'
    success_url = reverse_lazy('BAccount:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             'Фойдаланувчи ўчирилди.')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'BAccount/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'BAccount/user_is_activated.html'
    else:
        template = 'BAccount/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class RegisterDoneView(TemplateView):
    template_name = 'BAccount/register_done.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'BAccount/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('BAccount:register_done')


@login_required
def profile(request):
    return render(request, 'BAccount/profile.html')


class BAccountPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'BAccount/password_change.html'
    success_url = reverse_lazy('BAccount:profile')
    success_message = 'Фойдаланувчи пароли муваффақиятли ўзгартирилди'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'BAccount/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('BAccount:profile')
    success_message = 'Фойдаланувчи маълумотлари муваффақиятли янгиланди.'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class MFALoginView(LoginView):
    template_name = 'BAccount/login.html'


class MFALogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'BAccount/logout.html'


def index(request):
    template = get_template('BAccount/index.html')
    return HttpResponse(template.render(request=request))
