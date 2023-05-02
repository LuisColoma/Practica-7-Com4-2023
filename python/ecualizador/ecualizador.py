import numpy as np
import matplotlib.pyplot as plt  
from scipy import signal
from scipy.io import wavfile
from scipy.signal import residue, lfilter, freqz, zpk2tf
from scipy.optimize import least_squares
import scipy.io.wavfile as wav
from scipy.signal import butter, cheby1, convolve, lfilter, filtfilt, iirnotch, cheby2, ellip
import fir1

fs, x = wavfile.read('audio.wav')
lx = len(x) # Cálculo del tamaño del vector de audio
n = np.arange(len(x))
fs= 16000

G=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

fac=1; #Normalización de la frecuencia
#Frecuancias de corte para Filtros
Wn1 = fac*[0.01098, 0.02150];  #filtro banda 1
Wn2 = fac*[0.02150, 0.04150];  #filtro banda 2
Wn3 = fac*[0.05250, 0.07250];  #filtro banda 3
Wn4 = fac*[0.08500, 0.11500];  #filtro banda 4
Wn5 = fac*[0.11500, 0.18300];  #filtro banda 5
Wn6 = fac*[0.19400, 0.700];    #filtro banda 6
Wn7 = fac*[0.30000, 0.40500];  #filtro banda 7
Wn8 = fac*[0.41000, 0.60500];  #filtro banda 8
Wn9 = fac*[0.60000, 0.76040];  #filtro banda 9
Wn10 = fac*[0.77000, 0.92465]; #filtro banda 10

###################################Implementación de filtros########################################
#Cheby 1
b1, a1 = cheby1(5, 0.0001, Wn1, 'bandpass')
w1, h1 = freqz(b1, a1,fs)
y1 = signal.filtfilt(b1, a1, x)
wav.write('PY_filtro1.wav', fs, y1.astype(np.int16)) 

b2, a2 = cheby1(5, 10, Wn2, 'bandpass')
w2, h2 = freqz(b2, a2,fs)
y2 = signal.filtfilt(b2, a2, x)
wav.write('PY_filtro2.wav', fs, y2.astype(np.int16)) 

#cheby 2
b3, a3 = cheby2(5, 50, Wn3, 'bandpass')
w3, h3 = freqz(b3, a3,fs)
y3 = signal.filtfilt(b3, a3, x)
wav.write('PY_filtro3.wav', fs, y3.astype(np.int16)) 

b4, a4 = cheby2(5, 40, Wn4, 'bandpass')
w4, h4 = freqz(b4, a4,fs)
y4 = signal.filtfilt(b4, a4, x)
wav.write('PY_filtro4.wav', fs, y4.astype(np.int16)) 

#FIR
y5=y4
y6=y5
b5 = signal.firwin(40, Wn5,pass_zero=False)
ym5 = convolve(b5,x)
b6 = signal.firwin(60, Wn6,pass_zero=False)
ym6 = convolve(b6,x)
y5 = np.arange(len(x))
y6 = y5

for i in range(0,len(x)):
    y5[i]=ym5[i]
    y6[i]=ym6[i]

y5=np.transpose(y5)
w5, h5 = freqz(b5, 1,fs)
wav.write('PY_filtro5.wav', fs, y5.astype(np.int16)) 
y6=np.transpose(y6)
w6, h6 = freqz(b6, 1,fs)
wav.write('PY_filtro6.wav', fs, y6.astype(np.int16)) 


# ellip
b7, a7 = ellip(5,10,500,Wn7, 'bandpass')
w7, h7 = freqz(b7, a7,fs)
y7 = signal.filtfilt(b7, a7, x)
wav.write('PY_filtro7.wav', fs, y7.astype(np.int16)) 

b8, a8 = ellip(5,1,200,Wn8, 'bandpass')
w8, h8 = freqz(b8, a8,fs)
y8 = signal.filtfilt(b8, a8, x)
wav.write('PY_filtro8.wav', fs, y8.astype(np.int16)) 

#butter
b9, a9 = butter(N=2,Wn=Wn9,btype="bandpass")
w9, h9 = freqz(b9, a9,fs)
y9 = signal.filtfilt(b9, a9, x)
wav.write('PY_filtro9.wav', fs, y9.astype(np.int16)) 

b10, a10 = butter(N=3,Wn=Wn10,btype="bandpass")
w10, h10 = freqz(b10, a10,fs)
y10 = signal.filtfilt(b10, a10, x)
wav.write('PY_filtro10.wav', fs, y10.astype(np.int16)) 

v = np.size(G)
if v == 10:
    G = np.transpose(G)

y_final = G[0]*y1+G[1]*y2+G[2]*y3+G[3]*y4+G[4]*y5+G[5]*y6+G[6]*y7+G[7]*y8+G[8]*y9+G[9]*y10
wav.write('PY_salida.wav', fs, y_final.astype(np.int16)) 

##############################Graficación##########################
plt.figure(1)
plt.subplot(2,1,1)
plt.stem(n,x)
plt.title('X[n]')

plt.subplot(2,1,2)
plt.stem(n,y_final)
plt.title('Y[n]')

plt.figure(2)
plt.plot(w1,abs(h1))
plt.title('Primer Filtro ')

plt.figure(3)
plt.plot(w2,abs(h2))
plt.title('Segundo Filtro ')

plt.figure(4)
plt.plot(w3,abs(h3))
plt.title('Tercer Filtro ')

plt.figure(5)
plt.plot(w4,abs(h4))
plt.title('Cuarto Filtro ')

plt.figure(6)
plt.plot(w5,abs(h5))
plt.title('Quinto Filtro ')

plt.figure(7)
plt.plot(w6,abs(h6))
plt.title('Sexto Filtro ')

plt.figure(8)
plt.plot(w7,abs(h7))
plt.title('Septimo Filtro ')

plt.figure(9)
plt.plot(w8,abs(h8))
plt.title('Octavo Filtro ')

plt.figure(10)
plt.plot(w9,abs(h9))
plt.title('Noveno Filtro ')

plt.figure(11)
plt.plot(w10,abs(h10))
plt.title('Decimo Filtro ')

wt=w1+w2+w3+w4+w5+w6+w7+w8+w9+w10
ht=h1+h2+h3+h4+h5+h6+h7+h8+h9+h10

plt.figure(12)
plt.plot(wt,abs(ht))
plt.title('RELACION TOTAL DE FILTROS ')

plt.show()