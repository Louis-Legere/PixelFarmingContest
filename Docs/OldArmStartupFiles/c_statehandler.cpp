/*
		c_statehandler.cpp
		
		class to handle state behaviour for entry and timing
		
		NOTE: it seems possible to remove handlestate()
		NOTE: for the 2022-2023 version: add history!!
		NOTE: maybe even better to remove setNextState
		and simply put as last line: update(state)
		also be sure to adapt elapsedtime to ONLY return a value
		if update(state) has been called!!!!
*/

#include "c_statehandler.h"
#include <Controllino.h>

// during creation setup some items
c_statehandler::c_statehandler()
{
	nextstate = 0xFFFFFFFF;	// set to non-used value 
	curstate = 0xFFFFFFFF;	// use non enumerated number
	starttime = millis();	  // and get starttime
}


void c_statehandler::setNextState(uint32_t newstate)
{
	nextstate = newstate;
}

void c_statehandler::handlestate(void)
{
	if (nextstate != 0xFFFFFFFF)
	{	// state changed or re-entering same state! flag onentry
		curstate = nextstate;   // avoid entering second time
		starttime = millis();		// new starttime to use
		nextstate =  0xFFFFFFFF;	// set to non-used value again
		onentry = true;
	}
	else
	{	
		onentry = false;
	}
}


uint32_t c_statehandler::elapsedtime(void)
{
	return millis() - starttime;
}
