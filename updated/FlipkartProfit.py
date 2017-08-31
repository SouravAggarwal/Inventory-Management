#"Remove all , with -    in GargRetails Flipkart DB file"
from xlrd import open_workbook
import xlwt
import csv
import itertools

details=open_workbook("FlipDB.xls",'r')
sheet = details.sheet_by_index(0)
flipdb= [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
print(flipdb)


details=open_workbook("Details.xls",'r')
sheet = details.sheet_by_index(0)
Adetails= [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
print(Adetails)


flips=open("fliptrx.csv",'r')
transaction=[]
for line in flips:
    transaction.append(line.strip().split(','))
print(transaction)

f4=open("created_FlipProfit.csv",'w')

count=0
for i in range(0,len(flipdb)):
    for j in range(0,len(Adetails)):
        if(flipdb[i][26] in Adetails[j][4].split('@')):
            f4.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," %(flipdb[i][11],flipdb[i][16],flipdb[i][17],str(flipdb[i][20]),flipdb[i][12],flipdb[i][26],str(flipdb[i][24]),str(flipdb[i][31]),Adetails[j][9],Adetails[j][7],Adetails[j][0]))
            flag = 1
            summ = 0.0
            for k in range(0, len(transaction)):
                if((flipdb[i][16]  == "'" + (transaction[k][6])[-16:]) and (flipdb[i][17] == transaction[k][5])):
                    count =count+1
                    if (flag == 1):
                        f4.write("%s,%s,%s,%s,%s," % (transaction[k][4], transaction[k][11], transaction[k][12], transaction[k][40], transaction[k][33]))
                        flag = 0
                    summ = summ + float(transaction[k][23])
                    f4.write("%s| "%(transaction[k][23]))
            f4.write(",,%s, "%(summ))
            f4.write("\n")
print(count)
#	a	shipped	s

#---------------------------------------------------------------------------------------

count=0
s=set()
for i in range(len(transaction)):
    s.add(transaction[i][6])
f4.write("\n")
for i in s:
    flag=0
    count=0
    for j in range(len(transaction)):
        if(i == transaction[j][6]):
            if(flag == 0):
                q=transaction[j][5]
                flag=1
            count=count+1
            if(q != transaction[j][5]):
                print(i  , "'"+i[-16:] ,count)
                f4.write("\n %s,,%s,%s," % (i, "'"+i[-16:] ,count))
print("Those orderItemId which have different orderId in Flipkart Settlement file,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")

f4.close()
#------------------------------------------------------------------------------------------------
count=0
s=set()
for i in range(len(transaction)):
    s.add(transaction[i][5])

for i in s:
    flag=0
    count=0
    for j in range(len(transaction)):
        if(i == transaction[j][5]):
            if(flag == 0):
                q=transaction[j][6]
                flag=1
            count=count+1
            if(q != transaction[j][6]):
                print(i  ,i ,count)

print("All OrderId having different Itemid  in Flipkart Settlement file")
print("Remove all , with -    in GargRetails FlipkartDB file")
'''
GR Website FlipDB								Details(GR website)			Flipkart Transactions file
    GR Invoice Id	OrderItem Id	Order Id	Order Date	Invoice Amount	SKU code	Name	City	TAX 	Name	Purchased Price	WSN	Settlement Date	Status	Zone	Weight	Transactions		Total		Profit
'''