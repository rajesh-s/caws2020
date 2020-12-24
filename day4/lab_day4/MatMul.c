#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUM_TYPE float
#define RANGE 100

void multiplyMatrix(NUM_TYPE *Product, NUM_TYPE *X, NUM_TYPE*Y, const int  m, const int n, const int k)
{
  int i, j, p;
  for(i=0; i<m; i++)
    {
      for(p=0; p<n; p++)
	{
	  for(j=0; j<k; j++)
	    {
	      *(Product+i*k+p) = *(Product+i*k+p) +( *(X+i*n+j) * *(Y+j*k+p) );
	    }
	}
    }
}

void populateMatrices(NUM_TYPE *A, NUM_TYPE *B, int size)
{
  int i;
  srand(getpid());
  for(i = 0; i < size; i++)
    {
      *(A+size) = rand() % RANGE;
      *(B+size) = rand() % RANGE;
    }
}

int main()
{

  NUM_TYPE *A = NULL;
  NUM_TYPE *B = NULL;
  NUM_TYPE *C = NULL;

  int m = 2000;
  int n = 2000;
  
  A = (NUM_TYPE*)malloc(m*n*sizeof(NUM_TYPE));
  B = (NUM_TYPE*)malloc(m*n*sizeof(NUM_TYPE));
  C = (NUM_TYPE*)malloc(m*n*sizeof(NUM_TYPE));
  populateMatrices(A, B, m*n);

  multiplyMatrix(C, A, B, m, n, m);
  
  free(A);
  free(B);
  free(C);
  return 0;
}
