# include <iostream>
# include <string>
# include <vector>
# include <algorithm>
# include "game_objects.h"
# include "game_play.h"
# include "utilities.h"

Player getPlayerFromUser() {
    std::cout << "Please enter the name of your player" << "\n";
    std::string v{};
    std::cin >> v;
    return Player(v);
}


// define a function to get the decision from the user
bool userFight(const Monster& monster){
    std::string decision;
    std:: cout << "You have encountered a " << monster.getName() << "(" << monster.getSymbol() << ")\n";
    std:: cout << "(R)un or (F)ight\n";
    std:: cin >> decision;

    decision = toLower(decision);
    while (std::count(_VALID_FIGHT_RUN_INPUT.begin(),
                      _VALID_FIGHT_RUN_INPUT.end(),
                      decision) == 0)
    {

        std::cout << "Please enter a valid input ";
        for (std::string str : _VALID_FIGHT_RUN_INPUT) {
            std::cout << str << " ";
        }
        std:: cout << "\n";
        std:: cout << "(R)un or (F)ight\n";
        std:: cin >> decision;
        decision = toLower(decision);

    }
    return (decision == "f") || (decision == "fight");
}

void monster_attack(const Monster & monster,  Player& player) {
    std:: cout << "The " << monster.getName() << " hit you for " << monster.getDamagePerAttack() << " damage\n";
    player.reduceHealth(monster.getDamagePerAttack());
}

void player_attack(const Player& player, Monster& monster) {
    std:: cout <<  " You hit the " << monster.getDamagePerAttack() << " for " << player.getDamagePerAttack() << " damage\n";
    monster.reduceHealth(player.getDamagePerAttack());
}

bool run(Player& player, Monster& monster) {
    // get a random number between 0 and 1
    int escape_number = Random::get(1, 100);
    if (escape_number <= 50) {
        // the player escapes, wooh !! that was a close one
        std:: cout << "You successfully fled\n";
    }
    else {
        monster_attack(monster, player);
    }
    return player.isDead();
}

bool fight(Player& player, Monster& monster) {
    while (! player.isDead()) {
        // the first step is the player attacking
        player_attack(player, monster);
        // check if the monster is still alive
        if (monster.isDead()) {
            return true;
        }
        // the monster attacks
        monster_attack(monster, player);
    }
    if (! player.isDead()) {
        std:: cout << "You killed the " << monster.getName() << "\n";
        // time to collect the gold
        player.addGold(monster.getGold());
        return false;
    }
    return true;
}


void goodByeDeadPlayer(const Player& deadPlayer) {
    std:: cout << "You died at level " << deadPlayer.getLevel() << " carrying " << deadPlayer.getGold() << " gold";
    std:: cout << "Too bad you can't take it with you";
}

void CongratsWinner(const Player& winnerPlayer) {
    std:: cout << "You reached level " << winnerPlayer.getLevel() << ". You won carrying " << winnerPlayer.getGold() << "\n";
}

// let's define the game function
void game () {
    // first step is to get the player name from the user
    Player player{getPlayerFromUser()};
    // welcome the user
    std:: cout << "Welcome " << player.getName() << "!!\n";

    bool gameOver{false};

    while (! gameOver) {
        // generate a monster
        Monster round_monster {Monster::getRandomMonster()};
        bool round_fight = userFight(round_monster);
        if (round_fight) {
            gameOver = fight(player, round_monster);
        }
        else {
            gameOver = run(player, round_monster);
        }
    }
    if (player.isDead()) {

    }
}
