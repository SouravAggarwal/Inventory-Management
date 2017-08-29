from django.shortcuts import render,redirect
from .models import PayDB,FlipDB,SnapDB,Files
from django import forms
import datetime
from stocks.models import Mapping,Stock
from io import TextIOWrapper
import csv
from collections import defaultdict,Counter
import xlrd

class Upload(forms.Form):
	file=forms.FileField(widget=forms.FileInput(attrs={'color':'#FFFFFF','class' : 'btn btn-primary','style':'background-color:#000000'}))
	# file2=forms.FileField(widget=forms.FileInput(attrs={'color':'#FFFFFF','class' : 'btn btn-primary','style':'background-color:#000000'}))
	

####################################################################################
def home(request):
	m="LOGIN"
	if request.method =="POST":
		x=request.POST.get('user') 
		y=request.POST.get('pwd')
		if(x=="gargretails" and y=="retails.123"):
			return redirect("/landing")
		else:
			m="Wrong Credentials! Please Login Again..."
		
	return render(request,"login.html",{'message':m})
	
####################################################################################

def landing(request):
	Stocks=Stock.objects.all().order_by('id')
	Stockmappinglist=[]
	Stocklist=[]
	FSKU=[]
	SSKU=[]
	PSKU=[]
	for i in Stocks:
		Stockmappinglist.append(str(i).split('^^')[0])
		Stocklist.append(int(str(i).split('^^')[10]))
		FSKU.append(str(i).split('^^')[7].split('@'))
		SSKU.append(str(i).split('^^')[8].split('@'))
		PSKU.append(str(i).split('^^')[9].split('@'))
	choice=request.GET.get('channel')
	selectedheader=['No','Order ID','Product Name' ,'SKU','Quantity','Ordered On','Amount','Tracking ID']
	selectedModel=FlipDB
	selectedDict=['Ordered_On','Shipment_ID','ORDER_ITEM_ID','Order_Id','Order_State','Order_Type','FSN','SKU','Product','Invoice_No','VAT','Invoice_Date','Invoice_Amount','Selling_PPI','Shipping_CPI','Quantity','Price_inc_Subsidy','Buyer_name','Ship_to_name','Address_Line_1','Address_Line_2','City','State','PIN_Code','Proc_SLA','Dispatch_After_date','Dispatch_by_date','Form_requirement','Tracking_ID','Length','Breadth','Height','Weight','Attachment']
	if(choice=="Snapdeal"):
		selectedheader=['No','AWB Number','Courier','Suborder ID','Product','SKU','Selling Price','Order Date']
		selectedModel=SnapDB
		selectedDict=['Courier','Product','Reference_Code','Suborder_ID','SKU_code','AWB_Number','Order_Verified_Date','Order_Created_Date','Customer_Name','Shipping_Name','City','State','PinCode','SellingPPI','Tax_Amount_Percent','IMEI','Promised_ShipDate','MRP','Invoice_Code','Fulfilment_mode','Mobile_No','Email_ID','SUPC','Attributes','PaymentMode','HandoverDate','Courier_Code','Oneship_Center_Name','Address']
	elif(choice=="PayTm"):
		selectedModel=PayDB
		selectedDict=['OrderID']
	elif(choice=="FlipDB"):
		selectedheader=['No','Order ID','Product Name' ,'SKU','Quantity','Ordered On','Amount','Tracking ID']
		selectedModel=FlipDB
		selectedDict=['Ordered_On','Shipment_ID','ORDER_ITEM_ID','Order_Id','Order_State','Order_Type','FSN','SKU','Product','Invoice_No','VAT','Invoice_Date','Invoice_Amount','Selling_PPI','Shipping_CPI','Quantity','Price_inc_Subsidy','Buyer_name','Ship_to_name','Address_Line_1','Address_Line_2','City','State','PIN_Code','Proc_SLA','Dispatch_After_date','Dispatch_by_date','Form_requirement','Tracking_ID','Length','Breadth','Height','Weight','Attachment']
	if request.method == "POST":
		form = Upload(request.POST,request.FILES)
		choice=request.POST.get('channel')
		print(choice)
		if form.is_valid():
			# if(str(request.FILES['file1'])!=str(request.FILES['file2'])):
				# return render(request,'landing.html',{'form':Upload(),'warn':"THE FILES NAME DO NOT MATCH"})
			Files(FileUploaded=request.FILES['file']).save()
			format=str(request.FILES['file']).split('.')[1]
			# request.FILES['file1'].save_to_database(
				# model=selectedModel,
				# mapdict=selectedDict)
			ob=Files.objects.latest('timestamp')
			ob.FileSynced=str(request.FILES['file'])
			ob.save()
			if(format=="xlsx"):
				x=xlrd.open_workbook(file_contents=request.FILES['file'].read())
				x=x.sheet_by_index(0)
				SnapSKU=[]
				for i in range(1,x.nrows):
					SnapSKU.append(str(x.cell(i,4)).strip("text:'"))
				print(SnapSKU)
				for i in range(len(SnapSKU)):
					for j in range(len(SSKU)):
						if SnapSKU[i] in SSKU[j]:
							SnapSKU[i]=Stockmappinglist[j]
							
				SnapQty=list(Counter(SnapSKU).values())
				SnapSKU=list(Counter(SnapSKU).keys())
				print(SnapSKU,SnapQty)
				for i in SnapSKU:
					if i not in Stockmappinglist:
						return render(request,"landing.html",{'warn':"SOME SKUS DO NOT EXIST PLEASE RECHECK DOCUMENT",'form':Upload()})
				num=SnapDB.objects.all().count()
				for i in range(1,x.nrows):
					SnapDB(
							InvoiceID=str("GRSN-"+str(num+i)),
							Courier=str(x.cell(i,0)).strip("text:'"),
							Product=str(x.cell(i,1)).strip("text:'"),
							Reference_Code=str(x.cell(i,2)).strip("text:'"),
							Suborder_ID=str(x.cell(i,3)).strip("text:'"),
							SKU_code=str(x.cell(i,4)).strip("text:'"),
							AWB_Number=str(x.cell(i,5)).strip("text:'"),
							Order_Verified_Date=str(x.cell(i,6)).strip("text:'"),
							Order_Created_Date=str(x.cell(i,7)).strip("text:'"),
							Customer_Name=str(x.cell(i,8)).strip("text:'"),
							Shipping_Name=str(x.cell(i,9)).strip("text:'"),
							City=str(x.cell(i,10)).strip("text:'"),
							State=str(x.cell(i,11)).strip("text:'"),
							PinCode=str(x.cell(i,12)).strip("text:'"),
							SellingPPI=str(x.cell(i,13)).strip("text:'"),
							Tax_Amount_Percent=str(x.cell(i,14)).strip("text:'"),
							IMEI=str(x.cell(i,15)).strip("text:'"),
							Promised_ShipDate=str(x.cell(i,16)).strip("text:'"),
							MRP=int(str(x.cell(i,17)).strip("text:'")),
							Invoice_Code=str(x.cell(i,18)).strip("text:'"),
							Fulfilment_mode=str(x.cell(i,19)).strip("text:'"),
							Mobile_No=str(x.cell(i,20)).strip("text:'"),
							Email_ID=str(x.cell(i,21)).strip("text:'"),
							SUPC=str(x.cell(i,22)).strip("text:'"),
							Attributes=str(x.cell(i,23)).strip("text:'"),
							PaymentMode=str(x.cell(i,24)).strip("text:'"),
							HandoverDate=str(x.cell(i,25)).strip("text:'"),
							Courier_Code=str(x.cell(i,26)).strip("text:'"),
							Oneship_Center_Name=str(x.cell(i,27)).strip("text:'"),
							Address=str(x.cell(i,28)).strip("text:'")
							).save()
				
				for i in range(len(SnapSKU)):
					for j in range(len(Stockmappinglist)):
						if(SnapSKU[i] in Stockmappinglist[j]):
							s=Stock.objects.get(id=j+1)
							s.Stock=(int(Stocklist[j])-SnapQty[i])
							s.save()
				return redirect("/landing")
			elif(format=="csv"):
				x=TextIOWrapper(request.FILES['file'].file,encoding=request.encoding)
				data=[i for i in csv.reader(x.read().splitlines())]
				
				del(data[0])
				flipSKU=[]
				flipQty=[]
				x=0
				
				for i in data:
					if(i[7]!=''):
						flipSKU.append(i[7])
					if(i[15]!=''):
						flipQty.append(int(i[15]))
				for i in range(len(data)):
					for j in range(len(data[0])):
						if not data[i][j]:
							data[i][j]='0'
				print(data)
				d = defaultdict(list)
				for i in range(len(flipSKU)):
					for j in range(len(FSKU)):
						if flipSKU[i] in FSKU[j]:
							flipSKU[i]=Stockmappinglist[j]
				tit=zip(flipSKU,flipQty)
				for k,v in tit:
					d[k].append(v)
				for k,v in d.items():
					d[k]=sum(v)
				flipSKU=list(d.keys())
				flipQty=list(d.values())
				for i in flipSKU:
					if i not in Stockmappinglist:
						return render(request,"landing.html",{'warn':"SOME SKUS DO NOT EXIST PLEASE RECHECK DOCUMENT",'form':Upload()})
				num=FlipDB.objects.all().count()+1
				for i in data:		
					FlipDB(
						InvoiceID=str("GRFL-"+str(num+data.index(i))),
						Ordered_On=i[0],
						Shipment_ID=i[1],
						ORDER_ITEM_ID=i[2],
						Order_Id=i[3],
						Order_State=i[4],
						Order_Type=i[5],
						FSN=i[6],
						SKU=i[7],
						Product=i[8],
						Invoice_No=i[9],
						VAT=float(i[10]),
						Invoice_Date=i[11],
						Invoice_Amount=int(i[12]),
						Selling_PPI=int(i[13]),
						Shipping_CPI=int(i[14]),
						Quantity=int(i[15]),
						Price_inc_Subsidy=int(i[16]),	
						Buyer_name=i[17],
						Ship_to_name=i[18],
						Address_Line_1=i[19],
						Address_Line_2=i[20],
						City=i[21],
						State=i[22],
						PIN_Code=i[23],
						Proc_SLA=i[24],
						Dispatch_After_date=i[25],
						Dispatch_by_date=i[26],
						Form_requirement=i[27],
						Tracking_ID=i[28],
						Length=float(i[29]),
						Breadth=float(i[30]),
						Height=float(i[31]),
						Weight=float(i[32]),
						Attachment=i[33]).save()
				
				for i in range(len(flipSKU)):
					for j in range(len(Stockmappinglist)):
						if(flipSKU[i] in Stockmappinglist[j]):
							s=Stock.objects.get(id=j+1)
							s.Stock=(int(Stocklist[j])-(flipQty[i]))
							s.save()
				return redirect("/landing")
		else:
			return render(request,"landing.html",{'warn':"Please select a file!"})
	else:
		x=selectedModel.objects.filter(timestamp__gte=datetime.date.today())[:200]
		for i in x :
			print(i)
		if(x!= ""):
			t=0
			y=[str(i).split('^^') for i in x]
			for i in y:
				t=t+1
				i.insert(0,t)
		
		
		form = Upload()
	return render(
		request,
		'landing.html',
		{'form': form,'value':y,'headers':selectedheader})
def sync(request):
	pass