from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector, DensityMatrix, state_fidelity, partial_trace
import numpy as np


def prepare_state(qc, qubit, alpha, beta):
    norm = np.sqrt(abs(alpha)**2 + abs(beta)**2)
    alpha, beta = alpha/norm, beta/norm
    qc.initialize([alpha, beta], qubit)


def teleportation_visual(alpha, beta):
    q = QuantumRegister(3, 'q')
    c = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(q, c)

    prepare_state(qc, q[0], alpha, beta)
    qc.barrier()

    qc.h(q[1])
    qc.cx(q[1], q[2])
    qc.barrier()

    qc.cx(q[0], q[1])
    qc.h(q[0])
    qc.barrier()

    qc.measure(q[0], c[0])
    qc.measure(q[1], c[1])
    qc.barrier()

    return qc


def teleportation_unitary(alpha, beta):
    q = QuantumRegister(3, 'q')
    qc = QuantumCircuit(q)

    prepare_state(qc, q[0], alpha, beta)
    qc.h(q[1]); qc.cx(q[1], q[2])
    qc.cx(q[0], q[1]); qc.h(q[0])
    qc.cx(q[1], q[2]); qc.cz(q[0], q[2])
    return qc


def verify(alpha, beta):
    qc = teleportation_unitary(alpha, beta)
    final_state = Statevector.from_instruction(qc)
    rho = DensityMatrix(final_state)
    bob_state = partial_trace(rho, [0, 1])
    target = DensityMatrix([[abs(alpha)**2, alpha*np.conj(beta)],
                            [np.conj(alpha)*beta, abs(beta)**2]])
    return state_fidelity(bob_state, target)


tests = {
    "|0>": (1, 0),
    "|1>": (0, 1),
    "|+>": (1/np.sqrt(2), 1/np.sqrt(2)),
    "|->": (1/np.sqrt(2), -1/np.sqrt(2)),
    "|i+>": (1/np.sqrt(2), 1j/np.sqrt(2)),
}

print("\n--- Testing Teleportation Fidelity ---")
for name, (a, b) in tests.items():
    print(f"{name:4s} | Fidelity = {verify(a, b):.12f}")

phi = 2*np.pi*np.random.rand()
theta = 2*np.arccos(np.sqrt(np.random.rand()))
alpha = np.cos(theta/2)
beta  = np.exp(1j*phi)*np.sin(theta/2)
print("\nRandom State Fidelity =", verify(alpha, beta))

qc_example = teleportation_visual(1/np.sqrt(2), 1/np.sqrt(2))
print("\n--- Teleportation Circuit (Visual — Clean Output) ---")
print(qc_example.draw(output='text'))
