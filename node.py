# An input/output socket that (eventually) carries a value
class IOput(object):
    def __init__(self, node):
        # `node` is the node that owns this output.
        # For all other nodes this IOput is an input.
        self._node = node
        self._valid = False
        self._value = None
        self._computation_running = False

    def _ensure_value(self):
        if self._valid is True:
            # Nothing to do
            return

        if self._computation_running is True:
            # This IOput's value is being computed at the moment but someone
            # tries to access it already -> there must be a cyclic dependency somewhere
            raise RuntimeError('Cycle detected')

        try:
            self._computation_running = True
            self._node.compute()
        finally:
            self._computation_running = False

        if self._valid is False:
            raise RuntimeError('Output value is invalid even after node computation has finished. Make sure that all outputs are set when a node is computed.')

    # This function must only be called from the owning node.
    # To reflect this, the caller must pass itself as an argument.
    def set_value(self, caller, value):
        if caller != self._node:
            raise RuntimeError('The caller must be the owning node')
        self._value = value
        self._valid = True

    @property
    def value(self):
        self._ensure_value()
        return self._value


# Acts like a dict that only accepts pre-defined keys and the values must be IOputs
class Inputs(object):
    def __init__(self, *input_names):
        # Check that all input names are strings
        for input_name in input_names:
            if not isinstance(input_name, str):
                raise TypeError
        # Initially all input are set to None
        self._inputs = {input_name: None for input_name in input_names}

    def __setitem__(self, key, value):
        # Don't accept unknown keys
        if key not in self._inputs:
            raise KeyError
        # An input can only be set to an IOput or None
        if value is not None and not isinstance(value, IOput):
            raise TypeError
        self._inputs[key] = value

    def __getitem__(self, key):
        return self._inputs[key]

    def values(self):
        return self._inputs.values()


# Acts like a dict that has a fixed set of keys and its values are IOputs
class Outputs(object):
    def __init__(self, **kwargs):
        for v in kwargs.values():
            if not isinstance(v, IOput):
                raise TypeError
        self._outputs = kwargs

    def __getitem__(self, key):
        return self._outputs[key]


class Node(object):
    _inputs = ()
    _outputs = ()

    def __init__(self):
        self._inputs = Inputs(*self._inputs)
        ioputs = {output_name: IOput(self) for output_name in self._outputs}
        self._outputs = Outputs(**ioputs)

    # Subclasses must set the value of all their outputs when this method is called
    def compute(self):
        pass

    # Read-only `inputs` property
    @property
    def inputs(self):
        return self._inputs

    # Read-only `outputs` property
    @property
    def outputs(self):
        return self._outputs
