# encoding: utf-8
import json
import mimetypes

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView
from django.conf import settings
from django.core.urlresolvers import reverse
from .models import Upload
from .response import JSONResponse, response_mimetype
from .serialize import serialize
from .forms import BasicUploadForm, AdvancedUploadForm
from .settings import JQUERY_URL
from .registration import upload_handlers


class UploadCreateView(CreateView):
    model = Upload
    form_class = AdvancedUploadForm

    def handle_upload(self):
        mtype = mimetypes.guess_type(self.object.uploaded_file.name)[0]
        handler = upload_handlers.get_handler(mtype)
        if handler is not None:
            new_obj = handler(self.object)
            app_label = new_obj._meta.app_label
            model_name = getattr(new_obj._meta, 'model_name', None) or getattr(new_obj._meta, 'module_name', None)
            self.object.admin_url = reverse("admin:%s_%s_change" % (app_label, model_name), args=[new_obj.pk])
            self.object.related_object = new_obj
            thumb_attr = getattr(upload_handlers.get_handler(mtype), 'thumbnail_attribute', None)
            self.object.thumbnail_attr = thumb_attr
            self.object.save()
            if thumb_attr is not None and new_obj is not None:
                url = getattr(new_obj, thumb_attr)
                if callable(url):
                    self.object.thumbnail = url()
                else:
                    self.object.thumbnail = url.url
            else:
                self.object.thumbnail = '%suploader/img/missing-image.svg' % settings.STATIC_URL

    def form_valid(self, form):
        self.object = form.save()
        self.handle_upload()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        errors = [x.as_text() for x in form.errors.values()]
        files = {'files': [{
            'error': ", ".join(errors),
            'name': form.cleaned_data['uploaded_file'].name,
            'size': form.cleaned_data['uploaded_file'].size,
        }]}
        data = json.dumps(files)
        return HttpResponse(content=data, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(UploadCreateView, self).get_context_data(**kwargs)
        context.update(self.kwargs.get('extra_context', {}))
        context['JQUERY_URL'] = JQUERY_URL
        return context


class BasicVersionCreateView(UploadCreateView):
    template_name_suffix = '_basic_form'
    form_class = BasicUploadForm


class BasicPlusVersionCreateView(UploadCreateView):
    template_name_suffix = '_basicplus_form'


class AngularVersionCreateView(UploadCreateView):
    template_name_suffix = '_angular_form'


class JQueryVersionCreateView(UploadCreateView):
    template_name_suffix = '_jquery_form'


class UploadDeleteView(DeleteView):
    model = Upload

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class UploadListView(ListView):
    model = Upload
    template_name = 'admin/uploader/uploaded_files.html'

    def get_context_data(self, **kwargs):
        context = super(UploadListView, self).get_context_data(**kwargs)
        context.update(self.kwargs.get('extra_context', {}))
        context['JQUERY_URL'] = JQUERY_URL
        context['files'] = [serialize(p) for p in self.get_queryset()]
        return context
