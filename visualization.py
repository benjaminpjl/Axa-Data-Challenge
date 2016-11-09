from numpy import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import pylab as P
plt.style.use('ggplot');
from Preprocessing import load_data


preproc_data , features_data, rcvcall_data=load_data('train_2011_2012_2013.csv')

#Plot CSPL_RECEIVED_CALLS in function of ASS_ASSIGNMENT

preproc_data1 = preproc_data.groupby(["ASS_ASSIGNMENT"])['CSPL_RECEIVED_CALLS'].sum()
plt.figure()
preproc_data1.plot(kind="bar", x="ASS_ASSIGNMENT" , y="CSPL_RECEIVED_CALLS")
plt.legend()
plt.show()

#Plot CSPL_RECEIVED_CALLS in function of HOUR

preproc_data2 = preproc_data.groupby(["HOUR"])['CSPL_RECEIVED_CALLS'].sum()
plt.figure()
preproc_data2.plot(kind="bar", x="HOUR" , y="CSPL_RECEIVED_CALLS")
plt.legend()
plt.show()