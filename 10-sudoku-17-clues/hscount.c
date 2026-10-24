// Counts the K-cell groups that touch every unavoidable set (exactly, no duplicates).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
typedef unsigned __int128 u128;
typedef struct { u64 a,b; } M;
static M sets[4000]; static int n; static int K;
static u128 total=0; static u64 leaves=0;
static double C[90][90];
static u128 Ci[90][90];
static inline int pc(M m){return __builtin_popcountll(m.a)+__builtin_popcountll(m.b);}
static inline int has(M m,int i){return i<64?(m.a>>i)&1:(m.b>>(i-64))&1;}
static void rec(int depth,M forb,int *rem,int nr,int nforb){
    if(nr==0){ leaves++; int free_=81-depth-nforb; int need=K-depth; if(need>=0&&free_>=need) total+=Ci[free_][need]; return; }
    if(depth>=K) return;
    { int idx[4000]; for(int i=0;i<nr;i++) idx[i]=rem[i];
      for(int i=1;i<nr;i++){int x=idx[i],j=i-1; while(j>=0&&pc(sets[idx[j]])>pc(sets[x])){idx[j+1]=idx[j];j--;} idx[j+1]=x;}
      M used={0,0}; int k=0;
      for(int i=0;i<nr;i++){ M q=sets[idx[i]]; if(!((q.a&used.a)|(q.b&used.b))){used.a|=q.a;used.b|=q.b;k++;} }
      if(depth+k>K) return; }
    // choose uncovered set with fewest allowed cells
    int best=-1,bc=999;
    for(int i=0;i<nr;i++){ M s=sets[rem[i]]; M al={s.a&~forb.a,s.b&~forb.b}; int c=pc(al); if(c<bc){bc=c;best=rem[i];} }
    if(bc==0) return;
    M s=sets[best]; int cells[81],nc=0; for(int i=0;i<81;i++) if(has(s,i)&&!has(forb,i)) cells[nc++]=i;
    M f2=forb; int nf=nforb;
    for(int j=0;j<nc;j++){
        int *r2=malloc(sizeof(int)*nr); int n2=0;
        for(int i=0;i<nr;i++) if(!has(sets[rem[i]],cells[j])) r2[n2++]=rem[i];
        rec(depth+1,f2,r2,n2,nf); free(r2);
        if(cells[j]<64) f2.a|=1ULL<<cells[j]; else f2.b|=1ULL<<(cells[j]-64); nf++;
    }
}
int main(int argc,char**argv){
    FILE*f=fopen(argv[1],"r"); K=atoi(argv[2]); if(fscanf(f,"%d",&n)!=1) return 1;
    for(int i=0;i<n;i++) if(fscanf(f,"%llu %llu",&sets[i].a,&sets[i].b)!=2) return 1;
    for(int i=0;i<90;i++){Ci[i][0]=1; for(int j=1;j<=i;j++) Ci[i][j]=Ci[i-1][j-1]+(j<=i-1?Ci[i-1][j]:0);}
    int *rem=malloc(sizeof(int)*n); for(int i=0;i<n;i++) rem[i]=i;
    M z={0,0}; rec(0,z,rem,n,0);
    u64 hi=(u64)(total/1000000000000000000ULL), lo=(u64)(total%1000000000000000000ULL);
    if(hi) printf("K=%d: %llu%018llu groups touch every set (%llu search leaves)\n",K,hi,lo,leaves);
    else printf("K=%d: %llu groups touch every set (%llu search leaves)\n",K,lo,leaves);
    return 0;
}
