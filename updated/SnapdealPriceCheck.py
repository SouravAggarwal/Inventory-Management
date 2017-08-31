# snapdeal Inventory price check

from xlrd import open_workbook
import xlwt
import csv
import itertools

f4=open("created_snappaycheck1.csv",'w')

details=open_workbook("Details.xls",'r')
sheet = details.sheet_by_index(0)
Adetails= [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

snap=open_workbook("snapsku.xlsx",'r')
sheet = snap.sheet_by_index(0)
Asnap= [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

print(len(Asnap))
print(len(Adetails))

count=0
s=' '
for i in range(0, len(Asnap)):
    for j in range(0, len(Adetails)):
        if((Asnap[i][1] + '@' in Adetails[j][8])or (Asnap[i][1]+s  in Adetails[j][8]+s)):
            f4.write("%s,%s,%s,%s,%s,%s,%s,%s \n" % (Asnap[i][1],Asnap[i][2],Asnap[i][3],Asnap[i][6],Asnap[i][16],Adetails[j][0],Adetails[j][5],Adetails[j][7]))
# skucode, dropship, Name, (Snap)Selling_price,(Snap)Payable ,  (purchase)base_cost, item code , Name

f4.close()
