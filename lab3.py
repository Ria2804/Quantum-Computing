import streamlit as st
from qiskit.quantum_info import Statevector, Operator
import numpy as np

# --- App Configuration ---
st.set_page_config(
    page_title="Quantum State Simulator",
    layout="wide"
)

st.title("🔬 Quantum Computing Lab: Interactive Simulation")
st.write(
    "This app demonstrates the concepts from your lab manual: tensor products, "
    "operator evolution, and partial measurement."
)

# --- All quantum calculations are defined here ---

# Define initial states
plus_state = Statevector.from_label('+')
i_state = Statevector([1/np.sqrt(2), 1j/np.sqrt(2)])

# Part 1: Tensor Product
psi = plus_state.tensor(i_state)

# Part 2: Operator Evolution
CX_gate = Operator([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])
evolved_psi = psi.evolve(CX_gate)


# --- UI Layout ---

# Use st.latex() to render the mathematical notation beautifully
st.header("Part 1: Tensor Product of State Vectors")
with st.expander("Show Details", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("First state vector:")
        st.latex(r"|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)")
    with col2:
        st.write("Second state vector:")
        st.latex(r"|i\rangle = \frac{1}{\sqrt{2}}(|0\rangle + i|1\rangle)")
    with col3:
        st.write("Resulting tensor product $|ψ⟩ = |+⟩ ⊗ |i⟩$:")
        # Use .draw('latex_source') to get a string that st.latex can render
        st.latex(psi.draw('latex_source'))

st.markdown("---")

st.header("Part 2: Operator Evolution")
with st.expander("Show Details", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.write("Applying the CNOT (CX) Operator:")
        st.latex(CX_gate.draw('latex_source'))
    with col2:
        st.write("State after evolution $CX |ψ⟩$:")
        st.latex(evolved_psi.draw('latex_source'))

st.markdown("---")

st.header("Part 3: Interactive Partial Measurement")
st.write(
    "Here we measure only the first qubit (index 0) of the evolved state. "
    "Click the button multiple times to see different probabilistic outcomes."
)

# Create a button to trigger the measurement
if st.button("Simulate Measurement of Qubit 0", key="measure_button"):
    # Perform the measurement
    result, new_sv = evolved_psi.measure([0])

    st.success(f"**Measured Outcome: `{result}`**")

    st.write("After measurement, the state collapses to:")
    st.latex(new_sv.draw('latex_source'))
else:
    st.info("Click the button above to simulate a measurement.")