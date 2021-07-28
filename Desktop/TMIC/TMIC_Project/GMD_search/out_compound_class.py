class out_compound:
    def __init__(self, analyze_index, name, RT, cas, sim, rev,formula, specrum):
        self.name = name
        self.rt = RT
        self.cas = cas
        self.similarity = sim
        self.reverse = rev
        self.specrum = specrum
        self.formula = formula
        self.rt_diff = None
        self.anaylze_index = analyze_index
        self.sorted_filled_spectrum = None
        self.category = "Unknown"

    def get_name(self):
        return self.name

    def get_rt(self):
        return self.rt

    def get_cas(self):
        return self.cas

    def get_similarity(self):
        return self.similarity

    def get_reverse(self):
        return self.reverse

    def get_spectrum(self):
        return self.specrum

    def get_formula(self):
        return self.formula

    def set_rt_diff(self, rt_diff):
        self.rt_diff = rt_diff

    def set_category(self, category):
        self.category = category

    def set_sorted_filled_spectrum(self, spectrum):
        self.sorted_filled_spectrum = spectrum


