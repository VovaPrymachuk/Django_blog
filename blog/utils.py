from time import time

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify


def generate_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class ObjectListMixin:
    model = None
    template = None

    def get(self, request):
        obj = self.model.objects.all()
        context = {self.model.__name__.lower(): obj}
        return render(request, self.template, context)


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        context = {self.model.__name__.lower(): obj}
        return render(request, self.template, context)


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        context = {'form': bound_form, self.model.__name__.lower(): obj}
        return render(request, self.template, context)

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        context = {'form': bound_form, self.model.__name__.lower(): obj}
        return render(request, self.template, context)
