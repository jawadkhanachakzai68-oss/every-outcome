// BFS of the 3x3x3 cube group in the half-turn metric (18 moves), depth <= MAXD, counting distinct positions.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u128;
enum {URF,UFL,ULB,UBR,DFR,DLF,DBL,DRB};
enum {UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR};
struct C{ int cp[8],co[8],ep[12],eo[12]; };
C mk(initializer_list<int> cp,initializer_list<int> co,initializer_list<int> ep,initializer_list<int> eo){
  C c; int i=0; for(int x:cp)c.cp[i++]=x; i=0; for(int x:co)c.co[i++]=x; i=0; for(int x:ep)c.ep[i++]=x; i=0; for(int x:eo)c.eo[i++]=x; return c;}
C mul(const C&a,const C&b){ C r; for(int i=0;i<8;i++){r.cp[i]=a.cp[b.cp[i]]; r.co[i]=(a.co[b.cp[i]]+b.co[i])%3;}
  for(int i=0;i<12;i++){r.ep[i]=a.ep[b.ep[i]]; r.eo[i]=(a.eo[b.ep[i]]+b.eo[i])%2;} return r;}
static inline u128 enc(const C&c){ u128 k=0; for(int i=0;i<8;i++){k=(k<<3)|c.cp[i]; k=(k<<2)|c.co[i];} for(int i=0;i<12;i++){k=(k<<4)|c.ep[i]; k=(k<<1)|c.eo[i];} return k;}
static inline C dec(u128 k){ C c; for(int i=11;i>=0;i--){c.eo[i]=k&1;k>>=1;c.ep[i]=k&15;k>>=4;} for(int i=7;i>=0;i--){c.co[i]=k&3;k>>=2;c.cp[i]=k&7;k>>=3;} return c;}
int main(int argc,char**argv){
  int MAXD=argc>1?atoi(argv[1]):7;
  C id=mk({0,1,2,3,4,5,6,7},{0,0,0,0,0,0,0,0},{0,1,2,3,4,5,6,7,8,9,10,11},{0,0,0,0,0,0,0,0,0,0,0,0});
  C U=mk({UBR,URF,UFL,ULB,DFR,DLF,DBL,DRB},{0,0,0,0,0,0,0,0},{UB,UR,UF,UL,DR,DF,DL,DB,FR,FL,BL,BR},{0,0,0,0,0,0,0,0,0,0,0,0});
  C R=mk({DFR,UFL,ULB,URF,DRB,DLF,DBL,UBR},{2,0,0,1,1,0,0,2},{FR,UF,UL,UB,BR,DF,DL,DB,DR,FL,BL,UR},{0,0,0,0,0,0,0,0,0,0,0,0});
  C F=mk({UFL,DLF,ULB,UBR,URF,DFR,DBL,DRB},{1,2,0,0,2,1,0,0},{UR,FL,UL,UB,DR,FR,DL,DB,UF,DF,BL,BR},{0,1,0,0,0,1,0,0,1,1,0,0});
  C D=mk({URF,UFL,ULB,UBR,DLF,DBL,DRB,DFR},{0,0,0,0,0,0,0,0},{UR,UF,UL,UB,DF,DL,DB,DR,FR,FL,BL,BR},{0,0,0,0,0,0,0,0,0,0,0,0});
  C L=mk({URF,ULB,DBL,UBR,DFR,UFL,DLF,DRB},{0,1,2,0,0,2,1,0},{UR,UF,BL,UB,DR,DF,FL,DB,FR,UL,DL,BR},{0,0,0,0,0,0,0,0,0,0,0,0});
  C B=mk({URF,UFL,UBR,DRB,DFR,DLF,ULB,DBL},{0,0,1,2,0,0,2,1},{UR,UF,UL,BR,DR,DF,DL,BL,FR,FL,UB,DB},{0,0,0,1,0,0,0,1,0,0,1,1});
  vector<C> mv; C base[6]={U,R,F,D,L,B};
  for(int f=0;f<6;f++){ C p=base[f]; for(int q=0;q<3;q++){ mv.push_back(p); p=mul(p,base[f]); } }
  // sanity: each base has order 4
  for(int f=0;f<6;f++){ C p=base[f]; for(int q=0;q<3;q++) p=mul(p,base[f]); if(enc(p)!=enc(id)){fprintf(stderr,"bad move %d\n",f);return 1;} }
  vector<u128> prev2, prev, cur; cur.push_back(enc(id));
  printf("depth 0: 1\n"); fflush(stdout);
  for(int d=1; d<=MAXD; d++){
    vector<u128> nxt; nxt.reserve(cur.size()*14);
    for(u128 k: cur){ C c=dec(k); for(auto&m:mv) nxt.push_back(enc(mul(c,m))); }
    sort(nxt.begin(),nxt.end()); nxt.erase(unique(nxt.begin(),nxt.end()),nxt.end());
    auto rm=[&](const vector<u128>&old){ vector<u128> o; o.reserve(nxt.size()); size_t j=0; for(u128 x:nxt){ while(j<old.size()&&old[j]<x)j++; if(j<old.size()&&old[j]==x) continue; o.push_back(x);} nxt.swap(o); };
    if(d>=1){ vector<u128> s=cur; sort(s.begin(),s.end()); rm(s); }
    if(d>=2){ vector<u128> s=prev; sort(s.begin(),s.end()); rm(s); }
    printf("depth %d: %zu\n",d,nxt.size()); fflush(stdout);
    prev2.swap(prev); prev=cur; cur=nxt;
  }
}
