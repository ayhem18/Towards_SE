# include <iostream>
# include "game_objects.h"
# include "game_play.h"

#ifndef LEARNC___UTILITIES_H
#define LEARNC___UTILITIES_H


std::string toLower(const std::string& string) {
    std::string new_string;
    for (char c : string){
        new_string += std::tolower(c);
    }
    return new_string;
}

#endif //LEARNC___UTILITIES_H

