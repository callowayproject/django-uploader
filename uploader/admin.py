from django.contrib import admin

from .models import Upload
from .views import UploadCreateView


class UploadAdmin(admin.ModelAdmin):
    '''
    Admin View for Uploads
    '''
    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        super_resp = super(UploadAdmin, self).changelist_view(request, extra_context)
        return UploadCreateView.as_view(template_name="admin/uploader/change_list.html")(request, extra_context=super_resp.context_data)

    def list_view(self, request, extra_context=None):
        from views import UploadListView
        super_resp = super(UploadAdmin, self).changelist_view(request, extra_context)
        return UploadListView.as_view()(request, extra_context=super_resp.context_data)

    def get_urls(self):
        from django.conf.urls import patterns

        urls = super(UploadAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^uploaded_files/$', self.list_view)
        )
        return my_urls + urls

admin.site.register(Upload, UploadAdmin)
