import pandas as pd


def remove_lines(GMD):
    file_name = r'data/'+str(GMD.get_file_name())
    file_type = file_name.split(".")[-1]
    if file_type == "csv":
        remove_csv(file_name)
    if file_type == "xlsx":
        remove_xlsx(file_name, GMD)


def remove_csv(file_name, GMD):
    pass

def remove_xlsx(file_name, GMD):
    data = pd.read_excel(file_name)
    analy_index_list = []
    for i in data.index:
        analy_index_list.append(i+1)
    try:
        data.insert(0, 'analy index', analy_index_list, allow_duplicates=False)
    except:
        pass

    name_list = data.Name
    name_len = len(name_list)
    del_data = data

    for i in range(name_len):
        if ('siloxane' in name_list[i].lower()) or ('silecane' in name_list[i].lower()):
            del_data = del_data.drop(del_data[del_data.Name == name_list[i]].index)

    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1', index=False)
    del_data.to_excel(writer, sheet_name='Sheet2', index=False)
    writer.save()


