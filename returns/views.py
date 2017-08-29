from django.shortcuts import render,redirect
from django import forms
from stocks.models import Mapping,Stock
from home.models import PayDB,FlipDB,SnapDB,Files
from .models import FlipRetDB,SnapRetDB,SnapRetBuyerDB
from io import TextIOWrapper
import csv
from collections import defaultdict,Counter
import xlrd
import datetime

class Upload(forms.Form):
	file=forms.FileField(widget=forms.FileInput(attrs={'color':'#FFFFFF','class' : 'btn btn-primary','style':'background-color:#000000'}))
	
def rethome(request):
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
	selectedheader=['No','Tracking ID','Order ID' ,'Order Item ID','SKU','Product','Completed Date']
	selectedModel=FlipRetDB
	if(choice=="Snapdeal Courier"):
		selectedheader=['No','Product','SKU','Suborder ID','Return Delivered On','AWBNumber']
		selectedModel=SnapRetDB
	elif(choice=="Snapdeal Buyer"):
		selectedheader=['No','Product','SKU','Suborder ID','Return Delivered On','AWBNumber']
		selectedModel=SnapRetBuyerDB
	elif(choice=="FlipDB"):
		selectedheader=['No','Tracking ID','Order ID' ,'Order Item ID','SKU','Product','Completed Date']
		selectedModel=FlipRetDB
	if request.method == "POST":
		form = Upload(request.POST,request.FILES)
		print(choice)
		if form.is_valid():
			# if(str(request.FILES['file1'])!=str(request.FILES['file2'])):
				# return render(request,'rethome.html',{'form':Upload(),'warn':"THE FILES NAME DO NOT MATCH"})
			Files(FileUploaded=request.FILES['file']).save()
			format=str(request.FILES['file']).split('.')[1]
			# request.FILES['file1'].save_to_database(
				# model=selectedModel,
				# mapdict=selectedDict)
			ob=Files.objects.latest('timestamp')
			ob.FileSynced=str(request.FILES['file'])
			ob.save()
			if(format=="xlsx"):
				if(choice=="Snapdeal Courier"):
					crosssnap=[]
					allsnap=SnapDB.objects.all()
					allsnaprets=SnapRetDB.objects.all()
					crosssnapret=[]
					for i in allsnaprets:
						x=str(i)
						crosssnapret.append(x.split('^^')[2]+x.split('^^')[1])
					for i in allsnap:
						x=str(i)
						crosssnap.append(x.split('^^')[2]+x.split('^^')[4])
					#getting information from SnapDB
					print(crosssnapret,crosssnap)
					x=xlrd.open_workbook(file_contents=request.FILES['file'].read())
					x=x.sheet_by_index(0)
					SnapSKU=[]
				
					for i in range(1,x.nrows):
						print(str(x.cell(i,4)).strip("text:'")+str(x.cell(i,3)).strip("text:'"))
						if(str(x.cell(i,4)).strip("text:'")+str(x.cell(i,3)).strip("text:'") in crosssnap and str(x.cell(i,4)).strip("text:'")+str(x.cell(i,3)).strip("text:'") not in crosssnapret):
							SnapSKU.append(str(x.cell(i,3)).strip("text:'"))
					#get more information from the file xlsx and compare it with crosssnap, if the SKU- req index combination does not exist then delete SKU
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
							return render(request,"rethome.html",{'warn':"SOME SKUS DO NOT EXIST PLEASE RECHECK DOCUMENT",'form':Upload()})
					for i in range(1,x.nrows):
						if(str(x.cell(i,4)).strip("text:'")+str(x.cell(i,3)).strip("text:'") in crosssnap and str(x.cell(i,4)).strip("text:'")+str(x.cell(i,3)).strip("text:'") not in crosssnapret):
							SnapRetDB(
							
								Name=str(x.cell(i,0)).strip("text:'"),
								Attribute=str(x.cell(i,1)).strip("text:'"),
								SUPC=str(x.cell(i,2)).strip("text:'"),
								SKU=str(x.cell(i,3)).strip("text:'"),
								SuborderID=str(x.cell(i,4)).strip("text:'"),
								ReturnInitiatedOn=str(x.cell(i,5)).strip("text:'"),
								ReturnDeliveredOn=str(x.cell(i,6)).strip("text:'"),
								FulfilmentMode=str(x.cell(i,7)).strip("text:'"),
								AWBNumber=str(x.cell(i,8)).strip("text:'"),
								SellingPrice=str(x.cell(i,9)).strip("text:'"),
								PaymentMode=str(x.cell(i,10)).strip("text:'"),
								OrderDate=str(x.cell(i,11)).strip("text:'"),
								DeductedAmount=str(x.cell(i,12)).strip("text:'"),
								DuePaymentDate=str(x.cell(i,13)).strip("text:'"),
								DeductedAmount_Wallet=str(x.cell(i,14)).strip("text:'"),
								DuePaymentDate_Wallet=str(x.cell(i,15)).strip("text:'"),
								ReturnAcceptedon=str(x.cell(i,16)).strip("text:'"),
								).save()
				
					for i in range(len(SnapSKU)):
						for j in range(len(Stockmappinglist)):
							if(SnapSKU[i] in Stockmappinglist[j]):
								s=Stock.objects.get(id=j+1)
								s.Stock=(int(Stocklist[j])+SnapQty[i])
								s.save()
					return redirect("/returns")
				if(choice=="Snapdeal Buyer"):
					crosssnap=[]
					allsnap=SnapDB.objects.all()
					allsnaprets=SnapRetBuyerDB.objects.all()
					crosssnapret=[]
					for i in allsnaprets:
						x=str(i)
						crosssnapret.append(x.split('^^')[2]+x.split('^^')[1])
					for i in allsnap:
						x=str(i)
						crosssnap.append(x.split('^^')[2]+x.split('^^')[4])
					#getting information from SnapDB
					print(crosssnapret,crosssnap)
					x=xlrd.open_workbook(file_contents=request.FILES['file'].read())
					x=x.sheet_by_index(0)
					SnapSKU=[]
				
					for i in range(1,x.nrows):
						print(str(x.cell(i,3)).strip("text:'")+str(x.cell(i,2)).strip("text:'"))
						if(str(x.cell(i,3)).strip("text:'")+str(x.cell(i,2)).strip("text:'") in crosssnap and str(x.cell(i,3)).strip("text:'")+str(x.cell(i,2)).strip("text:'") not in crosssnapret):
							SnapSKU.append(str(x.cell(i,2)).strip("text:'"))
					#get more information from the file xlsx and compare it with crosssnap, if the SKU- req index combination does not exist then delete SKU
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
							return render(request,"rethome.html",{'warn':"SOME SKUS DO NOT EXIST PLEASE RECHECK DOCUMENT",'form':Upload()})
					for i in range(1,x.nrows):
						if(str(x.cell(i,3)).strip("text:'")+str(x.cell(i,2)).strip("text:'") in crosssnap and str(x.cell(i,3)).strip("text:'")+str(x.cell(i,2)).strip("text:'") not in crosssnapret):
							SnapRetBuyerDB(
							
								Name=str(x.cell(i,0)).strip("text:'"),
								SUPC=str(x.cell(i,1)).strip("text:'"),
								SKU=str(x.cell(i,2)).strip("text:'"),
								SuborderID=str(x.cell(i,3)).strip("text:'"),
								ReturnInitiatedOn=str(x.cell(i,4)).strip("text:'"),
								ReturnDeliveredOn=str(x.cell(i,5)).strip("text:'"),
								FulfilmentMode=str(x.cell(i,6)).strip("text:'"),
								AWBNumber=str(x.cell(i,7)).strip("text:'"),
								SellingPrice=str(x.cell(i,8)).strip("text:'"),
								PaymentMode=str(x.cell(i,9)).strip("text:'"),
								OrderDate=str(x.cell(i,10)).strip("text:'"),
								ShippingDate=str(x.cell(i,11)).strip("text:'"),
								Reason=str(x.cell(i,12)).strip("text:'"),
								ReturnAcceptedon=str(x.cell(i,13)).strip("text:'"),
								RTVCode=str(x.cell(i,14)).strip("text:'"),
								DeductedAmount=str(x.cell(i,15)).strip("text:'"),
								DuePaymentDate=str(x.cell(i,16)).strip("text:'"),
								Status=str(x.cell(i,17)).strip("text:'"),
								
								).save()
				
					for i in range(len(SnapSKU)):
						for j in range(len(Stockmappinglist)):
							if(SnapSKU[i] in Stockmappinglist[j]):
								s=Stock.objects.get(id=j+1)
								s.Stock=(int(Stocklist[j])+SnapQty[i])
								s.save()
					return redirect("/returns")
			elif(format=="csv"):
				allflip=FlipDB.objects.all()
				allprevfliprets=FlipRetDB.objects.all()
				crossflipret=[]
				crossflip=[]
				for i in allflip:
					x=str(i)
					crossflip.append(x.split('^^')[0]+x.split('^^')[2])
				print(crossflip)
				for i in allprevfliprets:
					x=str(i)
					crossflipret.append(x.split('^^')[1]+x.split('^^')[3])
				#getting information from flipDB
				x=TextIOWrapper(request.FILES['file'].file,encoding=request.encoding)
				data=[i for i in csv.reader(x.read().splitlines())]
				
				del(data[0])
				flipSKU=[]
				flipQty=[]
				x=0
				for i in data:
					if(i[10]!=''):
						if(i[4]+i[10] in crossflip and i[4]+i[10] not in crossflipret):
							print(i[10])
							flipSKU.append(i[10])
					if(i[26]!=''):
						if(i[4]+i[10] in crossflip and i[4]+i[10] not in crossflipret):
							print(i[10])
							flipQty.append(int(i[26]))
				print(flipSKU,flipQty)
				#get more information from the file csv and compare it with crosssnap, if the SKU- req index combination does not exist then delete SKU
				for i in range(len(data)):
					for j in range(len(data[0])):
						if not data[i][j]:
							data[i][j]='0'
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
						return render(request,"rethome.html",{'warn':"SOME SKUS DO NOT EXIST PLEASE RECHECK DOCUMENT",'form':Upload()})
			
				for i in data:
					
					if(i[4]+i[10] in crossflip and i[4]+i[10] not in crossflipret):
						FlipRetDB(
							ReturnApprovalDate=i[0],
							ReturnRequestedDate=i[1],
							ReturnID=i[2],
							TrackingId=i[3],
							OrderId=i[4],
							ORDERITEMID=i[5],
							ReturnType=i[6],
							ReturnSubType=i[7],
							ReplacementOrderItemID=i[8],
							ReturnStatus=i[9],
							SKU=i[10],
							FSN=i[11],
							Product=i[12],
							FFType=i[13],
							ReturnDeliveryPromiseDate=i[14],
							PickedUpDate=i[15],
							OutForDeliveryDate=i[16],
							CompletedDate=i[17],
							ReturnReason=i[18],
							ReturnSubReason=i[19],
							Comments=i[20],
							BuyerName=i[21],
							BuyerAddress=i[22],
							ReverseLogisticFormNo=i[23],
							ForwardLogisticFormNo=i[24],
							TotalPrice=i[25],
							Quantity=i[26],
							GoodQuantity=i[27],
							BadQuantity=i[28],
							VendorName=i[29],
							).save()
				
				for i in range(len(flipSKU)):
					for j in range(len(Stockmappinglist)):
						if(flipSKU[i] in Stockmappinglist[j]):
							s=Stock.objects.get(id=j+1)
							s.Stock=(int(Stocklist[j])+(flipQty[i]))
							s.save()
				return redirect("/returns")
		else:
			return render(request,"rethome.html",{'warn':"Please select a file!"})
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
		'rethome.html',
		{'form': form,'value':y,'headers':selectedheader})
			
	return render(request,"rethome.html",{'form':Upload()})