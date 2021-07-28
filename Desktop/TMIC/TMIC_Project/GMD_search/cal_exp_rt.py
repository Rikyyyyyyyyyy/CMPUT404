import pandas as pd


def cal_rt(search_info, compound_info):
    compare_file_name = r'data/' + str(search_info.get_compare_data_file())
    file_type = compare_file_name.split(".")[-1]
    if file_type == "csv":
        return( csv_cal(compare_file_name, compound_info))
    if file_type == "xlsx":
        return( xlsx_cal(compare_file_name, compound_info))


def csv_cal(compare_file_name, compound_info):
    pass


def xlsx_cal(compare_file_name, compound_info):
    compare_data = pd.read_excel(compare_file_name)
    compare_n = len(compare_data)
    ri = float(compound_info.get_dim_1())
    for z in compare_data.index:
        if z + 1 < compare_n:
            if ri > float(compare_data['1st R.T.(s)'][z]) and ri < float(compare_data['1st R.T.(s)'][z + 1]):
                rz = compare_data['1st R.T.(s)'][z]
                num_z = compare_data['Carbon #'][z]
                rz_1 = compare_data['1st R.T.(s)'][z + 1]
                exp_ri = 100 * ((ri - rz) / (rz_1 - rz) + num_z)
                return exp_ri

