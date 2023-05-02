clear
pkg load symbolic
pkg load signal
pkg load optim

[x,fs]= audioread('audio.wav');
energiaInit = 0;

fs = 16000;

for i=1:length(x)
    energiaInit = energiaInit + (sqrt(x(i,1)*x(i,1)));
endfor
disp('La energia de la entrada es:');
disp(energiaInit);
disp(' ');


Wc_init = [0.2, 0.5];   #Frecuencia de corte 2KHz-5Khz
[b,a] = butter(20,Wc_init);
y = filter(b,a,x); #salida de filtro pasa bandas

#Y1 = abs(fft(y,length(x)));

energiaFilterGeneral = 0;
for i=1:length(x)
    energiaFilterGeneral = energiaFilterGeneral + sqrt(y(i,1)*y(i,1));
endfor

disp('La energia de la entrada con pasa bandas es:');
disp(energiaFilterGeneral);
disp(' ');


fac=1;
Wn1 = fac*[0.2 , 0.26];
Wn2 = fac*[0.26 , 0.32];
Wn3 = fac*[0.32 , 0.38];
Wn4 = fac*[0.38 , 0.44];
Wn5 = fac*[0.44 , 0.50];


[b1,a1] = butter(10,Wn1);%filtro banda 1
[b2,a2] = butter(10,Wn2);%filtro banda 2
[b3,a3] = butter(10,Wn3);%filtro banda 3
[b4,a4] = butter(10,Wn4);%filtro banda 4
[b5,a5] = butter(10,Wn5);%filtro banda 5


y1=filter(b1,a1,y);
y2=filter(b2,a2,y);
y3=filter(b3,a3,y);
y4=filter(b4,a4,y);
y5=filter(b5,a5,y);

energiaFi1ter1=0;
energiaFi1ter2=0;
energiaFi1ter3=0;
energiaFi1ter4=0;
energiaFi1ter5=0;

for i=1:length(x)
    energiaFi1ter1 = energiaFi1ter1 + sqrt(y1(i,1)*y1(i,1));
    energiaFi1ter2 = energiaFi1ter2 + sqrt(y2(i,1)*y2(i,1));
    energiaFi1ter3 = energiaFi1ter3 + sqrt(y3(i,1)*y3(i,1));
    energiaFi1ter4 = energiaFi1ter4 + sqrt(y4(i,1)*y4(i,1));
    energiaFi1ter5 = energiaFi1ter5 + sqrt(y5(i,1)*y5(i,1));
endfor

disp('La energia de la señal de salida del primer filtro pasa bandas es:');
disp(energiaFi1ter1);
disp(' ');
disp('La energia de la señal de salida del segundo filtro pasa bandas es:');
disp(energiaFi1ter2);
disp(' ');
disp('La energia de la señal de salida del tercer filtro pasa bandas es:');
disp(energiaFi1ter3);
disp(' ');
disp('La energia de la señal de salida del cuarto filtro pasa bandas es:');
disp(energiaFi1ter4);
disp(' ');
disp('La energia de la señal de salida del quinto filtro pasa bandas es:');
disp(energiaFi1ter5);
disp(' ');


E_Total=(energiaFi1ter1+energiaFi1ter2+energiaFi1ter3+energiaFi1ter4+energiaFi1ter5);
disp('La energia total de todos los filtros es:');
disp(E_Total);
disp(' ');

#Calculo de Porcentajes
P=energiaFilterGeneral/energiaInit;
P1=energiaFi1ter1/energiaFilterGeneral;
P2=energiaFi1ter2/energiaFilterGeneral;
P3=energiaFi1ter3/energiaFilterGeneral;
P4=energiaFi1ter4/energiaFilterGeneral;
P5=energiaFi1ter5/energiaFilterGeneral;

Porcentajes = [P1, P2, P3, P4, P5];
disp('Porcentajes:');
disp(Porcentajes);

y=y1+y2+y3+y4+y5;
%Calculo de coeficientes para eleminicación bandas en audio, si la banda es aceptada el coeficiente será 1 y si no será 0
G=1:5; %definción de vector de coeficnetes
G=0*G;
for i=1:5
    if Porcentajes(i)>.25 %porcentaje de acepatación
        G(i)=1; %ganancia unitaria
    endif
endfor

yfinal=G(1)*y1+G(2)*y2+G(3)*y3+G(4)*y4+G(5)*y5;
audiowrite("salida_inciso1.wav", yfinal, fs);


figure(1)
n=1:length(x);
subplot(3,1,1)
stem(n,x)
title('x[n]')
subplot(3,1,2)
stem(n,y)
title('y[n]')
subplot(3,1,3)
stem(n,yfinal)
title('yfinal')

fvtool(b,a)
title('FILTRO PARA BANDA PRINCIAPAL (2.0-5.0)KHz')
%Filtros aplicados a la banda
fvtool(b1,a1)
title('PRIMER FILTRO: (2.0-2.6)KHz')
fvtool(b2,a2)
title('SEGUNDO FILTRO: (2.6-3.2)KHz')
fvtool(b3,a3)
title('TERCER FILTRO: (3.2-3.8)KHz')
fvtool(b4,a4)
title('CUARTO FILTRO: (3.8-4.2)KHz')
fvtool(b5,a5)
title('QUINTO FILTRO: (4.2-5.0)KHz')
fvtool(b,a,b1,a1,b2,a2,b3,a3,b4,a4,b5,a5)
title('RELACION TOTAL DE FILTROS')

