from django.contrib import admin
from .models import FlipDB,SnapDB,PayDB,Files
class FlipDBAdmin(admin.ModelAdmin):
	list_display=['Order_Id','timestamp']
class SnapDBAdmin(admin.ModelAdmin):
	list_display=['AWB_Number','timestamp']
class PayDBAdmin(admin.ModelAdmin):
	pass
class FilesAdmin(admin.ModelAdmin):
	list_display=['FileUploaded','timestamp']
admin.site.register(FlipDB,FlipDBAdmin)
admin.site.register(Files,FilesAdmin)
admin.site.register(SnapDB,SnapDBAdmin)
admin.site.register(PayDB,PayDBAdmin)