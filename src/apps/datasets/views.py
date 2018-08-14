import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from datasets.models import Data


class DataManagement(LoginRequiredMixin, TemplateView):
    template_name = 'datasets/management.html'


def download(request, key):
    data = get_object_or_404(Data, key=key)
    return FileResponse(open(data.data_file.path, 'rb'), as_attachment=True)
