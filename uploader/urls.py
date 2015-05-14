# encoding: utf-8
from django.conf.urls import patterns, url
from .views import (
    BasicVersionCreateView, BasicPlusVersionCreateView,
    JQueryVersionCreateView, AngularVersionCreateView,
    UploadCreateView, UploadDeleteView, UploadListView,
)

urlpatterns = patterns('',
    url(r'^basic/$', BasicVersionCreateView.as_view(), name='upload-basic'),
    url(r'^basic/plus/$', BasicPlusVersionCreateView.as_view(), name='upload-basic-plus'),
    url(r'^new/$', UploadCreateView.as_view(), name='upload-new'),
    url(r'^angular/$', AngularVersionCreateView.as_view(), name='upload-angular'),
    url(r'^jquery-ui/$', JQueryVersionCreateView.as_view(), name='upload-jquery'),
    url(r'^delete/(?P<pk>\d+)$', UploadDeleteView.as_view(), name='upload-delete'),
    url(r'^view/$', UploadListView.as_view(), name='upload-view'),
)
