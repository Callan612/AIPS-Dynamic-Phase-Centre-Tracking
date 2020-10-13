# AIPS-Proper-Motion-Correction
Description:  The purpose of this script is to automate the proper motion 
              correction of VLBI images using AIPS. It follows the process of 
              taking a calibrated data set, splitting it into an appropriate 
              number of time-bins according to a given proper motion, shifting
              the phase centre of each time-bin to so that a moving peak is 
              remains in the same position relative to the phase centre of the 
              first time-bin, and then concatenate the time-bins into a single 
              data set. The resultant image will follow a source as it moves.
Requirements: - Python 2.7
              - Updated AIPS installation
              - ParselTongue 
              - 'PMCorr.in' input file
How to use:   
TODO:         - Automate the JMFIT task to fit a peak in the final image
              - Run for multiple proper motions in a single excecution
Author: Callan Wood (Curtin University WA)
Date: 17/05/20
