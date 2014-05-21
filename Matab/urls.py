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
    url(r'^fill_medical_history/$', views.fill_medical_history),
    url(r'^write_response/$', views.write_response),
    url(r'^factor/(\d+)/$', views.show_factor),
    url(r'^print_medical_history/$', views.print_medical_history),
    url(r'^sign_technician_in/$', views.sign_technician_in),
    url(r'^sign_technician_out/$', views.sign_technician_out),
    url(r'^show_unpaid_factors/$', views.show_unpaid_factors),
    url(r'^add_good_to_store/$', views.add_good_to_store),
    
    
    url(r'^choose/personnel/$', views.choose_personnel),
    url(r'^choose/insurance/$', views.choose_insurance),
    url(r'^choose/complementary/$', views.choose_complementary),
    url(r'^choose/therapist/$', views.choose_therapist),
    url(r'^choose/patient/$', views.choose_patient ),
    url(r'^choose/operation/$', views.choose_operation),
    
    
    url(r'^storing/$', views.storing),
    
    url(r'^accounting/$', views.accounting_page),
    url(r'^accounting/patient$', views.accounting_patient),
    url(r'^accounting/personnel$', views.accounting_personnel),
    url(r'^accounting/insurance$', views.accounting_insurance),
    url(r'^accounting/complementary$', views.accounting_complementary),
    url(r'^accounting/therapist/$', views.accounting_therapist),
    
    url(r'^appointment/$', views.appointment),

    url(r'^register/patient/$', views.register_patient),
    url(r'^register/insurance/$', views.register_insurance),
    url(r'^register/therapist/$', views.register_therapist),
    url(r'^register/operation/$', views.register_operation),
    url(r'^register/complementary_insurance$', views.register_complementary_insurance),
    url(r'^register/good$', views.register_good),
    url(r'^register/appointment$', views.register_appointment),
    

    url(r'^edit$', views.edit ),
    url(r'^edit/patient$', views.edit_patient),
    url(r'^edit/therapist$', views.edit_therapist),
    url(r'^edit/insurance$', views.edit_insurance),
    url(r'^edit/complementary$', views.edit_complementary),
    url(r'^edit/personnel$', views.edit_personnel),
    url(r'^edit/operation/$', views.edit_operation),


    url(r'^session/patient/(\d+)/(.*)$', views.session_patient),
    url(r'^session/clear_patient$', views.session_clear_patient),
    url(r'^session/patient_and_set_factor/(\d+)(.*)$', views.session_patient_and_set_factor),

    url(r'^ajax/find_patients/$', views.ajax_find_patients),
    url(r'^ajax/find_insurances/$', views.ajax_find_insurances),
    url(r'^ajax/find_therapists/$', views.ajax_find_therapists),
    url(r'^ajax/find_operations/$', views.ajax_find_operations),
    url(r'^ajax/find_patients_list/$', views.ajax_find_patients_list),
    url(r'^ajax/patient_pay_factor/$', views.ajax_patient_pay_factor),
    url(r'^ajax/patient_pay_partial_factor/$', views.ajax_patient_pay_partial_factor),
    url(r'^ajax/find_good/$', views.ajax_find_good),
    url(r'^ajax/edit/good/$', views.ajax_edit_good),
    url(r'^ajax/edit/patient/$', views.ajax_edit_patient),
    url(r'^ajax/edit/therapist/$', views.ajax_edit_therapist),
    url(r'^ajax/edit/insurance/$', views.ajax_edit_insurance),
    url(r'^ajax/edit/complementary/$', views.ajax_edit_complementary),
    url(r'^ajax/edit/operation/$', views.ajax_edit_operation),

    url(r'^test_calendar/$', views.test_calendar),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)