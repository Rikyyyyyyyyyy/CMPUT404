import scipy.io as sio
import sim_v2 as sim_calculation
from out_compound_class import out_compound
import operator

def mat_search(exp_rt,GMD,cp):
    mat_Library = sio.loadmat('data/Mainlib.mat')
    library_compound = mat_Library['Compound']
    compound_num = len(library_compound[0])
    selected_compound = []

    for i in range(compound_num):
        if len(library_compound[0, i][10][0]) != 0:
            if library_compound[0, i][10][0, 0]['Phase'][0] == 'SemiStdNP' or library_compound[0, i][10][0, 0]['Phase'][0] =='StdNP':
                if exp_rt-50 < library_compound[0, i][10][0, 0]['Val'][0][0] < exp_rt+50:
                    selected_compound.append(library_compound[0, i])
        elif len(library_compound[0, i][9][0]) != 0:
            if exp_rt-50 < library_compound[0, i][9][0, 0]['Val'][0][0] < exp_rt+50:
                selected_compound.append(library_compound[0, i])

    ocp_list = []
    for i in range(len(selected_compound)):
        name = selected_compound[i][0][0]
        if len(selected_compound[i][10][0]) != 0:
            if selected_compound[i][10][0, 0]['Phase'][0] == 'SemiStdNP' or selected_compound[i][10][0, 0]['Phase'][0] =='StdNP':
                rt = selected_compound[i][10][0, 0]['Val'][0][0]
        elif len(selected_compound[i][9][0]) != 0:
            rt = selected_compound[i][9][0, 0]['Val'][0][0]
        try:
            cas = selected_compound[i][4][0][0]
        except:
            cas = None
        formula = selected_compound[i][1][0]
        MS = selected_compound[i][7][0]
        intensity = selected_compound[i][8][0]
        o_spectrum = ""
        for j in range(len(MS)):
            o_spectrum = o_spectrum + str(MS[j])+","+str(intensity[j])+" "

        sim, rev = sim_calculation.do_cal(o_spectrum, cp.spectrum)
        ocp = out_compound(cp.analy_index, name, rt, cas, sim, rev, formula, o_spectrum)
        ocp_list.append(ocp)
    ocp_list.sort(key=operator.attrgetter('similarity'))
    while ocp_list[-1].similarity == 1000:
        ocp_list.pop()
    return_list = []
    # for c in ocp_list:
    #     print(c.name)
    #     print(c.similarity)
    for i in range(1, int(GMD.hits_range)+1):
        return_list.append(ocp_list[-i])



    return return_list


