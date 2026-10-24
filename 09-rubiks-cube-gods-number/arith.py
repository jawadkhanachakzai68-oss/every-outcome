from math import factorial as f, comb
G=f(8)*3**7*f(12)//2*2**11 ; G2=(f(8)*3**7)*(f(12)*2**12)//12   # cube group order two ways
G=f(8)*f(12)*3**8*2**12//12
H=f(8)*f(8)*f(4)//2
cos=G//H
print('G',G, 'formula 8!*12!*3^8*2^12/12'); assert G==43252003274489856000
print('H',H); assert H==19508428800
print('G/H',cos, G%H); assert cos==2217093120 and G%H==0
print('3^7*2^11*C(12,4)=',3**7*2**11*comb(12,4)); assert 3**7*2**11*comb(12,4)==cos
print('cosets/16 (naive)',cos/16,' exact classes 138639780 (burnside)')
print('cosets/138639780',cos/138639780)
sets=55882296
print('positions per set (G/55,882,296)=',G/sets)
print('time: 55,882,296 sets x 20 s =',sets*20,'s =',sets*20/(365.25*86400),'years')
print('cube20: ~1.1e9 s ->',1.1e9/(365.25*86400),'years')
for r in (1e6,1e9):
    print('check one position at %g per second: %.3g years'%(r,G/r/(365.25*86400)))
print('48*2=',48*2,' G/96=',G/96)
print('growth ratios',[round(b/a,2) for a,b in zip([1,18,243,3240,43239,574908,7618438],[18,243,3240,43239,574908,7618438,100803036])])
# 2x2x2
print('2x2x2 positions 7!*3^6=',f(7)*3**6)
