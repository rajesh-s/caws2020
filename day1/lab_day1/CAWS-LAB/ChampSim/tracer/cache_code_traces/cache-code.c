#include<stdlib.h>
#include<stdio.h>
#include<assert.h>

#define LOGSIZE 23

int access[1L << LOGSIZE];
int main(int argc, char** argv)
{
	assert(argc == 2);
	int logsize = atoi(argv[1]);
	logsize -= 2;
	assert(logsize < LOGSIZE);
	printf("Building for array with logsize %d\n", logsize+2);
	register int size = 1L << logsize;
	for(int i = 0; i < size; i += 32)
		access[i] = (i+32)%size;
	register int j = 0;
	
	while(1)
	{
		j = *(access+j);
	}
	
/* 	register int i = 0;
	volatile int k = 0; 
 	while(1)
 	{
 		for(i = 0; i < size; i += 32)
 		{
 			k = *(access+i);
 		}
	}
*/	
}
