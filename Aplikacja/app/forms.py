from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import PersonalData
from app.models import ContractTable
import datetime
#from django.core.validators import RegexValidator
#from app.models import SentDocument

#class SentDocumentForm(forms.ModelForm):
 #   class Meta:
  #      model = SentDocument
   #     fields = ('id_person', 'file', )

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Wpisz login'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Wpisz hasło'}))
class CostForm(forms.Form):
    date = forms.DateField()
    cost = forms.FloatField()
class PersonalDataForm(forms.Form):
    pesel = forms.CharField()
    name = forms.CharField()
    surname = forms.CharField()
    identity_card = forms.CharField()
    telephon_number = forms.CharField()
    mail = forms.EmailField()
    monthly_expenses = forms.FloatField()
    city = forms.CharField()
    postal_code = forms.CharField()
    street = forms.CharField()
    house_number = forms.IntegerField()
    flat_number = forms.CharField()
    education = forms.CharField()
    marital_status = forms.CharField()
    #poniższe pole do wyboru zrodla dochodu przez osobe
    zrodlo_dochodu = forms.CharField()
class IncomeNameForm(forms.Form):
    name = forms.CharField()
    table_name = forms.CharField()
class ProposedOfferForm(forms.Form):
    initial_amount = forms.FloatField()
    maximal_amount = forms.FloatField()
    minimum_load_period = forms.IntegerField()
    maximum_load_period = forms.IntegerField()
class ConfirmedOfferForm(forms.Form):
    confirmed_amount = forms.FloatField()
    period_approved = forms.IntegerField()
class RequiredDocumentForm(forms.Form):
    documents_number = forms.CharField()#tutaj ma wpadać string z numerkami wymaganych dokumentów
class SentDocumentForm(forms.Form):#forma dla doradcy
    file = forms.FileField()
    name = forms.CharField()
    iban = forms.CharField()
class RejectionForm(forms.Form):#forma dla pracownika banku
    comment = forms.CharField()

class LastDecisionForm(forms.Form):
    decision = forms.CharField()
    comment = forms.CharField()