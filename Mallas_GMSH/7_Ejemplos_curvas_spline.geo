// Curva del seno entre 0 y 2Pi:
x = 0;

For i In {1:61}
    Point(i) = {x, Sin(x), 0};
    x += Pi/30;
EndFor

Spline(1) = {1:61};

//------------------------------------------------
// Curva polar rosa de 4 pétalos:
y = 3;

t = 0;

For i In {100:161}
    r = Sin(2*t);
    Point(i) = {r*Cos(t), r*Sin(t) + y, 0};
    t += Pi/30;
EndFor

Spline(2) = {100:161};

//-------------------------------------------------
// Curva polar Nefroide de Freeth:
x = 6;
y = 5;

t = 0;

For i In {200:261}
    r = 1 + 2*Sin(t/2);
    Point(i) = {r*Cos(t) + x, r*Sin(t) + y, 0};
    t += Pi/15;
EndFor

Spline(3) = {200:261};
