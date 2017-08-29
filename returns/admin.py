from django.contrib import admin
from .models import SnapRetDB,FlipRetDB,SnapRetBuyerDB
class FlipRetDBAdmin(admin.ModelAdmin):
	list_display=['ReturnID','OrderId']
class SnapRetDBAdmin(admin.ModelAdmin):
	list_display=['SUPC','SKU','AWBNumber']
class SnapRetBuyerDBAdmin(admin.ModelAdmin):
	list_display=['SUPC','SKU','AWBNumber']
admin.site.register(FlipRetDB,FlipRetDBAdmin)
admin.site.register(SnapRetBuyerDB,SnapRetBuyerDBAdmin)
admin.site.register(SnapRetDB,SnapRetDBAdmin)