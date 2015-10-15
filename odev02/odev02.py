__author__ = 'AKOLDAS'

import matplotlib.pyplot as plt
import numpy as np

import sysconfig as sys
import Airline as Airline



def canRedeem_1(current,goal,pathForMiles,airlinesVisited,network):

                    current = ''
                    goal = ''
                    pathForMiles = []
                    airlinesVisited = []
                    network = []


                    if(current == goal):
                        pathForMiles.append(current)
                        return True

                    elif(airlinesVisited.contains(current)):
                        return False
                    else:
                        airlinesVisited.append(current)
                        pathForMiles.append(current)


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
                            foundPath = canRedeem_1(partners[index], goal, pathForMiles, airlinesVisited, network)
                            index = index + 1

                    if(foundPath == False ):
                        pathForMiles.remove( pathForMiles.size() - 1)
                        return foundPath






scannerToReadAirlines = None
try:
    scannerToReadAirlines = open("airlines.txt", "r")
except sys.IOError as e:
    print('Could not connect to file airlines.txt.')


if(scannerToReadAirlines != None):
    airlinesPartnersNetwork = []
    newAirline = ''
    lineFromFile = ''
    airlineNames = ''

    while scannerToReadAirlines == True :
        lineFromFile = scannerToReadAirlines.next()
        airlineNames = lineFromFile.split(",")
        newAirline = ''
        airlinesPartnersNetwork.append( newAirline )

    print(airlinesPartnersNetwork)
    keyboard = raw_input('Enter your input: ')
    print('Enter airline miles are on: ')
    start = keyboard
    print('Enter goal airline: ')
    goal = keyboard
    pathForMiles = []
    airlinesVisited = []
    if canRedeem_1(start, goal, pathForMiles, airlinesVisited, airlinesPartnersNetwork):
        print('Path to redeem miles: ',pathForMiles)
    else:
        print('Cannot convert miles from ',start,' to ' ,goal ,'.')










