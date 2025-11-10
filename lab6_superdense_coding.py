# Lab 6: Implementation of Superdense Coding (Version Compatible with Older Qiskit)
# We use two-step execution: quantum RNG + superdense coding

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit import transpile

def generate_random_bits():
    # Quantum RNG using Hadamard superposition
    q = QuantumRegister(2, 'q')
    c = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(q, c)

    qc.h(q[0])
    qc.h(q[1])
    qc.measure(q, c)

    sim = AerSimulator()
    result = sim.run(transpile(qc, sim), shots=1).result()
    counts = result.get_counts()

    # Extract bitstring from counts dict
    bitstring = list(counts.keys())[0]  # e.g., '01'
    # Qiskit is little-endian → rightmost is q[0]
    c_bit = int(bitstring[-1])
    d_bit = int(bitstring[-2])

    return c_bit, d_bit


def superdense_encode_and_decode(c, d):
    q = QuantumRegister(2, 'q')
    c_out = ClassicalRegister(2, 'c_out')
    qc = QuantumCircuit(q, c_out)

    # Step 1: Create shared entangled pair (EPR)
    qc.h(q[0])
    qc.cx(q[0], q[1])

    # Step 2: Alice encoding rule
    if c == 1:
        qc.x(q[0])
    if d == 1:
        qc.z(q[0])

    # Step 3: Bob decoding
    qc.cx(q[0], q[1])
    qc.h(q[0])

    # Step 4: Measure
    qc.measure(q, c_out)

    return qc


def run(shots=1024):
    print("Step 1: Generating random bits using quantum randomness...")
    c, d = generate_random_bits()
    print(f"Random bits generated: c = {c}, d = {d}")

    print("\nStep 2: Running superdense coding protocol...\n")
    qc = superdense_encode_and_decode(c, d)

    sim = AerSimulator()
    result = sim.run(transpile(qc, sim), shots=shots).result()
    counts = result.get_counts()

    print(qc.draw(fold=-1))
    print("\nMeasurement Results:", counts)

    expected = f"{d}{c}"
    print(f"\nExpected output state: |{expected}⟩")
    print("✅ Protocol successful if |{}⟩ has the highest count.\n".format(expected))


if __name__ == "__main__":
    run()
