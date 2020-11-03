# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 11:34:13 2020

@author: Me
"""

import numpy as np
import pyperclip




full_path = input("Enter Gcode full path: ")
#C:\Users\Me\Desktop\prints_analysis_project\xyzCalibration_cube (3).gcode

name=full_path.rsplit("\\", 1)[1]
path=full_path.rsplit("\\", 1)[0]


same_path=input("Place export in the same directory? 1=yes, 0=no ")

if same_path=="1":
    out_path = path
else:
    out_path = input("Enter export destination path: ")

name=name.rsplit(".gcode",1)[0]
out_name=out_path+"\\"+name+"_pythonEdited.txt"


###########################################
layer_vec=np.zeros([1,4])
with open(full_path) as fid:
    for line in fid:
        
        # get layer height
        if line.startswith(';Layer height'):
            for i, c in enumerate(line):
                if c.isdigit():
                    ind=i
                    break
            layer_height=float(line[i:])
            
        # get layer count
        elif line.startswith(';LAYER_COUNT'):
            for i, c in enumerate(line):
                if c.isdigit():
                    ind=i
                    break
            layer_count=float(line[i:])
        
        # analyse each layer
        elif line.startswith(';LAYER:'):
            current_layer_num=int(line[7:-1])
            line=fid.readline()
            
            while not (line.startswith(";TIME")):
                print(line)
                
                #G1 lines:
                if line.startswith("G1") and "X" in line and "Y" in line:
                    x_ind=line.find("X")
                    y_ind=line.find("Y")
                    e_ind=line.find("E")
                    
                    x_pos=float(line[x_ind+1:y_ind-1])
                    if e_ind!=-1:
                        y_pos=float(line[y_ind+1:e_ind-1])
                    else:
                        y_pos=float(line[y_ind+1:-1])
                    
                    current=np.array([x_pos,y_pos,layer_height*current_layer_num,1])
                    layer_vec=np.vstack((layer_vec,current))
                              
                #G0 lines:
                if line.startswith("G0") and "X" in line and "Y" in line:
                    x_ind=line.find("X")
                    y_ind=line.find("Y")
                    z_ind=line.find("Z")
                    x_pos=float(line[x_ind+1:y_ind-1])
                    if z_ind!=-1:
                        y_pos=float(line[y_ind+1:z_ind-1])
                    else:
                        y_pos=float(line[y_ind+1:-1])
                        
                    current=np.array([x_pos,y_pos,layer_height*current_layer_num,0])
                    layer_vec=np.vstack((layer_vec,current))
                

                line=fid.readline()
                   
fid.close();    
layer_vec=layer_vec[1:,:]

np.savetxt(out_name, layer_vec,fmt=['%f','%f','%f','%d'])

pyperclip.copy(out_name)

print("Full file path is: ")
print(out_name)
input("The path is copied to clipboard. Press enter key to exit")
