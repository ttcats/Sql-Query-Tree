from django.contrib import admin

# Register your models here.
from query.models import Dbmessage,Databasemessage,Querymessage


admin.site.register(Dbmessage)
admin.site.register(Databasemessage)
admin.site.register(Querymessage)
