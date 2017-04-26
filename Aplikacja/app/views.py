from django.shortcuts import render
import re
from random import randint
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.conf import settings
from django.core import mail
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import Http404
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.db.models import Q #do wyciagania or w zapytaniu

from app.models import PersonalData
from app.models import IncomeName
from app.models import ContractTable
from app.models import PensionTable
from app.models import CreditApplication
from app.models import PortalUser
from app.models import AccessStatus
from app.models import BankOffer
from app.models import ProposedOffer
from app.models import ConfirmedOffer
from app.models import RequiredDocument
from app.models import TechnicalDocument
from app.models import SentDocument
from app.models import ApplicationCompleted


from app.forms import PersonalDataForm
from app.forms import IncomeNameForm
from app.forms import ProposedOfferForm
from app.forms import ConfirmedOfferForm
from app.forms import RequiredDocumentForm
from app.forms import SentDocumentForm
from app.forms import RejectionForm
from app.forms import LastDecisionForm



def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/start.html',#index
        {
            'title':'Strona domowa',
            'year':datetime.now().year,
        }
    )
def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Kontakt',
            'message':'Kontakt z autorem.',
            'imie_nazwisko_autora' :'Arkadiusz Pepliński',
            'miejscowosc_autora' :'Loryniec 7',
            'poczta_autora' :'83-406 Wąglikowice',
            'year':datetime.now().year,
        }
    )
def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'O stronie',
            'message':'Informacje o stronie.',
            'year':datetime.now().year,
            'tekst':'Aplikacja powstała na potrzeby pracy magisterskiej.',
            'tekst_dodatkowy':'Jakiś dodatkowy tekst na stronie.',
        }
    )
def startView(request):return render(request,'app/start.html') 
def personalDataView(request):
    #tutaj kod od tego by wnioski mógł składać tylko uzytkownik z rolą
    #widok uzupełniany przez Doradcę
    uzytkownicy_portalu = PortalUser.objects.filter().order_by('id')
    uzytkownikaktualny =  request.user.id #działa None/numerek id
    try:
        rolauzytkownika = PortalUser.objects.get(id_user__id=uzytkownikaktualny)#try catch działa tylko dla Krzyska/Mariolki, #id_user__id tak się dobieramy do elementów z foreign keya
        dostepy = AccessStatus.objects.filter(access_to_role=rolauzytkownika.role).order_by('status_id')# kazdy uzytkownik ma dostep do roli
    except PortalUser.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Uzytkownik nie ma przypisane żadnej roli!. W celu nadania dostepów skontaktuj się z właścicielem witryny.',}
                  )
    if (rolauzytkownika.role == "Pracownik banku"):
        return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Tylko doradca może składać wnioski.',
                  })
    #koniec kodu odpowiedzialnego za to że wnioski składa tylko użytkownik z rolą
    if request.method =='POST':
        form = PersonalDataForm(request.POST)
        if form.is_valid():
            pesel = request.POST.get('pesel','')
            name = request.POST.get('name','')
            surname = request.POST.get('surname','')
            identity_card = request.POST.get('identity_card','')
            telephon_number = request.POST.get('telephon_number','')
            mail = request.POST.get('mail','')#dodano walidację w html, która nie pozwoli na przesłanie w złym formacie, przyjmuje tylko polskie
            monthly_expenses = request.POST.get('monthly_expenses','')
            city = request.POST.get('city','')
            postal_code = request.POST.get('postal_code','')
            street = request.POST.get('street','')
            house_number = request.POST.get('house_number','')
            flat_number = request.POST.get('flat_number','')
            education = request.POST.get('education','')
            marital_status = request.POST.get('marital_status','')

            zrodlo_dochodu = request.POST.get('zrodlo_dochodu','')#zrodlo dochodu uzpelniane by  przeslac dane do bazy danych
            #ponizsze pola do umowy
            date_start_of_employment = request.POST.get('date_start_of_employment_input','')
            end_of_employment = request.POST.get('end_of_employment_input','')
            occupational_group = request.POST.get('occupational_group_select','')
            awerage_six_monthly_income = request.POST.get('awerage_six_monthly_income_input','')
            profession = request.POST.get('profession_input','')
            nip = request.POST.get('nip_input','')
            #ponizsze pola do emerytury
            date_start = request.POST.get('date_start_input','')
            date_end = request.POST.get('date_end_input','')
            pension_amount = request.POST.get('pension_amount_input','')
            card_number =request.POST.get('card_number_input','')

            personal_data_obj = PersonalData(pesel=pesel,name = name,surname=surname,identity_card=identity_card,telephon_number=telephon_number,mail=mail,monthly_expenses=monthly_expenses,city=city,postal_code=postal_code,street=street,house_number=house_number,flat_number=flat_number,education=education,marital_status=marital_status)# utworzenie nowego obiektu
            #poniżej kod odpowiedzialny za nie zapisanie tego samego peselu do bazy.
            try:
                personal_data_obj.save()
            except IntegrityError as e:
                return render(request,
                  'app/personalData.html',
                         {
                           'form':form,
                           'title':'Blad zapisu',
                           'message':e.args[0]+' \nNa podany pesel składano już wniosek kredytowy. Podaj dane nowego klienta.', 
                         }
            )#
            #poniżej tworzenie wniosku gdy baza pozwoliła na zapis wniosku,zmieniono status_id na 2
            new_application = CreditApplication(personal_data = personal_data_obj, status_id = 2,icome_id = int(zrodlo_dochodu))#added_documents = 2,proposed_offer_id=4
            new_application.save()
            #wybór źródła dochodu.- wysłanie maila
            if zrodlo_dochodu=='2' or zrodlo_dochodu=='3' or zrodlo_dochodu=='4':
               tytulmaila = 'Dodano Um 2/3/4 '+str(new_application.id)
               tresc = 'O decyzji kredytowej poinformujemy mailowo. \nTwój numer wniosku to: '+str(new_application.id)+'\nNatomiast zrodlo dochodu to:'+str(zrodlo_dochodu)+'\nPrzeslane dane to:'+'\ndate_start_of_employment = '+str(date_start_of_employment)+'\nend_of_employment = '+str(end_of_employment)+'\noccupational_group ='+str(occupational_group)+'\nawerage_six_monthly_income ='+str(awerage_six_monthly_income)+ '\nprofession = '+str(profession)+'\nnip = '+ str(nip)+' !'
               #send_mail(tytulmaila,tresc, 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl'])#tytul,tresc,do kogo, tablica innych?
            if zrodlo_dochodu=='1':
               tytulmaila = 'Dodano Umowa '+str(new_application.id)
               tresc = 'O decyzji kredytowej poinformujemy mailowo. \nTwój numer wniosku to: '+str(new_application.id)+'\nnatomiast zrodlo dochodu to:'+str(zrodlo_dochodu)+'\nprzeslane dane to:'+'\ndate_start_of_employment = '+str(date_start_of_employment)+'\noccupational_group ='+str(occupational_group)+'\nawerage_six_monthly_income ='+str(awerage_six_monthly_income)+ '\nprofession = '+str(profession)+'\nnip = '+ str(nip)+' !'
               #send_mail(tytulmaila, tresc, 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl'])
            if zrodlo_dochodu=='5' or zrodlo_dochodu=='6':
               tytulmaila = 'Dodano EM RENTA bezterminowa '+str(new_application.id)
               tresc = 'O decyzji kredytowej poinformujemy mailowo. \nTwój numer wniosku to: '+str(new_application.id)+'\nnatomiast zrodlo dochodu to:'+str(zrodlo_dochodu)+'\nprzeslane dane to:'+'\nPola emeryta lub renty bezterminowej'
               #send_mail(tytulmaila,tresc, 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl'])
            if zrodlo_dochodu=='7':
               tytulmaila = 'Dodano RENTA terminowa '+str(new_application.id)
               tresc = 'O decyzji kredytowej poinformujemy mailowo. \nTwój numer wniosku to: '+str(new_application.id)+'\nnatomiast zrodlo dochodu to:'+str(zrodlo_dochodu)+'\nprzeslane dane to:'+'Pola renty terminowej'
               #send_mail('Dodano RENTA terminowa '+str(new_application.id),tresc, 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl'])
               #zapis do contractTable
            if zrodlo_dochodu=='2' or zrodlo_dochodu=='3' or zrodlo_dochodu=='4':
               contract_table = ContractTable(application = new_application,date_start_of_employment=date_start_of_employment,end_of_employment=end_of_employment,occupational_group=occupational_group,awerage_six_monthly_income=awerage_six_monthly_income,profession=profession,nip=nip)
               contract_table.save()
            if zrodlo_dochodu=='1':
               contract_table = ContractTable(application = new_application,date_start_of_employment=date_start_of_employment,occupational_group=occupational_group,awerage_six_monthly_income=awerage_six_monthly_income,profession=profession,nip=nip)
               contract_table.save()
               #zapis do pensionTable
            if zrodlo_dochodu=='5' or zrodlo_dochodu=='6':
               pension_table = PensionTable(application = new_application,date_start=date_start,pension_amount=pension_amount,card_number=card_number)
               pension_table.save()
            if zrodlo_dochodu=='7':
               pension_table = PensionTable(application = new_application,date_start=date_start,date_end=date_end,pension_amount=pension_amount,card_number=card_number)
               pension_table.save()
            try:
                send_mail(tytulmaila,tresc, 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl'])#tytul,tresc,do kogo, tablica innych?
            except:#powodzenie nawet, gdy nie wyjdzie mail
                return render(request,
                  'app/start.html',
                         {
                           'message':'Złożono poprawnie wniosek o numerze: '+str(new_application.id), 
                         }
            )
            #tutaj powodzenie gdy wyszedł mail
            return render(request,
                  'app/start.html',
                         {
                           'message':'Złożono poprawnie wniosek o numerze: '+str(new_application.id), 
                         }
            )
        else:
            try:
                send_mail('Nie dodano', 'musisz wiecej zarabiac, wtedy moze dostaniesz kredyt', 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl']) 
            except:
                   return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Wprowadzono nieprawidłowy mail.',}
                  )
            #return HttpResponseRedirect(reverse('contact3'))#przenosi do innego widoku  - contact, jesli walidacje nie bedzie spelniona - gdy nastąpi nieoczekiwany bład walidacji
    else:
         form = PersonalDataForm()
    return render(request,
                  'app/personalData.html',
                         {
                           'form':form,
                         }
                   )
def indexOfertaView(request):
    try:
        all_creditapplications = CreditApplication.objects.all()#wszystkie wnioski
    except CreditApplication.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {'message':'W bazie nie ma żadnych wniosków.'})
    #dopisane 3 kwietnia - w celu wyszukiwania tych wniosków do których dostęp ma pracownik
    uzytkownikaktualny =  request.user.id #id aktualnie zalogowanego uzytkownika
    try:
        uzytkownikzbazy = PortalUser.objects.get(id_user_id__exact=uzytkownikaktualny)#rekord aktualnego użytkownika
    except PortalUser.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {'message':'Użytkownik nie ma przypisanej roli.'})
    zawoduzytkownikazbazy = uzytkownikzbazy.role#zawod aktualnego uzytkownika z bazy: Doradca lub Pracownik Banku
    if zawoduzytkownikazbazy=='Pracownik banku':
       #zmienne niepotrzebne dla pracownika banku
       creditapplications_wait_for_confirmed_offert = None
       creditapplications_wait_for_add_documents = None
       creditapplications_complete_app = None
       creditapplications_in_rejection = None
       #koniec zmiennych niepotrzebnych dla pracownika banku
       try:#tutaj w zasadzie będzie tylko 2,3 - pozostałe są na innych etapach.- to przerobić tylko na 2
           creditapplications_for_person =  CreditApplication.objects.filter(Q(status='2')|Q(status='4')|Q(status='6')|Q(status='8')).order_by('id')#wszystkie wnioski dla pracownika banku
       except CreditApplication.DoesNotExist:
              return render(request,
                  'app/komunikat.html',
                  {'message':'Pracownik banku nie ma wniosków, na których może pracować'})
       etykieta_na_strone = 'Wnioski po stronie Pracownika banku. 2/4/6/8'
       doklej_url = 'wyslijoferte'
       doklej_etykiete = 'Zaproponuj ofertę do wniosku'
       #tutaj zmiany dotyczące tego, by podzielić wnioski na statusy doradcy
       try:
           creditapplications_wait_for_offert =  CreditApplication.objects.filter(Q(status='2')).order_by('id')#wszystkie wnioski dla pracownika banku oczekujace na ofertę
       except CreditApplication.DoesNotExist:
           creditapplications_wait_for_offert = None   
       try:    
           creditapplications_wait_for_documents =  CreditApplication.objects.filter(Q(status='4')).order_by('id')#wszystkie wnioski dla pracownika banku oczekujące na dokumenty
       except CreditApplication.DoesNotExist:
           creditapplications_wait_for_documents = None
       try:    
           creditapplications_wait_for_decision =  CreditApplication.objects.filter(Q(status='6')).order_by('id')#wszystkie wnioski dla pracownika banku oczekujace na ostateczną decyzję
       except CreditApplication.DoesNotExist:
           creditapplications_wait_for_decision = None 
       try:    
           creditapplications_in_resignation =  CreditApplication.objects.filter(Q(status='8')).order_by('id')#wszystkie wnioski dla pracownika banku na rezygnacji klienta - może odczytać powód
       except CreditApplication.DoesNotExist:
           creditapplications_wait_for_decision = None        
    if zawoduzytkownikazbazy=='Doradca':#to przerobić tylko na 3
       #zmienna niepotrzebne dla doradcy
       creditapplications_wait_for_offert = None;
       creditapplications_wait_for_documents = None
       creditapplications_wait_for_decision = None
       creditapplications_in_resignation = None
       #koniec zmiennych niepotrzebych doradcy
       try:#tutaj w zasadzie będzie tylko 1,3,5,7,9 zrobić podział
           creditapplications_for_person =  CreditApplication.objects.filter(Q(status='1')|Q(status='3')|Q(status='5')|Q(status='7')|Q(status='9')).order_by('id')#wszystkie wnioski dla pracownika banku
       except PortalUser.DoesNotExist:
              return render(request,
                  'app/komunikat.html',
                  {'message':'Doradca nie ma wniosków na których może pracować.'})
       etykieta_na_strone = 'Wnioski po stronie Doradcy. 1/3/5/7/9'
       doklej_url = 'zatwierdzoferte'
       doklej_etykiete = 'Zatwierdź ofertę do wniosku'
              #tutaj zmiany dotyczące tego, by podzielić wnioski na statusy doradcy
       try:
           creditapplications_wait_for_confirmed_offert =  CreditApplication.objects.filter(Q(status='3')).order_by('id')#wszystkie wnioski dla Doradcy oczekujace na zatwierdzenie oferty
       except CreditApplication.DoesNotExist:
           creditapplications_wait_for_confirmed_offert = None 
       try:
           creditapplications_wait_for_add_documents =  CreditApplication.objects.filter(Q(status='5')).order_by('id')#wszystkie wnioski dla Doradcy oczekujace na dodanie dokumentów
       except CreditApplication.DoesNotExist:
           creditapplications_wait_for_add_documents = None
       try:
           creditapplications_complete_app =  CreditApplication.objects.filter(Q(status='7')).order_by('id')#wszystkie wnioski dla Doradcy pozytywnie zakonczone
       except CreditApplication.DoesNotExist:
           creditapplications_complete_app = None
       try:
           creditapplications_in_rejection =  CreditApplication.objects.filter(Q(status='9')).order_by('id')#wszystkie wnioski dla Doradcy odrzucone
       except CreditApplication.DoesNotExist:
           creditapplications_in_rejection = None    
    return render(request,
                  'app/indexOferta.html', 
                  {
                      'all_creditapplications':all_creditapplications,
                      'creditapplications_for_person':creditapplications_for_person,
                      'etykieta_na_strone':etykieta_na_strone,
                      'doklej_url':doklej_url,
                      'doklej_etykiete':doklej_etykiete,
                      'creditapplications_wait_for_offert':creditapplications_wait_for_offert,#dopisane
                      'zawoduzytkownikazbazy':zawoduzytkownikazbazy,#dopisane
                      'creditapplications_wait_for_documents':creditapplications_wait_for_documents,#dopisane
                      'creditapplications_wait_for_decision':creditapplications_wait_for_decision,#dopisane
                      'creditapplications_in_resignation':creditapplications_in_resignation,#dopisane
                      'creditapplications_wait_for_confirmed_offert':creditapplications_wait_for_confirmed_offert,#dopisane8
                      'creditapplications_wait_for_add_documents':creditapplications_wait_for_add_documents,#dopisane8
                      'creditapplications_complete_app':creditapplications_complete_app,#dopisane8
                      'creditapplications_in_rejection':creditapplications_in_rejection,
                      }) 
def creditapplicationView(request, credit_id):
    #creditapplication
    uzytkownikaktualny =  request.user.id#sprawdzić czy taki użytkownik ma taką samą rolę
    try:
        creditapplication = CreditApplication.objects.get(pk=credit_id)#tutaj zwraca konkretny wniosek wyszykująć po id
    except CreditApplication.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {'message':'Podany wniosek nie istnieje'})
    statuswniosku = creditapplication.status_id#kazdy wniosek ma status.zwraca liczbe,tak się szuka w rekordzie z bazy
    osobanawniosku = creditapplication.personal_data_id#kazdy wniosek ma osobę.zwraca liczbe z bazy
    try:
        personaldata = PersonalData.objects.get(pk=osobanawniosku)#tutaj zwraca konkretna osoba przydzielona do wniosku
    except PersonalData.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {'message':'Do wniosku nie jest przydzielona żadna osoba.'})
    dochodzwniosku = creditapplication.icome_id#dochód z wniosku.zwraca liczbe z bazy
    try:
        rekorddostep = AccessStatus.objects.get(pk=int(statuswniosku))# konkretny rekord z tabelki access status
    except AccessStatus.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {'message':'Brak podanego statusu.'})
    dostepdowniosku = rekorddostep.access_to_role #nazwa rroli ktora ma dostep do tego wniosku
    try:
        uzytkownikzbazy = PortalUser.objects.get(id_user_id__exact=uzytkownikaktualny)#rekord aktualnego użytkownika
    except PortalUser.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {'message':'Użytkownik nie jest w tabelce Portal user.'})    
    zawoduzytkownikazbazy = uzytkownikzbazy.role#zawod aktualnego uzytkownika z bazy
    if zawoduzytkownikazbazy==dostepdowniosku:
         wynik='Tak'#sprawdzenie czy elementy tutaj utworzone są równe - działa ok
    else:
         wynik='Nie'
    if dochodzwniosku == 1 or dochodzwniosku == 2 or dochodzwniosku == 3 or dochodzwniosku == 4:
       try:
           Dochod = ContractTable.objects.get(application_id__exact=credit_id)#jesli contract table  
       except ContractTable.DoesNotExist:
           return render(request,
                  'app/komunikat.html',
                  {'message':'Brak dochodu w tabelce.'})   
       idDochodu = Dochod.id
       kontrakt = "true"
    else:
       try:
           Dochod = PensionTable.objects.get(application_id__exact=credit_id)#jesli pensiontable
       except PensionTable.DoesNotExist:
           return render(request,
                  'app/komunikat.html',
                  {'message':'Brak dochodu w tabelce.'})   
       idDochodu = Dochod.id
       kontrakt = None
    try:
        proposedoffer = ProposedOffer.objects.get(pk=creditapplication.proposed_offer_id)#oferta przydzielona dla danego człowieczka
    except:
        proposedoffer = None
    try:
        confirmedoffer = ConfirmedOffer.objects.get(pk=creditapplication.confirmed_offer_id)#oferta zatwierdzona
    except:
        confirmedoffer = None
    try:
        requiredDocuments = RequiredDocument.objects.get(pk=creditapplication.required_document_id)#wymagane dokumenty
    except:
        requiredDocuments = None
    try:
        addedDocuments = SentDocument.objects.get(pk=creditapplication.added_documents_id)#dostarczone dokumenty
    except:
        addedDocuments = None
    if statuswniosku==8 or statuswniosku==9:
        zakonczony = "TAK"
    else:
        zakonczony = None
    if statuswniosku==7:
        zakonczony_c = "TAK"
    else:
        zakonczony_c = None
    return render(request,
                  'app/szczegoly.html',
                  {
                      'creditapplication':creditapplication,
                      'statuswniosku':statuswniosku,
                      'osobanawniosku':osobanawniosku, 
                      'dochodzwniosku':dochodzwniosku,
                      'idDochodu':idDochodu,
                      'dostepdowniosku':dostepdowniosku,
                      'uzytkownikzbazy':uzytkownikzbazy,
                      'zawoduzytkownikazbazy':zawoduzytkownikazbazy,
                      'wynik':wynik,
                      'personaldata':personaldata,
                      'Dochod':Dochod,
                      'kontrakt':kontrakt,
                      'proposedoffer':proposedoffer,
                      'confirmedoffer':confirmedoffer,
                      'requiredDocuments':requiredDocuments,
                      'addedDocuments':addedDocuments,
                      'zakonczony_c':zakonczony_c,
                      'zakonczony':zakonczony,
                      'rekorddostep':rekorddostep,
                  })
def proposedofferView(request,creditapplication_id):
    #widok uzupełniany przez Pracownika banku
    try:
        creditapplication = CreditApplication.objects.get(pk=creditapplication_id)#tutaj zwraca konkretny cost wyszykująć po id
    except CreditApplication.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Wniosek nie istnieje.',
                      })
    #dopisane
    if(creditapplication.status_id!=2):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosek na innym etapie.',
                  })
    #dopisanie  oferty przydzielonej przez Bank
    try:
        #IloscOfert = BankOffer.objects.all().count()
        #numeroferty = randint(1,int(IloscOfert))
        OfertaBankuDlaWniosku = BankOffer.objects.get(id=3)#przypisana na sztywno
    except BankOffer.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Brak oferty w Banku',}
                  )
    #
    if request.method =='POST':
       form = ProposedOfferForm(request.POST)
       if form.is_valid():
          initial_amount = request.POST.get('initial_amount','')
          maximal_amount = request.POST.get('maximal_amount','')
          minimum_load_period = request.POST.get('minimum_load_period','')
          maximum_load_period = request.POST.get('maximum_load_period','')
          proposed_offer_obj = ProposedOffer(initial_amount=initial_amount,maximal_amount=maximal_amount,minimum_load_period=minimum_load_period,maximum_load_period=maximum_load_period)
          try:
              proposed_offer_obj.save()
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z zapisem oferty dla klienta.',}
                  )
          #dopisanie kolumny oraz zmiana statusu
          creditapplication.proposed_offer=proposed_offer_obj
          creditapplication.status_id=3
          creditapplication.save(update_fields=['proposed_offer','status'])#tak się zmienia odpowiednie dane na wniosku
          return render(request,
                  'app/start.html',
                         {
                           'message':'Wystawiono ofertę na wniosku '+str(creditapplication_id), 
                         }
                  )
       else:
          try:
              send_mail('Nie uzupelniono tabelki ProposedOffer', 'Forma zle zwalidowana', 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl']) 
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z wysłaniem maila.',}
                  )
    else:
         form = ProposedOfferForm()
    return render(request,
                  'app/proposedOffer.html',
                         {
                           'form':form,
                           'creditapplication':creditapplication,
                           'OfertaBankuDlaWniosku':OfertaBankuDlaWniosku,#dopisane
                           #'IloscOfert':IloscOfert,
                         }
                   )
def confirmedofferView(request,creditapplication_id):
    try:
        creditapplication = CreditApplication.objects.get(pk=creditapplication_id)#tutaj zwraca konkretny wniosek wyszykująć po id
    except CreditApplication.DoesNotExist:
        return render(request,
                  'app/komunikat.html',{'message':'Nie ma takiego wniosku.'})#jeśli wniosek nie istnieje to odpowiedni komunikat się pojawia
        #dopisane
    if(creditapplication.status_id!=3):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosek jest na innym etapie.',
                  })
    
    #dopisanie  oferty przydzielonej przez pracownika banku dla naszego klienta
    try:
        proposedoffer = ProposedOffer.objects.get(pk=creditapplication.proposed_offer_id)
    except ProposedOffer.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Brak oferty wystawionej przez pracownika banku dla klienta',}
                  )
    if request.method =='POST':
       form = ConfirmedOfferForm(request.POST)
       if form.is_valid():
          confirmed_amount = request.POST.get('confirmed_amount','')
          period_approved = request.POST.get('period_approved','')#wyliczyć ratę i koszt kredytu
          #wyliczone kwota raty oraz całkowity koszt kredytu - zakladam ze na start aplikacji bierzemy 10 %
          installment_amount = int(int(confirmed_amount)/int(period_approved))
          totall_credit_amount = int(installment_amount*1.1)*int(period_approved)
          #koniec wyliczeń
          confirmed_offer_obj = ConfirmedOffer(confirmed_amount=confirmed_amount,period_approved=period_approved,installment_amount=installment_amount,totall_credit_amount=totall_credit_amount)
          try:
              confirmed_offer_obj.save()
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z zapisem oferty zatwierdzonej przez klienta.',}
                  )
          #modyfikacja wniosku - dopisanie kolumnu oraz zmiana statusu
          creditapplication.confirmed_offer=confirmed_offer_obj
          creditapplication.status_id=4
          creditapplication.save(update_fields=['confirmed_offer','status'])#tak się zmienia odpowiednie dane na wniosku
          return render(request,
                  'app/start.html',
                         {
                           'message':'Zatwierdzono ofertę dla  wniosku '+str(creditapplication_id), 
                         }
                  )
       else:
          #try:
           #   send_mail('Nie uzupelniono tabelki ConformedOffer', 'Forma zle zwalidowana', 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl']) 
          #except:
           return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Przesłano niewłaściwe wartości.',}
                  )
    else:
         form = ConfirmedOfferForm()
    return render(request,
                  'app/confirmedOffer.html',
                         {
                           'form':form,
                           'creditapplication':creditapplication,
                           'proposedoffer':proposedoffer,
                         }
                   ) 
def requireddocumentsView(request,creditapplication_id):
    #widok uzupełniany przez Pracownika banku
    try:
        creditapplication = CreditApplication.objects.get(pk=creditapplication_id)#tutaj zwraca konkretny wniosek wyszykująć po id
    except CreditApplication.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Wniosek nie istnieje.',
                      })
    #dopisanie  dokumentów - wyswietlenie listy dokumentów
        #dopisane
    if(creditapplication.status_id!=4):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosek na innym etapie.',
                  })
    try:#technical documents
        technicalDocuments = TechnicalDocument.objects.all()
    except TechnicalDocument.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Brak listy dokumentów do wyboru  w  Banku',}
                  )
    #
    if request.method =='POST':
       form = RequiredDocumentForm(request.POST)
       if form.is_valid():
          documents_number = request.POST.get('documents_number','')
          required_documents_obj = RequiredDocument(documents_number = documents_number)
          try:
              required_documents_obj.save()
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z zapisem wymaganych dokumentów dla klienta.',}
                  )
          #dopisanie kolumny oraz zmiana statusu
          creditapplication.required_document=required_documents_obj
          creditapplication.status_id=5
          creditapplication.save(update_fields=['required_document','status'])#tak się zmienia odpowiednie dane na wniosku
          return render(request,
                  'app/start.html',
                         {
                           'message':'Wyznaczono liste wymaganych dokumentów dla wniosku '+str(creditapplication_id), 
                         }
                  )
       else:
          try:
              send_mail('Nie uzupelniono tabelki Wymaganych dokumentów', 'Forma zle zwalidowana', 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl']) 
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z wysłaniem maila.',}
                  )
    else:
         form = RequiredDocumentForm()
    return render(request,
                  'app/requiredDocuments.html',
                         {
                           'form':form,
                           'creditapplication':creditapplication,
                           'technicalDocuments':technicalDocuments,
                         }
                   )
def sentdocumentView(request,creditapplication_id):
    #widok dla doradcy- służy do dodania dokumentu
    try:
        creditapplication = CreditApplication.objects.get(pk=creditapplication_id)#tutaj zwraca konkretny wniosek wyszykująć po id
    except CreditApplication.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Wniosek nie istnieje.',
                      })
    if(creditapplication.status_id!=5):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosek na innym etapie.',
                  })
    #potrzeba jeszcze zmiennej do listy wymaganych dokumentów
    try:
        requiredDocuments = RequiredDocument.objects.get(pk=creditapplication.required_document_id)#tutaj zwraca konkretny wniosek wyszykująć po id
    except RequiredDocument.DoesNotExist:
        return render(request,
                  'app/komunikat.html', {
                      'message':'Brak wymaganych dokumentów. Wniosek jest na innym etapie.',}
                  )
    #tutaj trzeba wydobyć cyfry z napisu jest ok
    napis = requiredDocuments.documents_number
    numery = list(map(int,re.findall('\d+', napis)))
    #teraz trzeba nazwy dokumentów wydobyć
    dokumenty = TechnicalDocument.objects.filter(id__in=numery)
    if request.method =='POST':
       form = SentDocumentForm(request.POST, request.FILES)#w templetse forma przesyła nie tylko post,ale i files
       if form.is_valid():
          #dodanie numeru rachunku 
          iban = request.POST.get('iban','')
          #po dodaniu iban
          sent_documents_obj = SentDocument(file = request.FILES['file'],name = request.POST['name'])
          try:
              sent_documents_obj.save()
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z zapisem dostarczonych dokumentów.',
                  }
                  )
          #dopisanie  by znaleść osobę do numeru rachunku
          try:
              osoba = PersonalData.objects.get(pk=creditapplication.personal_data_id)
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Nie można znaleść właściciela wniosku.',
                  }
                  )
          osoba.iban_number = iban
          osoba.save(update_fields=['iban_number'])
          #dopisanie kolumny oraz zmiana statusu
          creditapplication.added_documents=sent_documents_obj
          creditapplication.status_id=6
          creditapplication.save(update_fields=['added_documents','status'])#tak się zmienia odpowiednie dane na wniosku
          return render(request,
                  'app/start.html',
                         {
                           'message':'Dostarczono dokumenty dla wniosku '+str(creditapplication_id), 
                         }
                  )
       else:
          try:
              send_mail('Nie uzupelniono tabelki Dostarczonych dokumentów', 'Forma zle zwalidowana ', 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl']) 
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z wysłaniem maila.',}
                  )
    else:
         form = SentDocumentForm()
    return render(request,
                  'app/sentDocument.html',
                         {
                           'form':form,
                           'creditapplication':creditapplication,
                           'requiredDocuments':requiredDocuments,
                           'numery':numery,
                           'dokumenty':dokumenty,
                           #'napiszTabelki':napiszTabelki,
                           #'liczby':liczby,
                           #'dlugosc':dlugosc,
                         }
                   )
def lastDecisionView(request,creditapplication_id):
    #widok dla pracownika banku - nadanie ostatecznej decyzji
    try:
        creditapplication = CreditApplication.objects.get(pk=creditapplication_id)#tutaj zwraca konkretny wniosek wyszykująć po id
    except CreditApplication.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Wniosek nie istnieje.',
                      })
    if(creditapplication.status_id!=6):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosek na innym etapie.',
                  })
    try:
        requiredDocuments = RequiredDocument.objects.get(pk=creditapplication.required_document_id)#tutaj lista konkretnych dokumentów - żądanych przez pracownika banku
    except RequiredDocument.DoesNotExist:
        return render(request,
                  'app/komunikat.html', {
                      'message':'Brak wymaganych dokumentów. Wniosek jest na innym etapie.',}
                  )
    try:
        addedDocuments = SentDocument.objects.get(pk=creditapplication.added_documents_id)#tutaj rekord dokumentów dodanych
    except SentDocument.DoesNotExist:
        return render(request,
                  'app/komunikat.html', {
                      'message':'Brak przesłanych dokumentów.',}
                  )
        #być może jakaś forma
    #tutaj trzeba wydobyć cyfry z napisu jest ok
    napis = requiredDocuments.documents_number
    numery = list(map(int,re.findall('\d+', napis)))
    #teraz trzeba nazwy dokumentów wydobyć
    dokumenty = TechnicalDocument.objects.filter(id__in=numery)
    if request.method =='POST':
       form = LastDecisionForm(request.POST)
       if form.is_valid():
          decision = request.POST.get('decision','')
          comment = request.POST.get('comment','')
          if decision == "1":#odrzut
              creditapplication.status_id = 9
              creditapplication.comment = comment
              creditapplication.save(update_fields=['status','comment'])#tak się zmienia odpowiednie dane na wniosku
              return render(request,
                  'app/start.html',
                         {
                           'message':'Odrzucono wniosek: '+str(creditapplication_id), 
                         }
                  )
          if decision == "2":#pozytyw
              creditapplication.status_id = 7
              creditapplication.comment = comment
              creditapplication.save(update_fields=['status','comment'])#tak się zmienia odpowiednie dane na wniosku
              application_complete_obj = ApplicationCompleted(application = creditapplication, info = comment)
              try:
                  application_complete_obj.save()
              except:
                  return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z zapisem zakończonego wniosku.',}
                  )
              return render(request,
                  'app/start.html',
                         {
                           'message':'Wypłacono gotówkę na wniosku : '+str(creditapplication_id), 
                         }
                  )
       else:
          try:
              send_mail('Nie nadano ostatecznej decyzji', 'Forma zle zwalidowana', 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl']) 
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z wysłaniem maila.',}
                  )
    else:
         form = LastDecisionForm()
    return render(request,
                  'app/lastDecision.html',
                         {
                           'form':form,
                           'creditapplication':creditapplication,
                           'requiredDocuments':requiredDocuments,
                           'addedDocuments':addedDocuments,
                           'dokumenty':dokumenty,
                         }
                   )
def rejectionView(request,creditapplication_id):
    #widok dla doradcę - nadanie odrzutu
    try:
        creditapplication = CreditApplication.objects.get(pk=creditapplication_id)#tutaj zwraca konkretny wniosek wyszykująć po id
    except CreditApplication.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Wniosek nie istnieje.',
                      })
    if(creditapplication.status_id==9):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosek jest już na odrzuceniu.',
                  })
    if(creditapplication.status_id==7):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosków pozytywnie zakończonych nie można odrzucać.',
                  })
    if(creditapplication.status_id==3 or creditapplication.status_id==5 or creditapplication.status_id==8):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosek na innym etapie.',
                  })
    uzytkownikaktualny =  request.user.id #id aktualnie zalogowanego uzytkownika
    try:
        uzytkownikzbazy = PortalUser.objects.get(id_user_id__exact=uzytkownikaktualny)#rekord aktualnego użytkownika
    except PortalUser.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {'message':'Użytkownik nie ma przypisanej roli.'})
    zawoduzytkownikazbazy = uzytkownikzbazy.role#zawod aktualnego uzytkownika z bazy: Doradca lub Pracownik Banku
    if zawoduzytkownikazbazy=='Doradca':
        return render(request,
                  'app/komunikat.html',
                  {'message':'Ten uzytkownik nie może odrzucać wniosków.'})
    if request.method =='POST':
       form = RejectionForm(request.POST)
       if form.is_valid():
          comment = request.POST.get('comment','')
          creditapplication.comment=comment
          creditapplication.status_id=9
          creditapplication.save(update_fields=['comment','status'])
          return render(request,
                  'app/start.html',
                         {
                           'message':'Odrzucono wniosek: '+str(creditapplication_id), 
                         }
                  )
       else:
          try:
              send_mail('Odrzucono wniosek', 'Forma zle zwalidowana ', 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl']) 
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z wysłaniem maila.',}
                  )
    else:
         form = RejectionForm()
    return render(request,
                  'app/rejection.html',
                         {
                           'form':form,
                           'creditapplication':creditapplication,
                         }
                   )
def resignationView(request,creditapplication_id):
    #widok dla pracownika banku - nadanie odrzutu
    try:
        creditapplication = CreditApplication.objects.get(pk=creditapplication_id)#tutaj zwraca konkretny wniosek wyszykująć po id
    except CreditApplication.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Wniosek nie istnieje.',
                      })
    if(creditapplication.status_id==8):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosek jest już na rezygnacji.',
                  })
    if(creditapplication.status_id==7):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Na wnioskach pozytywnie zakończonych nie można rezygnować..',
                  })
    if(creditapplication.status_id==2 or creditapplication.status_id==4 or creditapplication.status_id==6 or creditapplication.status_id==9):
           return render(request,
                  'app/komunikat.html',   
                  {
                      'message':'Wniosek na innym etapie.',
                  })
    uzytkownikaktualny =  request.user.id #id aktualnie zalogowanego uzytkownika
    try:
        uzytkownikzbazy = PortalUser.objects.get(id_user_id__exact=uzytkownikaktualny)#rekord aktualnego użytkownika
    except PortalUser.DoesNotExist:
        return render(request,
                  'app/komunikat.html',
                  {'message':'Użytkownik nie ma przypisanej roli.'})
    zawoduzytkownikazbazy = uzytkownikzbazy.role#zawod aktualnego uzytkownika z bazy: Doradca lub Pracownik Banku
    if zawoduzytkownikazbazy=='Pracownik banku':
        return render(request,
                  'app/komunikat.html',
                  {'message':'Ten użytkownik nie może nadawać rezygnacji.'})
    if request.method =='POST':
       form = RejectionForm(request.POST)
       if form.is_valid():
          comment = request.POST.get('comment','')
          creditapplication.comment=comment
          creditapplication.status_id=8
          creditapplication.save(update_fields=['comment','status'])
          return render(request,
                  'app/start.html',
                         {
                           'message':'Zrezygnowano na  wniosku: '+str(creditapplication_id), 
                         }
                  )
       else:
          try:
              send_mail('Wniosek na rezygnacji', 'Forma zle zwalidowana ', 'arek.peplinski@wp.pl', ['arek.peplinski@wp.pl']) 
          except:
              return render(request,
                  'app/komunikat.html',
                  {
                      'message':'Problem z wysłaniem maila.',}
                  )
    else:
         form = RejectionForm()
    return render(request,
                  'app/resignation.html',
                         {
                           'form':form,
                           'creditapplication':creditapplication,
                         }
                   )
