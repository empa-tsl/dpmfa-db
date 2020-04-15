# -*- coding: utf-8 -*-
"""

Created on 09.04.2020
@author: dew
Test model for importing SQL databases

"""

###############################################################################

import Test_Model
import Simulator as sc
import numpy as np
#import matplotlib.pyplot as plt
#import numpy.random as nr
#from scipy.stats import gaussian_kde 
#import pandas as pd

###############################################################################

# define model
model = Test_Model.model
# check validity
model.checkModelValidity()

###############################################################################

startYear = 1988
# total time range considered, also for np.arange, important for development of  Accumulation, release, concentration 
# if Tperiods is changed, the import settings of the production data in the model must also be changed (if Tperiods get higher)
Tperiods = 5
# defined period for checking the flows (here 2018)
Speriod = 0

RUNS=10

###############################################################################

# set up the simulator object
simulator = sc.Simulator(RUNS, Tperiods, 2250, True, True) # 2250 is just a seed
# define what model  needs to be run
simulator.setModel(model)
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
print 'Logged Outflows:'
print '-----------------------'
print ''
# loop over the list of compartments with loggedoutflows
for Comp in loggedOutflows:
    print 'Flows from ' + Comp.name +':' 
    # in this case name is the key, value is the matrix(data), in this case .items is needed
    for Target_name, value in Comp.outflowRecord.items():
        print ' --> ' + str(Target_name)+ ': Mean = '+str(round(np.mean(value[:,Speriod]),0))+' ± '+str(round(np.std(value[:,Speriod]),0))   
    print''
print '-----------------------'
print ''

###############################################################################

import csv

# export all outflows to csv
for Comp in loggedOutflows: # loggedOutflows is the compartment list of compartmensts with loggedoutflows
    for Target_name, value in Comp.outflowRecord.items(): # in this case name is the key, value is the matrix(data), in this case .items is needed     
        with open('loggedOutflows_'+Comp.name+'to'+Target_name+'.csv', 'wb') as RM :
            a = csv.writer(RM, delimiter=' ')
            data = np.asarray(value)
            a.writerows(data) 

# export all inflows to csv
for Comp in loggedInflows: # loggedOutflows is the compartment list of compartmensts with loggedoutflows
    with open('loggedInflows_'+Comp+'.csv', 'wb') as RM :
        a = csv.writer(RM, delimiter=' ')
        data = np.asarray(loggedInflows[Comp])
        a.writerows(data) 


