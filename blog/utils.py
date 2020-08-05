from time import time

from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.text import slugify


def generate_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class ObjectListMixin:
    model = None
    template = None

    def get(self, request):
        obj = self.model.objects.all()
        context = {str(self.model.__name__.lower()) + 's': obj}
        return render(request, self.template, context)


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        context = {
            self.model.__name__.lower(): obj,
            'admin_object': obj,
            'detail': True,
        }
        return render(request, self.template, context)


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        if request.user.id == obj.author_id or request.user.is_staff \
                or request.user.is_superuser:
            bound_form = self.model_form(instance=obj)
            context = {'form': bound_form, self.model.__name__.lower(): obj}
            return render(request, self.template, context)
        else:
            raise ValidationError(
                'Only creator can edit that %s' % self.model.__name__.lower()
            )

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        context = {'form': bound_form, self.model.__name__.lower(): obj}
        return render(request, self.template, context)


class ObjectDeleteMixin:
    model = None
    get_template = None
    post_template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        if request.user.id == obj.author_id or request.user.is_staff \
                or request.user.is_superuser:
            context = {self.model.__name__.lower(): obj}
            return render(request, self.get_template, context)
        else:
            raise ValidationError(
                'Only creator can delete that %s' % self.model.__name__.lower()
            )

    def post(self, request, slug):
        tag = self.model.objects.get(slug__iexact=slug)
        tag.delete()
        return redirect(reverse(self.post_template))
