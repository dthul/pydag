# pydag

This is a minimal proof-of-concept implementation of a directed acyclic graph
(DAG) that can be used to model and execute modular computations.

Each computation step is represented as a node with inputs and outputs that can
be connected to other nodes. Only when an output is actually accessed the
needed computations will be executed lazily.

Take a look at `example.py` for a usage example.
