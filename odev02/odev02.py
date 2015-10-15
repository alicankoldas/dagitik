__author__ = 'AKOLDAS'

import matplotlib.pyplot as plt
import numpy as np

import Airline as Airline
import sys

class AirlineProblem :






        class canRedeem(Airline):

            current = ''
            goal = ''
            pathForMiles = []
            airlinesVisited = []
            network = []

            def __init__(self,name):
                self.name = name

            def canRedeem_1(self,current,goal,pathForMiles,airlinesVisited,network):
                if(current == goal):
                    pathForMiles.add(current)
                    return True

                elif(airlinesVisited.contains(current)):
                    return False
                else:
                    airlinesVisited.add(current)
                    pathForMiles.add(current)


                pos = -1
                index = 0
                while(pos == -1 and index < network.size()):
                        if(network.get(index).getName().equals(current)):
                            pos = index
                        index = index + 1


                if( pos == - 1):
                        return False

                index = 0
                partners = network.get(pos).getPartners()
                foundPath = False
                while( foundPath == False and index < len(partners)):
                        foundPath = self.canRedeem_1(partners[index], goal, pathForMiles, airlinesVisited, network)
                        index = index + 1

                if(foundPath == False ):
                    pathForMiles.remove( pathForMiles.size() - 1)
                    return foundPath



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
            return self.name + ", partners: " + self.partners

