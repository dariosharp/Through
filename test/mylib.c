#include <stdlib.h>
#include <string.h>
#include "mylib.h"

int add(int a, int b) {
   return a + b;
}

static int execomand(char * a){
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
	char *destination = malloc(strlen(string) * sizeof(char));
	strcpy(destination, string);	
   return destination;
}

char * move(char* data){
	char *destination = malloc(strlen(data) * sizeof(char));
	memmove(destination, data, strlen(data) + 1);
   return destination;
}





