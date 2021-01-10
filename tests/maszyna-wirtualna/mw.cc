/*
 * Kod interpretera maszyny rejestrowej do projektu z JFTT2020
 *
 * Autor: Maciek Gębala
 * http://ki.pwr.edu.pl/gebala/
 * 2020-11-12
 * (wersja long long)
*/
#include <iostream>

#include <tuple>
#include <vector>
#include <map>

#include <cstdlib> 	// rand()
#include <ctime>

#include "instructions.hh"
#include "colors.hh"

using namespace std;

void run_machine( vector< tuple<int,int,int> > & program )
{
  map<long long,long long> pam;

  long long r[6];
  int lr;

  long long t, io;

  cout << cBlue << "Uruchamianie programu." << cReset << endl;
  lr = 0;
  srand( time(NULL) );
  for(int i = 0; i<6; i++ ) r[i] = rand();
  t = 0;
  io = 0;
  while( get<0>(program[lr])!=HALT )	// HALT
  {
    switch( get<0>(program[lr]) )
    {
      case GET:	cout << "? "; cin >> pam[r[get<1>(program[lr])]]; io+=100; lr++; break;
      case PUT:	cout << "> " << pam[r[get<1>(program[lr])]] << endl; io+=100; lr++; break;

      case LOAD:	r[get<1>(program[lr])] = pam[r[get<2>(program[lr])]]; t+=20; lr++; break;
      case STORE:	pam[r[get<2>(program[lr])]] = r[get<1>(program[lr])]; t+=20; lr++; break;

      case ADD:	r[get<1>(program[lr])] += r[get<2>(program[lr])] ; t+=5; lr++; break;
      case SUB:	if( r[get<1>(program[lr])] >= r[get<2>(program[lr])] )
                       	r[get<1>(program[lr])] -= r[get<2>(program[lr])];
                       else
                       	r[get<1>(program[lr])] = 0;
                       t+=5; lr++; break;
      case RESET:	r[get<1>(program[lr])] = 0 ; t+=1; lr++; break;
      case INC:	r[get<1>(program[lr])]++ ; t+=1; lr++; break;
      case DEC:	if( r[get<1>(program[lr])]>0 ) r[get<1>(program[lr])]--; t+=1; lr++; break;
      case SHR:	r[get<1>(program[lr])] >>= 1; t+=1; lr++; break;
      case SHL:	r[get<1>(program[lr])] <<= 1; t+=1; lr++; break;

      case JUMP: 	lr += get<2>(program[lr]); t+=1; break;
      case JZERO:	if( r[get<1>(program[lr])]==0 ) lr += get<2>(program[lr]); else lr++; t+=1; break;
      case JODD:	if( r[get<1>(program[lr])] % 2 != 0 ) lr += get<2>(program[lr]); else lr++; t+=1; break;
      default: break;
    }
    if( lr<0 || lr>=(int)program.size() )
    {
      cerr << cRed << "Błąd: Wywołanie nieistniejącej instrukcji nr " << lr << "." << cReset << endl;
      exit(-1);
    }
  }
  cout << cBlue << "Skończono program (koszt: " << (t+io) << "; w tym i/o: " << io << ")." << cReset << endl;
}
