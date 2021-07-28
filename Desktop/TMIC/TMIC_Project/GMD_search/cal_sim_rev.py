import numpy as np
import sys
import math
from operator import itemgetter
from matchms.filtering import normalize_intensities


def do_cal(o_spectrum, l_spectrum):
    # get the observation matrix
    o_spectrum_list = o_spectrum.split(" ")
    o_matrix = []
    l_matrix = []
    for o in o_spectrum_list:
        if o != "":
            m = o.split(",")
            int_map = map(int, m)
            int_list = list(int_map)
            o_matrix.append(int_list)
    o_matrix = np.array(o_matrix)
    o_matrix = o_matrix[np.argsort(o_matrix[:, 0])]
    o_min = o_matrix[0][0]
    o_max = o_matrix[-1][0]


    # get the Library matrix
    l_spectrum_list = l_spectrum.split(" ")
    for l in l_spectrum_list:
        if l !="":
            m = l.split(":")
            int_map = map(int, m)
            int_list = list(int_map)
            l_matrix.append(int_list)
    l_matrix = np.array(l_matrix)
    l_matrix = l_matrix[np.argsort(l_matrix[:, 0])]
    l_min = l_matrix[0][0]
    l_max = l_matrix[-1][0]

    # calculate the range of the valid matrix
    if o_min <= l_min:
        min_max = l_min
    else:
        min_max = o_min

    if l_max <= o_max:
        max_min = l_max
    else:
        max_min = o_max

    # fill in the 0 for both of observation and library matrix in range (min_max,max_min)
    del_o_range = []
    for z in range(len(o_matrix)):
        if o_matrix[z][0] < min_max:
            del_o_range.append(z)
        if o_matrix[z][0] > max_min:
            del_o_range.append(z)
    o_matrix = np.delete(o_matrix, del_o_range, 0)

    del_l_range = []
    for z in range(len(l_matrix)):
        if l_matrix[z][0] < min_max:
            del_l_range.append(z)
        if l_matrix[z][0] > max_min:
            del_l_range.append(z)
    l_matrix = np.delete(l_matrix, del_l_range, 0)
    if len(o_matrix) == 0 or len(l_matrix) == 0:
        return -9999,-9999
    # apoend minmax in to the small list
    if o_matrix[-1][0] < max_min:
        o_matrix = np.append(o_matrix, np.array([[max_min, 0]]), 0)
    elif l_matrix[-1][0] < min_max:
        l_matrix = np.append(l_matrix, np.array([[max_min, 0]]), 0)
    else:
        pass

    # fill in 0 in both observation matrix and library matrix
    o_matrix_0_fill = []
    o_index = min_max
    for matrix in o_matrix:
        if o_index <= max_min:
            while matrix[0] != o_index:
                o_matrix_0_fill.append([o_index, 0])
                o_index = o_index+1
            o_index = o_index + 1
    if len(o_matrix_0_fill) != 0:
        o_matrix = np.append(o_matrix, np.array(o_matrix_0_fill), 0)
    o_matrix = o_matrix[np.argsort(o_matrix[:, 0])]

    l_matrix_0_fill = []
    l_index = min_max
    for matrix in l_matrix:
        if l_index <= max_min:
            while matrix[0] != l_index:
                l_matrix_0_fill.append([l_index, 0])
                l_index = l_index + 1
            l_index = l_index + 1
    if len(l_matrix_0_fill) != 0:
        l_matrix = np.append(l_matrix, np.array(l_matrix_0_fill), 0)
    l_matrix = l_matrix[np.argsort(l_matrix[:, 0])]

    # 0 out masses with bundance of under %5 of the base peak -- Library
    l_matrix_max = l_matrix[np.argsort(l_matrix[:, 1])]
    l_max_col = l_matrix_max[-1][1]
    for i in l_matrix:
        if i[1] < 0.05*l_max_col:
            i[1] = 0
    sim = cal_sim(o_matrix, l_matrix)
    rev = cal_rev(o_matrix, l_matrix)
    # rev = 10

    np.set_printoptions(threshold=sys.maxsize)
    # print(rev)
    return sim, rev


def cal_sim(ob, li):
    # for i in range(len(ob)):
    #     if li[i][1] == 0 and ob[i][1] != 0:
    #         ob[i][1] = 0
    ob_col = []
    for i in ob:
        ob_col.append(i[1])
    li_col = []
    for i in li:
        li_col.append(i[1])
    upper = 0
    lower_ob = 0
    lower_li = 0
    for i in range(len(ob)):
        temp = ob_col[i]*li_col[i]
        upper = upper + temp

    for i in range(len(ob)):
        ob_temp_square = ob_col[i]*ob_col[i]
        lower_ob = lower_ob + ob_temp_square
        li_temp_square = li_col[i]*li_col[i]
        lower_li = lower_li + li_temp_square
    tem_ob = lower_ob
    lower_ob = math.sqrt(lower_ob)
    lower_li = math.sqrt(lower_li)
    if lower_ob != 0:
        sim = upper/(lower_ob*lower_li)
        sim = sim*1000
        return sim
    else:
        return -9999


def cal_rev(ob, li):
    for i in range(len(ob)):
        if ob[i][1] == 0 and li[i][1] != 0:
            li[i][1] = 0

    ob_col = []
    for i in ob:
        ob_col.append(i[1])
    li_col = []
    for i in li:
        li_col.append(i[1])
    upper = 0
    lower_ob = 0
    lower_li = 0
    for i in range(len(ob)):
        temp = ob_col[i] * li_col[i]
        upper = upper + temp
    for i in range(len(ob)):
        ob_temp_square = ob_col[i] * ob_col[i]
        lower_ob = lower_ob + ob_temp_square
        li_temp_square = li_col[i] * li_col[i]
        lower_li = lower_li + li_temp_square
    lower_ob = math.sqrt(lower_ob)
    lower_li = math.sqrt(lower_li)
    if lower_ob != 0:
        rev = upper / (lower_ob * lower_li)
        rev = rev * 1000
        return rev
    else:
        return -9999
