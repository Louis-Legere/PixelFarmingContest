/*
		c_statehandler.h
		
		class to handle state behaviour for entry and timing
*/

#ifndef C_STATEHANDLER_H
#define C_STATEHANDLER_H

#include <stdint.h>
#include <stdbool.h>
#include <Controllino.h>

class c_statehandler
{
	private:
		uint32_t starttime;
	  uint32_t nextstate;
	  uint32_t curstate;
	
	public:
	  bool onentry;

		c_statehandler();  // constructor
		void setNextState(uint32_t statenextstate);
		uint32_t elapsedtime(void);
		void handlestate(void);
};

#endif // C_STATEHANDLER_H

