from node import Node

class Value(Node):
    _outputs = ('v',)

    def __init__(self, value):
        super().__init__()
        self.outputs['v'].value = value


class Add(Node):
    _inputs = ('v1', 'v2')
    _outputs = ('v',)

    def compute(self):
        super().compute()
        result = self.inputs['v1'].value + self.inputs['v2'].value
        self.outputs['v'].value = result


v1 = Value(5)
v2 = Value(2)
add = Add()
add.inputs['v1'] = v1.outputs['v']
add.inputs['v2'] = v2.outputs['v']

# Everything is lazily computed so no computation happened up to this point
# The access to the `value` property will kick off the computation
print(add.outputs['v'].value)
