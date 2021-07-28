import scipy.io as sio
import sim_v2 as sim_calculation
from out_compound_class import out_compound
import operator

def mat_search(exp_rt,GMD,cp,library_compound,compound_num):

    ocp_list = []

    for i in range(compound_num):
        name = library_compound[0, i][0][0]
        try:
            cas = library_compound[0, i][4][0][0]
        except:
            cas = None
        formula = library_compound[0, i][1][0]

        if len(library_compound[0, i][10][0]) != 0:
            if library_compound[0, i][10][0, 0]['Phase'][0] == 'SemiStdNP' or library_compound[0, i][10][0, 0]['Phase'][0] =='StdNP':
                rt = library_compound[0, i][10][0, 0]['Val'][0][0]
        elif len(library_compound[0, i][9][0]) != 0:
            rt = library_compound[0, i][9][0, 0]['Val'][0][0]
        else:
            rt = 0
        MS = library_compound[0, i][7][0]
        intensity = library_compound[0, i][8][0]
        o_spectrum = ""
        for j in range(len(MS)):
            o_spectrum = o_spectrum + str(MS[j])+","+str(intensity[j])+" "
        sim, rev = sim_calculation.do_cal(o_spectrum, cp.spectrum)
        ocp = out_compound(cp.analy_index, name, rt, cas, sim, rev, formula, o_spectrum)
        ocp_list.append(ocp)
        print(i)

    ocp_list.sort(key=operator.attrgetter('similarity'))
    while ocp_list[-1].similarity == 1000:
        ocp_list.pop()
    return_list = []
    for i in range(1, int(GMD.hits_range)+1):
        return_list.append(ocp_list[-i])

    return return_list


