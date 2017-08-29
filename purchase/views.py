from django.shortcuts import render,redirect
from django import forms
from stocks.models import Mapping,Stock
from .models import Purchased
import datetime
class Upload(forms.Form):
	file=forms.FileField(widget=forms.FileInput(attrs={'color':'#FFFFFF','class' : 'btn btn-primary','style':'background-color:#000000'}))
	
###########################################################################################################################################

def purchase(request):
	form=""
	choice=request.GET.get('channel')
	choicePurchase=request.POST.get('submit')
	selectedheader=['Purchase ID','Purchase Date','Remarks','ItemCode','Base Price','ProductName','Capacity','Old Quantity','Quantity','Total Quantity']
	t=Purchased.objects.all().order_by("-id")
	y=[str(i).split('^^') for i in t]
	if(choice=="Show Purchase"):
		selectedheader=['Purchase ID','Purchase Date','Remarks','ItemCode','Base Price','ProductName','Capacity','Old Quantity','Quantity','Total Quantity']
		return render(request,"purchasehome.html",{'value':y,'headers':selectedheader,'isShow':'YES'})
	elif(choice=="Create Purchase"):
		x=[i for i in range(0,25)]
		list_P_N=[]
		list_Cap=[]
		list_B_P=[]
		actual_Icode_list=[]
		Old_Stocks_list=[]
		name_list_final=[]
		Stocks=Stock.objects.all().order_by('id')
		Stockmappinglist=[]
		Stocklist=[]
		t=Mapping.objects.all()
		for i in t:
			actual_Icode_list.append(str(i).split('^^')[0])
		for i in Stocks:
			Stockmappinglist.append(str(i).split('^^')[0])
			Stocklist.append(int(str(i).split('^^')[10]))
		print(choicePurchase)
		if(choicePurchase=="validate"):
			validated="yes"
			a1=request.POST.get('Purchase_ID')
			a2=request.POST.get('Purchase_Date')
			a3=request.POST.get('Remarks')
			name_list=request.POST.getlist('Item_Code')
			Old_Quantity_list=[]
			Total_Quantity_list=[]
			Quant_list=request.POST.getlist('Quantity')
			
			Quant_list=[Q_e for (n_e,Q_e) in zip(name_list,Quant_list) if n_e in actual_Icode_list]
			
			for i in name_list:
				if(i in actual_Icode_list):
					name_list_final.append(i)
					Old_Quantity_list.append(Stocklist[Stockmappinglist.index(i)])
			for i in range(len(Old_Quantity_list)):
				Total_Quantity_list.append(int(Old_Quantity_list[i])+int(Quant_list[i]))
			print(Old_Quantity_list)
			for i in name_list_final:
				queryresponse=Mapping.objects.filter(ItemCode__exact=i)
				for i in queryresponse:
					list_P_N.append(str(i).split('^^')[1])
					list_B_P.append(str(i).split('^^')[5])
					list_Cap.append(str(i).split('^^')[3])
			resp=zip(name_list_final,list_P_N,list_Cap,list_B_P,Old_Quantity_list,Quant_list,Total_Quantity_list)
			return render(request,"purchasehome.html",{"response":resp,"validated":validated,'a1':a1,'a2':a2,'a3':a3,'isShow':''})
		elif(choicePurchase=="submit"):
			PurchaseID=request.POST.get('Purchase_ID')
			PurchaseDate=request.POST.get('Purchase_Date')
			Remark=request.POST.get('Remarks')
			ItemCodes=request.POST.getlist('Item_Code')
			times=len(ItemCodes)
			PurchaseIDs=[PurchaseID for i in range(times) ]
			PurchaseDates=[PurchaseDate for i in range(times) ]
			Remarks=[Remark for i in range(times) ]
			ProductNames=request.POST.getlist('Product_Name')
			Capacities=request.POST.getlist('Capacity')
			BasePrices=request.POST.getlist('Base_Price')
			OldQuantities=request.POST.getlist('Old_Quantity')
			Quantities=request.POST.getlist('Quantity')
			TotalQuantities=request.POST.getlist('Total_Quantity')
			#Stocks=Stock.objects.all()
			#Stockmappinglist=[]
			#Stocklist=[]
			print(OldQuantities,Quantities)
			
			#for i in Stocks:
			#	Stockmappinglist.append(str(i).split('^^')[0])
			#	Stocklist.append(int(str(i).split('^^')[10]))
			for i in range(times):
				Purchased(stock=Stock.objects.get(id=Stockmappinglist.index(ItemCodes[i])+1),
						Purchase_ID=PurchaseIDs[i],
						Purchase_Date=PurchaseDates[i],
						Remarks=Remarks[i],
						ItemCode=ItemCodes[i],
						Base_Price=BasePrices[i],
						ProductName=ProductNames[i],
						Capacity=Capacities[i],
						Old_Quantity=OldQuantities[i],
						Quantity=Quantities[i],
						Total_Quantity=TotalQuantities[i]).save()
				print(Stocklist,Quantities)
				s=Stock.objects.get(id=Stockmappinglist.index(ItemCodes[i])+1)
				s.Stock=Stocklist[Stockmappinglist.index(ItemCodes[i])]+int(Quantities[i])
				s.save()
		return render(request,"purchasehome.html",{"range":x,"input":"yes",'isShow':''})	
	#elif(choice=="Adjust Stock"):
		#selectedModel=Stock
		# selectedDict=['Ordered_On','Shipment_ID','ORDER_ITEM_ID','Order_Id','Order_State','Order_Type','FSN','SKU','Product','Invoice_No','VAT','Invoice_Date','Invoice_Amount','Selling_PPI','Shipping_CPI','Quantity','Price_inc_Subsidy','Buyer_name','Ship_to_name','Address_Line_1','Address_Line_2','City','State','PIN_Code','Proc_SLA','Dispatch_After_date','Dispatch_by_date','Form_requirement','Tracking_ID','Length','Breadth','Height','Weight','Attachment']
	return render(
		request,
		'purchasehome.html',
		{'choice':choice,'value':y,'headers':selectedheader,'isShow':'YES'})

	


		