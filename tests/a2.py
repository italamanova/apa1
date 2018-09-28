import sys
#
# class I(object):
#     strI = "Printing I string"
#
#     def m(self):
#         i = 1
#         print('I: m method in I')
#
#
# class A(I):
#     pass
#     # def m(self):
#     #     print('A: m method in A')
#
#
# class B(object):
#     def __init__(self):
#         self.m()
#
#
# class C(A, B):
#     def m(self):
#         print('C: m method in C')


class Delegation:
    # def n(self, var_smth):
    #     kokoko = var_smth.m()
    #     kokoko1 = var_smth.m()
    #     var_smth.m()

    def main(self):
        i = 1
        i.m()



if __name__ == '__main__':
    Delegation().main()
