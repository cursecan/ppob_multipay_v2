from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'v2/home-pg.html'

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            return redirect('dashboard:index')

        return super().dispatch(request, *args, **kwargs)