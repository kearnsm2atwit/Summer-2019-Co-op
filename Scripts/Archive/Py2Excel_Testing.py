import xlwt
from xlwt import Workbook


wb = Workbook()

sheet1 = wb.add_sheet('Sheet 1')

for x in range(0,10):
    sheet1.write(x,0, 'Test')


wb.save('Test.xls')