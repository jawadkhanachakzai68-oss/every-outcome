# Receipt 6: the big-number arithmetic behind the video.
from math import comb, factorial
grids=9356757911700480*362880+9026464508992512*362880
grids=(9356757911700480+9026464508992512)*362880
assert grids==6670903752021072936960
G=factorial(9)*6**8*2
print("grids:",f"{grids:,}")
print("symmetry group size (9! x 6^8 x 2):",f"{G:,}")
print("grids / group size =",grids/G,"  published essentially different:",5472730538)
print("C(81,16) =",f"{comb(81,16):,}"," C(81,17) =",f"{comb(81,17):,}")
print("naive 16-clue checks = grids x C(81,16) = %.3e"%(grids*comb(81,16)))
print("naive with symmetry  = 5,472,730,538 x C(81,16) = %.3e"%(5472730538*comb(81,16)))
print("ratio C(81,17)/C(81,16) =",comb(81,17)/comb(81,16))
# time estimates
SEC_YEAR=365.25*86400
print("paper: ~800 processor-years / 5,472,730,538 grids = %.2f s per grid"%(800*SEC_YEAR/5472730538))
mine=343.0
print("my slow version on one grid: %.0f s -> %.0f years for all grids on one core"%(mine,5472730538*mine/SEC_YEAR))
print("one grid per second at 1 core: %.1f years"%(5472730538/SEC_YEAR))
print("7 million CPU hours = %.0f years"%(7e6/24/365.25))
