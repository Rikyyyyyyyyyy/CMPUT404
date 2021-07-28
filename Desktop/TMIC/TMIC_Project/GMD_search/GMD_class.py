class GS:
    def __init__(self, file_name, compare_file_name, ri_window, hits_range, alkane_ri, rt_diff, acc_sim):
        self.file_name = file_name
        self.compare_file_name = compare_file_name
        self.ri_window = ri_window
        self.hits_range = hits_range
        self.alkane_ri = alkane_ri
        self.acceptable_rt_diff = rt_diff
        self.acceptable_sim = acc_sim

    def get_compare_data_file(self):
        return self.compare_file_name

    def get_file_name(self):
        return self.file_name

    def get_ri_window(self):
        return self.ri_window

    def get_hits_range(self):
        return self.hits_range

    def get_alkane_ri(self):
        return self.alkane_ri

    def get_acc_rt_diff(self):
        return self.acceptable_rt_diff

    def get_acc_sim(self):
        return self.acceptable_sim