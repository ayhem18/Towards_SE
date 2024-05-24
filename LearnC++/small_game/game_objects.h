// This script represents the implementation of the main Game classes. The Game is described in the
// challenge question (3rd question) at the bottom of the following page:

// https://www.learncpp.com/cpp-tutorial/chapter-24-summary-and-quiz/
# include<string>
# include "random.h"
# include <map>

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

inline int _DEFAULT_PLAYER_HEALTH = 10;
inline char _PLAYER_SYMBOL = '@';
inline int _INITIAL_DAMAGE = 1;
inline int _WIN_LEVEL = 20;

class Player: public  Creature {
private:
    int level {1};
public:
    explicit Player(const std::string& name):
        Creature{name,
                 _PLAYER_SYMBOL,
                 _DEFAULT_PLAYER_HEALTH,
                 _INITIAL_DAMAGE,
                 0
                 }, // call the base class constructor
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


// create a monster class
class Monster: public Creature {
private:
    static inline Creature monsterData [] {
        Creature{"dragon", 'D', 20, 4, 100},
        Creature{"orc", 'o', 4, 2, 25},
        Creature {"slime", 's', 1, 1, 10}
    };
public:
    enum Type{
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


class Potion {
public:
    enum Size {
        small,
        medium,
        large
    };

    Potion(Potion::Size size, int effect): m_size{size}, m_effect{effect} {};
    Potion() = delete;

    // pure virtual function
    virtual void affect(Creature& creature) const = 0;
    // pure virtual function
    virtual const std::string& getPotionName() const = 0;
    Potion::Size getSize() const {
        return m_size;
    };
    // define the virtual destructor
    virtual ~Potion() = default;

protected:
    int m_effect {0};
    Potion::Size m_size {};
};

class HealthPotion: public Potion {
private:
    static inline std::map<Potion::Size, int> size_effect_map {
        {Potion::small, 2},
        {Potion::medium, 2},
        {Potion::large, 5}};
    static inline const std::string potion_name{"Health Potion"};
public:
    explicit HealthPotion(Potion::Size size): Potion(size, size_effect_map[size]) {};
    virtual void affect(Creature& creature) const {
        // increase the creature's damage per attack
        creature.setHealth(creature.getHealth() + m_effect);
    };
    const std::string& getPotionName() const {
        return potion_name;
    };
};

class StrengthPotion: public Potion {
private:
    static inline std::map<Potion::Size, int> size_effect_map {
            {Potion::small, 1},
            {Potion::medium, 2},
            {Potion::large, 2}};
    static inline const std::string potion_name{"Strength Potion"};

public:
    explicit StrengthPotion(Potion::Size size): Potion(size, size_effect_map[size]) {};

    virtual void affect(Creature& creature) const {
        // increase the creature's damage per attack
        creature.setDamagePerAttack(creature.getDamagePerAttack() + m_effect);
    };
    virtual  const std::string& getPotionName() const {
        return potion_name;
    };
};

class PoisonPotion: public Potion {
private:
    static inline std::map<Potion::Size, int> size_effect_map {
            {Potion::small, -1},
            {Potion::medium, -1},
            {Potion::large, -1}};

    static inline const std::string potion_name{"Poison Potion"};

public:
    explicit PoisonPotion(Potion::Size size): Potion(size, size_effect_map[size]) {};

    virtual void affect(Creature& creature) const {
        // increase the creature's damage per attack
        creature.setHealth(creature.getHealth() + m_effect);
    };

    virtual const std::string& getPotionName() const {
        return potion_name;
    };
};


#endif //LEARNC___GAME_OBJECTS_H
