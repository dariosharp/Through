#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include "mylib.h"


int main(int argc, char *argv[]) {
   int opt;   
   char * result;
	while ((opt = getopt(argc, argv, "hapcm")) != EOF) {
    	switch (opt) {
        	case 'p':
				if (argc < 3){
					printf("Error: not enough arguments\n");
					return 1;
				}
				if (parser(argv[2]) == 0){
					printf("Command Executied with success\n");
					return 0;
				}
				printf("Error: Command [%s] not correctly executed\n", argv[2]);
				return 1;	
            break;
         case 'a':
				int a = atoi(argv[2]);
				int b = atoi(argv[3]);	
            printf("%i + %i = %i\n",a,b,add(a,b));
            break;
         case 'c':
				if (argc < 3){
					printf("Error: not enough arguments\n");
					return 1;
				}
				result  = copy(argv[2]);
				printf("Here the copied value: %s\n", result);
            break;
         case 'm':
				if (argc < 3){
					printf("Error: not enough arguments\n");
					return 1;
				}			
				result = move(argv[2]);
				printf("Here the moved value: %s\n", result);
            break;
       	case 'v': 
		default:
			printf("Usage: %s [-hapcm]\n", argv[0]);
			printf("\t -a: add two numbers\n");
			printf("\t -p: check a string\n");
			printf("\t -c: copy string\n");
			printf("\t -m: move bytes\n");
			return 0;
      }
   }
   return 0;
}







