#!/usr/bin/python

###################################
def SetStyle(obj, mc, mz, ms, ls = 1, lw = 1):
    obj.SetMarkerSize(mz)
    obj.SetMarkerStyle(ms)
    obj.SetMarkerColor(mc)
    obj.SetLineColor(mc)
    obj.SetLineWidth(lw)
    obj.SetLineStyle(ls)


###################################



# https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int-in-python

def makefloat(value):
    val = 0.
    try:
        val = float(value)
    except:
        val = 1.*int(value)
    return val

###################################
def MakeTime(stime):
    # example: 'Tue Jan 29 14:10:41.061217 2019'
    time = 0.
    print 'Making time from {}'.format(stime)
    timestr = stime.split()[3]
    ic = 0
    for item in timestr.split(':'):
        time = time*60. + makefloat(item)
    return time
