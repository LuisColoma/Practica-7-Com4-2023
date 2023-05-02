import numpy as np
import matplotlib.pyplot as plt  
from scipy import signal
from scipy.io import wavfile
from scipy.signal import residue, lfilter, freqz, zpk2tf
from scipy.optimize import least_squares
import scipy.io.wavfile as wav

fs, x = wavfile.read('audio.wav')
lx = len(x) # Cálculo del tamaño del vector de audio
n = np.arange(len(x))
fs= 16000

j = 0
EnergiaInit = 0

for i in range(0,len(x)):
    j = j+1
    EnergiaInit = EnergiaInit + np.abs(x[i])
print('La potencia de la señal de entrada es:', EnergiaInit)


b, a = signal.butter(N=20,Wn=(2000, 5000),btype="bandpass",fs=16000)
y_g = signal.filtfilt(b, a, x)

EnergiaFiltroGeneral = 0
for i in range(0,len(y_g)):
    EnergiaFiltroGeneral = EnergiaFiltroGeneral + np.abs(y_g[i])
print('La potencia de la señal de entrada con filtro pasa bandas de 2KHz a 5KHz es:', EnergiaFiltroGeneral)


b1, a1 = signal.butter(N=10,Wn=(2000, 2600),btype="bandpass",fs=16000)
w1, h1 = freqz(b1, a1,fs)
b2, a2 = signal.butter(N=10,Wn=(2600, 3200),btype="bandpass",fs=16000)
w2, h2 = freqz(b2, a2,fs)
b3, a3 = signal.butter(N=10,Wn=(3200, 3800),btype="bandpass",fs=16000)
w3, h3 = freqz(b3, a3,fs)
b4, a4 = signal.butter(N=10,Wn=(3800, 4400),btype="bandpass",fs=16000)
w4, h4 = freqz(b4, a4,fs)
b5, a5 = signal.butter(N=10,Wn=(4400, 5000),btype="bandpass",fs=16000)
w5, h5 = freqz(b5, a5,fs)


y1 = signal.filtfilt(b1, a1, y_g)
y2 = signal.filtfilt(b2, a2, y_g)
y3 = signal.filtfilt(b3, a3, y_g)
y4 = signal.filtfilt(b4, a4, y_g)
y5 = signal.filtfilt(b5, a5, y_g)

energiaFi1ter1=0
energiaFi1ter2=0
energiaFi1ter3=0
energiaFi1ter4=0
energiaFi1ter5=0


for i in range(0,len(x)):
    energiaFi1ter1 = energiaFi1ter1 +  np.abs(y1[i])
    energiaFi1ter2 = energiaFi1ter2 +  np.abs(y2[i])
    energiaFi1ter3 = energiaFi1ter3 +  np.abs(y3[i])
    energiaFi1ter4 = energiaFi1ter4 +  np.abs(y4[i])
    energiaFi1ter5 = energiaFi1ter5 +  np.abs(y5[i])

print('La potencia del filtro 1 es:', energiaFi1ter1)
print('La potencia del filtro 2 es:', energiaFi1ter2)
print('La potencia del filtro 3 es:', energiaFi1ter3)
print('La potencia del filtro 4 es:', energiaFi1ter4)
print('La potencia del filtro 5 es:', energiaFi1ter5)

EnergiaTotal = energiaFi1ter1+energiaFi1ter2+energiaFi1ter3+energiaFi1ter4+energiaFi1ter5
print('La potencia del total es:', EnergiaTotal)

##############Calculo de Porcentajes######################

P = EnergiaFiltroGeneral/EnergiaInit
P1=energiaFi1ter1/EnergiaFiltroGeneral
P2=energiaFi1ter2/EnergiaFiltroGeneral
P3=energiaFi1ter3/EnergiaFiltroGeneral
P4=energiaFi1ter4/EnergiaFiltroGeneral
P5=energiaFi1ter5/EnergiaFiltroGeneral

Porcentajes = [P1, P2, P3, P4, P5]
print(Porcentajes)

G= [0, 0, 0, 0, 0]

for i in range(0,5):
    if Porcentajes[i]>0.25:
        G[i]=1
    
y_final = G[0]*y1+G[1]*y2+G[2]*y3+G[3]*y4+G[4]*y5
wav.write('PY_Salida ejercicio 1.wav', fs, y_final.astype(np.int16)) 

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

wt=w1+w2+w3+w4+w5
ht=h1+h2+h3+h4+h5

plt.figure(7)
plt.plot(wt,abs(ht))
plt.title('RELACION TOTAL DE FILTROS ')
plt.show()