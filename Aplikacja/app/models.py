from django.db import models
from django.utils import timezone

class PortalUser(models.Model):
    role = models.CharField(max_length=20)
    id_user = models.ForeignKey('auth.User',primary_key = True)#id z tabelkiUser
class AccessStatus(models.Model):
    status_id = models.AutoField(primary_key = True)
    status_name = models.CharField(max_length=50)
    access_to_role = models.CharField(max_length=20)
class PersonalData(models.Model):
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    pesel = models.CharField(max_length=11,unique=True,blank=False)#wymagalne
    name = models.CharField(max_length=50,blank=False)#wymagalne
    surname = models.CharField(max_length=50,blank=False)#wymagalne
    identity_card = models.CharField(max_length=9)#wymagalne
    telephon_number = models.CharField(max_length = 9,blank = True)#niewymaglane
    mail = models.EmailField(max_length = 100,blank=False)#wymagalne
    monthly_expenses = models.FloatField(blank=False)#wymagalne
    city = models.CharField(max_length = 50,blank = False)#wymagalne
    postal_code = models.CharField(max_length = 6,blank = False)#wymagalne
    street = models.CharField(max_length = 50,blank = True)#nie jest wymagalne
    house_number = models.IntegerField(blank=False)#wymagalne
    flat_number = models.CharField(max_length = 5,blank = True)#nie jest wymagalne
    GIMNAZJALNE = 'GIM'
    PODSTAWOWE = 'POD'#PRAWIDLOWE PODSTAWOWE
    ZASADNICZE_ZAWODOWE = 'ZAZ'
    SREDNIE = 'SRE'
    WYZSZE = 'WYZ'
    EDUCATION_CHOICES = (
        (GIMNAZJALNE, 'gimnazjalne'),
        (PODSTAWOWE, 'podstawowe'),
        (ZASADNICZE_ZAWODOWE, 'zasadnicze zawodowe'),
        (SREDNIE, 'średnie'),
        (WYZSZE, 'wyższe'),
    )
    education = models.CharField(max_length = 20,
                                 blank = False,
                                 choices=EDUCATION_CHOICES,
                                 default=PODSTAWOWE)#wymagalne z listy rozwijanej
    KAWALER = 'kawaler'
    PANNA = 'panna'
    WDOWIEC = 'wdowiec'
    WDOWA = 'wdowa'
    ROZWODNIK = 'rozwodnik'
    ROZWODKA = 'rozwódka' #prawidlowe ROZWODNIK
    BRAK = 'brak'
    MARTIAL_CHOICES = (
        (BRAK,'brak'),
        (KAWALER, 'kawaler'),
        (PANNA, 'panna'),
        (WDOWIEC, 'wdowiec'),
        (WDOWA, 'wdowa'),
        (ROZWODNIK, 'rozwodnik'),
        (ROZWODKA, 'rozwódka'),
    )
    marital_status = models.CharField(max_length = 20,
                                      blank = False,
                                      choices=MARTIAL_CHOICES,
                                      default=BRAK)#wymagalne z listy rozwijanej
    iban_number = models.CharField(max_length = 26, blank=True,null=True) 
class IncomeName(models.Model):
     id = models.AutoField(primary_key = True) # automatycznie się dodaje
     name = models.CharField(max_length=50)
     table_name = models.CharField(max_length=50) # tutaj trafia nazwa bazy
class ProposedOffer(models.Model):
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    initial_amount = models.DecimalField(decimal_places=2,max_digits=8,blank=False) # wymagalna zaproponowana kwota
    maximal_amount = models.DecimalField(decimal_places=2,max_digits=8,blank=False) # wymagalne maksymalna kwota
    minimum_load_period = models.IntegerField(blank = False) # wymagalne minimalny okres kredytowania
    maximum_load_period = models.IntegerField(blank = False) # wymagalne maksymalny okres kredytowania

class ConfirmedOffer(models.Model):
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    confirmed_amount = models.DecimalField(decimal_places=2,max_digits=8,blank=False) # zatwierdzona kwota
    period_approved = models.IntegerField(blank = False) #zatwierdzony okres
    installment_amount = models.DecimalField(decimal_places=2,max_digits=8,blank=False) # kwota raty bedzie wyliczane ale nie pokazywane
    totall_credit_amount = models.DecimalField(decimal_places=2,max_digits=8,blank=False)# laczna kwota kredytu bedzie wyliczane ale nie pokazywane
class TechnicalDocument(models.Model):
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    document_name = models.CharField(max_length= 50,unique=True,blank=False) # wymagalne 
class RequiredDocument(models.Model):
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    documents_number = models.CharField(max_length= 50,blank=False) # wymagalne 
class SentDocument(models.Model):
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    file = models.FileField(upload_to='documents/%Y/%m/%d//')# ścieżka gdzie ma się zapisać plik
    name = models.CharField(max_length= 50,blank=False) # wymagalne 
    #NEGAT0 = 'brak'
    #NEGAT1 = 'neg1'
    #NEGAT2 = 'neg2'
    #NEGAT3 = 'neg3'
    #NEGAT4 = 'neg4'
    #NEGAT5 = 'neg5'
    #NEGAT6 = 'neg6'
    #NEGAT_CHOICES = (
     #   (NEGAT0, 'Dokument pawidłowy'),
     #   (NEGAT1, 'Plik się nie otwiera'),
     #   (NEGAT2, 'Brak podpisu'),
     #   (NEGAT3, 'Slaba jakosc dokumentu'),
     #   (NEGAT4, 'Nieczytelne dane'),
     #   (NEGAT5, 'Zly format dokumentu'),
     #   (NEGAT6, 'Nieprawidlowy okres dochodowy'),
    #)
    reason_negativ_decision = models.CharField(max_length = 50,
                                      blank = True)#,
                                      #choices=NEGAT_CHOICES,
                                      #default=NEGAT0)
    added_date = models.DateTimeField(default=timezone.now)
class CreditApplication(models.Model):
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    personal_data = models.OneToOneField(PersonalData, on_delete=models.CASCADE,blank = False,null=True)#jesli usuniety zostanie człowieczek to również usuniety będzie dokument, unikatowy system nie pozwoli na dodanie nowego wniosku kredytowego dla danej osoby
    icome = models.ForeignKey(IncomeName,on_delete=models.CASCADE,blank = True,null=True) # niewymagalne, moze być puste
    proposed_offer = models.ForeignKey(ProposedOffer,on_delete=models.CASCADE,blank = True,null=True)# niewymagalne, moze być puste
    confirmed_offer = models.ForeignKey(ConfirmedOffer,on_delete=models.CASCADE,blank = True,null=True)#może być pusty niewymagany
    required_document = models.ForeignKey(RequiredDocument,on_delete=models.CASCADE,blank = True,null=True)# niewymagalne, moze być puste
    added_documents = models.ForeignKey(SentDocument,on_delete=models.CASCADE,blank=True,null=True)# niewymagalne, moze być puste
    status = models.ForeignKey(AccessStatus,on_delete=models.CASCADE,blank = False) # wymagalne
    comment = models.CharField(max_length= 50,blank=True,null=True)# dodane pole do wprowadzenia komentarza
class ContractTable(models.Model):
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    application = models.OneToOneField(CreditApplication,on_delete=models.CASCADE,blank = False,null=True) #wymagalne, moze być puste
    date_start_of_employment = models.DateField(blank=False)# musi być podane
    end_of_employment = models.DateField(blank = True, null = True)# może być niepodane
    el1 = 'el1'
    el2 = 'el2'
    el3 = 'el3'
    el4 = 'el4'
    el5 = 'el5'
    el6 = 'el6'
    el7 = 'el7'
    el8 = 'el8'
    el9 = 'el9'
    GROUP_CHOICES = (
        (el1, 'Parlamentarzyści, wyżsi urzędnicy i kierownicy'),
        (el2, 'Specjaliści'),
        (el3, 'Technicy i inni średni personel'),
        (el4, 'Pracownicy biurowi'),
        (el5, 'Pracownicy usług osobistych i sprzedawcy'),
        (el6, 'Robotnik przemysłowy'),
        (el7, 'Operator i monter maszyn'),
        (el8, 'Siły zbrojne'),
        (el9, 'Inne'),
    )
    occupational_group = models.CharField(max_length = 50,
                                      blank = False,
                                      choices = GROUP_CHOICES,
                                      default=el2)#wymagalne
    awerage_six_monthly_income = models.FloatField(blank=False)#wymagalne
    profession = models.CharField(max_length = 50,blank=False)#wymagalne
    nip = models.CharField(max_length= 10,blank=False)#wymagalne
class PensionTable(models.Model):
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    application = models.OneToOneField(CreditApplication,on_delete=models.CASCADE,blank = False,null=True) #wymagalne, moze być puste
    date_start = models.DateField(blank=False)# musi być podane
    date_end = models.DateField(blank = True, null = True) 
    pension_amount = models.FloatField(blank=False)#wymagalne
    card_number = models.CharField(max_length= 50,blank=False)#wymagalne
class BankOffer(models.Model):# z tej tabelki bedzie pobierany id do którego wpadł klient
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    name = models.CharField(max_length= 50,blank=False)#wymagalne / nazwa oferty
    description = models.CharField(max_length= 100,blank=False)#wymagalne / opis dla kogo jest oferta
    amount = models.IntegerField(blank=False) #kwota 
    period = models.IntegerField(blank = False) # wymagalne okres
class ApplicationCompleted(models.Model): #Wnioski ukończone - na odrzuceniu, na rezygnacji,
    id = models.AutoField(primary_key = True) # automatycznie się dodaje
    application = models.OneToOneField(CreditApplication,on_delete=models.CASCADE,blank = False,null=True) #wymagalne, moze być puste
    info = models.CharField(max_length= 100,blank=True)#niewymagalne / komunikat na wniosku 



#class Post(models.Model):
  #  autor = models.ForeignKey('auth.User')
  #  tytul = models.CharField(max_length=200)
  #  tresc = models.TextField()
  #  data_utworzenia = models.DateTimeField(default=timezone.now)
  #  data_publikacji = models.DateTimeField(blank=True, null=True)

#    def publikuj(self):
 #       self.data_publikacji = timezone.now()
  #      self.save()

  #  def __str__(self):
  #      return self.tytul
#class Cost(models.Model):
 #   cost = models.FloatField(blank = False)
 #   date = models.DateField(blank = False)
    #            tutaj modele do aplikacji

