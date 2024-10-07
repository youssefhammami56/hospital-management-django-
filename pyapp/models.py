from django.db import models

# Create your models here.

class doctor(models.Model):
    
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    cin=models.CharField(max_length=100)
    specialite=models.CharField(max_length=100, null=True)
    description=models.CharField(max_length=100, null=True)
    ser=models.ForeignKey('service',on_delete=models.CASCADE, null=True)
    statut=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username

class patient(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    cin=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class rdv(models.Model):
    pat=models.ForeignKey(patient,on_delete=models.SET_NULL, null=True)
    doc=models.ForeignKey(doctor,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    statut=models.CharField(max_length=100)
    def __str__(self):
        return self.pat.name
class FichePatient(models.Model):
    patient=models.ForeignKey(patient,on_delete=models.CASCADE,)
    doctor=models.ForeignKey(doctor,on_delete=models.CASCADE,)
    date=models.DateField()
    cinf=models.CharField(max_length=100)
    description=models.TextField()
    traitement=models.TextField()
    time=models.TimeField()
    nbrhos=models.IntegerField()
    test=models.BooleanField(("test"), default=False)
    def __str__(self):
        return self.patient.name

class service(models.Model):
    nom=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    def __str__(self):
        return self.nom
class facture(models.Model):
    patient=models.ForeignKey(patient,on_delete=models.CASCADE,)
    montanttotal=models.IntegerField()
    prixtest=models.FloatField()
    prixhos=models.FloatField()
    prixconsultation=models.FloatField(default=75)
    
    def __str__(self):
        return self.patient.name
      