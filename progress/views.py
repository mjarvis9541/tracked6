  
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView, View
from django.urls import reverse_lazy
from .models import Progress
from .forms import ProgressForm


class ProgressListView(LoginRequiredMixin, ListView):
    """ View to list all the Progresss in progress """
    
    ordering = ['-date']
    paginate_by = 25

    def get_queryset(self, **kwargs):
        return Progress.objects.filter(user=self.request.user)


class ProgressCreateView(LoginRequiredMixin, CreateView):
    """ Create a new post in the progress app """

    model = Progress
    form_class = ProgressForm
    success_url = '/'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProgressDetailView(DetailView):
    model = Progress


class ProgressUpdateView(LoginRequiredMixin, UpdateView):
    model = Progress
    form_class = ProgressForm


class ProgressDeleteView(LoginRequiredMixin, DeleteView):
    model = Progress
    success_url = reverse_lazy('progress:list')