from bs4 import BeautifulSoup
import re
from out_compound_class import out_compound
import requests

def GMD_search(ri, GMD, compound_info):
    riwindow = GMD.get_ri_window()
    rt = "VAR5"
    specrum_list = compound_info.get_specrum().split(" ")
    good_peaks = []
    for s in specrum_list:
        if s[-1] != "0":
            good_peaks.append(s)
    specrum = ""
    for g in good_peaks:
        specrum = specrum + g +","

    r = GMD.get_hits_range()

    url = "http://gmd.mpimp-golm.mpg.de/webservices/wsLibrarySearch.asmx/LibrarySearch?ri="+str(ri)+"&riWindow="+str(riwindow)+"&AlkaneRetentionIndexGcColumnComposition="+str(rt)+"&spectrum="+str(specrum)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    td = soup.find_all('spectrumid')

    compounds_list = []
    r = int(r)
    rest_r = 0
    if r > len(td):
        r = len(td)
        rest_r = int(GMD.get_hits_range())-len(td)
    for i in range(r):
        specrum_id = td[i].get_text()
        spec_url = "http://gmd.mpimp-golm.mpg.de/webservices/SpectrumJcampDx.ashx?id=" + str(specrum_id)
        spec_response = requests.get(spec_url)
        spec_html = spec_response.text
        spec_soup = BeautifulSoup(spec_html, "html.parser")
        text_soup = spec_soup.get_text()
        file_lines = text_soup.split("\n")

        name_line = file_lines[0]
        cas_line = file_lines[10]
        ri_line = file_lines[13]
        formula_line = file_lines[11]
        spectrum_lines = file_lines[29:-3]
        name = name_line.split("=")[-1]
        cas_num = cas_line.split("=")[-1]
        ri_num = ri_line.split("=")[-1]
        formula = formula_line.split("=")[-1]
        spectrum_str = ""
        for spec in spectrum_lines:
            new_spec = re.sub('\r', '', spec)
            spectrum_str = spectrum_str + new_spec
        ocp = out_compound(compound_info.analy_index, name, ri_num, cas_num, None, None, formula, spectrum_str)
        compounds_list.append(ocp)
    for i in range(rest_r):
        ocp = out_compound(compound_info.analy_index, "None", "None", "None", "None", "None", "None", "None")
        compounds_list.append(ocp)
    return compounds_list







