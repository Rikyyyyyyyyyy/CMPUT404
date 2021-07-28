from GMD_class import GS
import remove_compound
from compound_class import Compound
import sys
import cal_exp_rt
import pandas as pd
import GMD_search
import xlrd
from xlutils.copy import copy as xl_copy
import sim_v2
import pyexcel as p
import operator
import Category_search
import mat_searchV2
import scipy.io as sio
from out_compound_class import out_compound

ori_diff_range = ["T2:T", "AA2:AA", "AH2:AH","AO2:AO","AV2:AV","BC2:BC","BJ2:BJ","BQ2:BQ","BX2:BX","CE2:CE"]
ori_sim_range = ["P2:P","W2:W","AD2:AD","AK2:AK","AR2:AR","AY2:AY","BF2:BF","BM2:BM","BT2:BT","CA2:CA"]


def printProgressBar(i, max, postText):
    n_bar = 10  # size of progress bar
    j = i / max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()


def main():
    print("please select the library you want to use")
    print("------1 GMD Library")
    print("------2 NIST Library")
    library = input("select your library: ")
    data_file = input("please input data file name: ")
    compare_data_file = input("please input the compare data file: ")
    ri_window = input("Please input the Ri window range: ")
    hits_range = input("Please input how many hits you want: ")
    alkane_ri = input("Please input the Alkane Retention Index Gc Column Composition: ")
    rt_diff = input("Please give an acceptable RT difference: ")
    acc_sim = input("Please give an acceptable smallest similarity or reverse bound: ")

    GMD_s = GS(data_file, compare_data_file, ri_window, hits_range, alkane_ri, rt_diff, acc_sim)
    remove_compound.remove_lines(GMD_s)

    wb = xlrd.open_workbook(r'data/'+data_file)
    sheet = wb.sheet_by_index(1)
    col_num = sheet.ncols

    new_wb = xl_copy(wb)
    del_sheet = new_wb.get_sheet(1)

    start_col = col_num

    diff_format_range_list = []
    sim_format_range_list = []

    ## open the mat database
    if int(library) == 2:
        mat_Library = sio.loadmat('data/Mainlib.mat')
        library_compound = mat_Library['Compound']
        compound_num = len(library_compound[0])
    for i in range(int(hits_range)):
        del_sheet.write(0, i + start_col, "Hit " + str(i + 1) + " Name")
        del_sheet.write(0, i + start_col+1, "Hit " + str(i + 1) + " RT")
        del_sheet.write(0, i + start_col+2, "Hit " + str(i + 1) + " Similarity")
        del_sheet.write(0, i + start_col+3, "Hit " + str(i + 1) + " Reverse")
        del_sheet.write(0, i + start_col+4, "Hit " + str(i + 1) + " CAS")
        del_sheet.write(0, i + start_col+5, "Hit " + str(i + 1) + " Formula")
        del_sheet.write(0, i + start_col+6, "Hit " + str(i + 1) + " RT diff")
        diff_format_range_list.append(ori_diff_range[i])
        sim_format_range_list.append(ori_sim_range[i])
        start_col = start_col + 6

    file_name = r'data/' + str(GMD_s.get_file_name())
    del_data = pd.read_excel(file_name, 'Sheet2')
    good_result = 0
    total_result = len(del_data)*int(hits_range)



    result_sheet_name = []
    result_sheet_analyze_num = []
    result_sheet_sim = []
    result_sheet_diff = []
    result_category = []
    result_RI = []
    result_RT = []
    result_mass = []
    result_ori_name = []
    # for j in del_data.index:

    for j in range(167, 168):
        result_sheet_ocp = []
        start_col = col_num
        analy_index = del_data["analy index"][j]
        name = del_data["Name"][j]
        rt = del_data["R.T. (s)"][j]
        dim1 = del_data["1st Dimension Time (s)"][j]
        dim2 = del_data["2nd Dimension Time (s)"][j]
        cas = del_data["CAS"][j]
        area = del_data["Area"][j]
        quant_m = del_data["Quant Masses"][j]
        quant_sn = del_data["Quant S/N"][j]
        uni_m = del_data["UniqueMass"][j]
        sim = del_data["Similarity"][j]
        rev = del_data["Reverse"][j]
        spec = del_data["Spectra"][j]
        cp = Compound(analy_index, name, rt, dim1, dim2, cas, area, quant_m, quant_sn, uni_m, sim, rev, spec)
        Category_search.category_search(cp)
        exp_rt = cal_exp_rt.cal_rt(GMD_s, cp)
        out_compound_list = []
        if int(library) == 1:
            out_compound_list = GMD_search.GMD_search(exp_rt, GMD_s, cp)
        elif int(library) == 2 and exp_rt != None:
            out_compound_list = mat_searchV2.mat_search(exp_rt, GMD_s, cp, library_compound, compound_num)
        else:
            for i in range(int(GMD_s.hits_range)):
                out_compound_list.append(out_compound(cp.analy_index, None, None, None, None, None, None, None,))

        # keep the data for the best hit if no then unknown
        # definition for best hit: the find the best similarity (need to >700) and if it's Rt diff (-30> x <30)
        # keep the analyze number, compound name, similarity, diff
        if int(library) == 1:
            for ocp in out_compound_list:
                if ocp.name != "None":
                    sim, rev = sim_v2.do_cal(ocp.get_spectrum(), spec,)
                    diff_rt = float(ocp.get_rt()) - exp_rt
                else:
                    sim = int(-99999)
                    rev = int(-99999)
                    diff_rt = int(-99999)
                ocp.set_category(cp.category)
                del_sheet.write(j+1, start_col, str(ocp.get_name()))
                del_sheet.write(j+1, start_col + 1, str(ocp.get_rt()))
                del_sheet.write(j+1, start_col + 2, str(sim))
                del_sheet.write(j+1, start_col + 3, str(rev))
                del_sheet.write(j+1, start_col + 4, str(ocp.get_cas()))
                del_sheet.write(j+1, start_col + 5, str(ocp.get_formula()))
                del_sheet.write(j + 1, start_col + 6, str(diff_rt))
                ocp.similarity = sim
                ocp.reverse = rev
                ocp.set_rt_diff(diff_rt)
                if diff_rt < float(GMD_s.get_acc_rt_diff()) and sim > float(GMD_s.get_acc_sim()):
                    good_result = good_result + 1
                start_col = start_col + 7
                result_sheet_ocp.append(ocp)
        elif int(library) == 2 and exp_rt != None:
            for ocp in out_compound_list:
                ocp.set_category(cp.category)
                diff_rt = float(ocp.get_rt()) - exp_rt
                del_sheet.write(j + 1, start_col, str(ocp.get_name()))
                del_sheet.write(j + 1, start_col + 1, str(ocp.get_rt()))
                del_sheet.write(j + 1, start_col + 2, str(ocp.get_similarity()))
                del_sheet.write(j + 1, start_col + 3, str(ocp.get_reverse()))
                del_sheet.write(j + 1, start_col + 4, str(ocp.get_cas()))
                del_sheet.write(j + 1, start_col + 5, str(ocp.get_formula()))
                del_sheet.write(j + 1, start_col + 6, str(diff_rt))
                ocp.set_rt_diff(diff_rt)
                if diff_rt < float(GMD_s.get_acc_rt_diff()) and sim > float(GMD_s.get_acc_sim()):
                    good_result = good_result + 1
                start_col = start_col + 7
                result_sheet_ocp.append(ocp)

        else:
            for ocp in out_compound_list:
                del_sheet.write(j + 1, start_col, str(ocp.get_name()))
                del_sheet.write(j + 1, start_col + 1, str(ocp.get_rt()))
                del_sheet.write(j + 1, start_col + 2, str(sim))
                del_sheet.write(j + 1, start_col + 3, str(rev))
                del_sheet.write(j + 1, start_col + 4, str(ocp.get_cas()))
                del_sheet.write(j + 1, start_col + 5, str(ocp.get_formula()))
                del_sheet.write(j + 1, start_col + 6, str(None))
                start_col = start_col + 7


        # in case we have any None Similarity -> sometime we can access the request url
        for i in result_sheet_ocp:
            if i.similarity == None:
                i.similarity = float('-inf')

        result_sheet_ocp.sort(key=operator.attrgetter('similarity'))
        find_best = False
        for i in range(int(len(result_sheet_ocp))-1, -1, -1):
            if (result_sheet_ocp[i].similarity >= 700) and (-30 < result_sheet_ocp[i].rt_diff < 30):
                    result_sheet_analyze_num.append(result_sheet_ocp[i].anaylze_index)
                    result_category.append(result_sheet_ocp[i].category)
                    result_sheet_name.append(result_sheet_ocp[i].name)
                    result_sheet_sim.append(result_sheet_ocp[i].similarity)
                    result_sheet_diff.append(result_sheet_ocp[i].rt_diff)
                    result_RI.append(result_sheet_ocp[i].rt)
                    result_RT.append(cp.rt)
                    result_mass.append(cp.quant_m)
                    result_ori_name.append(cp.name)
                    find_best = True
                    break
        if not find_best:
            result_sheet_analyze_num.append(cp.analy_index)
            result_RI.append("Unknown")
            result_category.append("Unknown")
            result_sheet_name.append("Unknown")
            result_sheet_sim.append("Unknown")
            result_sheet_diff.append("Unknown")
            result_RT.append("Unknown")
            result_mass.append("Unknown")
            result_ori_name.append(cp.name)

        printProgressBar(j, len(del_data), ' Processing '+str(j+1) +' over '+str(len(del_data)))

    new_wb.save('data/Output.xls')

    # make the output file as xlsx file
    p.save_book_as(file_name='data/Output.xls',
                   dest_file_name='data/Output.xlsx')
    sheet = pd.read_excel("data/Output.xlsx", sheet_name="Sheet1")
    del_sheet = pd.read_excel("data/Output.xlsx", sheet_name="Sheet2")

    # colors used to color the conditional cells
    writer = pd.ExcelWriter('data/Output.xlsx', engine='xlsxwriter')
    sheet.to_excel(writer, sheet_name="Original Data", index=False)
    del_sheet.to_excel(writer, sheet_name="Output Data", index=False)

    # Here is the sheet 3 -> result data sheet
    good_result_data = pd.DataFrame({"analyze index": result_sheet_analyze_num, "Category": result_category, "ori_Name": result_ori_name, "name": result_sheet_name, "RI": result_RI, "R.T.(s)": result_RT, "Quant_mass": result_mass, "similarity": result_sheet_sim, "RT diff": result_sheet_diff})
    good_result_data.to_excel(writer, sheet_name="Best hit data", index=False)

    # Here is the sheet 4 -> calculate the good result rate sheet
    good_result_rate = good_result / total_result
    calculate_good_result_rate = pd.DataFrame({"result": ['good result', 'total data', 'good result rate'], "data": [good_result, total_result, good_result_rate]})
    calculate_good_result_rate.to_excel(writer, sheet_name="Good result rate", index=False)

    workbook = writer.book
    worksheet_2 = writer.sheets['Output Data']

    good_result_data_worksheet = writer.sheets['Best hit data']

    green_format = workbook.add_format({'bg_color': '#C6EFCE',
                                        'font_color': '#006100'})
    red_format = workbook.add_format({'bg_color': '#FFC7CE',
                                      'font_color': '#9C0006'})
    diff_num = GMD_s.get_acc_rt_diff()
    neg_diff_num = 0 - float(diff_num)

    for diff_format_range in diff_format_range_list:
        diff_format_range = diff_format_range + str(len(del_data))
        worksheet_2.conditional_format(diff_format_range, {'type': 'cell',
                                                           'criteria': 'between',
                                                           'minimum': neg_diff_num,
                                                           'maximum': diff_num,
                                                           'format': green_format})

        worksheet_2.conditional_format(diff_format_range, {'type': 'cell',
                                                           'criteria': 'not between',
                                                           'minimum': neg_diff_num,
                                                           'maximum': diff_num,
                                                           'format': red_format})
    sim_num = GMD_s.get_acc_sim()
    for sim_format_range in sim_format_range_list:
        sim_format_range = sim_format_range + str(len(del_data))
        worksheet_2.conditional_format(sim_format_range, {'type': 'cell',
                                                          'criteria': '>',
                                                          'value': sim_num,
                                                          'format': green_format})
        worksheet_2.conditional_format(sim_format_range, {'type': 'cell',
                                                          'criteria': '<=',
                                                          'value': sim_num,
                                                          'format': red_format})
    good_result_data_format_range = "B2:H" + str(len(del_data))
    good_result_data_worksheet.conditional_format(good_result_data_format_range, {'type': 'cell',
                                                                                 'criteria': '!=',
                                                                                 'value': '"Unknown"',
                                                                     'format': green_format})

    writer.save()


main()

