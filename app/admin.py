from django.contrib import admin
from .models import State, Division, District, Nrc, Referral, Status, Refree, UserNrc, News

admin.site.register(State)
admin.site.register(Division)
admin.site.register(District)
admin.site.register(Nrc)
admin.site.register(Status)
admin.site.register(Referral)
admin.site.register(Refree)
admin.site.register(UserNrc)
admin.site.register(News)

