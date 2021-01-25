'''
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
Date: 17/05/20
'''
from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
from AIPSTV import AIPSTV
import numpy as np

def parseInputFile():
    file = open('PMCorr.in','r')

    # First need to find AIPSuserno
    line = file.readline()
    while line:
        
        if (line != '\n') and (line[0] != "#"):
            splitLine1 = line.split(';')
            splitLine2 = splitLine1[0].split('=')
            if splitLine2[0].strip() == 'AIPSuserno':
                AIPS.userno = int(splitLine2[1])
                print "User Number =",AIPS.userno
        line = file.readline()

    file.seek(0)
    # AIPS tasks are created with defaults
    fitld = AIPSTask('FITLD')
    imagr = AIPSTask('IMAGR')
    split = AIPSTask('SPLIT')
    clcor = AIPSTask('clcor')
    splat = AIPSTask('splat')
    split = AIPSTask('split')
    dbcon = AIPSTask('dbcon')
    jmfit = AIPSTask('jmfit')

    # other defaults that shouldn't be changed
    dbcon.dopos[1][1] = 0.0 
    clcor.opcode = 'ANTP'

    line = file.readline()
    while line:
        
        if (line != '\n') and (line[0] != "#"):
            splitLine1 = line.split(';')
            #fitld inputs
            if splitLine1[0] == 'fitld':
                splitLine2 = splitLine1[1].split('=')
                if splitLine2[0].strip() == 'datain':
                    fitld.datain = splitLine2[1].strip()
                    print "fitld.datain =",fitld.datain
            
            #imagr inputs
            if splitLine1[0] == 'imagr':
                splitLine2 = splitLine1[1].split('=')
                if splitLine2[0].strip() == 'robust':
                    imagr.robust = int(splitLine2[1])
                    print "imagr.robust =",imagr.robust
                if splitLine2[0].strip() == 'niter':
                    imagr.niter = int(splitLine2[1])
                    print "imagr.niter =",imagr.niter
                if splitLine2[0].strip() == 'cellsi':
                    imagr.cellsi = AIPSList([float(splitLine2[1]),float(splitLine2[1])])
                    print "imagr.cellsi =",imagr.cellsi
                if splitLine2[0].strip() == 'imsi':
                    imagr.imsi = AIPSList([int(splitLine2[1]),int(splitLine2[1])])
                    print "imagr.imsi =",imagr.imsi
                if splitLine2[0].strip() == 'boxfile':
                    imagr.boxfile = splitLine2[1].strip() 
                    print "imagr.boxfile =",imagr.boxfile
                if splitLine2[0].strip() == 'rashift':
                    imagr.rashift = AIPSList([float(splitLine2[1])])
                    print "imagr.rashift =",imagr.rashift
                if splitLine2[0].strip() == 'decshift':
                    imagr.decshift = AIPSList([float(splitLine2[1])])
                    print "imagr.decshift =",imagr.decshift
                if splitLine2[0].strip() == 'flux':
                    imagr.flux = float(splitLine2[1])
                    print "imagr.flux =" ,imagr.flux

            #splat inputs
            if splitLine1[0] == 'splat':
                splitLine2 = splitLine1[1].split('=')
                if splitLine2[0].strip() == 'docal':
                    splat.docal = int(splitLine2[1])
                    print "splat.docal =",splat.docal
                if splitLine2[0].strip() == 'gainuse':
                    splat.gainuse = int(splitLine2[1])
                    print "splat.gainuse =",splat.gainuse
                if splitLine2[0].strip() == 'flagver':
                    splat.flagver = int(splitLine2[1])
                    print "splat.flagver =",splat.flagver
                if splitLine2[0].strip() == 'doband':
                    splat.doband = int(splitLine2[1])
                    print "splat.doband =",splat.doband
                if splitLine2[0].strip() == 'bpver':
                    splat.bpver = int(splitLine2[1])
                    print "splat.bpver =",splat.bpver

            #split inputs
            if splitLine1[0] == 'split':
                splitLine2 = splitLine1[1].split('=')
                if splitLine2[0].strip() == 'docal':
                    split.docal = int(splitLine2[1])
                    print "split.docal =",split.docal
                if splitLine2[0].strip() == 'gainuse':
                    split.gainuse = int(splitLine2[1])
                    print "split.gainuse =",split.gainuse
                if splitLine2[0].strip() == 'flagver':
                    split.flagver = int(splitLine2[1])
                    print "split.flagver =",split.flagver
                if splitLine2[0].strip() == 'doband':
                    split.doband = int(splitLine2[1])
                    print "split.doband =",split.doband
                if splitLine2[0].strip() == 'aparm':
                    splitLine3 = splitLine2[1].split(',')
                    split.aparm = AIPSList([int(splitLine3[0]),int(splitLine3[1])])
                    print "split.aparm =",split.aparm
                if splitLine2[0].strip() == 'nchav':
                    split.nchav = int(splitLine2[1])
                    print "split.nchav =",split.nchav
                if splitLine2[0].strip() == 'chinc':
                    split.chinc = int(splitLine2[1])
                    print "split.chinc =",split.chinc   
            '''
            #jmfit inputs
            if splitLine1[0] == 'jmfit':
                splitLine2 = splitLine1[1].split('=')
                if splitLine2[0].strip() == 'dowidth':
                    jmfit.dowidth = int(splitLine2[1])
                    print "jmfit.dowidth =" ,jmfit.dowidth
                if splitLine2[0].strip() == 'blc':
                    splitLine3 = splitLine2[1].split(',')
                    jmfit.blc = AIPSList(int(splitLine3[0]),int(splitLine3[1]))
                    print "jmfit.blc =" ,jmfit.blc
                if splitLine2[0].strip() == 'trc':
                    splitLine3 = splitLine2[1].split(',')
                    jmfit.trc = AIPSList(int(splitLine3[0]),int(splitLine3[1]))
                    print "jmfit.trc =" ,jmfit.trc
            '''

            #Miscellaneous parameters
            splitLine2 = splitLine1[0].split('=')
            if splitLine2[0].strip() == 'properMotion':
                properMotion = float(splitLine2[1])
                print "properMotion =",properMotion
            if splitLine2[0].strip() == 'positionAngle':
                positionAngle = float(splitLine2[1])
                print "positionAngle =",positionAngle
            if splitLine2[0].strip() == 'sourceName':
                sourceName = splitLine2[1].strip()
                split.sour = AIPSList([sourceName])
                clcor.sour = AIPSList([sourceName])
                print "sourceName =",sourceName
            if splitLine2[0].strip() == 'obsStartTime':
                obsStartTime = splitLine2[1].strip()
                print "obsStartTime =",obsStartTime
            if splitLine2[0].strip() == 'obsEndTime':
                obsEndTime = splitLine2[1].strip()
                print "obsEndTime =",obsEndTime
            if splitLine2[0].strip() == 'cleanup':
                cleanup = (splitLine2[1].strip() == 'True')
                print "cleanup =",cleanup
        line = file.readline()
    file.close()
    return fitld, imagr, split, clcor, splat, dbcon, \
           properMotion, positionAngle, sourceName, obsStartTime, \
           obsEndTime, cleanup


print '\n####################################'
print '#        Reading Parameters        #'
print '####################################'
fitld, imagr, split, clcor, splat, dbcon, \
           properMotion, positionAngle, sourceName, startTime, \
           endTime, cleanup = parseInputFile()
print '####################################\n'
#Load in data from working unix directory
fitld.outname = 'calData'
fitld.go()

uvdata = AIPSUVData('calData','UVDATA',1,1)
print 'Callibrated data set loaded: ', uvdata.exists()

splat.indata = uvdata

#TODO: get tv to work
#tv = AIPSTV(host = 'localhost')

# creating full image
# first run split on full data set, then imagr
split.indata = uvdata
temp = split.gainuse
split.gainuse = splat.gainuse
split.go()
split.gainuse = temp

fulldata = AIPSUVData(sourceName,'SPLIT',1,1)
imagr.indata = fulldata
imagr.outname = sourceName+'_F'
imagr.go()

#Now for time bining
def convertTime(time):
    '''
    Converts time in days into correct format for AIPS
    '''
    day = int(time)
    hour = int((time - day)*24)
    mins = int((time - day - float(hour)/24.0)*60*24)
    sec = round((time - day - float(hour)/24.0-float(mins)/(24.0*60.0))*3600*24,10)
    return day, hour, mins, sec

startList = [float(ii) for ii in startTime.split()]
endList = [float(ii) for ii in endTime.split()]

s_day = startList[0]
s_hour = startList[1]
s_min = startList[2]
s_sec = startList[3]

s_time = s_day + s_hour/24 + s_min/(60*24) + s_sec/(3600*24)

e_day = endList[0]
e_hour = endList[1]
e_min = endList[2]
e_sec = endList[3]
e_time = e_day + e_hour/24 + e_min/(60*24) + e_sec/(3600*24)

o_time = e_time - s_time
print "Observation time is:", o_time, "days"

#Calculate number of time bins
numBins = np.ceil(properMotion*o_time/(imagr.cellsi[1]))

#Number of bins in which there is no data
emptyBins = 0

binTime = o_time / numBins
print "Each time bin is:",binTime, "days long"
print "There are",numBins,"time bins"
posAngleRad = np.deg2rad(positionAngle)

for ii in range(0,int(numBins)):
    #timebinning
    
    tb_start = s_time + ii*binTime
    tb_end = s_time + (1+ii)*binTime
    tbs_day, tbs_hour,tbs_min,tbs_sec  = convertTime(tb_start)
    tbe_day, tbe_hour,tbe_min,tbe_sec  = convertTime(tb_end)
    splat.timerang = AIPSList([tbs_day, tbs_hour,tbs_min,tbs_sec,
                               tbe_day, tbe_hour,tbe_min,tbe_sec])
    
    
    splatdata = AIPSUVData(sourceName,'SPLAT',1,ii+1)

    splat.outdata = splatdata
    #splat to make multi source file
    try:
        splat.go()
    except:
        print "--------------------------------"
        print "ERROR!: Timebin",ii,"has no data"
        print "--------------------------------"
        emptyBins = emptyBins + 1
        continue
    
    #use clcor for position shifting
    angSep = ii*binTime*properMotion
    raShift =  -angSep*np.sin(posAngleRad)
    decShift = -angSep*np.cos(posAngleRad)

    clcor.indata = splatdata
    clcor.clcorprm[5] = round(raShift,10)
    clcor.clcorprm[6] = round(decShift,10)

    try:
        clcor.go()
    except:
        print "------------------------------------------"
        print "ERROR!: Timebin",ii,"has no on source data"
        print "------------------------------------------"
        emptyBins = emptyBins + 1
        continue


    #ii+2 since full data set has same name so have to start at seq 2
    #now run split 
    split.indata = splatdata
    
    split.go()

# do the combination
if numBins > 1:
    dbcon.indata = AIPSUVData(sourceName,'SPLIT',1,2)
    for ii in range(1,int(numBins-emptyBins)):
        dbcon.in2data = AIPSUVData(sourceName,'SPLIT',1,ii+2)
        dbcon.outdata = AIPSUVData(sourceName,'DBCON',1,ii+1)
        dbcon.go()
        dbcon.indata = AIPSUVData(sourceName,'DBCON',1,ii+1)

#now create image of final shifted data
imagr.indata = AIPSUVData(sourceName,'DBCON',1,int(numBins-emptyBins))
imagr.outname = sourceName+'_S'
imagr.go()

if cleanup:

    # Now we delete all splat, split and intermediate dbcon files
    for ii in range(1,int(numBins)+1): #splat for every bin
        delData = AIPSUVData(sourceName, 'SPLAT',1,ii)
        delData.zap()

    for ii in range(1,int(numBins-emptyBins)+1):
        delData = AIPSUVData(sourceName, 'SPLIT',1,ii+1)
        delData.zap()

    uvdata.zap()

    for ii in range(2,int(numBins-emptyBins)): #delete all dbcon except last
        delData = AIPSUVData(sourceName, 'DBCON',1,ii)
        delData.zap()
