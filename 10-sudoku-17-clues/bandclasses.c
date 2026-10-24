// Lists every valid top band (row 1 = 1..9), then merges bands that are the same up to
// swapping rows inside the band, columns inside a stack, whole stacks, and renaming digits.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static u64 *keys; static int nb=0;
static int R[3][9];
static int boxm[3], colm[9], rowm[3];
static u64 enc(int r[3][9]){ // rename digits so row 0 = 0..8, then base-9 key of rows 1 and 2
    int m[9]; for(int c=0;c<9;c++) m[r[0][c]]=c;
    u64 k=0; for(int i=1;i<3;i++)for(int c=0;c<9;c++) k=k*9+m[r[i][c]]; return k; }
static void dec(u64 k,int r[3][9]){ for(int c=0;c<9;c++) r[0][c]=c;
    for(int i=2;i>=1;i--)for(int c=8;c>=0;c--){ r[i][c]=k%9; k/=9; } }
static int cmpu(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
static void rec(int p){
    if(p==27){ keys[nb++]=enc(R); return; }
    int r=p/9,c=p%9,b=c/3;
    int avail=0x1FF&~rowm[r]&~colm[c]&~boxm[b];
    while(avail){ int bit=avail&-avail; avail^=bit; int d=__builtin_ctz(bit);
        R[r][c]=d; rowm[r]|=bit; colm[c]|=bit; boxm[b]|=bit;
        rec(p+1);
        rowm[r]^=bit; colm[c]^=bit; boxm[b]^=bit; }
}
static int *par; static int NB;
static int find(int x){ while(par[x]!=x){par[x]=par[par[x]];x=par[x];} return x; }
static int look(u64 k){ int lo=0,hi=NB-1; while(lo<=hi){int m=(lo+hi)/2; if(keys[m]==k) return m; if(keys[m]<k) lo=m+1; else hi=m-1;} return -1; }
int main(){
    keys=malloc(sizeof(u64)*3000000);
    for(int c=0;c<9;c++){R[0][c]=c; colm[c]|=1<<c; boxm[c/3]|=1<<c; rowm[0]|=1<<c;}
    rec(9);
    fprintf(stderr,"%d top bands with row 1 fixed\n",nb);
    qsort(keys,nb,sizeof(u64),cmpu); NB=nb;
    par=malloc(sizeof(int)*nb); for(int i=0;i<nb;i++) par[i]=i;
    int rowsw[2][2]={{0,1},{1,2}};
    int sw[6][2]={{0,1},{1,2},{3,4},{4,5},{6,7},{7,8}};
    for(int i=0;i<nb;i++){
        int B[3][9]; dec(keys[i],B);
        for(int g=0;g<10;g++){
            int T[3][9]; memcpy(T,B,sizeof(T));
            if(g<2){ int a=rowsw[g][0],b=rowsw[g][1]; for(int c=0;c<9;c++){int t=T[a][c];T[a][c]=T[b][c];T[b][c]=t;} }
            else if(g<8){ int a=sw[g-2][0],b=sw[g-2][1]; for(int r=0;r<3;r++){int t=T[r][a];T[r][a]=T[r][b];T[r][b]=t;} }
            else { int s0=(g==8)?0:1, s1=s0+1; for(int r=0;r<3;r++)for(int k=0;k<3;k++){int t=T[r][s0*3+k];T[r][s0*3+k]=T[r][s1*3+k];T[r][s1*3+k]=t;} }
            int j=look(enc(T)); if(j<0){fprintf(stderr,"lookup failed\n");return 1;}
            int a=find(i),b=find(j); if(a!=b) par[a]=b;
        }
    }
    int *cnt=calloc(nb,sizeof(int)); for(int i=0;i<nb;i++) cnt[find(i)]++;
    int ncls=0; for(int i=0;i<nb;i++) if(cnt[i]) ncls++;
    fprintf(stderr,"%d classes\n",ncls);
    for(int i=0;i<nb;i++) if(find(i)==i){ int B[3][9]; dec(keys[i],B); printf("%d",cnt[i]); for(int r=0;r<3;r++)for(int c=0;c<9;c++) printf(" %d",B[r][c]); printf("\n"); }
    return 0;
}
