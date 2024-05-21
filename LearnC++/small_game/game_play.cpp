# include <iostream>
# include <string>
# include <algorithm>
# include "game_objects.h"
# include "game_play.h"
# include "utilities.h"

std::vector<std::string> _VALID_FIGHT_RUN_INPUT {"r", "f", "fight", "run"};

Player getPlayerFromUser() {
    std::cout << "Please enter the name of your player" << "\n";
    std::string v{};
    std::cin >> v;
    return Player(v);
}

// define a function to get the decision from the user
bool userFightInput(const Monster& monster){
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
        for (const std::string& str : _VALID_FIGHT_RUN_INPUT) {
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
    std:: cout <<  "You hit the " << monster.getName() << " for " << player.getDamagePerAttack() << " damage\n";
    monster.reduceHealth(player.getDamagePerAttack());
}

bool run(Player& player, Monster& monster) {
    // get a random number between 0 and 1
    int escape_number = Random::get(1, 100);
    if (escape_number <= 50) {
        // the player escapes !! that was a close one
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
            // break from the loop at this point to level up
            break;
        }
        // the monster attacks
        monster_attack(monster, player);
    }
    if (! player.isDead()) {
        std:: cout << "You killed the " << monster.getName() << "\n";
        // time to collect the gold
        player.addGold(monster.getGold());
        // make sure to level up
        player.levelUp();
        return false;
    }
    return true;
}

Potion generateRandomPotion() {
    // randomly selected  the type
    int type_index = Random::get(0, 2);
    // randomly selected  the size
    int size_index = Random::get(0, 2);

    switch(type_index) {
        case 0:
            return HealthPotion(static_cast<Potion::Size>(size_index));
        case 1:
            return StrengthPotion(static_cast<Potion::Size>(size_index));
        default:
            return PoisonPotion(static_cast<Potion::Size>(size_index));
    }
}

std::vector<std::string> _VALID_POTION_INPUT {"y", "yes", "n", "no"};

bool userPotionInput() {
    std::string decision;
    // inform the user
    std::cout << "You found a potion\n";
    std:: cout << "Do You want to drink it ? (Y)es, (N)o ?";
    std:: cin >> decision;

    decision = toLower(decision);
    while (std::count(_VALID_FIGHT_RUN_INPUT.begin(),
                      _VALID_FIGHT_RUN_INPUT.end(),
                      decision) == 0)
    {

        std::cout << "Please enter a valid input ";
        for (const std::string& str : _VALID_POTION_INPUT) {
            std::cout << str << " ";
        }
        std:: cout << "\n";
        std:: cout << "Do You want to drink it ? (Y)es, (N)o ?";
        std:: cin >> decision;
        decision = toLower(decision);

    }
    return (decision == "y") || (decision == "yes");
}

void userDrinkPotion(Player& player, const Potion& p) {
    std::cout << "You drank a " << p.getPotionName() << " of size " << p.getSize() << "\n";
    p.affect(player);
}

bool player_and_potions(Player& player) {
    // a potion exists only 30 % of the time
    int potion_prob = Random::get(0, 100);
    if (potion_prob >= 30) {
        return false;
    }

    // a potion was found
    Potion p = generateRandomPotion();
    // ask the player whether
    bool drink {userPotionInput()};

    if (drink) {
        userDrinkPotion(player, p);
        return player.isDead();
    }
    return false;
}

void goodByeDeadPlayer(const Player& deadPlayer) {
    std:: cout << "You died at level " << deadPlayer.getLevel() << " carrying " << deadPlayer.getGold() << " gold\n";
    std:: cout << "Too bad you can't take it with you";
}

void congratsWinner(const Player& winnerPlayer) {
    std:: cout << "You reached level " << winnerPlayer.getLevel() << ". You won carrying " << winnerPlayer.getGold() << "\n";
}

// let's define the game logic
void game () {
    // first step is to get the player name from the user
    Player player{getPlayerFromUser()};
    // welcome the user
    std:: cout << "Welcome " << player.getName() << "!!\n";

    bool gameOver{false};

    while (! gameOver) {
        // generate a monster
        Monster round_monster {Monster::getRandomMonster()};
        bool round_fight = userFightInput(round_monster);
        if (round_fight) {
            gameOver = fight(player, round_monster);
        }
        else {
            gameOver = run(player, round_monster);
        }
        // check if the player has won
        if (player.hasWon()) {
            break;
        }

        // deal with potions
        gameOver = player_and_potions(player);
    }
    if (player.isDead()) {
        goodByeDeadPlayer(player);
    }
    else {
        congratsWinner(player);
    }
}
