class I(object):
    strI = "Printing I string"

    def m(self):
        i = 1
        print('I: m method in I')
        self.kokoko()


class A(I):
    def m(self):
        print('A: m method in A')
        B()


class B(I):
    def __init__(self):
        pass


class C(B, A):
    def m(self):
        print('C: m method in C')
        B()

class Delegation:
    def n(self, var_smth):
        kokoko = var_smth.l()
        kokoko1 = var_smth.m()
        var_smth.m()

    def main(self):
        i = 1
        i.m()
        i.n()

if __name__ == '__main__':
    Delegation().main()
