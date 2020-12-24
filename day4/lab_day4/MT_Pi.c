#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int Nthreads;
int myid[100];
long int N;
double sum[100];
pthread_t tid[200];

double h;

void *mycpi(void *arg) {
  int myrank;
  int i, j;
  double x;
  
  myrank = *(int *)arg;

  h   = 1.0 / (double) N;
  sum[myrank] = 0.0;

  for (i = N/Nthreads*myrank+1; i <= N/Nthreads*(myrank+1); i ++) {
    x = h * ((double)i - 0.5);
    sum[myrank] += 4.0 / (1.0 + x*x);
  }
}


int main(int argc, char *argv[])
{
  int done = 0,  numprocs, i, rc;
  double PI25DT = 3.141592653589793238462643;
  double mypi, pi, h, x, a;
 
  /*
  if (argc != 2) {
    printf("Usage: a.out N\n");
    exit(0);
  }
  */

  if (argc > 2) {
    N = atoi(argv[2]);
    Nthreads = atoi(argv[1]);
  } else if (argc > 1) {
    N = 1000000000;
    Nthreads = atoi(argv[1]);
  } else {N=1000; Nthreads = 1;}


  for (i=0; i<Nthreads; i++) {
    myid[i] = i;
    pthread_create(&tid[i], NULL, &mycpi, &myid[i]);
  } 

  for (i=0; i<Nthreads; i++) {
    pthread_join(tid[i], NULL);
  } 

  h   = 1.0 / (double) N;

  mypi = 0;
  for (i=0; i<Nthreads; i++) {
    mypi += h * sum[i];
  }

  printf("pi is approximately %.16f, Error is %.16f\n", mypi, fabs(mypi - PI25DT));
  return 0;
}
