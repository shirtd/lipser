import numpy.linalg as la
import numpy as np

import scipy.fftpack
import scipy


def ripple(t, f=1, l=1, d=1, w=1, s=1):
    t = w * (t + s)
    return np.exp(-t / l) * np.cos(2*np.pi*f**(1/d)*t)

def ripple_grid(x, y, f=1, l=1, d=1, w=1, s=1):
    return ripple(la.norm(np.stack((x, y), axis=2), axis=2), f, l, d, w, s)

def get_ripple(x, y, f=1, l=1, d=1, w=1, s=1, exp=-3, noise=False, scale=False):
    f = ripple_grid(x, y, f, l, d, w, s)
    if noise:
        f *= (1 + grf(exp, x.shape[0]*x.shape[1]))
    return (f - f.min()) / (f.max() - f.min()) if scale else f

def get_circle(x, y, n=128, r=[0.2, 1.], c=[[0,0],[0,0]]):
    xy = np.stack((x,y), axis=2)
    t = np.linspace(0, 2*np.pi, n)
    z = np.vstack([np.vstack((rr*np.sin(t), rr*np.cos(t))).T + np.array(cc) for rr,cc in zip(r,c)])
    return np.array([[la.norm(z - xy[i,j], axis=1).min() for j in range(xy.shape[1])] for i in range(xy.shape[0])])


def gaussian(X, Y, c=[0., 0.], s=[0.5, 0.5]):
    return np.exp(-((X-c[0])**2 / (2*s[0]**2) + (Y-c[1])**2 / (2*s[1]**2)))

def make_gaussian(X, Y, args):
    return sum(w*gaussian(X, Y, c, r) for w, c, r in args)

def gaussian_random_field(alpha=-3.0, m=128, normalize=True):
    size = int(np.sqrt(m))
    k_ind = np.mgrid[:size, :size] - int((size + 1) / 2)
    k_idx = sp.fftpack.fftshift(k_ind)
    # Defines the amplitude as a power law 1/|k|^(alpha/2)
    amplitude = np.power(k_idx[0] ** 2 + k_idx[1] ** 2 + 1e-10, alpha / 4.0)
    amplitude[0,0] = 0
    # Draws a complex gaussian random noise with normal (circular) distribution
    noise = np.random.normal(size = (size, size)) + 1j * np.random.normal(size = (size, size))
    G = np.fft.ifft2(noise * amplitude).real # To real space
    return util.stats.scale(G) if normalize else G


mk_gauss = make_gaussian
grf = gaussian_random_field
