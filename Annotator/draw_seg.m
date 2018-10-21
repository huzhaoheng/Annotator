function Iout = draw_seg(m, Ipath)

color = [255,0,0];
se2 = strel('disk',1);
bb = m;
I = imread(Ipath);
Ir = I(:,:,3);
Ig = I(:,:,2);
Ib = I(:,:,1);
perim = bwperim(bb);
perim = imdilate(perim, se2);  
idx = find(perim>0);
Ir(idx) = color(1);
Ig(idx) = color(2);
Ib(idx) = color(3);
Iout = cat(3, Ir, Ig, Ib);