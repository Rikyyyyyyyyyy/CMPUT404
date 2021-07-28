class Compound:
    def __init__(self, analy_index, name, RT, dim1, dim2, cas, area, quant_m, quant_sn, uni_m, sim, rev, specrum):
        self.analy_index = analy_index
        self.name = name
        self.rt = RT
        self.dim_1 = dim1
        self.dim_2 = dim2
        self.cas = cas
        self.area = area
        self.quant_m = quant_m
        self.quant_sn = quant_sn
        self.unique_m = uni_m
        self.similarity = sim
        self.reverse = rev
        self.spectrum = specrum
        self.category = "Unknown"

    def get_analy_index(self):
        return self.analy_index

    def get_name(self):
        return self.name

    def get_rt(self):
        return self.rt

    def get_dim_1(self):
        return self.dim_1

    def get_specrum(self):
        return self.spectrum

    def get_cas(self):
        return self.cas

    def get_sim(self):
        return self.similarity

    def get_rev(self):
        return self.reverse

    def set_category(self, category):
        self.category = category



