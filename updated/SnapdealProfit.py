#check for duplicacy in snapdb file
from xlrd import open_workbook
import xlwt
import csv
import itertools

details=open_workbook("SnapDB.xls",'r')
sheet = details.sheet_by_index(0)
snapdb= [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
print(snapdb)


details=open_workbook("Details.xls",'r')
sheet = details.sheet_by_index(0)
Adetails= [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
print(Adetails)


details=open_workbook("transaction.xlsx",'r')
sheet = details.sheet_by_index(0)
transaction= [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
print(transaction)

f4=open("created_snappaycheck1.csv",'w')

for i in range(0,len(snapdb)):
    for j in range(0,len(Adetails)):
        if(snapdb[i][23] in Adetails[j][8].split('@')):
            f4.write("%s,%s,%s,%s,%s,%s,%s,%s,%s," %(str(snapdb[i][28]),snapdb[i][11],str(snapdb[i][0]),snapdb[i][17],snapdb[i][20],snapdb[i][23],snapdb[i][25],Adetails[j][7],Adetails[j][0]))
            flag = 1
            summ = 0.0

            for k in range(0, len(transaction)):
                if (snapdb[i][0] == transaction[k][38]):
                    if (flag == 1):
                        f4.write("%s,%s,%s," % (transaction[k][6], transaction[k][4], transaction[k][34]))
                        flag = 0
                    summ = summ + transaction[k][33]
                    f4.write("%s| "%(transaction[k][33]))
            f4.write(",,%s, "%(summ))
            f4.write("\n")
f4.close()
