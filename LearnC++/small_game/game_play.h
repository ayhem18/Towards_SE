# include <iostream>
# include <string>
# include <vector>
# include "game_objects.h"

#ifndef LEARNC___GAME_PLAY_H
#define LEARNC___GAME_PLAY_H


Player getPlayerFromUser();
std::vector<std::string> _VALID_FIGHT_RUN_INPUT {"r", "f", "fight", "run"};

// define a function to get the decision from the user
bool userFight(const Monster& monster);

// let's define the game function
void game ();


#endif //LEARNC___GAME_PLAY_H
