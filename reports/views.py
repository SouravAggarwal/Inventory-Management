from django.shortcuts import render
import django_excel as excel
from stocks.models import Stock,Adjusted,Mapping
from home.models import PayDB,SnapDB,FlipDB
from returns.models import FlipRetDB,SnapRetDB,SnapRetBuyerDB
from purchase.models import Purchased
def reportshome(request):
	if request.method =="POST":
		channel =request.POST.get('channel')
		if(channel=="FlipDB"):
			selectDB=FlipDB
		elif(channel=="SnapDB"):
			selectDB=SnapDB
		elif(channel=="PayDB"):
			selectDB=PayDB
		elif(channel=="Stock"):
			selectDB=Stock
		elif(channel=="Adjusted"):
			selectDB=Adjusted
		elif(channel=="Details"):
			selectDB=Mapping
		elif(channel=="Purchased"):
			selectDB=Purchased
		elif(channel=="FlipReturns"):
			selectDB=FlipRetDB
		elif(channel=="SnapReturns Courier"):
			selectDB=SnapRetDB
		elif(channel=="SnapReturns Buyer"):
			selectDB=SnapRetBuyerDB
		return excel.make_response_from_a_table(selectDB, 'xls', file_name=channel)
	return render(request,'rhome.html')