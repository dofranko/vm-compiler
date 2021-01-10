/*
 * Parser interpretera maszyny wirtualnej do projektu z JFTT2020
 *
 * Autor: Maciek Gębala
 * http://ki.pwr.edu.pl/gebala/
 * 2020-11-12
*/
%code requires { 
#include<vector> 
#include<tuple>
using namespace std;
}
%{

#define YYSTYPE long long

#include <iostream>
#include <tuple>
#include <vector>

#include "instructions.hh"
#include "colors.hh"

using namespace std;

extern int yylineno;
int yylex( void );
void yyset_in( FILE * in_str );
void yyerror( vector< tuple<int,int,int> > & program, char const *s );

%}
%parse-param { vector< tuple<int,int,int> > & program }
%token COM_1
%token COM_2
%token JUMP_1
%token JUMP_2
%token STOP
%token REG
%token LABEL
%token ERROR
%%
input :
    input line
  | %empty
  ;

line :
    COM_1 REG	{ program.push_back( make_tuple($1,$2,0) ); }
  | COM_2 REG REG { program.push_back( make_tuple($1,$2,$3) ); }
  | JUMP_1 LABEL { program.push_back( make_tuple($1,0,$2) ); }
  | JUMP_2 REG LABEL { program.push_back( make_tuple($1,$2,$3) ); }
  | STOP { program.push_back( make_tuple($1,0,0) ); }
  | ERROR { yyerror( program, "Nierozpoznany symbol" ); }
  ;
%%
void yyerror( vector< tuple<int,int,int> > & program, char const *s )
{
  cerr << cRed << "Linia " << yylineno << ": " << s << cReset << endl;
  exit(-1);
}

void run_parser( vector< tuple<int,int,int> > & program, FILE * data ) 
{
  cout << cBlue << "Czytanie kodu." << cReset << endl;
  yyset_in( data );
  yyparse( program );
  cout << cBlue << "Skończono czytanie kodu (liczba rozkazów: " << program.size() << ")." << cReset << endl;
}
