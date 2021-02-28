from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    View,
)
from django.urls import reverse_lazy
from .models import Progress
from .forms import ProgressForm
from django.contrib import messages
from utils.mixins import UserFormKwargsMixin


class ProgressListView(LoginRequiredMixin, ListView):
    """ View to list all the Progresss in progress """

    ordering = ('-date',)
    paginate_by = 25

    def get_queryset(self, **kwargs):
        return Progress.objects.filter(user=self.request.user) #.order_by('-date')


class ProgressCreateView(LoginRequiredMixin, UserFormKwargsMixin, CreateView):
    """ Create a new post in the progress app """

    model = Progress
    form_class = ProgressForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProgressDetailView(DetailView):
    model = Progress


class ProgressUpdateView(LoginRequiredMixin, UserFormKwargsMixin, UpdateView):
    model = Progress
    form_class = ProgressForm


class ProgressDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # SuccessMessageMixin hooks to form_valid which is not present on DeleteView to push its message to the user.

    model = Progress
    success_url = reverse_lazy('progress:list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Deleted {obj}')
        return super().delete(request, *args, **kwargs)