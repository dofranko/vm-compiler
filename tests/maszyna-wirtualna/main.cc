/*
 * Kod maszyny wirtualnej do projektu z JFTT2020
 *
 * Autor: Maciek Gębala
 * http://ki.pwr.edu.pl/gebala/
 * 2020-11-12
*/
#include <iostream>

#include <tuple>
#include <vector>

#include "colors.hh"

using namespace std;

extern void run_parser( vector< tuple<int,int,int> > & program, FILE * data );
extern void run_machine( vector< tuple<int,int,int> > & program );

int main( int argc, char const * argv[] )
{
  vector< tuple<int,int,int> > program;
  FILE * data;

  if( argc!=2 )
  {
    cerr << cRed << "Sposób użycia programu: interpreter kod" << cReset << endl;
    return -1;
  }

  data = fopen( argv[1], "r" );
  if( !data )
  {
    cerr << cRed << "Błąd: Nie można otworzyć pliku " << argv[1] << cReset << endl;
    return -1;
  }

  run_parser( program, data );

  fclose( data );

  run_machine( program );

  return 0;
}
