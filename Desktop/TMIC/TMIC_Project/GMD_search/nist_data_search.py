import scipy.io as sio


def mat_search_name(key_word):
    mat_Library = sio.loadmat('data/Mainlib.mat')
    library_compound = mat_Library['Compound']
    compound_num = len(library_compound[0])
    selected_compound_name = []
    num_word_found = 0

    for i in range(compound_num):
        if key_word.lower() in library_compound[0, i][0][0].lower():
            if len(library_compound[0, i][10][0]) != 0:
                if library_compound[0, i][10][0, 0]['Phase'][0] == 'SemiStdNP' or \
                        library_compound[0, i][10][0, 0]['Phase'][0] == 'StdNP':
                    selected_compound_name.append([library_compound[0, i][0][0], library_compound[0, i][10][0, 0]['Val'][0][0]])
            elif len(library_compound[0, i][9][0]) != 0:
                selected_compound_name.append([library_compound[0, i][0][0],
                                              library_compound[0, i][9][0, 0]['Val'][0][0]])

            num_word_found = num_word_found+1
    return selected_compound_name

def mat_search_mass(mass):
    mat_Library = sio.loadmat('data/Mainlib.mat')
    library_compound = mat_Library['Compound']
    compound_num = len(library_compound[0])
    selected_compound_name = []
    num_word_found = 0

    for i in range(compound_num):
        if mass == int(library_compound[0, i][3][0]):
            selected_compound_name.append([library_compound[0, i][0][0]])
    return selected_compound_name

def main():
    ins = input("how would you like the search? 1.Name 2.Mass: ")

    if ins == "1":
        kw = input("give me a keyword: ")
        lists = mat_search_name(kw)
        for i in lists:
            print(i)
    if ins == "2":
        mass = input("Please give me the mass: ")
        lists = mat_search_mass(int(mass))
        for i in lists:
            print(i)

main()