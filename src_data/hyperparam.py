"""
Simplified HyperParam for troppap repo
"""

class HyperParam:

    def __init__(self):
        
        self.report_often = 2000 # report every that many closures
        self.check_size_often = 500 # test memory left every...
        self.confthr = 0.65

        self.nrtr = 0  # to be updated by Dataset
        self.nrits = 0 # to be updated by Dataset

        self.pend_len_limit = 4098 # 2 to power 12
        # Alternatives considered: 1000, 8192, 16384 = 2 to power 14

        self.genabsupp = 0
        # ~ if self.nrtr < 100:
            # ~ self.genabsupp = 3
        # ~ else:
            # ~ self.genabsupp = 5 # absolute number of transactions
