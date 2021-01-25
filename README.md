# AIPS-Proper-Motion-Correction
Description:  The purpose of this script is to automate the proper motion 
              correction of VLBI images using AIPS. It follows the process of 
              taking a calibrated data set, splitting it into an appropriate 
              number of time-bins according to a given proper motion (in 
              mas/day) such that no component moves more than 1 pixel per time
              bin, shifting the phase centre of each time-bin to so that a moving 
              peak remains in the same position relative to the phase centre of the 
              first time-bin, and then concatenate the time-bins into a single 
              data set. The resultant image will follow a source as it moves.
              
Requirements: - Python 2.7

              - AIPS installation
              
              - ParselTongue 
              
              - 'PMCorr.in' input file
              
How to use:   Modify the PMCorr.in input file and execute this script with
              ParselTongue. The input data file needs to be the original 
              calibrated data set with callibration tables attached. Images
              need to be inspected within the AIPS software. This script 
              requires an empty AIPS workspace.
              
TODO:         - Automate the JMFIT task to fit a peak in the final image
              - Run for multiple proper motions in a single excecution
              - Get AIPS TV to work
Author: Callan Wood (Curtin University WA)
Date: 25/1/21
