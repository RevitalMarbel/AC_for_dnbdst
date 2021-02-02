import math
import graph_compare_functions
import pickle
import pylab as plt


def distance4RaDec(ra1,ra2,dec1,dec2):
    d1 = math.radians(dec1)
    d2 = math.radians(dec2)
    r1 = math.radians(ra1)
    r2 = math.radians(ra2)

    a=math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(r1-r2)

    return math.degrees(math.acos(a))

def distance4( lat1, lat2, lon1, lon2, ratio=1):
    R = 6373.0+550

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = (R * c) / ratio
    return distance

import numpy, scipy.optimize

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = numpy.array(tt)
    yy = numpy.array(yy)
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*numpy.pi)
    fitfunc = lambda t: A * numpy.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}

#this function get a dictionary of trees (mst computed in main) and compare ...
def get_trees_diff(file_name):
    dbfile = open(file_name, 'rb')
    trees = pickle.load(dbfile)
    print(len(trees[0].nodes))
    differences=[]
    for i in range( len(trees)-1):
        diff= graph_compare_functions.graph_difference(trees[i],trees[i+1])
        differences.append(diff)
    return differences



##this function returns a dictionary that contains all nodes pairs( keys) and the sin function (values)
def  get_area_from_distances_file(file_name, tresh):
    dbfile = open(file_name, 'rb')
    dist = pickle.load(dbfile)
    res={}
    sum=0.0
    #print(dist["1_2"])
    for key in dist:
        # #print(key, '=>', dist[key])
        # tt = numpy.linspace(0, len(dist[key]), len(dist[key]))
        # res[key] = fit_sin(tt, numpy.array(dist[key]))
        area=area_of_pair(dist[key], tresh)
        res[key]=area
        sum+=area
    print(sum/float(len(dist.values())+1))
    dbfile.close()
    return res


#return a disctionary with the distances in time (time)
def  get_distance_from_distances_file(file_name, time):
    dbfile = open(file_name, 'rb')
    dist = pickle.load(dbfile)
    res={}

    for key in dist:
        if(time<len(dist[key])  ):
            area=dist[key][time]
           # print (area, "area")
            res[key]=area
            #print(key)

        else:
            print(key,time ,dist[key])

    dbfile.close()
    return res

def area_of_pair(y_data, treshold):
    tt = numpy.linspace(0, len(y_data), len(y_data))

    listForIntegral=[]
    for i in range(len(y_data)):
        if(y_data[i] - treshold >0):
            listForIntegral.append(y_data[i] - treshold)
        else:
            listForIntegral.append(0)
    area2 = numpy.trapz(listForIntegral, dx=1)
    res=area2/(len(y_data)+1)
    #print (res)
    return res



def main():

    list=get_trees_diff("treePickle")
    print(list[0])
    plt.plot([i for i in range(len(list)) ], list)
    plt.show()

if __name__ == "__main__":
    main()


