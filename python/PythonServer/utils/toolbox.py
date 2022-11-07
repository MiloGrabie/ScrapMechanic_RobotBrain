import numpy as np


def vectorize(dico):
    return np.array([
        dico.x,
        dico.y,
        dico.z,
    ])