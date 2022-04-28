import numpy as np



class MenaceSetup:
    def __init__(self, board_states):
        self.board_states =board_states
        self.num_of_beads = self.init_beads()
        
            

    def init_beads(self):
        beads = {}
        zero_count = max(self.board_states.count('0')-1,2)
        for indx, state_ in enumerate(self.board_states):
            if state_ == '0':
                beads[indx] = zero_count
        return beads

    def set_num_beads(self, key, rewarded_beads):
        self.num_of_beads[key] += rewarded_beads

    def get_num_beads(self):
        random_bead = np.random.rand(1)
        val = np.array(list(self.num_of_beads.values()))
        keys_ = np.array(list(self.num_of_beads.keys()))
        if np.sum(val) == 0:
            val = np.ones(val.shape[0])
        val = val/np.sum(val)

        prob_ = 0
        for indx, i in enumerate(val):
            prob_ += i
            if random_bead < prob_:
                return keys_[indx]

