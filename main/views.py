from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


# Create your views here.
class IndexView(View):
    template_name = 'index.html'

    async def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
