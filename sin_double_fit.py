import numpy as np
from scipy.optimize import leastsq
import pylab as plt

N = 50 # number of data points
#t = np.linspace(0, 4*np.pi, N)
t = np.linspace(0, N, N)
f = 1.15247 # Optional!! Advised not to use
#data = 3.0*np.sin(f*t+0.001) + 0.5 + np.random.randn(N) # create artificial data with noise
data=np.array([54.18774988775157, 48.066871865365556, 40.94392808335357, 33.08749146592149, 24.704450441638542, 15.92184102688897, 6.721616540181973, 3.1137695228403377, 13.913036647963299, 25.67502241092539, 37.33860009331154, 46.82751871461432, 52.52838276045228, 54.28579155295427, 52.88536568947857, 49.26596813439121, 44.16685794014423, 38.09069597606885, 31.376004556359355, 24.267644474348515, 16.94084942414486, 9.472834199275884, 1.7842531699261694, 6.395308435886173, 15.41667546636493, 25.25261272125989, 34.79720502855182, 42.04462109108431, 45.633962488556726, 45.68123544938142, 43.10441881847599, 38.83051163679037, 33.51800176796311, 27.589594109768, 21.333013541018524, 14.966325158393463, 8.647391522539177, 2.4410211393875776, 3.7290068314175904, 10.097955001954423, 16.94292458121573, 24.156211165213513, 30.670789228604903, 34.81200766664463, 35.74749629640943, 33.9552761388043, 30.380271690422816, 25.769112794574184, 20.57494026087136, 15.078421387216636])

guess_mean = np.mean(data)
guess_std = 3*np.std(data)/(2**0.5)/(2**0.5)
guess_phase = 30
guess_freq = 1
guess_amp = 1

# we'll use this to plot our first estimate. This might already be good enough for you
data_first_guess = guess_std*np.sin(t+guess_phase)*np.sin(t+guess_phase) + guess_mean

# Define the function to optimize, in this case, we want to minimize the difference
# between the actual data and our "guessed" parameters
optimize_func = lambda x: x[0]*np.sin(x[1]*t+x[2]) + x[3] - data
optimize_func_double=lambda x: x[5]*np.sin(x[0]*t +x[1])*np.sin(x[2]*t+x[3])+x[4] -data


#est_amp, est_freq, est_phase, est_mean = leastsq(optimize_func_double, [guess_amp, guess_freq, guess_phase, guess_mean])[0]

est_freq1,est_phase1, est_freq2,est_phase2 , est_mean, amp = leastsq(optimize_func_double, [ guess_freq, guess_phase, guess_freq, guess_phase, guess_mean, guess_amp])[0]


# recreate the fitted curve using the optimized parameters
data_fit = amp*np.sin(est_freq1*t+est_phase1)*np.sin(est_freq2*t+est_phase2) + est_mean

# recreate the fitted curve using the optimized parameters

fine_t = np.arange(0,max(t),0.1)
#data_fit=est_amp*np.sin(est_freq*fine_t+est_phase)+est_mean

data_fit = amp*np.sin(est_freq1*t+est_phase1)*np.sin(est_freq2*t+est_phase2) + est_mean

plt.plot(t, data, '.')
plt.plot(t, data_first_guess, label='first guess')
plt.plot(t, data_fit, label='after fitting')
plt.legend()
plt.show()