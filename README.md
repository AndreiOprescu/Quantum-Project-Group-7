# Read Please!

In the "main.py" script, add the following lines to connect to the IBM runtime hardware with your own token. Put them just below the import statements:

```
QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform", 
    token="YOUR_IBM_QUANTUM_API_KEY",
    overwrite=True  
)
```
