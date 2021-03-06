from signatures import generate_keys, verify, sign

class Tx:

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_addr, amount):
        """Adds input into the Tx"""
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        """Adds output into the Tx"""
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        """Adds required escrow signature into the Tx"""
        self.reqd.append(addr)

    def sign(self, private):
        """Signs the transactions with the private key"""
        message = self.__gather()
        newsigs = sign(message, private)
        self.sigs.append(newsigs)

    def is_valid(self):
        """Validates data in the transaction"""
        data = self.__gather()
        total_in = 0
        total_out = 0
        for address, amount in self.inputs:
            found = False
            for signature in self.sigs:
                if verify(data, signature, address):
                    found = True
            if not found:
                return False
            if amount < 0:
                return False
            total_in += amount
        for address in self.reqd:
            found = False
            for signature in self.sigs:
                if verify(data, signature, address):
                    found = True
            if not found:
                return False
        for address, amount in self.outputs:
            if amount < 0:
                return False
            total_out += amount
        if total_out > total_in:
            return False
        return True

    def __repr__ (self):
        repr_str = "INPUTS: \n"
        for address, amount in self.inputs:
            repr_str += "\t" + str(amount) + " from " + str(address)  +"\n"
        repr_str = "OUTPUS: \n"
        for address, amount in self.outputs:
            repr_str += "\t" + str(amount) + " to " + str(address) +  "\n"
        repr_str = "ESCROW SIGNATURES: \n"
        for r in self.reqd:
            repr_str += "\t" + str(r) + "\n"
        repr_str = "SIGNATURES: \n"
        for s in self.sigs:
            repr_str += "\t" + str(s) + "\n"
        return repr_str

    def __gather(self):
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return data

if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()
    pr4, pu4 = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)
    if Tx1.is_valid():
        print("Success! Tx is valid")
    else:
        print("ERROR! Tx is invalid")

    Tx2 = Tx()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr1)

    Tx3 = Tx()
    Tx3.add_input(pu3, 1.2)
    Tx3.add_output(pu1, 1.1)
    Tx3.add_reqd(pu4)
    Tx3.sign(pr3)
    Tx3.sign(pr4)

    for t in [Tx1, Tx2, Tx3]:
        if t.is_valid():
            print("Success! Tx is valid")
        else:
            print("ERROR! Tx is invalid")

    # Wrong signatures
    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.sign(pr2)

    # Escrow Tx not signed by the arbiter
    Tx5 = Tx()
    Tx5.add_input(pu3, 1.2)
    Tx5.add_output(pu1, 1.1)
    Tx5.add_reqd(pu4)
    Tx5.sign(pr3)

    # Two input addrs, signed by one
    Tx6 = Tx()
    Tx6.add_input(pu3, 1)
    Tx6.add_input(pu4, 0.1)
    Tx6.add_output(pu1, 1.1)
    Tx6.sign(pr3)

    # Outputs exceed inputs
    Tx7 = Tx()
    Tx7.add_input(pu4, 1.2)
    Tx7.add_output(pu1, 1)
    Tx7.add_output(pu2, 2)
    Tx7.sign(pr4)

    # Negative values
    Tx8 = Tx()
    Tx8.add_input(pu2, -1)
    Tx8.add_output(pu1, -1)
    Tx8.sign(pr2)

    # Modified Tx
    Tx9 = Tx()
    Tx9.add_input(pu1, 1)
    Tx9.add_output(pu2, 1)
    Tx9.sign(pr1)
    # outputs = [(pu2,1)]
    # change to [(pu3,1)]
    Tx9.outputs[0] = (pu3,1)


    for t in [Tx4, Tx5, Tx6, Tx7, Tx8, Tx9]:
        if t.is_valid():
            print("ERROR! Bad Tx is valid")
        else:
            print("Success! Bad Tx is invalid")









