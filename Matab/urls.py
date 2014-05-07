from Radiology import views
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Matab.views.home', name='home'),
    # url(r'^Matab/', include('Matab.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add_users/$', views.add_users),
    url(r'^$', views.login_view),
    url(r'logout/$', views.logout_view),
    url(r'^reception/$', views.reception),
    url(r'^waitingList/$', views.waiting_list),
    url(r'appointment/$', views.appointment_day),
    url(r'appointment/([^/]+)/$', views.appointment),
    url(r'^fill_medical_history/$', views.fill_medical_history),
    url(r'^write_response/$', views.write_response),
    url(r'^factor/(\d+)/$', views.show_factor),


    url(r'^register/patient/$', views.register_patient),
    url(r'^register/insurance/$', views.register_insurance),
    url(r'^register/therapist/$', views.register_therapist),
    url(r'^register/operation/$', views.register_operation),
    url(r'^register/complementary_insurance$', views.register_complementary_insurance),


    url(r'^session/patient/(\d+)/(.*)$', views.session_patient),
    url(r'^session/clear_patient$', views.session_clear_patient),

    url(r'^ajax/find_patients/$', views.ajax_find_patients),
    url(r'^ajax/find_insurances/$', views.ajax_find_insurances),
    url(r'^ajax/find_therapists/$', views.ajax_find_therapists),
    url(r'^ajax/find_operations/$', views.ajax_find_operations),
    url(r'^ajax/patient_pay_factor/$', views.ajax_patient_pay_factor),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)