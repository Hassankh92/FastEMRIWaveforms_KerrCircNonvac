import numpy as np

try:
    import cupy as xp

except ImportError:
    import numpy as xp

from flux import RunFluxInspiral
from amplitude import Amplitude


class FEW:
    def __init__(self, inspiral_kwargs={}):
        """
        Carrier class for FEW
        """
        self.inspiral_gen = RunFluxInspiral()
        self.inspiral_kwargs = inspiral_kwargs

        self.amplitude_gen = Amplitude()

    def __call__(self, M, mu, p0, e0, theta, phi):

        # get trajectory
        (t, p, e, Phi_phi, Phi_r) = self.inspiral_gen(
            M, mu, p0, e0, **self.inspiral_kwargs
        )

        # convert for gpu
        p = xp.asarray(p)
        e = xp.asarray(e)
        Phi_phi = xp.asarray(Phi_phi)
        Phi_r = xp.asarray(Phi_r)

        # amplitudes
        self.amplitude_gen(p, e)

        return


if __name__ == "__main__":
    import time

    few = FEW()
    M = 1e6
    mu = 1e1
    p0 = 10.0
    e0 = 0.3
    theta = np.pi / 3.0
    phi = np.pi / 4.0

    check = few(M, mu, p0, e0, theta, phi)
    num = 1000

    st = time.perf_counter()
    for _ in range(num):
        check = few(M, mu, p0, e0, theta, phi)
    et = time.perf_counter()

    print((et - st) / num)
