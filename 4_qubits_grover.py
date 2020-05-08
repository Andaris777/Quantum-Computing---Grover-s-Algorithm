# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:11:41 2020

@author: Ludovic
"""

from math import pi
from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit.providers.ibmq import least_busy
from qiskit import IBMQ
IBMQ.save_account('ee21a38145df6f33181385a311fef503faacd13a50184ceb5594a846c586ce078cf8fb8f4aa2ff1f93577a38a270f19d9fa381dd5b3a3498293fd37d53f17001')


#number of qubit
nb_qubit = 4
qr = QuantumRegister(4)
qc = QuantumCircuit(qr)
#################################
### Step 1
### Superposition states
#################################

for i in range(0,nb_qubit,1):
    qc.h(i)

#################################
### Step 2
### Oracle
#################################

#Let's define oracle for state |1110>
qc.x(qr[0])
qc.cu1(pi/4, qr[0], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(-pi/4, qr[1], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(pi/4, qr[1], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])
qc.x(qr[0])

#################################
### Step 3
### Reflection
#################################

for i in range(0,nb_qubit,1):
    qc.h(i)
    qc.x(i)

# Do controlled-Z

qc.cu1(pi/4, qr[0], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(-pi/4, qr[1], qr[3])
qc.cx(qr[0], qr[1])
qc.cu1(pi/4, qr[1], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])
qc.cx(qr[1], qr[2])
qc.cu1(-pi/4, qr[2], qr[3])
qc.cx(qr[0], qr[2])
qc.cu1(pi/4, qr[2], qr[3])



for i in range(0,nb_qubit,1):
    qc.x(i)
    qc.h(i)

qc.measure_all()

#ideal quantum environment
simulator = Aer.get_backend('qasm_simulator')
shots = 1
results = execute(qc, backend=simulator, shots=shots).result()
answer = results.get_counts()
plot_histogram(answer)

##################################################################
### Real device
##################################################################

# Load IBM Q account and get the least busy backend device
provider = IBMQ.load_account()
device = least_busy(provider.backends(simulator=False))
print("Running on current least busy device: ", device)

# Run our circuit on the least busy backend. Monitor the execution of the job in the queue
from qiskit.tools.monitor import job_monitor
job = execute(qc, backend=device, shots=1024, max_credits=10)
job_monitor(job, interval = 2)

# Get the results from the computation
results = job.result()
answer = results.get_counts(qc)
plot_histogram(answer)

# ##################################################################
# ### Circuit draw
# ##################################################################

qc.draw(output='mpl', filename="qc.png")