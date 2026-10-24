// Counts every completed 9x9 Sudoku grid with the "bands" method.
// grid = 3 bands of 3 rows. Fix band 1 (one of the classes in band_classes.txt),
// try every band 2, and count the band 3 fills that finish the grid. Digits are 0..8.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
typedef unsigned long long u64;
#define HSIZE (1<<22)
typedef struct { uint16_t k[9]; u64 v; uint8_t used; } Ent;
static Ent *tab; static u64 nkeys=0;

static u64 rec3(const uint16_t *L,int pos,int *rm,int *bm,int *cu){
    if(pos==27) return 1;
    int r=pos/9,c=pos%9,b=c/3; u64 n=0;
    int avail=L[c]&~rm[r]&~bm[b]&~cu[c];
    while(avail){ int bit=avail&-avail; avail^=bit;
        rm[r]|=bit; bm[b]|=bit; cu[c]|=bit;
        n+=rec3(L,pos+1,rm,bm,cu);
        rm[r]^=bit; bm[b]^=bit; cu[c]^=bit; }
    return n;
}
static int cmp16(const void*a,const void*b){return (int)*(uint16_t*)a-(int)*(uint16_t*)b;}
static u64 band3(const uint16_t *L){
    uint16_t s[3][3]; 
    for(int k=0;k<3;k++){ for(int j=0;j<3;j++) s[k][j]=L[k*3+j]; qsort(s[k],3,2,cmp16); }
    // sort the three stacks
    for(int a=0;a<3;a++)for(int b=a+1;b<3;b++) if(memcmp(s[a],s[b],6)>0){uint16_t t[3];memcpy(t,s[a],6);memcpy(s[a],s[b],6);memcpy(s[b],t,6);}
    uint16_t key[9]; memcpy(key,s,18);
    u64 h=1469598103934665603ULL; for(int i=0;i<9;i++){h^=key[i];h*=1099511628211ULL;}
    u64 i=h&(HSIZE-1);
    while(tab[i].used){ if(!memcmp(tab[i].k,key,18)) return tab[i].v; i=(i+1)&(HSIZE-1);}
    int rm[3]={0,0,0}, bm[3]={0,0,0}, cu[9]={0};
    u64 v=rec3(key,0,rm,bm,cu);
    memcpy(tab[i].k,key,18); tab[i].v=v; tab[i].used=1; nkeys++;
    return v;
}
static int colm[9], rowm[3], boxm[3];
static u64 total_for_band1;
static u64 nband2; static int first0=0;
static void rec2(int pos){
    if(pos==27){ uint16_t L[9]; for(int c=0;c<9;c++) L[c]=(~colm[c])&0x1FF; total_for_band1+=band3(L); nband2++; return; }
    int r=pos/9,c=pos%9,b=c/3;
    int avail=0x1FF&~rowm[r]&~colm[c]&~boxm[b];
    if(c==0 && r>0) avail&=~((first0<<1)-1);   // rows of band 2 in increasing order of first digit (x6 later)
    while(avail){ int bit=avail&-avail; avail^=bit;
        int save0=first0; if(c==0) first0=bit;
        rowm[r]|=bit; colm[c]|=bit; boxm[b]|=bit;
        rec2(pos+1); first0=save0;
        rowm[r]^=bit; colm[c]^=bit; boxm[b]^=bit; }
}
int main(int argc,char**argv){
    tab=calloc(HSIZE,sizeof(Ent));
    FILE*f=fopen(argv[1],"r"); int w; int d[27]; u128 sum=0; int ncls=0; u64 totb2=0;
    int stride=argc>2?atoi(argv[2]):1, off=argc>3?atoi(argv[3]):0; int limit=1<<30; int idx=0;
    while(ncls<limit && fscanf(f,"%d",&w)==1){
        for(int i=0;i<27;i++) if(fscanf(f,"%d",&d[i])!=1) return 1;
        if(idx++%stride!=off) continue;
        for(int c=0;c<9;c++){colm[c]=0; for(int r=0;r<3;r++) colm[c]|=1<<d[r*9+c];}
        rowm[0]=rowm[1]=rowm[2]=0; boxm[0]=boxm[1]=boxm[2]=0;
        total_for_band1=0; nband2=0; rec2(0);
        total_for_band1*=6; nband2*=6; sum+=(u128)w*total_for_band1; totb2+=nband2; ncls++;
        if(ncls%10==0) fprintf(stderr,"class %d weight %d band2 options %llu completions %llu\n",ncls,w,nband2,total_for_band1);
    }
    u128 grids=sum;
    char buf[64]; int n=0; u128 x=grids; if(!x) buf[n++]='0'; while(x){buf[n++]='0'+(int)(x%10); x/=10;}
    printf("classes %d  distinct band-3 shapes %llu\n",ncls,nkeys);
    printf("PARTIAL SUM (before the x 9! for renaming digits) = "); for(int i=n-1;i>=0;i--) putchar(buf[i]); putchar('\n');
    return 0;
}
