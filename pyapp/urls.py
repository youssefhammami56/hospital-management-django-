
from django.contrib import admin
from django.urls import include, path
from pyapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('formdemande', views.formdemande, name='formdemande'),
    path('ajoutdemande', views.ajoutdemande, name='ajoutdemande'),
    path('register', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout', views.logoutuser, name='logout'),
    path('adminnavbar', views.adminnavbar, name='adminnavbar'),
    path('listedespatterminer', views.listedespatterminer, name='listedespatterminer'),
    path('listedespatientenattente', views.listedespatientenattente, name='listedespatientenattente'),
    #path('accepterdemande/<int:id>', views.accepterdemande, name='accepterdemande'),
    path('supprimerdemande/<int:id>', views.supprimerdemande, name='supprimerdemande'),
    path('patientenattent', views.patientenattent, name='patientenattent'),
    path('ajoutdoctor', views.ajoutdoctor, name='ajoutdoctor'),
    path('listedoctor', views.listedoctor, name='listedoctor'),
    path('adddoctoraction', views.adddoctoraction, name='adddoctoraction'),
    path('creerrdv/<int:id>', views.creerrdv, name='creerrdv'),
    path('creerrdv/addrdv/<int:id>', views.addrdv, name='addrdv'),
    path('listrdv', views.listrdv, name='listrdv'),
    path('affichfiche/<int:id>', views.affichfiche, name='affichfiche'),
    path('index2/<int:id>', views.index2, name='index2'),
    path('index2/addfich/<int:id>', views.addfich, name='addfich'),
    path('affichfichepatient/<int:id>', views.affichfichepatient, name='affichfichepatient'),
    path('modiffiche/<int:id>', views.modiffiche, name='modiffiche'),
    path('modiffiche/modif/<int:id>', views.modif, name='modif'),
    path('suppdoc/<int:id>', views.suppdoc, name='suppdoc'),
    path('modifdoc/<int:id>', views.modifdoc, name='modifdoc'),
    path('modifdoc/modifdocaction2/<int:id>', views.modifdocaction2, name='modifdocaction'),
    path('delete/<int:id>', views.delete, name='deletepatient'),
    path('profiledoctor/<int:id>', views.profiledoctor, name='profiledoctor'),
    path('profiledoctor/modifprofiledoc/<int:id>', views.modifprofiledoc, name='modifprofiledoc'),
    path('profiledoctor/modifprofiledoc/modifdoc/<int:id>', views.modifdocaction, name='modifdoc'),
    path('supprdv/<int:id>', views.supprdv, name='supprdv'),
    path('senddocmail/<int:id>', views.senddocmail, name='senddocmail'),
    path('stat', views.stat, name='stat'),
    path('profiledoctor2/<int:id>', views.profiledoctor2, name='profiledoctor2'),
    path('profiledoctor/MypassChangeView',views.MyPasswordChangeView.as_view(),name='MypassChangeView'),
    path('MypassResetView',views.loginpage,name='MypassResetView'),
    path('modifpat/<int:id>', views.modifpat, name='modifpat'),
    path('modifpat/modifpataction/<int:id>', views.modifpataction, name='modifpataction'),
    path('affichefichepatient2/<int:id>', views.affichefichepatient2, name='affichefichepatient2'),
    path('formajoutservice', views.formajoutservice, name='formajoutservice'),
    path('ajoutservice', views.ajoutservice, name='ajoutservice'),
    path('listeservice', views.listservice, name='listeservice'),
    path('suppservice/<int:id>', views.suppservice, name='suppservice'),
    path('modifservice/<int:id>', views.modifservice, name='modifservice'),
    path('modifservice/modifserviceaction/<int:id>', views.modifserviceaction, name='modifserviceaction'),
    path('rendergetfichebycin', views.rendergetfichebycin, name='rendergetfichebycin'),
    path('getfichebycinpatient', views.getfichebycinpatient, name='getfichebycinpatient'),
    path('getfacturepat/<int:id>', views.getfacturepat, name='getfacturepat'),
    path('modifierservice/<int:id>', views.modifierservice, name='modifierservice'),
    path('modifierservice/modifierserviceaction/<int:id>', views.modifierserviceaction, name='modifierserviceaction'),
    
    
]