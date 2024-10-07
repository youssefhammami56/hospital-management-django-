from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from pyapp.models import FichePatient, facture,   patient,doctor,rdv, service
from django.contrib.auth import authenticate,login,logout
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
from datetime import date, datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetDoneView,PasswordChangeView

def index(request):
    img='/static/img/1.png'
    img2='/static/img/2.png'
    img3='/static/img/3.png'
    
    return render(request, 'index.html', {'img':img,'img2':img2,'img3':img3})
def contact(request):
    return render(request, 'contact.html')

def about(request):
    img='/static/img/1.png'
    return render(request, 'about.html', {'img':img})

def formdemande(request):
    today = date.today()
    max_date = today.strftime('%Y-%m-%d')

    
    return render(request, 'demande.html',{'max_date':max_date})

def ajoutdemande(request):
    nom=request.POST['name']
    cin=request.POST['cin']
    email=request.POST['email']
    tel=request.POST['phone']
    address=request.POST['adresse']
    description=request.POST['description']
    datee=request.POST['date']
    
    if patient.objects.filter(cin=cin):
        p=patient.objects.get(cin=cin)
        if rdv.objects.filter(pat=p).exists():
            if rdv.objects.get(pat=p).statut=='done':
                r=rdv.objects.get(pat=p)
                r.delete()
                
                fac=facture.objects.get(patient=p)
               
                
                p.description=description
                p.save()
                messages.success(request,'your request has been sent successfully')
               
                return HttpResponseRedirect(reverse('formdemande'))
            else:
                messages.error(request,'dear patient, you already have an appointment with us')
            return HttpResponseRedirect(reverse('formdemande'))
        else:
            messages.error(request,'dear patient you have a request we will make an appointment with you')
            
            return HttpResponseRedirect(reverse('formdemande'))
   

    else:
        d=patient(name=nom,cin=cin,email=email,phone=tel,address=address,description=description,date=datee)
        d.save()
        messages.success(request,'your request has been sent successfully')
        return HttpResponseRedirect(reverse('formdemande'))

def register(request):
    form = CreateUserForm()  
    if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                
                user=form.cleaned_data.get('username')
                pass1=form.cleaned_data.get('password1')
                d=doctor(username=user,password=pass1)
                d.save()
                messages.success(request, 'Account was created succesfully for ' + user)
                return redirect('login')        
    context={'form':form}
    return render(request,'register.html',context)

def loginpage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('stat')
        else:
            return redirect('listrdv')
        
    else:
   
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            
           
            if doctor.objects.filter(username=username,password=password):
                doc=doctor.objects.get(username=username,password=password)
                user=authenticate(request,username=username,password=password)
                if user is not None:
        
                    login(request,user)
                   
                else:
                    messages.info(request,'Username or password is incorrect')

                
                
            else:
                user=authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    
                else:
                    messages.info(request,'Username or password is incorrect')
            if request.user.is_superuser:
                return redirect('stat')
            else:
                return redirect('listrdv')
        return render(request,'login.html')

@login_required(login_url='login')
def logoutuser(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def adminnavbar(request):
    rdvv=rdv.objects.all()
    #je veux les patient qui n'ont pas de rdv
    a="asdasd"
    ppp=patient.objects.all()
    for i in rdvv:
        for j in ppp:
            if i.pat==j:
                ppp=ppp.exclude(id=j.id)
                
    return render(request,'adminnavbar.html',{'p':ppp,'a':a})
    
@login_required(login_url='login')
def listedespatterminer(request):
    #get patient qui ont deja un rdv
    p=patient.objects.all()
    d=[]
    for i in p:
        if rdv.objects.filter(pat=i).exists():
            if rdv.objects.get(pat=i).statut=='done':
                d.append(i)
    
    return render(request,'listepatterminer.html',{'d':d})
@login_required(login_url='login')
def listedespatientenattente(request):
    #get patient qui ont deja un rdv
    p=patient.objects.all()
    d=[]
    for i in p:
        if rdv.objects.filter(pat=i).exists():
            if rdv.objects.get(pat=i).statut=='en attente':
                d.append(i)
    
    return render(request,'listedesdemandes.html',{'d':d})
@login_required(login_url='login')
def supprimerdemande(request,id):
    d=patient.objects.get(id=id)
   
    if facture.objects.filter(patient=d).exists():
       fac=facture.objects.get(patient=d)
       fac.delete()
    rdvv=rdv.objects.get(pat=d)
    rdvv.delete()
    
    name=d.name
    email=EmailMessage('Hello from hopital','dear '+d.name+' your demande has been rejected on va vous contacter ulterirement',settings.EMAIL_HOST_USER,[d.email])
    #email.send()
    
    messages.success(request,'  '+name+' was successfully deleted !  ')
    return HttpResponseRedirect(reverse('listedespatterminer'))
#def accepterdemande(request,id):
    d=demande.objects.get(id=id)
    p=patient.objects.all()
    for i in p:
        if i.id==d.id:
            messages.info(request,'patient already exist')
            d.delete()
            return HttpResponseRedirect(reverse('listedesdemandes'))
    p=patient(name=d.name,cin=d.cin,email=d.email,phone=d.phone,address=d.address,description=d.description,date=d.date)
    p.save()
    email=EmailMessage('Hello from hospital','dear '+d.name+' your request has been accepted we have set an appointment on the date you have chosen',settings.EMAIL_HOST_USER,[d.email])
    #email.send()
    messages.success(request,'patient added')
    d.delete()
    return HttpResponseRedirect(reverse('listedesdemandes'))
@login_required(login_url='login')
def patientenattent(request):
    
    rdvv=rdv.objects.all()
    #je veux les patient qui n'ont pas de rdv
    p=patient.objects.all()
    for i in rdvv:
        for j in p:
            if i.pat==j:
                p=p.exclude(id=j.id)
    pp=patient.objects.all()
    for i in pp:
        for j in rdvv:
            if i.cin==j.pat.cin:
                
                    p=p.exclude(id=i.id)

    
    
    return render(request,'patientenattent.html',{'p':p,'rdvv':rdvv})
@login_required(login_url='login')
def ajoutdoctor(request):
    dep=service.objects.all()
    return render(request,'ajoutdoctor.html',{'dep':dep})
@login_required(login_url='login')
def adddoctoraction(request):
    username=request.POST['name']
    email=request.POST['email']
    password=request.POST['password']
    password2=request.POST['password2']
    address=request.POST['address']
    sp=request.POST['spec']
    cin=request.POST['cin']
    s=request.POST['s']
    statut=request.POST['statut']
    dep=service.objects.get(id=s)
    phone=request.POST['phone']
    if password!=password2:
        messages.error(request,'you need to confirm the password')
        return HttpResponseRedirect(reverse('ajoutdoctor'))
    elif doctor.objects.filter(username=username):
        messages.error(request,'username already exist')
        return HttpResponseRedirect(reverse('ajoutdoctor'))
    else:
        d=doctor(username=username,email=email,password=password,phone=phone,address=address,cin=cin,specialite=sp,ser=dep,statut=statut)
        d.save()
        User.objects.create_user(username=username,email=email,password=password)
        messages.success(request,'doctor added successfully')
        return HttpResponseRedirect(reverse('listedoctor'))
@login_required(login_url='login')
def listedoctor(request):
    userr=doctor.objects.all()
    return render(request,'listedoctor.html',{'userr':userr})
@login_required(login_url='login')
def creerrdv(request,id):
    d=patient.objects.get(id=id)
    img='/static/img/1.png'
    doc=doctor.objects.all()
    r=rdv.objects.all()
    error=False
    today=datetime.today()
    min_date=today.strftime('%Y-%m-%d')
    
    firstheure=datetime.time(datetime.now())
    start=firstheure.strftime('%H')
    #
    end_time=firstheure.strftime('%H:%M')
    
        
    
    return render(request,'creerrdv.html',{'p':d,'doc':doc,'img':img,'min_date':min_date,'start':start,'end_time':end_time})
@login_required(login_url='login')
def listrdv(request):
    #je veux avoir les rdv qui ont date et time superieur a la date et time actuelle
    if request.user.is_superuser:
        rdvv=rdv.objects.all()
        f=FichePatient.objects.all()
        return render(request,'listerendervous.html',{'rdvv':rdvv,'f':f})
    else:
        a=request.user.username
        d=doctor.objects.get(username=a)
        rdvv=rdv.objects.filter(doc=d)
    return render(request,'listerendervous.html',{'rdvv':rdvv,'a':a,'d':d})
@login_required(login_url='login')
def addrdv(request,id):
    pat=request.POST['name']
    doc=request.POST['s']
    date=request.POST['date']
    time=request.POST['time']
    statut='en attente'
    p=patient.objects.get(id=id)
    d=doctor.objects.get(id=doc)
    docname=d.username
    if rdv.objects.filter(doc=doc,date=date,time=time):
        messages.error(request,docname+' already has an appointment for this date and time')
        return HttpResponseRedirect(reverse('creerrdv',args=[p.id]))
    else:
        email=EmailMessage('Hello from hospital','dear '+p.name+' your appointment has been accepted on '+date+' at '+time+' with doctor '+docname,settings.EMAIL_HOST_USER,[p.email])
        email.send()
        email=EmailMessage('Hello from hospital','dear '+docname+' you have a new appointment on '+date+' at '+time+' with patient '+p.name,settings.EMAIL_HOST_USER,[d.email])
        email.send()
   
        rdvv=rdv(pat=p,doc=d,date=date,time=time,statut=statut)
        rdvv.save()

    
        messages.success(request,'appointment added successfully')
        return HttpResponseRedirect(reverse('patientenattent'))
@login_required(login_url='login')
def affichfiche(request,id):
    p=patient.objects.get(id=id)
    return render(request,'fiche.html',{'p':p})

@login_required(login_url='login')
def index2(request,id):
    doctorr=doctor.objects.all()
    rddv=rdv.objects.get(id=id)
    p=rddv.pat
   
    
    pa=patient.objects.get(id=p.id)
    f=FichePatient.objects.all()
    

    
    error=""
    for i in f:
        if i.patient.id==p.id:
            error="patient has already a fich"
            messages.info(request,pa.name+'already has a file you can consult it')
            return HttpResponseRedirect(reverse('listrdv'))
    
    return render(request, 'ajoutfiche.html',{'doctorr':doctorr,'p':pa,'error':error})
@login_required(login_url='login')
def addfich(request,id):

    nom=request.POST['patient']
    doctorr=request.POST['doc']
    cin=request.POST['cin']
    date=request.POST['date']
    description=request.POST['desc']
    trait=request.POST['trait']
    t=request.POST['time']
    test=request.POST['test']
    if test=='oui':
        test= True
        prixtest=50

    else:
        test=False
        prixtest=0
    nbrhos=request.POST['nbrhosp']
    d=doctor.objects.get(id=doctorr)
    p=patient.objects.get(id=id)
    f=FichePatient.objects.all()
    rdvv=rdv.objects.get(pat=p)
    rdvv.statut='done' 
    rdvv.save()
    #check if patient has already a fich
    for i in f:
        if i.patient.id==p.id:
            
            return HttpResponseRedirect(reverse(''))
            
    f=FichePatient(patient=p,doctor=d,date=date,cinf=cin,description=description,traitement=trait,time=t,test=test,nbrhos=nbrhos)
  
    nbr=int(nbrhos)

    prixhos=100*nbr
    prix=prixhos+prixtest+75
    fac=facture(patient=p,montanttotal=prix,prixtest=prixtest,prixhos=prixhos,prixconsultation=75)
    fac.save()
    f.save()
    messages.success(request,'File addes succefully')


    
    return HttpResponseRedirect(reverse('listrdv'))
@login_required(login_url='login')
def affichfichepatient(request,id):
    rd=rdv.objects.get(id=id)
    p=rd.pat
    # i want to check if patient has already a fich if yes i want to display it if not i want to display a message by the cin of patient
    f=FichePatient.objects.all()
    for i in f:
        if i.patient.cin==p.cin:
            f=FichePatient.objects.get(patient=p)
            return render(request,'fiche2.html',{'f':f,'p':p})
    messages.info(request,'the appointment has not yet been made')
    return HttpResponseRedirect(reverse('listrdv'))

    
   
@login_required(login_url='login')
def modiffiche(request,id):
    f=FichePatient.objects.get(id=id)
    p=patient.objects.get(id=f.patient.id)
    d=doctor.objects.all()
    
    template=loader.get_template('modiffiche.html')
    context={
        'f':f,
        'p':p,
        'd':d,
        
    }

   
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')
def modif(request,id):
    f=FichePatient.objects.get(id=id)
    p=patient.objects.get(id=f.patient.id)
    p.name=request.POST['patient']
    rdvv=rdv.objects.get(pat=p)
    rdvv.statut='done' 
    rdvv.save()
    p.save()
    fac=facture.objects.get(patient=p)
    test=request.POST['test']
    nbrhos=request.POST['nbrhosp']
    if test == "oui":
        prixtest=50
    else:
        prixtest=0

    nbr=int(nbrhos)

    prixhos=100*nbr
    prix=prixhos+prixtest+75
    fac.patient=p
    fac.montanttotal=prix
    fac.prixtest=prixtest
    fac.prixhos=prixhos
    fac.save()
    
    d=request.POST['doctor']
    f.patient.name=request.POST['patient']
    f.description=request.POST['desc']
    f.traitement=request.POST['trait']
    f.date=request.POST['date']
    f.time=request.POST['time']
    f.doctor=doctor.objects.get(username=d)
    if test == "oui":
        f.test=True
    else:
        f.test=False

    f.nbrhos=nbrhos

    
    f.save()
    return HttpResponseRedirect(reverse('listrdv'))
@login_required(login_url='login')
def suppdoc(request,id):
    d=doctor.objects.get(id=id)

    d.delete()
    userr=User.objects.get(username=d.username)
    userr.delete()
    messages.success(request,'doctor deleted')
    return HttpResponseRedirect(reverse('listedoctor'))
@login_required(login_url='login')
def modifdoc(request,id):
    d=doctor.objects.get(id=id)
    s=service.objects.all()
    template=loader.get_template('modifierdoctor.html')
    context={
        'd':d,
        's':s,
    }
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')
def modifdocaction2(request,id):
    pass1=request.POST['password']
    pass2=request.POST['password2']
    if pass1!=pass2:
        messages.info(request,'passwords are not the same')
        return HttpResponseRedirect(reverse('modifdoc',args=(id,)))
    else:
        i=id
        d=doctor.objects.get(id=i)
        name=request.POST['name']
        d.username=request.POST['name']
        d.email=request.POST['email']
        d.password=request.POST['password']
        d.address=request.POST['address']
        d.cin=request.POST['cin']
        d.phone=request.POST['phone']
        ser=request.POST['service']
        d.ser=service.objects.get(id=ser)
        d.specialite=request.POST['specialite']
        
        d.save()
        userr=User.objects.get(id=i+1)
        userr.username=request.POST['name']
        userr.email=request.POST['email']
        userr.password=userr.password
        
        userr.save()
        messages.success(request,'doctor successfully modified')
    return HttpResponseRedirect(reverse('listedoctor'))
@login_required(login_url='login')
def delete(request,id):
    p=patient.objects.get(id=id)
    p.delete()
    messages.success(request,'patient deleted')
    return HttpResponseRedirect(reverse('patientenattent'))
@login_required(login_url='login')
def profiledoctor2(request,id):
   
    d=doctor.objects.get(id=id)
    template=loader.get_template('profile.html')
    context={
        'd':d,
        
    }
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')
def profiledoctor(request,id):
    user=request.user
    i=id-1
    d=doctor.objects.get(id=i)
    template=loader.get_template('profile.html')
    context={
        'd':d,
        'user':user,
    }
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')
def modifprofiledoc(request,id):
    i=id
    
    d=doctor.objects.get(id=i)
    s=service.objects.all()
    template=loader.get_template('modifdoctor.html')
    context={
        'd':d,
        's':s,
    }
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')

def modifdocaction(request,id):
    
    d=doctor.objects.get(id=id)
    userr=User.objects.get(id=id+1)
    userr.username=request.POST['name']
    userr.email=request.POST['email']
    userr.password=userr.password
    
    userr.save()
    d.username=request.POST['name']
    d.email=request.POST['email']
    d.password=request.POST['password']
    d.address=request.POST['address']
    d.cin=request.POST['cin']
    d.phone=request.POST['phone']
    d.specialite=request.POST['specialite']
    d.description=request.POST['description']
    
    d.statut=request.POST['statut']
    
    d.save()
    
    messages.success(request,'doctor successfully modified')
    return HttpResponseRedirect(reverse('profiledoctor', args=(id+1,)))
@login_required(login_url='login')
def supprdv(request,id):
    r=rdv.objects.get(id=id)
    r.delete()
    
    messages.success(request,'appointment deleted successfully')
    return HttpResponseRedirect(reverse('listrdv'))
@login_required(login_url='login')
def senddocmail(request,id):
    d=doctor.objects.get(id=id)
    email=d.email
    subject="test"
    message="hello"+d.username+"you must file all your informations"
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    #send_mail(subject,message,email_from,recipient_list)
    return HttpResponseRedirect(reverse('listedoctor'))
@login_required(login_url='login')
def stat(request):
    d=doctor.objects.all()
    dd=doctor.objects.filter(statut='disponible')
    p=patient.objects.all()
    r=rdv.objects.all()
    rd=rdv.objects.filter(statut='en attente')
    rdd=rdv.objects.filter(statut='done')
    eroor=1
    
    ppp = patient.objects.all()
    for i in r:
        for j in ppp:
            if i.pat == j:
                ppp = ppp.exclude(id=j.id)
                eroor=1
   
    f=FichePatient.objects.all()
    s=service.objects.all()
    ld=len(d)
    lrdd=len(rdd)
    r=len(r)
    
    lr=len(rd)
    lf=len(f)
    lrd=len(rd)
    ldm=len(p)
    lp=ldm-lr
    s=len(s)
    dd=len(dd)
    
    
    context={
        'ld':ld,
        'lp':lrd,
        'lr':lr,
        'lf':lf,
        'ldm':ldm,
        'lrdd':lrdd,
        'lp':lp,
        'r':r,
        's':s,
        'dd':dd,
        'ppp':ppp,
        'eroor':eroor,
    }
    return render(request,'stat.html',context)


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'password-change.html'
    success_url = reverse_lazy('MypassResetView')

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password-reset-done.html'
@login_required(login_url='login')
def modifpat(request,id):
    p=patient.objects.get(id=id)
    img='/static/img/1.png'
    template=loader.get_template('modifpat.html')
    context={
        'p':p,
        'img':img,
    }
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')
def modifpataction(request,id):
    p=patient.objects.get(id=id)
    p.name=request.POST['name']
    p.email=request.POST['email']
    
    p.address=request.POST['adresse']
    p.cin=request.POST['cin']
    p.phone=request.POST['phone']
    p.description=request.POST['description']
    p.save()
    messages.success(request,'patient modified')
    return HttpResponseRedirect(reverse('patientenattent'))
@login_required(login_url='login')
def affichefichepatient2(request,id):
    p=patient.objects.get(id=id)
    if rdv.objects.filter(pat=p).exists():
        rdvv=rdv.objects.get(pat=p)
        if FichePatient.objects.filter(patient=p).exists():
            f=FichePatient.objects.get(patient=p)
            template=loader.get_template('fiche2.html')
            context={
            'p':p,
            'f':f,
            'rdvv':rdvv,
         }
            return HttpResponse(template.render(context,request))
        else:
            messages.error(request,' '+p.name+ ' does not have a file  ')
            return HttpResponseRedirect(reverse('listedesdemandes'))
    
      
       
    else:
        messages.error(request,' '+p.name+ '  does not have an appointment ')
        return HttpResponseRedirect(reverse('listedesdemandes'))
@login_required(login_url='login')
def formajoutservice(request):
    template=loader.get_template('ajouterservice.html')
    context={
        
    }
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')
def ajoutservice(request):
    if request.method=='POST':
        s=service()
        s.nom=request.POST['name']
        s.description=request.POST['description']
        s.save()
        messages.success(request,'service added successfully')
    return HttpResponseRedirect(reverse('listeservice'))
@login_required(login_url='login')
def listservice(request):
    s=service.objects.all()
    tabdoctor=[]
    for i in s:
        tabdoctor.append(i)

    template=loader.get_template('listeservice.html')
    context={
        's':s,
        'tabdoctor':tabdoctor,
    }
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')
def suppservice(request,id):
    s=service.objects.get(id=id)
    s.delete()
    messages.success(request,'service deleted')
    return HttpResponseRedirect(reverse('listeservice'))
@login_required(login_url='login')
def modifservice(request,id):
    s=service.objects.get(id=id)
    template=loader.get_template('modifservice.html')
    context={
        's':s,
    }
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')
def modifserviceaction(request,id):
    s=service.objects.get(id=id)
    s.nom=request.POST['name']
    s.description=request.POST['description']
    s.save()
    messages.success(request,'service modified')
    return HttpResponseRedirect(reverse('listservice'))

def rendergetfichebycin(request):
    template=loader.get_template('getfichebycin.html')
    context={

    }
    
    return HttpResponse(template.render(context,request))

def getfichebycinpatient(request):
    if request.method=='POST':
        cin=request.POST['cin']
        if patient.objects.filter(cin=cin).exists():
            p=patient.objects.get(cin=cin)
            if rdv.objects.filter(pat=p).exists():
                rdvv=rdv.objects.get(pat=p)
                if FichePatient.objects.filter(patient=p).exists():
                    f=FichePatient.objects.get(patient=p)
                    template=loader.get_template('fiche2.html')
                    context={
                    'p':p,
                    'f':f,
                    'rdvv':rdvv,
                }
                    return HttpResponse(template.render(context,request))
                else:
                    messages.error(request,' '+p.name+ '  does not have a file  ')
                    return HttpResponseRedirect(reverse('listedesdemandes'))
    
      
       
            else:
                messages.error(request,' '+p.name+ '  does not have an appointment ')
                return HttpResponseRedirect(reverse('listedesdemandes'))
        else:
            messages.error(request,'patient not found')
            return HttpResponseRedirect(reverse('rendergetfichebycin'))
@login_required(login_url='login')
def getfacturepat(request,id):
    p=patient.objects.get(id=id)
    if rdv.objects.filter(pat=p).exists():

        fac=facture.objects.get(patient=p)
        f=FichePatient.objects.get(patient=p)
        tax=fac.montanttotal*0.25
        totale=fac.montanttotal+tax
        
        template=loader.get_template('facture.html')
        context={
        'p':p,
        'f':f,
        'fac':fac,
        'tax':tax,
        'totale':totale,
         }
        return HttpResponse(template.render(context,request))
    else:
            messages.error(request,' '+p.name+ '  does not have an invoice  ')
            return HttpResponseRedirect(reverse('listedesdemandes'))
@login_required(login_url='login')
def modifierservice(request,id):
    s=service.objects.get(id=id)
    template=loader.get_template('modifservice.html')
    context={
        's':s,
    }
    return HttpResponse(template.render(context,request))
@login_required(login_url='login')
def modifierserviceaction(request,id):
    s=service.objects.get(id=id)
    s.nom=request.POST['name']
    s.description=request.POST['description']
    s.save()
    messages.success(request,'service modified')
    return HttpResponseRedirect(reverse('listeservice'))

    
      
       
  
   

        

    
        





