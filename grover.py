import pyquil.quil as pq
import pyquil.api as api
from pyquil.gates import *
from grove.amplification.grover import Grover
import numpy as np
from grove.utils.utility_programs import ControlledProgramBuilder
import grove.amplification.oracles as oracle

def grovers(n, s):
    """
    generates a pyquil program for grover search
    :param n: number of qubits
    :param s: number to search for (0 <= s <= 2^(n)-1)
    :return: quantum program
    """

    # Construct program
    grover = pq.Program()
    # set up minus
    grover.inst(X(n))
    grover.inst(H(n))

    # grover_r = Grover()
    for i in range(n):
        grover.inst(H(i))
    # BUILD UF (ONLY WORKS FOR 0 AS OF NOW)
    U_f = np.identity(2**(n+1))
    flip = s
    U_f[flip][flip] = 0
    U_f[2**(n+1)-1][flip] = 1
    U_f[flip][2**(n+1)-1] = 1
    U_f[2**(n+1)-1][2**(n+1)-1] = 0

    grover.defgate('Uf', U_f)

    string = ""
    for i in range (n+1):
        string += " "+str(i)
    string2 = ""
    for i in range(n ):
        string2 += " " + str(i)

    second = -1*np.identity(2 ** (n))
    second[0][0] = 1
    grover.defgate('second', second)

    #for _ in range (int((np.pi *2**(n/2))/4)):
    for _ in range(int(2**(n+2))):


        # apply Uf
        grover.inst('Uf' + string)
        #grover.inst(SWAP(s, n+1))

        for i in range(n):
            grover.inst(H(i))

        grover.inst("second" + string2)

        for i in range(n):
            grover.inst(H(i))
    for i in range(n):
        grover.measure(i)

    return  grover


if __name__ == "__main__":
    qvm = api.SyncConnection()
    for i in range(50):
        p = grovers(6, 0)
        #results = qvm.run(p, classical_addresses=[])
        results = qvm.wavefunction(p)
        print(results)




