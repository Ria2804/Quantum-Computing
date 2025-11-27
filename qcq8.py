from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

## 1. Implement the Query Gate (deutsch_function)

def deutsch_function(case: int):
    """Generate a valid Deutsch function as a QuantumCircuit (Query Gate)."""
    if case not in [1, 2, 3, 4]:
        raise ValueError("`case` must be 1, 2, 3, or 4.") # [cite: 80, 81]
    
    # Creates a two-qubit circuit (q0: input, q1: output/ancilla) [cite: 82]
    f = QuantumCircuit(2)
    
    # Constant functions: f1(x)=0, f4(x)=1. Balanced functions: f2(x)=x, f3(x)=not x.
    
    if case in [2, 3]: # Implements the f(x)=x or f(x)=not x behavior
        # Applies a CNOT (cx) gate where q0 (index 0) is the control and q1 (index 1) is the target.
        # The manual shows 'cx(0,1)', although it has a typo showing 'cx(8,1)' in the source[cite: 84].
        f.cx(0, 1) # [cite: 83, 84]
    if case in [3, 4]: # Flips the output (q1) for f3 and f4
        # Applies an X gate to the output qubit (q1, index 1). [cite: 85, 86]
        f.x(1) 
    
    return f # [cite: 87]

## 2. Compile the Full Deutsch Circuit (compile_circuit)

def compile_circuit(function: QuantumCircuit):
    """Compiles a circuit for use in Deutsch's algorithm."""
    # Based on the manual's example for one bit to one bit, n=1 (input qubit),
    # so the full circuit is n+1=2 qubits and n=1 classical bit.
    n = function.num_qubits - 1 
    
    # Creates the full circuit with n+1 qubits and n classical bits. [cite: 102]
    qc = QuantumCircuit(n + 1, n)
    
    # Initialization of the output qubit (q1, index n) to |-> state: X gate... [cite: 103]
    qc.x(n) 
    # ...followed by Hadamard gates on all qubits. [cite: 104]
    qc.h(range(n + 1)) 
    
    # Barrier for visual separation [cite: 105]
    qc.barrier()
    
    # Plug in the query gate (function) [cite: 106]
    qc.compose(function, inplace=True)
    
    # Barrier for visual separation [cite: 107]
    qc.barrier()
    
    # Final Hadamard gates on the input qubit(s) (q0, range(n)) [cite: 108]
    qc.h(range(n))
    
    # Measurement of the input qubit(s) (q0) into the classical register. [cite: 109]
    qc.measure(range(n), range(n))
    
    return qc # [cite: 110]

## 3. Run the Algorithm and Determine Result (deutsch_algorithm)

def deutsch_algorithm(function: QuantumCircuit):
    """Determine if a Deutsch function is constant or balanced."""
    # Compile the full circuit [cite: 130]
    qc = compile_circuit(function) 
    
    # Run the circuit once on an Aer simulator and get the memory (measurement result). [cite: 131]
    result = AerSimulator().run(qc, shots=1, memory=True).result()
    measurements = result.get_memory() # [cite: 132]
    
    # If the measurement of q0 is '0', the function is constant. [cite: 133, 134]
    if measurements[0] == "0":
        return "constant"
    # If the measurement of q0 is '1', the function is balanced. [cite: 135]
    return "balanced"

# Execution: Plug in the circuit for case=3 and display
f = deutsch_function(3) # [cite: 138]
print(f"Query Gate (Case 3):")
print(f.draw(output='text', fold=-1))
print("\nDeutsch's Algorithm Result:")
# Display the result (should be 'balanced' for case 3: f(x)=not x) [cite: 140, 146]
print(deutsch_algorithm(f)) 

# The compiled circuit for case 3 (for visualization)
compiled_f_3 = compile_circuit(f)
print("\nFull Compiled Circuit (Case 3):")
print(compiled_f_3.draw(output='text', fold=-1))