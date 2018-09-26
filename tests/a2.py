class I:
    strI = "Printing I string"

    def m(self):
        i = 1
        print('I: m method in I')


class A(I):
    pass
    # def m(self):
    #     print('A: m method in A')


class B(A):
    def __init__(self):
        self.m()


class C(B):
    def m(self):
        print('C: m method in C')


class Delegation:
    @classmethod
    def n(self, var_smth):
        kokoko = var_smth.m()
        kokoko1 = var_smth.m()
        var_smth.m()

    def main(self):
        i = B()
        i.m()
        self.n()


if __name__ == '__main__':
    Delegation().main()
