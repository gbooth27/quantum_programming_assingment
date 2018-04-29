import pyquil.quil as pq
import pyquil.api as api
from pyquil.gates import *
from grove.amplification.grover import Grover



def grovers(n, s):
    """
    generates a pyquil program for grover search
    :param n: number of qubits
    :param s: number to search for (0 <= s <= 2^(n)-1)
    :return: quantum program
    """

    # Construct a Bell State program.
    grover = pq.Program()
    grover_r = Grover()



