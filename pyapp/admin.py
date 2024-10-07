from django.contrib import admin

from pyapp.models import  doctor, patient,rdv, FichePatient,service,facture



class patientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',  'phone', 'address','cin','description','date')
admin.site.register(patient,patientAdmin)
class doctorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'phone', 'address','cin','specialite','description','ser','statut')
admin.site.register(doctor,doctorAdmin)
class rdvAdmin(admin.ModelAdmin):
    list_display = ('pat', 'doc', 'date','time','statut')
admin.site.register(rdv,rdvAdmin)
class FichePatientAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor','cinf','description','traitement','date','time','nbrhos','test')
admin.site.register(FichePatient,FichePatientAdmin)
class serviceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
admin.site.register(service,serviceAdmin)
class factureAdmin(admin.ModelAdmin):
    list_display = ('patient', 'prixhos','prixtest','montanttotal','prixconsultation')
admin.site.register(facture,factureAdmin)
 
