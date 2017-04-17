from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
# poniższe dwie linijki są potrzebne do zapisu plików w bazie
from django.conf import settings
from django.conf.urls.static import static

import app.forms
import app.views

from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()
urlpatterns = [
    url(r'^$', app.views.home, name='home'), 
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Logowanie',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^start', app.views.startView, name='start'),
    url(r'^personalData/$',app.views.personalDataView,name='personalData'),
    url(r'^wniosek/$',app.views.indexOfertaView,
        name='indexOferta'),
    url(r'^wniosek/(?P<credit_id>[0-9]+)/$',app.views.creditapplicationView,
        name='szczegoly'),
    url(r'^wniosek/(?P<creditapplication_id>[0-9]+)/wyslijoferte/$',
        app.views.proposedofferView,name='proposedOffer'),
    url(r'^wniosek/(?P<creditapplication_id>[0-9]+)/zatwierdzoferte/$',
        app.views.confirmedofferView,name='confirmedOffer'),
    url(r'^wniosek/(?P<creditapplication_id>[0-9]+)/wyslijwymaganedokumenty/$',
        app.views.requireddocumentsView,name='requiredDocuments'),
    url(r'^wniosek/(?P<creditapplication_id>[0-9]+)/przeslijdokumenty/$',
        app.views.sentdocumentView,name='sentDocument'),
    url(r'^wniosek/(?P<creditapplication_id>[0-9]+)/ostatecznadecyzja/$',
        app.views.lastDecisionView,name='lastDecision'),
    url(r'^wniosek/(?P<creditapplication_id>[0-9]+)/odrzucenie/$',
        app.views.rejectionView,name='rejection'),
    url(r'^wniosek/(?P<creditapplication_id>[0-9]+)/rezygnacja/$',
        app.views.resignationView,name='resignation'),

]
# poniższa linijka jest potrzebna do odczytu pliku na stronie
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
