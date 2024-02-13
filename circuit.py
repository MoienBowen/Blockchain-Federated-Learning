import math
import random
import numpy as np

# Circuit represents a boolean circuit with n inputs and one output.
# The circuit is represented as a list of gates, where each gate has a type
# (AND, OR, XOR, or NOT) and a list of input indices. The output of the gate
# is the result of applying the type to the inputs. The output of the circuit
# is the output of the last gate.
class Circuit:
    def __init__(self, n, gates):
        self.n = n # number of inputs
        self.gates = gates # list of gates

    # Eval evaluates the circuit on a given input vector x of length n.
    # Returns the output of the circuit as a boolean value.
    def Eval(self, x):
        assert len(x) == self.n # check input length
        values = x[:] # copy input vector
        for gate in self.gates: # iterate over gates
            gate_type = gate[0] # get gate type
            gate_inputs = gate[1:] # get gate inputs
            gate_output = None # initialize gate output
            if gate_type == "AND": # AND gate
                gate_output = True # start with True
                for i in gate_inputs: # iterate over inputs
                    gate_output = gate_output and values[i] # apply AND
            elif gate_type == "OR": # OR gate
                gate_output = False # start with False
                for i in gate_inputs: # iterate over inputs
                    gate_output = gate_output or values[i] # apply OR
            elif gate_type == "XOR": # XOR gate
                gate_output = False # start with False
                for i in gate_inputs: # iterate over inputs
                    gate_output = gate_output != values[i] # apply XOR
            elif gate_type == "NOT": # NOT gate
                assert len(gate_inputs) == 1 # check input length
                i = gate_inputs[0] # get input index
                gate_output = not values[i] # apply NOT
            else: # invalid gate type
                raise ValueError("Invalid gate type: " + gate_type)
            values.append(gate_output) # append gate output to values
        return values[-1] # return output of last gate

    def num_gates(self):
        count = 0
        for gate in self.gates:
            if gate[0] in ["AND", "XOR"]:
                count += 1
        print(type(count))
        print("43567890")
        return count

    # String returns a string representation of the circuit.
    def __str__(self):
        s = "Circuit with " + str(self.n) + " inputs and " + str(len(self.gates)) + " gates:\n" # start with header
        for i, gate in enumerate(self.gates): # iterate over gates
            gate_type = gate[0] # get gate type
            gate_inputs = gate[1:] # get gate inputs
            s += str(i + self.n) + " = " + gate_type + "(" # add gate output and type
            for j, k in enumerate(gate_inputs): # iterate over inputs
                s += str(k) # add input index
                if j < len(gate_inputs) - 1: # not last input
                    s += ", " # add comma
            s += ")\n" # add newline
        return s

# NewRandomCircuit generates a random circuit with n inputs and m gates.
# Each gate has a random type and a random number of inputs (between 1 and k).
# The inputs of each gate are chosen randomly from the previous outputs.
def NewRandomCircuit(n, m, k):
    gates = [] # initialize gates list
    num_mul_gate = 0
    for i in range(m): # iterate over gates
        gate_type = random.choice(["AND", "OR", "XOR", "NOT"]) # choose random type
        if gate_type in ["AND", "XOR"]:
            num_mul_gate += 1
        gate_inputs = [] # initialize inputs list
        # num_inputs = random.randint(1, k) # choose random number of inputs
        num_inputs = k # choose random number of inputs
        if gate_type == "NOT": # NOT gate
            num_inputs = 1 # override number of inputs
        for j in range(num_inputs): # iterate over inputs
            gate_input = random.randint(0, n + i - 1) # choose random input from previous outputs
            gate_inputs.append(gate_input) # append input to list
        gate = [gate_type] + gate_inputs # create gate
        gates.append(gate) # append gate to list

    while (num_mul_gate < m/2):
        circuit = NewRandomCircuit(n, m, k)
        num_mul_gate = 0
        for i in range(len(circuit.gates)): 
            gate = gates[i] 
            if gate[0] in ["AND", "XOR"]:
                num_mul_gate += 1
    return Circuit(n, gates) # return circuit

# NewRandomInput generates a random input vector of length n.
def NewRandomInput(n):
    x = [] # initialize input vector
    for i in range(n): # iterate over inputs
        x.append(random.choice([True, False])) # choose random boolean value
    return x


def lagrange_interpolation(x, y):
    n = len(x)
    c = np.zeros(n)
    for i in range(n):
        p = 1
        q = 1
        for j in range(n):
            if i != j:
                p = np.convolve(p, [1, -x[j]]) 
                q = q * (x[i] - x[j]) 
        c = c + y[i] * p / q 
    return c


def polynomial_multiplication(a, b):
    return np.convolve(a, b)


def build_fgh(circuit, F):
    gates = circuit.gates 
    f_inputs = [] 
    g_inputs = [] 
    f_indices = [] 
    g_indices = [] 
    num_mul_gate = 0
    for i in range(len(gates)):
        gate = gates[i] 
        if gate[0] in ["AND", "XOR"]:
            num_mul_gate += 1
            f_inputs.append(gate[1])
            g_inputs.append(gate[2]) 
            f_indices.append(i * 2 + 1)
            g_indices.append(i * 2 + 2)

    assert 2 * num_mul_gate < F 

    f = lagrange_interpolation(f_indices, f_inputs)
    g = lagrange_interpolation(g_indices, g_inputs)
    h = polynomial_multiplication(f, g) 
    return f, g, h


# # Example usage
# n = 2 # number of inputs
# m = 5 # number of gates
# k = 2 # maximum number of inputs per gate
# circuit = NewRandomCircuit(n, m, k) # generate random circuit
# print(circuit) # print circuit
# x = NewRandomInput(n) # generate random input
# # x = [1,2,3,4,5,6,7,8,9,0]
# print("Input:", x) # print input
# y = circuit.Eval(x) # evaluate circuit on input
# print("Output:", y) # print output

# f, g, h = build_fgh(circuit, 2**128)
# print("f =", f)
# print("g =", g)
# print("h =", h)

