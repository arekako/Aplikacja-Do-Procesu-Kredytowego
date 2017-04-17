from django.contrib import admin
from .models import PortalUser
from .models import AccessStatus
from .models import IncomeName
from .models import TechnicalDocument
from .models import BankOffer

admin.site.register(PortalUser)
admin.site.register(AccessStatus)
admin.site.register(IncomeName)
admin.site.register(TechnicalDocument)
admin.site.register(BankOffer)
