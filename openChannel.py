import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os

from scipy.optimize import fsolve

from tkinter import filedialog
from tkinter import Tk
from pathlib import Path

# Anlytical solution 
## Declare variables 
g = 9.81 #Gravity vector 
H = 0.05 # Height of column
alpha = 5 # Angle of plane
nu = 1e-3 #Kinematic viscosity
d = 5e-4 # Particle diameter. Only used for the inertial number in this case

y = np.arange(0,H,H/100)
velocity_vec = -g*math.sin(math.radians(alpha))/nu*y**2/2 + g*math.sin(math.radians(alpha))/nu*H*y
dudy = g*math.sin(math.radians(alpha))/nu*(H-y)
p_kin = g*H*(1-y/H)*math.cos(math.radians(alpha)) #Kinematic pressure, same as being used in pimpleFoam.

#Identify OpenFOAM-directory
#root = Tk()
#root.withdraw()
#folder_selected = filedialog.askdirectory()
folder_selected = 'C:/Users/sindregy/Dropbox/NTNU/Prosjekter/Gihub_tut/Python_script/inclined_plane_newtonian'
print(folder_selected)

dirlist = [ item for item in os.listdir(folder_selected+'/postProcessing/singlegraph/') if os.path.isdir(os.path.join(folder_selected+'/postProcessing/singlegraph/', item)) ]

# Create directory for storing data
newDirName = folder_selected+'/Figures'
try:
    # Create target Directory
    os.mkdir(newDirName)
    print("Directory " , newDirName ,  " Created ") 
except FileExistsError:
    print("Directory " , newDirName ,  " already exists")

l = 0 # Tellevektor for tiden
for i in dirlist:
    path_vel = folder_selected+'/postProcessing/singlegraph/'+ i +'/line_U.xy'
    data_vel = np.loadtxt(path_vel, skiprows=0) 
    Positions = data_vel[:,0]
    vel = data_vel[:,1]
    time = float(i)
    plt.plot(Positions,vel,'o',label='Numerical solution')
    plt.plot(y,velocity_vec,label='Analytical solution')
    plt.ylabel('Velocity [m/s]')
    plt.xlabel('Position [m]')
    plt.title('Time='+i)
    plt.legend()
    plt.savefig(newDirName+'/Velocity'+i+'.png')
    plt.close()
    
    path_volumes = folder_selected+'/postProcessing/singlegraph/'+ i +'/line_p_inertialNumber_strainRate.xy'
    data_volumes = np.loadtxt(path_volumes, skiprows=0) 
    pressure = data_volumes[:,1]
    plt.plot(Positions,pressure,'o',label='Numerical solution')
    plt.plot(y, p_kin,label='Analytical solution')
    plt.ylabel('Kinematic pressure [m/s]')
    plt.xlabel('Position [m]')
    plt.title('Time='+i)
    plt.legend()
    plt.savefig(newDirName+'/Pressure'+i+'.png')
    plt.close()

    strain = data_volumes[:,3]
    plt.plot(Positions,strain,'o',label='Numerical solution')
    plt.plot(y, dudy,label='Analytical solution')
    plt.ylabel('Strain rate [1/s]')
    plt.xlabel('Position [m]')
    plt.title('Time='+i)
    plt.legend()
    plt.savefig(newDirName+'/StrainRate'+i+'.png')
    plt.close()