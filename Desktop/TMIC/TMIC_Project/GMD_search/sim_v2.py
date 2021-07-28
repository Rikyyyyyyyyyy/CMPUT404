import numpy as np
import sys
from matchms import calculate_scores, Scores, Spectrum
from sklearn.metrics.pairwise import cosine_similarity
import scipy.spatial as sp
from matchms.similarity import CosineGreedy
from matchms.similarity import IntersectMz



def do_cal(o_spectrum, l_spectrum):
    # get the observation matrix
    o_spectrum_list = o_spectrum.split(" ")
    hash_o = [0]*10000
    hash_l = [0]*10000
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
    rev_l = l_matrix.copy()
    rev_o = o_matrix.copy()

    for i in l_matrix:
        hash_l[i[0]] = i[1]
    for i in o_matrix:
        hash_o[i[0]] = i[1]

    ## similarity
    for i in l_matrix:
        if hash_o[i[0]] != 0 and i[1] == 0:
            for j in o_matrix:
                if j[0] == i[0]:
                    j[1] = 0

    ## observation
    for i in rev_o:
        if hash_l[i[0]] != 0 and i[1] == 0:
            for j in rev_l:
                if j[0] == i[0]:
                    j[1] = 0





# ####### for similarity
#     for i in range(len(l_matrix)):
#         for j in range(len(o_matrix)):
#             if l_matrix[i][0] == o_matrix[j][0]:
#                 if l_matrix[i][1] == 0 and o_matrix[j][1] != 0:
#                     o_matrix[j][1] = 0
#
# ####### for reverse
#     for i in range(len(rev_l)):
#         for j in range(len(rev_o)):
#             if rev_l[i][0] == rev_o[j][0]:
#                 if rev_o[j][1] == 0 and rev_l[i][1] != 0:
#                     rev_l[i][1] = 0


    ####################### TEMP
    ob_mz =[]
    ob_in = []
    li_mz = []
    li_in = []
    for i in l_matrix:
        li_mz.append(float(i[0]))
        li_in.append(float(i[1]))
    for i in o_matrix:
        ob_mz.append(float(i[0]))
        ob_in.append(float(i[1]))
    rev_ob_mz = []
    rev_ob_in = []
    rev_li_mz = []
    rev_li_in = []
    for i in rev_l:
        rev_li_mz.append(float(i[0]))
        rev_li_in.append(float(i[1]))
    for i in rev_o:
        rev_ob_mz.append(float(i[0]))
        rev_ob_in.append(float(i[1]))


    spectrum_ob = Spectrum(mz=np.array(ob_mz), intensities=np.array(ob_in))
    spectrum_li = Spectrum(mz=np.array(li_mz), intensities=np.array(li_in))

    rev_spectrum_ob = Spectrum(mz=np.array(rev_ob_mz), intensities=np.array(rev_ob_in))
    rev_spectrum_li = Spectrum(mz=np.array(rev_li_mz), intensities=np.array(rev_li_in))

    cosine_greedy = CosineGreedy(tolerance=0.2)
    try:
        rev_score = cosine_greedy.pair(rev_spectrum_li, rev_spectrum_ob)
        rev_score = rev_score['score']
    except:
        rev_score = -1

    try:
        score = cosine_greedy.pair(spectrum_ob, spectrum_li)
        score = score['score']
    except:
        score = -1
    return score*1000, rev_score*1000
    ####################### TEMP

    # l_min = l_matrix[0][0]
    # l_max = l_matrix[-1][0]

    # calculate the range of the valid matrix
#     if o_min <= l_min:
#         min_max = l_min
#     else:
#         min_max = o_min
#
#     if l_max <= o_max:
#         max_min = l_max
#     else:
#         max_min = o_max
#
#     # fill in the 0 for both of observation and library matrix in range (min_max,max_min)
#     del_o_range = []
#     for z in range(len(o_matrix)):
#         if o_matrix[z][0] < min_max:
#             del_o_range.append(z)
#         if o_matrix[z][0] > max_min:
#             del_o_range.append(z)
#     o_matrix = np.delete(o_matrix, del_o_range, 0)
#
#     del_l_range = []
#     for z in range(len(l_matrix)):
#         if l_matrix[z][0] < min_max:
#             del_l_range.append(z)
#         if l_matrix[z][0] > max_min:
#             del_l_range.append(z)
#     l_matrix = np.delete(l_matrix, del_l_range, 0)
#     # apoend minmax in to the small list
#     if len(o_matrix) == 0 or len(l_matrix) == 0:
#         return -9999, -9999
#     if o_matrix[-1][0] < max_min:
#         o_matrix = np.append(o_matrix, np.array([[max_min, 0]]), 0)
#     elif l_matrix[-1][0] < min_max:
#         l_matrix = np.append(l_matrix, np.array([[max_min, 0]]), 0)
#     else:
#         pass
#
#     # fill in 0 in both observation matrix and library matrix
#     o_matrix_0_fill = []
#     o_index = min_max
#     for matrix in o_matrix:
#         if o_index <= max_min:
#             while matrix[0] != o_index:
#                 o_matrix_0_fill.append([o_index, 0])
#                 o_index = o_index+1
#             o_index = o_index + 1
#     if len(o_matrix_0_fill) != 0:
#         o_matrix = np.append(o_matrix, np.array(o_matrix_0_fill), 0)
#     o_matrix = o_matrix[np.argsort(o_matrix[:, 0])]
#
#     l_matrix_0_fill = []
#     l_index = min_max
#     for matrix in l_matrix:
#         if l_index <= max_min:
#             while matrix[0] != l_index:
#                 l_matrix_0_fill.append([l_index, 0])
#                 l_index = l_index + 1
#             l_index = l_index + 1
#     if len(l_matrix_0_fill) != 0:
#         l_matrix = np.append(l_matrix, np.array(l_matrix_0_fill), 0)
#     l_matrix = l_matrix[np.argsort(l_matrix[:, 0])]
#
#     # 0 out masses with bundance of under %5 of the base peak -- Library
#     l_matrix_max = l_matrix[np.argsort(l_matrix[:, 1])]
#     l_max_col = l_matrix_max[-1][1]
#     for i in l_matrix:
#         if i[1] < 0.01*l_max_col:
#             i[1] = 0
#     sim = cal_sim(o_matrix, l_matrix)
#     rev = cal_rev(o_matrix, l_matrix)
#
#     np.set_printoptions(threshold=sys.maxsize)
#     # print(rev)
#     return sim, rev
#
#
# def cal_sim(ob, li):
#     # for i in range(len(ob)):
#     #     if li[i][1] != 0 and ob[i][1] == 0:
#     #         ob[i][1] = 0
#     ob_col = []
#     ob_mz = []
#     ob_in = []
#     for i in ob:
#         ob_mz.append(float(i[0]))
#         ob_in.append(float(i[1]))
#     li_col = []
#     li_mz = []
#     li_in = []
#     for i in li:
#         li_mz.append(float(i[0]))
#         li_in.append(float(i[1]))
#     spectrum_ob = Spectrum(mz=np.array(ob_mz), intensities=np.array(ob_in))
#     spectrum_li = Spectrum(mz=np.array(li_mz), intensities=np.array(li_in))
#     cosine_greedy = CosineGreedy(tolerance=0.2)
#
#     score = cosine_greedy.pair(spectrum_ob, spectrum_li)
#
#     cos_sim2 = np.dot(li.transpose(), ob) / (np.linalg.norm(li) * np.linalg.norm(ob))
#     cos_sim = np.dot(li_col, ob_col) / (np.linalg.norm(li_col) * np.linalg.norm(ob_col))
#     p_corr = np.corrcoef(li_col, ob_col)
#
#     return score['score']
#
#     # print(cos_lib)
#
# def cal_rev(ob, li):
#     for i in range(len(ob)):
#         if li[i][1] != 0 and ob[i][1] ==0:
#             ob[i][1] = 0
#
#     ob_col = []
#     for i in ob:
#         ob_col.append(i[1])
#     li_col = []
#     for i in li:
#         li_col.append(i[1])
#
#     cos_sim = np.dot(ob_col, li_col) / (np.linalg.norm(ob_col) * np.linalg.norm(li_col))
#     return cos_sim

