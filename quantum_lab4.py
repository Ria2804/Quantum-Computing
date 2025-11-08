# =============================
# Lab 4: Design of Quantum Circuits
# =============================

from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_state_city, plot_bloch_multivector
import matplotlib.pyplot as plt

# --- Function to simulate a statevector ---
def simulate_state(circuit):
    simulator = Aer.get_backend('aer_simulator_statevector')
    compiled = transpile(circuit, simulator)
    result = simulator.run(compiled).result()
    state = result.get_statevector(compiled)
    print(state)
    plot_state_city(state, title="Statevector Representation")
    plt.show()
    return state

# --- HSHT circuit ---
def hsht_circuit():
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.s(0)
    qc.h(0)
    qc.t(0)
    return qc

print("=== HSHT Operation ===")
qc_hsht = hsht_circuit()
qc_hsht.draw('mpl', filename='hsht_circuit.png')
plt.show()

# --- Input |0> ---
print("\nInput |0> State:")
simulate_state(qc_hsht)

# --- Input |1> ---
print("\nInput |1> State:")
qc1 = QuantumCircuit(1)
qc1.x(0)  # prepares |1>
qc1.compose(qc_hsht, inplace=True)
simulate_state(qc1)

# --- Reversibility Check ---
print("\n=== Checking Reversibility ===")
rev = qc_hsht.compose(qc_hsht.inverse())
simulate_state(rev)
print("Reversibility confirmed if output ≈ [1, 0] (|0⟩ state).")

# --- Bell State Circuit ---
print("\n=== Bell State Circuit ===")
bell = QuantumCircuit(2)
bell.h(0)
bell.cx(0, 1)

bell.draw('mpl', filename='bell_circuit.png')
plt.show()

# Simulate
state = simulate_state(bell)
plot_bloch_multivector(state)
plt.show()

