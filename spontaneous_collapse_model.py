'''Time evolution class'''

'''This class implement the dynamical evolution of a system composed of n particles (all spin 1/2 particles)
by a defined hamiltonian and shows the expectation values of the operator 1/2*Z (i.e. the spin) at each timestep
of the evolution.'''

'''If set, the class implement also the spontaneus collapse model.'''

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector, SparsePauliOp, Pauli
from qiskit_algorithms import TimeEvolutionProblem
from qiskit_algorithms.time_evolvers.trotterization import TrotterQRTE
from qiskit.primitives import Estimator

import utils_spont_collapse



class Spin_onehalf_evolution:

    def __init__(self, num_particles, hamiltonian, time, timesteps, lam = None, initial_state = None, sp_collapse = True):
        self.num_particles = num_particles
        self.hamiltonian = hamiltonian
        self.time = time
        self.timesteps = timesteps
        self.lam = lam
        self.initial_state = initial_state
        self.sp_collapse = sp_collapse
        self.estimator = Estimator()  #Estimator that evaluates the expectation values of the observable

    def _first_state(self):
        '''Call this function if we are at t=0, i.e. the evolution starts'''
        qreg = QuantumRegister(size = self.num_particles)
        qcir = QuantumCircuit(qreg)
        return qcir

    def _evolution_problem_init (self):
        '''Define the observable/observables'''
        if self.num_particles == 1:
            obs = list(SparsePauliOp(data = ['Z'], coeffs = [0.5]))
        else:
            obs = utils_spont_collapse.obs_array(num_particles = self.num_particles)


        '''If spontaneous collapse is implemented, define the timesteps_collapse_array for every particle'''
        collapse_times = None  #In case self.sp_collapse = False
        if self.sp_collapse:
            if self.num_particles == 1:
                collapses = utils_spont_collapse.timesteps_collapse_array(
                    num_timesteps=self.timesteps,
                    time=self.time,
                    lam=self.lam
                    )
                collapse_times = [collapses]
            else:
                if self.num_particles <= 0: 
                    raise ValueError(f"num_particles must be an integer greater than 0, but {self.num_particles} provided")
                collapses = []
                for _ in range(self.num_particles):
                    i_collapses = utils_spont_collapse.timesteps_collapse_array(
                        num_timesteps=self.timesteps,
                        time=self.time,
                        lam=self.lam
                    )
                    collapses.append(i_collapses)
                collapse_times = collapses
        
        return obs, collapse_times

    def evolution(self, obs, collapse_times):
        '''Set the initial state'''
        if self.initial_state == None:
            self.initial_state = self._first_state()  #Circuit
        else:
            if not isinstance(self.initial_state, (Statevector, QuantumCircuit)):
                raise ValueError(f"state_in must be Statevector | QuantumCircuit, but {type(self.state_in)} provided")

        '''Define the problem'''
        problem = TimeEvolutionProblem(
        hamiltonian = self.hamiltonian, 
        time = self.time,
        initial_state = self.initial_state,
        aux_operators = obs)

        '''Evolution'''
        trotter_evolution = TrotterQRTE(estimator = self.estimator, num_timesteps = self.timesteps).evolve(evolution_problem = problem)

        '''Get all the expectation values evaluated during the evolution'''
        if self.num_particles == 1:
            obs_values = np.array(trotter_evolution.observables)[:,:,0][:,0]
        else:
            pass

        self._visualization(obs_values)


    def _visualization(self, obs_values):
        '''Plot the expectation values evolution during time'''
        timesteps_vector = np.linspace(0, self.time, num = self.timesteps + 1)
        #obs_values = self.evolution()


        if self.num_particles == 1:
            fig = plt.figure(figsize = (8,6))
            plt.plot(timesteps_vector, obs_values, 'o-')
        else:
            pass

