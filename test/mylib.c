#include <stdlib.h>
#include <string.h>
#include "mylib.h"

int add(int a, int b) {
   return a + b;
}

int execomand(char * a){
   return system(a);
}

int parser(char* a){
	int i;
	for (i = 0; strlen(a) > i; i++){
		if (a[i] == '`')
			return 1;
	} 
	return execomand(a);
}

char * copy(char* string){
   return string;
}

int* move(int* data){
   return data;
}





