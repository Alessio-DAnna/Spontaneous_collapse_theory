'''This module contains utile functions that implement the spontaneous collapse model.
This module is part of the module "spontaneous_collapse_model.py" '''

from qiskit.quantum_info import SparsePauliOp

import numpy as np



def timesteps_collapse_array(num_timesteps, time, lam):
    '''This function returns an array containing the timesteps indeces (for the trotterization evolution defined in the module
    "spontaneous_collapse_model) at which the spontaneous collapse occurs.
    The indeces are sampled according to a Poisson distribution.'''
    
    #Extract a Poisson-distributed array elements
    poisson_indeces = np.random.poisson(lam=lam, size = int(np.round(num_timesteps/lam)))

    #Verify that the sum of the elements does not exceed num_timesteps, otherwise define the required vector
    if sum(poisson_indeces) >= num_timesteps:
        return timesteps_collapse_array(num_timesteps, time, lam)
    else:
        timesteps_collapse_array = []
        for i in range(len(poisson_indeces)):
            if i == 0:
                timesteps_collapse_array.append(poisson_indeces[0])
            else:
                timesteps_collapse_array.append(timesteps_collapse_array[-1] + poisson_indeces[i])
        return timesteps_collapse_array



def obs_array(num_particles):
    '''E.g. 4 particles -> obs_array = [1/2*ZIII, 1/2*IZII, 1/2*IIZI, 1/2*IIIZ]'''
    obs_array = []
    for i in range(num_particles):
        ids_before = "I"*i
        ob = "Z"
        ids_after = "I"*(num_particles-i-1)
        ob_construction = ids_before + ob + ids_after
        obs_array.append(SparsePauliOp(data=ob_construction, coeffs=0.5))
    
    return obs_array



def collapse():
    pass
