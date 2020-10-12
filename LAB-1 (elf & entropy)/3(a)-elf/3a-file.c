#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main() {
   char *s = malloc(9);
   s[0] = 'a';
   for(int i = 1; i <= 8; i++){
       s[i] = s[i - 1] + 1;
   }
   s[9] = '\0';
   char *in = malloc(10);
   
   printf("password: ");
   fgets(in, 10, stdin);        // 'abcdefghi'
   if(strcmp(in, s) == 0) 
       printf("Yes!\n");
   
   else 
       printf("No!\n");
       
   return 0;
}
