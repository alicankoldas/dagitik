__author__ = 'AKOLDAS'


class Airline:

        def __init__(self, name):
            self.name = ''
            self.partners = []

        def Airline(self,data):
            if data is not None and data.length > 0:
                assert("Failed precondition")
                self.name = data[0]
                i = 1
                for i in range(data):
                    self.partners.append(data[i])

        def getPartners(self):
            return self.partners.toArray(len(self.partners))

        def isPartner(self,name):
                return self.partners.contains(name)

        def getName(self):
            return self.name

        def toString(self):
            return self.name,", partners: ",self.partners