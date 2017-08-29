from django.contrib import admin
from .models import Purchased

class PurchasedAdmin(admin.ModelAdmin):
	list_display=['Purchase_ID']
admin.site.register(Purchased,PurchasedAdmin)
