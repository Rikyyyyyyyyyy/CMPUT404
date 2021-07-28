# -*- coding: utf-8 -*-
import xlrd
import xlwt
from xlutils.copy import copy as xl_copy
def generate_area(area_r,area_i):
    xlrd.xlsx.ensure_elementtree_imported(False, None)
    xlrd.xlsx.Element_has_iter = True
    wb = xlrd.open_workbook(r'data/LabData.xlsx')
    sheet = wb.sheet_by_index(0)
    col_num = sheet.ncols
    row_num = sheet.nrows

    out_wb = xl_copy(wb)
    sheet2 = out_wb.add_sheet('Sheet2')

    sheet2.write(0, 0, 'Analyze index')
    for i in range(1, row_num+1):
        sheet2.write(i, 0, i)

    sheet2.write(0, 1, 'Name')
    for i in range(2, row_num):
        name_val = sheet.cell_value(i, 0)
        sheet2.write(i-1, 1, name_val)

    sheet2.write(0, 2, 'Mass')
    for i in range(2, row_num):
        mass_val = sheet.cell_value(i, 1)
        sheet2.write(i-1, 2, mass_val)

    name_i = 3
    for j in range(2,col_num,5):
        name = sheet.cell_value(0,j)
        sheet2.write(0,name_i,name)
        name_i = name_i + 1

    for i in range(2, row_num):
        col_index = 3
        for k in range(5, col_num, int(area_r)):
            area_val = sheet.cell_value(i, k)
            if area_val == '':
                sheet2.write(i-1,col_index,0)
            else:
                sheet2.write(i-1, col_index, area_val)
            col_index = col_index +1

    out_wb.save('data/Output.xls')


def main():
    each_area = input("the range for each area: ")
    area_index = input("where is the area locate: ")
    generate_area(each_area,area_index)



main()