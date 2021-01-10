/*
 * Lexer interpretera maszyny wirtualnej do projektu z JFTT2020
 *
 * Autor: Maciek Gębala
 * http://ki.pwr.edu.pl/gebala/
 * 2020-11-12
*/
%option noyywrap
%option yylineno
%option nounput
%{
#include "parser.hh"
#include "instructions.hh"

int yylex();
%}
%%
\(([^\)]|\n)*\) ;
[ \t]+          ;
GET             { yylval = GET;   return COM_1; };
PUT             { yylval = PUT;   return COM_1; };
LOAD            { yylval = LOAD;  return COM_2; };
STORE           { yylval = STORE; return COM_2; };
ADD             { yylval = ADD;   return COM_2; };
SUB             { yylval = SUB;   return COM_2; };
RESET           { yylval = RESET; return COM_1; };
INC             { yylval = INC;   return COM_1; };
DEC             { yylval = DEC;   return COM_1; };
SHR             { yylval = SHR;   return COM_1; };
SHL             { yylval = SHL;   return COM_1; };
JUMP            { yylval = JUMP;  return JUMP_1; };
JZERO           { yylval = JZERO; return JUMP_2; };
JODD            { yylval = JODD;  return JUMP_2; };
HALT            { yylval = HALT;  return STOP; };
a               { yylval = 0;     return REG; };
b               { yylval = 1;     return REG; };
c               { yylval = 2;     return REG; };
d               { yylval = 3;     return REG; };
e               { yylval = 4;     return REG; };
f               { yylval = 5;     return REG; };
\-?[1-9][0-9]*  { yylval = atoi( yytext );  return LABEL; };
\n              ;
.               return ERROR;
%%
