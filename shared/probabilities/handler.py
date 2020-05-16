from shared.probabilities import probability_table as pt


class Handler(object):
    """Handler class for managing bet probability retrieval"""

    def __init__(self):
        super(Handler, self).__init__()
        self.probs_table = pt.get()
