'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''

class Node:
    def __init__(self,id,domain):
        self.domain = domain
        self.id = id

    def __str__(self):
        return str("NODE#"+str(self.id)+" : "+str(self.domain))

    def __repr__(self):
        return self.__str__()