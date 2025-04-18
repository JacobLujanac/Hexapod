
# function to determine movement goal
  # factor in
    # target state (comes from path planning algorithim)
    # current state


## assign which legs will make up each tripod

## The type of movement will be determined
## The angles for each joint will be determined based off of the type of move
## Will have to change the sign of the angle depending on if its on the left or right sides
## This will update the servo.SetDegree (which is the next degree that the legs are moving to)

import math
import numpy as np


# REVISIONS TO MAKE
    # hex_loc -> get from accelerometer
    # hex_ang -> get from accelerometer
    # targ_loc -> get from path planning script
    # targ_tol -> get from path planning script


###############################################################
#               Variable Initialization                      #
###############################################################

# UPDATE (get orientation and position from accelerometer)

hex_loc = np.array([0,0]) # GET FROM ACCELEROMETER
hex_ang = np.array([-1,5]) # GET FROM ACCELEROMETER

targ_loc = np.array([0,5]) # GET FROM PATH PLANNING SCRIPT
targ_tolerance = 0.5 # GET FROM PATH PLANNING SCRIPT

# Normalize into unit vectors
def unit_vec(vec):
    u = vec / math.hypot(*vec)
    return u


hex_dir = unit_vec(hex_ang)
vec_targ = unit_vec(targ_loc - hex_loc)   


vec_targ_perp = np.array([-vec_targ[1],vec_targ[0]]) # Perpendicular direction, use to establish tolerance range

lim1 = targ_loc + (targ_tolerance * vec_targ_perp)
lim2 = targ_loc - (targ_tolerance * vec_targ_perp)

vec_lim1 = unit_vec(lim1 - hex_loc)  
vec_lim2 = unit_vec(lim2 - hex_loc)  

# Calculate angle between vectors


def angleBetweenVec(vec1,vec2):
    '''
    Calculates the angle between two unit vectors

    A cross B = |A||B|sin(theta)
    --> theta = arcsin(A cross B)
    '''

    theta = math.asin(np.cross(vec1 ,vec2))
    theta = math.degrees(theta)

    return theta

theta_targetRange = abs( angleBetweenVec(vec_lim1,vec_lim2) )
theta_hexToTarg = angleBetweenVec(hex_dir,vec_targ)

###############################################################
#               Movement Decision                             #
###############################################################

if (abs(theta_hexToTarg) <= (theta_targetRange/2)):
    Movement = "Forward"

    print(f"Movement ={Movement}")

else:
    Movement = "Rotate"
    theta_rotate = theta_hexToTarg

    print(f"Movement ={Movement}")
    print(f"/theta_rotate = {theta_rotate}")
    print(f"/theta_range = {theta_targetRange/2}")    

