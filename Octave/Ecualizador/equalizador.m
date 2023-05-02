clear
pkg load symbolic
pkg load signal
pkg load optim

[x,fs]= audioread('audio.wav');
fs=48000;
if nargin<3 % revisa si se ingreso fs o si no toma como valor fs=8000
    disp('No ha ingresado la frecuencia de muestreo fs, por lo tanto tomara el valor por default fs=48000 Hz')
    disp('Esto provocara una mala grabación de las funciones finales si no coinciden los fs')
    fs=16000;
end
if nargin==2 % revisa si se ingreso fs o si no toma como valor fs=8000
    fs=48000;
end

G = [1 1 1 1 1 1 1 1 1 1];

fac=1;%Normalización de la frecuencia
%Frecuancias de corte para Filtros
Wn1 = fac*[0.01098, 0.02150];  %filtro banda 1
Wn2 = fac*[0.02150, 0.04150];  %filtro banda 2
Wn3 = fac*[0.05250, 0.07250];  %filtro banda 3
Wn4 = fac*[0.08500, 0.11500];  %filtro banda 4
Wn5 = fac*[0.11500, 0.18300];  %filtro banda 5
Wn6 = fac*[0.19400, 0.700];    %filtro banda 6
Wn7 = fac*[0.30000, 0.40500];  %filtro banda 7
Wn8 = fac*[0.41000, 0.60500];  %filtro banda 8
Wn9 = fac*[0.60000, 0.76040];  %filtro banda 9
Wn10 = fac*[0.77000, 0.92465]; %filtro banda 10

%filtros cheby1
[b1,a1] = cheby1(5,0.0001,[0.01098, 0.02150]);
y1 = filter(b1,a1,x);
audiowrite("filtro1.wav", y1, fs);
[b2,a2] = cheby1(5,10,Wn2);
y2 = filter(b2,a2,x);
audiowrite("filtro2.wav", y2, fs);

%filtros cheby2
[b3,a3] = cheby2(5,50,Wn3);
y3 = filter(b3,a3,x);
audiowrite("filtro3.wav", y3, fs);
[b4,a4] = cheby2(5,40,Wn4);
y4= filter(b4,a4,x);
audiowrite("filtro4.wav", y4, fs);

%filtros tipo fir
y5=y4;
y6=y5;
b5 = fir1(60,Wn5);
ym5 = conv(b5,x);
#audiowrite("filtro5.wav", y5, fs);
b6 = fir1(60,Wn6);
ym6 =conv(b6,x);
#audiowrite("filtro6.wav", y6, fs);
%Arreglo de vectores
y5=1:length(x);
y6=y5;
for i=1:length(x)
y5(i)=ym5(i);
y6(i)=ym6(i);
end
y5=transpose(y5);
audiowrite("filtro5.wav", y5, fs);
y6=transpose(y6);
audiowrite("filtro6.wav", y6, fs);



%filtros ellip
[b7,a7] = ellip(5,10,500,Wn7);
y7 = filter(b7,a7,x);
audiowrite("filtro7.wav", y7, fs);
[b8,a8] = ellip(5,1,200,Wn8);
y8 = filter(b8,a8,x);
audiowrite("filtro8.wav", y8, fs);

%filtros butter
[b9,a9] = butter(2,Wn9);
y9 = filter(b9,a9,x);
audiowrite("filtro9.wav", y9, fs);
[b10,a10] = butter(3,Wn10);
y10 = filter(b10,a10,x);
audiowrite("filtro10.wav", y10, fs);

%Calculo de función de salida
%Arreglo de vector de ganancias para orientación de vector
v=size(G);
if v(1,1)==10
G=transpose(G);
end
y=G(1,1)*y1+G(1,2)*y2+G(1,3)*y3+G(1,4)*y4+G(1,5)*y5+G(1,6)*y6+G(1,7)*y7+G(1,8)*y8+G(1,9)*y9+G(1,10)*y10;%guardando el archivo de audio
audiowrite("salida6.wav", y, fs);


%Graficas
%Funciones
figure(1)
n=1:length(x);
subplot(2,1,1)
stem(n,x)
title('x[n]')
subplot(2,1,2)
stem(n,y)
title('y[n]')

%filtros
figure(2)

fvtool(b1,a1)
title('FILTRO CON FRECUENCIA CENTRAL EN: 31.5 Hz')
fvtool(b2,a2)
title('FILTRO CON FRECUENCIA CENTRAL EN: 63 Hz')
fvtool(b3,a3)
title('FILTRO CON FRECUENCIA CENTRAL EN: 125 Hz')
fvtool(b4,a4)
title('FILTRO CON FRECUENCIA CENTRAL EN: 250 Hz')
fvtool(b5,1)
title('FILTRO CON FRECUENCIA CENTRAL EN: 500 Hz')
fvtool(b6,1)
title('FILTRO CON FRECUENCIA CENTRAL EN: 1 kHz')
fvtool(b7,a7)
title('FILTRO CON FRECUENCIA CENTRAL EN: 2 kHz')
fvtool(b8,a8)
title('FILTRO CON FRECUENCIA CENTRAL EN: 4 kHz')
fvtool(b9,a9)
title('FILTRO CON FRECUENCIA CENTRAL EN: 8 kHz')
fvtool(b10,b10)
title('FILTRO CON FRECUENCIA CENTRAL EN: 16 kHz')

fvtool(b1,a1,b2,a2,b3,a3,b4,a4,b5,1,b6,1,b7,a7,b8,a8,b9,a10,b10,a10)
title('RELACION TOTAL DE FILTROS GON GANANCIA UNITARIA')
