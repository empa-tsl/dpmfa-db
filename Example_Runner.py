# -*- coding: utf-8 -*-
"""

Created on 09.04.2020
@author: dew
Test model for importing SQL databases

"""

###############################################################################

import numpy as np
import csv
import os

import Example_Model
from dpmfa import simulator as sc

#import matplotlib.pyplot as plt
#import numpy.random as nr
#from scipy.stats import gaussian_kde 
#import pandas as pd

###############################################################################

# define model
exampleModel = Example_Model.model
# check validity
exampleModel.checkModelValidity()

exampleModel.debugModel()

###############################################################################

startYear = 1993
# total time range considered, also for np.arange
# if Tperiods is changed, the import settings of the production data in the model
# must also be changed (if Tperiods get higher)
Tperiods = 23
# defined period for checking the flows (here 2018)
Speriod = 4

RUNS = 100

###############################################################################

# set up the simulator object
simulator = sc.Simulator(RUNS, Tperiods, 2250, True, True) # 2250 is just a seed
# define what model  needs to be run
simulator.setModel(exampleModel)

simulator.debugSimulator()

# run the model
simulator.runSimulation()

###############################################################################

# find out the sinks and the stocks of the system
sinks = simulator.getSinks()
stocks = simulator.getStocks()

###############################################################################

# compartment with loggedInflows
loggedInflows = simulator.getLoggedInflows() 
# compartment with loggedOutflows
loggedOutflows = simulator.getLoggedOutflows()

###############################################################################

## display mean ± std for each flow
print('Logged Outflows:')
print('-----------------------')
print('')
# loop over the list of compartments with loggedoutflows
for Comp in loggedOutflows:
    print('Flows from ' + Comp.name +':')
    # in this case name is the key, value is the matrix(data), in this case .items is needed
    for Target_name, value in Comp.outflowRecord.items():
        print(' --> ' + str(Target_name)+ ': Mean = '+str(round(np.mean(value[:,Speriod]),0))+' ± '+str(round(np.std(value[:,Speriod]),0)))
    print('')
print('-----------------------')
print('')

################################################################################

# export all outflows to csv
for Comp in loggedOutflows: # loggedOutflows is the compartment list of compartmensts with loggedoutflows
    for Target_name, value in Comp.outflowRecord.items(): # in this case name is the key, value is the matrix(data), in this case .items is needed     
        with open(os.path.join("example_output","loggedOutflows_" + Comp.name + "_to_" + Target_name + ".csv"), 'w') as RM :
            a = csv.writer(RM, delimiter=' ')
            data = np.asarray(value)
            a.writerows(data) 

# export all inflows to csv
for Comp in loggedInflows: # loggedOutflows is the compartment list of compartmensts with loggedoutflows
    with open(os.path.join("example_output",'loggedInflows_'+Comp+'.csv'), 'w') as RM :
        a = csv.writer(RM, delimiter=' ')
        data = np.asarray(loggedInflows[Comp])
        a.writerows(data) 


