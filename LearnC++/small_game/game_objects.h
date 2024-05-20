// This script represents the implementation of the main Game classes. The Game is described in the
// challenge question (3rd question) at the bottom of the following page:

// https://www.learncpp.com/cpp-tutorial/chapter-24-summary-and-quiz/
# include<string>
# include "random.h"

#ifndef LEARNC___GAME_OBJECTS_H
#define LEARNC___GAME_OBJECTS_H

class Creature {
protected:
    const std::string m_name;
    const char m_char {};
    int m_health {0};
    int damage_per_attack {};
    int gold {};
public:
    // constructor
    Creature(const std::string& name, const char& c, int health, int damage_pa, int gold):
    m_name{name}, m_char{c}, m_health{health}, damage_per_attack{damage_pa}, gold {gold} {};

    // no default constructor allowed
    Creature () = delete;

    // setters and getters
    const std::string& getName() const {
        return m_name;
    }
    const char getSymbol() const {
        return m_char;
    }

    int getHealth() const {
        return m_health;
    }
    void setHealth(int mHealth) {
        m_health = mHealth;
    }

    int getDamagePerAttack() const {
        return damage_per_attack;
    }
    void setDamagePerAttack(int damagePerAttack) {
        damage_per_attack = damagePerAttack;
    }

    int getGold() const {
        return gold;
    }
    void setGold(int gold) {
        this -> gold = gold;
    }

    // some utility functions
    void reduceHealth(int damage) {
        m_health -= damage;
    }

    void addGold(int more_gold) {
        gold += more_gold;
    }

    bool isDead() {
        return m_health <= 0;
    }

};


int _DEFAULT_PLAYER_HEALTH = 10;
char _PLAYER_SYMBOL = '@';
int _INITIAL_DAMAGE = 1;
int _WIN_LEVEL = 20;

class Player: public  Creature {
private:
    int level {1};
public:
    explicit Player(const std::string& name):
        Creature{name,
                 _PLAYER_SYMBOL,
                 _DEFAULT_PLAYER_HEALTH,
                 _INITIAL_DAMAGE,
                 0  }, // call the base class constructor
        level{1} // set the leve to '1'
        {};

    int getLevel() const {
        return level;
    }

    void levelUp(){
        level +=1;
        damage_per_attack +=1;
    }

    bool hasWon() const {
        return level >= _WIN_LEVEL;
    }
};

//namespace Monster {
//}

// create a monster class
class Monster: public Creature {

private:
    static inline Creature monsterData [] {
        Creature{"dragon", 'D', 20, 4, 100},
        Creature{"orc", 'o', 4, 2, 25},
        Creature {"slime", 's', 1, 1, 10}
    };
public:
    enum Type {
        dragon,
        orc,
        slime,
    };

    static const int MAX_TYPES = 3;

    explicit Monster(Type type):
        Creature {monsterData[type]} {};

    static Monster getRandomMonster() {
        int monster_type = Random::get(0, MAX_TYPES - 1);
        return Monster{static_cast<Type>(monster_type)};
    }

};



#endif //LEARNC___GAME_OBJECTS_H
