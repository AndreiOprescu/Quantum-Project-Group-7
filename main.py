import matplotlib.pyplot as plt
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, EstimatorOptions
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Setup Service
service = QiskitRuntimeService()
backend = service.least_busy(simulator=False, operational=True)

# Define the Experiment Parameters
depths = [1, 3, 5]
results_data = []

# Configure ZNE Options (Resilience Level 2)
options = EstimatorOptions()
options.resilience_level = 2
options.resilience.zne_mitigation = True
options.resilience.zne.extrapolator = "polynomial_degree_2"
options.resilience.zne.noise_factors = [1, 3, 5]

# See the error created by different sized circuits
for d in depths:
    # Create circuit
    circuit = RealAmplitudes(num_qubits=2, reps=d)
    observable = SparsePauliOp.from_list([("ZZ", 1.0)])

    # Transpile
    pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
    isa_circuit = pm.run(circuit)
    isa_observable = observable.apply_layout(isa_circuit.layout)

    # Run the circuit with the Estimator class
    estimator = EstimatorV2(mode=backend, options=options)
    job = estimator.run([(isa_circuit, isa_observable, [0.1] * circuit.num_parameters)])

    print(f"Running Depth {d}, Job ID: {job.job_id()}")
    results_data.append(job.result()[0].data.evs)

# Print out the results
for d, val in zip(depths, results_data):
    print(f"Depth (Reps) {d}: Mitigated Expectation Value = {val}")