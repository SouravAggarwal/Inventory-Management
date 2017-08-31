from xlrd import open_workbook
import xlwt
import csv
import itertools

details=open_workbook("Details.xls",'r')
sheet = details.sheet_by_index(0)
Adetails= [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

choice=input("Enter f or s")
if (choice is 's'):
    snap=open_workbook("snapsku.xlsx",'r')
    sheet = snap.sheet_by_index(0)
    Asnap= [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

    zz=[[]]
    mm=[[]]
    detail_snaplist=[[]]
    for i in range(len(Adetails)):
        zz.append((Adetails[i][8]))
    for j in zz:
        detail_snaplist.append((str(j)).split("@"))

    print(detail_snaplist)

    merged = list(itertools.chain(*detail_snaplist))
    print (merged)
####
    qq=[[]]

    for k in range(len(Asnap)):
        qq.append(Asnap[k][1])
    print (qq)

#####checking
    print("Element not in list:::::::::::")
    for i in qq:
        if (i not in (merged)):
            print (i)
    print ("Duplicate id ::::::::::")
    print(set([x for x in merged if merged.count(x) > 1]))
    print ("Snapdeal ")

######################################################################################################333

elif(choice is 'f'):
    flip = open("Order-CSV.csv", 'r')
    Aflip = []
    qq=[]
    for line in flip:  # conversion of flip file into array in f1_Array
        Aflip.append(line.strip().split(','))
    for i in Aflip:
        print (i)
    print("ENDS HERE")
 #   for k in range(len(Aflip)):
  #      qq.append(Aflip[k][7])
   # print(qq)

    zz = [[]]

    detail_snaplist = [[]]
    for i in range(len(Adetails)):
        zz.append((Adetails[i][4]))
    for j in zz:
        detail_snaplist.append((str(j)).split("@"))

    print(detail_snaplist)

    merged = list(itertools.chain(*detail_snaplist))
    print(merged)
    ####
    qq = [[]]
    print ("Elements of Flipkart")
    for i in range(0,len(Aflip)-3):
        print(Aflip[i][7])

    #####checking
    print("Element not in list:::::::::::")
    print(len(Aflip))
    for i in range(0,len(Aflip)-3):
        print(Aflip[i][7])
        if (Aflip[i][7] not in (merged)):
            print(i)
    print ("Duplicated:::::")
    print(set([x for x in merged if merged.count(x) > 1]))
    print("Flipkart ")