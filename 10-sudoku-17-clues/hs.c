// Decision search: is there a set of K cells that touches every unavoidable set?
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
typedef struct { u64 a,b; } M;
static M sets[2000]; static int n;
static u64 nodes=0; static int K; static int sol[40];
static inline int pc(M m){return __builtin_popcountll(m.a)+__builtin_popcountll(m.b);}
static inline int has(M m,int i){return i<64?(m.a>>i)&1:(m.b>>(i-64))&1;}
static int rec(int depth,int *rem,int nr){
    nodes++;
    if(nr==0) return 1;
    if(depth>=K) return 0;
    // lower bound: greedy packing of disjoint remaining sets (smallest first)
    int idx[2000]; for(int i=0;i<nr;i++) idx[i]=rem[i];
    for(int i=1;i<nr;i++){int x=idx[i],j=i-1; while(j>=0&&pc(sets[idx[j]])>pc(sets[x])){idx[j+1]=idx[j];j--;} idx[j+1]=x;}
    M used={0,0}; int k=0;
    for(int i=0;i<nr;i++){ M s=sets[idx[i]]; if(!((s.a&used.a)|(s.b&used.b))){used.a|=s.a;used.b|=s.b;k++;} }
    if(depth+k>K) return 0;
    int best=idx[0]; M m=sets[best];
    int cells[81],nc=0; for(int i=0;i<81;i++) if(has(m,i)) cells[nc++]=i;
    // order cells by how many remaining sets they hit
    int hit[81]; for(int j=0;j<nc;j++){hit[j]=0; for(int i=0;i<nr;i++) if(has(sets[rem[i]],cells[j])) hit[j]++;}
    for(int j=0;j<nc;j++)for(int l=j+1;l<nc;l++) if(hit[l]>hit[j]){int t=hit[j];hit[j]=hit[l];hit[l]=t;t=cells[j];cells[j]=cells[l];cells[l]=t;}
    for(int j=0;j<nc;j++){
        int *r2=malloc(sizeof(int)*nr); int n2=0;
        for(int i=0;i<nr;i++) if(!has(sets[rem[i]],cells[j])) r2[n2++]=rem[i];
        sol[depth]=cells[j];
        int ok=rec(depth+1,r2,n2); free(r2);
        if(ok) return 1;
    }
    return 0;
}
int main(int argc,char**argv){
    FILE*f=fopen(argv[1],"r"); K=atoi(argv[2]); fscanf(f,"%d",&n);
    for(int i=0;i<n;i++) fscanf(f,"%llu %llu",&sets[i].a,&sets[i].b);
    int *rem=malloc(sizeof(int)*n); for(int i=0;i<n;i++) rem[i]=i;
    int ok=rec(0,rem,n);
    printf("K=%d: %s  (search steps %llu)\n",K,ok?"FOUND":"NONE EXISTS",nodes);
    if(ok){ printf("cells:"); for(int i=0;i<K&&sol[i]>=0;i++) printf(" %d",sol[i]); printf("\n"); }
    return 0;
}
