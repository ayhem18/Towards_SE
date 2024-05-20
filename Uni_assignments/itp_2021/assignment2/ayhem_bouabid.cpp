
#include <iostream>
#include <tuple>
#include <thread>
#include <chrono>
#include <memory>
#include <vector>

/**
 * this enum is used to determine the symbol of the units in the maze
 */
enum Type{
    MOUNT=0,FLAG,S,P,R,s,p,r
};
/**
 * This enum is used to store the possible outcomes of the game
 */
enum Result{
    FIRST_PLAYER_WINS=0,SECOND_PLAYER_WINS,TIE
};
/**
 * this enum is used to stored the possible cause of loss
 */
enum Cause{
    OUT_OF_BOUND_STAY_WITHIN_THE_HUMAN_REALM=0,TRY_TO_CLIMB_A_MOUNT_ARE_YOU_STUPID_BRO,TWO_UNITS_IN_SAME_POSITION_KEEP_THE_SOCIAL_DISTANCING
    ,TIMEOUT_WE_ARE_IN_THE_AGE_OF_SPEED,THE_ENEMY_FLAG_IS_OURS
};

using namespace std;
using namespace std::chrono_literals;


const int BOUNDARY=15;
const int TIMEOUT = 400; // maximum number of milliseconds that a player is allowed to take


// ITEM 3.b. ii : My justification for using templates
// since almost all of the objects used in the game are specified, displaying the actual
// world seems among the few possible applications of templates.

/**
 *
 * @tparam T :type of the objects the pointers are pointing to
 * @tparam N : size of array
 * @param array  the passed array
 */
template<typename T, unsigned int N >
void print2DArray(array<array<shared_ptr<T>,N>,N> array){
    for(int index=1; index<N; index++){
        for(int j=1; j<N; j++){
            if(array[j][index]){
                array[j][index]->display();
            }
            else{
                cout<<"   ";
            }
        }
        cout<<endl;
    }
}

/**
 * utility function to avoid negative return values and overflow
 * caused by % operator
 *
 * @param number
 * @param mod
 * @return the positive remainder of the division of number on mod;
 */

int mod(const int & number, const int  & mod){
    return ((number%mod)+mod)%mod;
}
/**
 * utility function to return random integer values
 * @return  random values
 */
int random(){
  srand(time(0));
  return rand();
}


class Position{
public:
    std::tuple<int, int> pos;
    //constructors
    Position(const int & x, const int & y):pos(x,y){};
    Position(const Position & aP):Position(get<0>(aP.pos),get<1>(aP.pos)){};

    /**
     * const member function
     * @return a pair(x,y). It is easier to deal with pairs than with tuples
     */
    pair<int,int> getPosition() const {
        pair<int,int> result={get<0>(pos),get<1>(pos)};
        return result ;
    }
    /* overload the equality operator */
    bool operator == (const Position & anotherPosition){
        return get<0>(pos)==get<0>(anotherPosition.pos) && get<1>(pos) == get<1>(anotherPosition.pos);
    }
    /*overload the difference operator */
    bool operator !=(const Position & anotherPosition){
        return !(this->operator==(anotherPosition));
    }
    Position()=default;

    /* display the coordinates represented by the position */
    void display()const{
        cout<<" x : "<<getPosition().first<<" y : "<<getPosition().second<<endl;
    }
};
/**
 * this class is a base class for all the classes used in the game
 */
class Object{
public:
    Position position;
    Type symbol;
    Object(int x, int y, Type symbol): position(x,y),symbol(symbol){};
    Object(const Position & aP,Type s): position(aP),symbol(s){};
    Object(const Object & another):Object(another.position, another.symbol){};

    /**
     * this a utility method to facilitate the display of the world
     * @return the char representation of the symbol
     */
    char symbolChar() const {
        switch(symbol){
            case MOUNT:
                return 'M';
            case FLAG:
                return 'F';
            case S:
                return 'S';
            case P:
                return 'P';
            case R:
                return 'R';
            case s:
                return 's';
            case p:
                return 'p';
            default:
                return 'r';
        }
    }
    void display() const{
        cout<<symbolChar()<<"  ";
    }

};
class Player1Object : public Object{
public :

    int index;

    Player1Object(int x, int y, Type symbol,int index):Object(x,y,symbol),index(index){};
    Player1Object(const Position & aP, Type s,int index): Object(aP,s),index(index){};
    Player1Object(const Player1Object & another): Player1Object(another.position,another.symbol,another.index){};
    /**
     *  as a part of the strategy the first player's units need to stop at predefined
     *  positions before attacking
     * @return the position where the attacking units should stop moving
     */

    Position finalAttackPosition(){
        if(symbol==S && index<11){
            return Position(1,7+index);
        }
        else if(symbol==P && index<11){
            return Position(2,2+index);
        }
        return position;
    }

    /**
     * this method guides the first player's units to their finalAttackPositions
     * @return the position of the units before they start attacking the enemy's units
     */
    Position move(){
        if(symbol==S){
        if(position.getPosition().second!=BOUNDARY && position.getPosition().first!=1  ){
            return Position(position.getPosition().first,position.getPosition().second+1);
        }
        else{
            if(position.getPosition().first!=1){
                return Position(position.getPosition().first-1,position.getPosition().second);
            }
            else
                return Position(position.getPosition().first,position.getPosition().second-1);
        }
        }

        else {
            if(position.getPosition().first==1 ){
                return Position(1,position.getPosition().second-1);
            }

            if(position.getPosition().second!=BOUNDARY && position.getPosition().first!=2 ){
                return Position(position.getPosition().first,position.getPosition().second+1);
            }
            else{
                if(position.getPosition().first!=2){
                    return Position(position.getPosition().first-1,position.getPosition().second);
                }

                else
                    return Position(position.getPosition().first,position.getPosition().second-1);
            }


        }
    }

    /**
     *
     * @return whether a certain object reached the position of enemy's flag
     */
    bool won(){
        return position==Position(1,1);
    }

    /**
     * this method guides the units (after reaching the attacking positions) to the enemy's flag
     * @return the next position while attacking the enemy's units.
     */
    Position attack(){
        if(position.getPosition().first==2)
            return Position(1,position.getPosition().second);
        else{
            return Position(position.getPosition().first,position.getPosition().second-1);
        }
    }

    ~Player1Object()=default;
};
class Player2Object : public Object{
public:
    int index;
    Player2Object(int x, int y, Type symbol,int index): Object(x,y,symbol),index(index){};
    Player2Object(const Position & aP, Type s,int index): Object(aP,s),index(index){};
    Player2Object(const Player2Object & another): Player2Object(another.position,another.symbol,another.index){};
    ~Player2Object()=default;
};
class Mountain: public Object{
public:
    Mountain(int x, int y):Object(x,y,MOUNT){};
};

/**
 * This is method is important for game controlling
 * @param o1 a pointer to a movable object
 * @param o2 a pointer to a movable object
 * @return whether those two objects have similar symbols : (s,S / S,S)
 *
 */
bool areSimilar(const shared_ptr<Object>  & o1, const shared_ptr<Object> & o2){
    return abs((o2->symbol - o1->symbol))==0 || abs(o2->symbol-o1->symbol)==3 ;
}

/**
 *
 * @param o1 a pointer to a movable object
 * @param o2 a pointer to a movable object
 * @return  a pointer to the winner in the confrontation between those objects
 */
decltype(auto) Survivor(const shared_ptr<Object>  & o1, const shared_ptr<Object> & o2){
    if(o1->symbol==s || o1->symbol==S){
        return  (o2->symbol!=r && o2->symbol!=R) ? o1:o2;
    }
    else if(o1->symbol==p || o1->symbol==P){
        return (o2->symbol!=S) && o2->symbol!=s ? o1:o2;
    }
    else
        return (o2->symbol!=P) && o2->symbol!=p ? o1:o2;
}
/**
 *
 * @param o1 a pointer to a movable object
 * @param o2 a pointer to a movable object
 * @return  a pointer to the loser in the confrontation between those objects
 */
decltype(auto) Dead(const shared_ptr<Object> & o1 ,const shared_ptr<Object> & o2){
    if(o1->symbol==s || o1->symbol==S){
        return  (o2->symbol!=r && o2->symbol!=R) ? o2:o1;
    }
    else if(o1->symbol==p || o1->symbol==P){
        return (o2->symbol!=S) && o2->symbol!=s ? o2:o1;
    }
    else
        return (o2->symbol!=P) && o2->symbol!=p ? o2:o1;

}

class World {
public :

    //ITEM 3.b.i : containers of shared pointers to unit objects
    // shared pointers can be copied and still have ownership over the object: the best choice
    vector<shared_ptr<Player1Object>> player1List;
    vector<shared_ptr<Player2Object>> player2List;
    vector<shared_ptr<Mountain>> mountainList;
    array<array<shared_ptr<Object>,BOUNDARY+1>,BOUNDARY+1> maze;

    World(){
        player1List.reserve(31);
        player2List.reserve(31);
        mountainList.reserve(20);
    }

    /**
     * This method initialize the first/second player objects in the vector above indicating their initial positions and indices(used in the strategy)
     *  the implementation of this method is far from optimal. It is performed this way for strategy-related purposes
     */
    void setPlayers(){
        int index;
        shared_ptr<Player1Object> a;
        shared_ptr<Player2Object> b;

        // set flags of both players
        player1List.push_back(make_shared<Player1Object>(std::move(Player1Object(15,15,FLAG,0))));
        player2List.push_back(make_shared<Player2Object>(std::move(Player2Object(1,1,FLAG,0))));

        //setting the firstLine of S/r objects for the 1st/2nd Player
        for( index=0; index<5; index++){
            a=make_shared<Player1Object>(std::move(Player1Object(10,14-index,S,1+index)));
            player1List.push_back(a);
            b= make_shared<Player2Object>(std::move(Player2Object(1,2+index,r,1+index)));
            player2List.push_back(b);
            maze[a->position.getPosition().second][a->position.getPosition().first]=a;
            maze[b->position.getPosition().second][b->position.getPosition().first]=b;
        }
        //setting the firstLine of P/p objects for the 1st/2nd Player
        for(index=0; index<5; index++){
            a=make_shared<Player1Object>(std::move(Player1Object(11,14-index,P,6+index)));
            player1List.push_back(a);
            b= make_shared<Player2Object>(std::move(Player2Object(2,2+index,p,6+index)));
            player2List.push_back(b);
            maze[a->position.getPosition().second][a->position.getPosition().first]=a;
            maze[b->position.getPosition().second][b->position.getPosition().first]=b;
        }
        //setting the firstLine of R/s objects for the 1st/2nd Player
        for(index=0; index<5; index++){
            a=(make_shared<Player1Object>(std::move(Player1Object(12,14-index,R,11+index))));
            player1List.push_back(a);
            b= make_shared<Player2Object>(std::move(Player2Object(3,2+index,s,11+index)));
            player2List.push_back(b);
            maze[a->position.getPosition().second][a->position.getPosition().first]=a;
            maze[b->position.getPosition().second][b->position.getPosition().first]=b;
        }
        //setting the second Line of S/r objects for the 1st/2nd Player
        for( index=0; index<5; index++){
            a=(make_shared<Player1Object>(std::move(Player1Object(Player1Object(13,14-index,S,16+index)))));
            player1List.push_back(a);
            b= make_shared<Player2Object>(std::move(Player2Object(4,2+index,r,16+index)));
            player2List.push_back(b);
            maze[a->position.getPosition().second][a->position.getPosition().first]=a;
            maze[b->position.getPosition().second][b->position.getPosition().first]=b;
        }
        //setting the second Line of P/p objects for the 1st/2nd Player
        for(index=0; index<5; index++){
            a=(make_shared<Player1Object>(std::move(Player1Object(Player1Object(14,14-index,P,21+index)))));
            player1List.push_back(a);
            b= make_shared<Player2Object>(std::move(Player2Object(5,2+index,p,21+index)));
            player2List.push_back(b);
            maze[a->position.getPosition().second][a->position.getPosition().first]=a;
            maze[b->position.getPosition().second][b->position.getPosition().first]=b;
        }
        //setting the second Line of S/r objects for the 1st/2nd Player
        for(index=0; index<5; index++){
            a=(make_shared<Player1Object>(std::move(Player1Object(Player1Object(15,10+index,R,26+index)))));
            player1List.push_back(a);
            b= make_shared<Player2Object>(std::move(Player2Object(6,2+index,s,26+index)));
            player2List.push_back(b);
            maze[a->position.getPosition().second][a->position.getPosition().first]=a;
            maze[b->position.getPosition().second][b->position.getPosition().first]=b;
        }


    }
    void setMountains(){
       vector<int> coordinates={11,3,13,3,10,5,14,5,11,6,12,6,13,6,7,8,8,8,9,8,3,11,3,12,3,13,5,11,5,12,5,13,6,13,7,11,7,12,7,13};
       for(int index=0; index<coordinates.size(); index+=2){
           mountainList.push_back(make_shared<Mountain>(std::move(Mountain(coordinates[index+1],coordinates[index]))));
       }

    }

    /**
     * This method adds the objects to the maze.
     */
    void setUp(){
        setPlayers();
        setMountains();
        for(auto & p : player1List){
            maze[(*p).position.getPosition().second][(*p).position.getPosition().first]=p;
        }
        for(auto & p : player2List){
            maze[(*p).position.getPosition().second][(*p).position.getPosition().first]=p;
        }
        for(auto & p : mountainList){
            maze[(*p).position.getPosition().second][(*p).position.getPosition().first]=p;
        }
    }

    /**
     *
     * @return whether the first Player won
     */
    bool firstWin()const {
        return maze[1][1]->symbol!=FLAG;
    }

    /**
     *
     * @return whether the second Player won
     */
    bool secondWin()const {
        return maze[BOUNDARY][BOUNDARY]->symbol!=FLAG;
    }

    /**
     *
     * @param position: position of the cell we want to check
     * @return the pointer pointing to the cell corresponding to position
     */
    shared_ptr<Object> at (const Position & position)const{
        int x=position.getPosition().first;
        int y=position.getPosition().second;
        return maze[y][x];
    }
    /**
     * This method is met when two non-similar objects met at the same position
     * This method updates the position of the winner(to battlePosition) and erases the loser from the maze and the lists
     * @param survivor : pointer to the winning object
     * @param dead : pointer to the losing object
     * @param battlePosition : the meeting position
     */
    void updateWinnerRemoveDead( const shared_ptr<Object> &survivor,const shared_ptr<Object>  &dead,const Position& battlePosition){
        maze[dead->position.getPosition().second][dead->position.getPosition().first].reset();
        maze[survivor->position.getPosition().second][survivor->position.getPosition().first].reset();

        auto iteratorWin1=player1List.begin(),iteratorLoss1=player1List.begin();
        auto iteratorWin2=player2List.begin(),iteratorLoss2=player2List.begin();

        for(auto iterator=player1List.begin();iterator!=player1List.end();iterator++){

            if((*iterator)->position==survivor->position){
                iteratorWin1=iterator;
            }
            if((*iterator)->position ==dead->position){
                cout<<"List 1 REDUCED"<<endl;
                iteratorLoss1=iterator;
            }
        }


        for(auto iterator=player2List.begin();iterator!=player2List.end();iterator++){

            if((*iterator)->position==survivor->position){
                iteratorWin2=iterator;

            }
            if((*iterator)->position ==dead->position){
                cout<<"List 2 REDUCED"<<endl;
                iteratorLoss2=iterator;

            }
        }
        if((iteratorWin1)!=player1List.begin()){
            (*iteratorWin1)->position=battlePosition;
        }
        if(iteratorWin2!=player2List.begin()){
            (*iteratorWin2)->position=battlePosition;
        }
        if(iteratorLoss1!=player1List.begin()){
            player1List.erase(iteratorLoss1);
        }
        if(iteratorLoss2!=player2List.begin()){
            player2List.erase(iteratorLoss2);
        }

        maze[battlePosition.getPosition().second][battlePosition.getPosition().first]=survivor;
        maze[battlePosition.getPosition().second][battlePosition.getPosition().first]->position=battlePosition;
    }

    /**
     * This method is called when the two actions performed coincide at the final position
     * @param pos1 starting position of the first object
     * @param pos2 end position of the second object
     * @param destination : position when the two objects meet and battle.
     */
    void battleToANewPos(const Position & pos1,const Position & pos2,const Position & destination){
        if(!areSimilar(at(pos1),at(pos2))){
            shared_ptr<Object> survivor= Survivor(at(pos1),at(pos2));
            shared_ptr<Object> dead= Dead(at(pos1),at(pos2));
            updateWinnerRemoveDead(survivor,dead,destination);
        }
    }

    /**
     * This method is called when the two actions performed do not coincide in the final position
     * @param pos1 starting position
     * @param pos2 end position
     */
    void moveToANewPos(const Position & source,const Position & destination ){
        int oldX=source.getPosition().first,oldY=source.getPosition().second;
        int x=destination.getPosition().first,y=destination.getPosition().second;
        if(!at(destination)){
            maze[y][x]=at(source);
            maze[y][x]->position=destination;

            for(auto & p : player1List){
                if(p->position==source){
                    p->position=destination;
                    break;
                }
            }
            for(auto & p : player2List){
                if(p->position==source){
                    p->position=destination;
                    break;
            }
            }

            maze[oldY][oldX].reset();
        }
        else{
            if(!areSimilar(at(source),at(destination))){
                shared_ptr<Object> survivor=Survivor(at(source),at(destination));
                shared_ptr<Object> dead= Dead(at(source),at(destination));
                updateWinnerRemoveDead(survivor,dead,destination);
            }
        }
    }

//    void displayWorld(){
//        for(int index=1; index<BOUNDARY+1; index++){
//            for(int j=1; j<BOUNDARY+1; j++){
//                if(maze[j][index]){
//                    maze[j][index]->display();
//                }
//                else{
//                    cout<<"   ";
//                }
//            }
//            cout<<endl;
//        }
//    }

    // this method displays the world
    void displayWorld(){
        print2DArray<Object,BOUNDARY+1>(maze);
    }

};

class Action {
public:
    Position from; // current row, column of the unit to be moved
    Position to; // position to where the unit must be moved
    // This method displays the starting and ending positions of the action
    void display(){
        cout<<"FROM : ";
        from.display();
        cout<<"TO : ";
        to.display();
    }
    // constructors
    Action(const Position &from, const Position &to): from(from), to(to){};
    Action()= default;
};


//ITEM 3.c : the first player moves according to a basic strategy

/**
 *
 * @param world: an instance of the world
 * @return the next action performed by player 1
 */

/**
 * this function checks whether the given position lies within the boundary of the world
 * @param position given position
 * @return
 */
bool PositionInBound(const Position & position){
    int x=position.getPosition().first;
    int y=position.getPosition().second;
    return (x>=1 && x<=BOUNDARY) &&(y>=1 && y<=BOUNDARY);
}
/**
 *
 * @param action: given action
 * @return whether the action has both its starting and final positions lie within bounds
 */

bool actionInBound(const Action & action){
    return PositionInBound(action.to) && PositionInBound(action.from);
}

Action actionPlayerOne(const  World &world) {
    // in the first phase preparing 10 1stPlayer objects to attack
    // move the objects until every one of them reaches its finalAttackPosition()
    for(auto &p : world.player1List){
        if((p)->position!=p->finalAttackPosition()){
            return Action(p->position,p->move());
        }
    }

    // the second phase is to attack the enemy's units

    for(int index=1; index<world.player1List.size();index++){
        auto p=world.player1List[index];
        if(!p->won()){
            return Action(p->position,p->attack());
        }
    }
    return Action(world.player1List[0]->position,world.player1List[0]->position);
}

/**
 * @param pos given position
 * @return the position just left to pos
 */
Position moveLeft(const Position & pos){
    return Position(pos.getPosition().first,pos.getPosition().second-1);
}
/**
 *
 * @param pos given position
 * @return the position just right to pos
 */
Position moveRight(const Position & pos){
    return Position(pos.getPosition().first, pos.getPosition().second+1);
}
/**
 *
 * @param pos given position
 * @return the position just in front to pos
 */
Position moveForward(const Position & pos){
    return Position(pos.getPosition().first+1,pos.getPosition().second);
}

Position moveBackward(const Position & pos){
    return Position(pos.getPosition().first-1,pos.getPosition().second);
}

//ITEM 3.c : the second player moves pseudo-randomly.

Position legalMove(const Position & pos , const World & world){
    vector<Position> positions;
    if(!(world.at(moveForward(pos))) && PositionInBound(moveForward(pos))){
        positions.push_back(moveForward(pos));
    }
    if(!(world.at(moveLeft(pos))) && PositionInBound(moveLeft(pos))){
        positions.push_back(moveLeft(pos));
    }
    if(!(world.at(moveRight(pos))) && PositionInBound(moveRight(pos))){
        positions.push_back(moveRight(pos));
    }
    if(!(world.at(moveBackward(pos))) && PositionInBound(moveBackward(pos))){
        positions.push_back(moveBackward(pos));
    }

    if (positions.empty())
        return pos;

    int r=mod(random(),positions.size());
    return positions[r];

}
/**
 *
 * @param pos given a position
 * @return either the left,right or forward move of this position with a high chance of returning the forward move()
 * */
Position randomMove(const Position & pos, const World & world){
//    int direction=mod(random(),20);
//    if(direction<=16){
//        return moveForward(pos);
//    }
//    else if(direction==17){
//        return moveLeft(pos);
//    }
//    else {
//        return moveRight(pos);
//    }

    if(legalMove(pos,world)!=pos){
        return legalMove(pos,world);
    }

    return legalMove(moveForward(pos),world);

}

/**
 * in the first 30 moves the symbols are determined. However the instance as well as the moves themselves are random(using the methods above)
 *
 * @param world : an instance of the world
 * @return the next move of the second player
 */
Action actionPlayerTwo( const World &world) {
    // TODO Implement some basic strategy and remove the lines below

    static int index = 1;
    shared_ptr<Player2Object> p;

    if(index>0 && index<=10){
        p=world.player2List[26+mod(random(),5)];
    }
    else if(index>10 && index<=20){
        p=world.player2List[21+mod(random(),5)];
    }
    else if(index>20 && index<=30){
        p=world.player2List[16+mod(random(),5)];
    }
    else if(index>30 && index<=40){
        p=world.player2List[11+mod(random(),5)];
    }
    else if(index>40 && index<=50){
        p=world.player2List[6+mod(random(),5)];
    }
    else if(index>50 && index<=60){
        p=world.player2List[1+mod(random(),5)];
    }
    else{
    p = world.player2List[1 + mod(random(), 30)];
}
    index++;
    return Action(p->position,randomMove(p->position,world));
}

Action actionPlayerTwoTrivial(const World & world){
    static int index=1;
    index++;
    if(mod(index,2)==0){
        return Action(Position(6,2),Position(7,2));
    }
    else
        return Action(Position(7,2),Position(6,2));
}

// ITEM 3.a. 4 : this method verifies whether the action performed by 1stPlayer is legal
// moving towards a mountain/ or a similar position, or out of bounds...
bool validateActionPlayer1(const Action & action,World& world, Result &result,Cause &cause){
    bool pick_a_player=false;
    for(auto & p : world.mountainList){
        if(p->position==action.to){
            result=SECOND_PLAYER_WINS;
            cause=TRY_TO_CLIMB_A_MOUNT_ARE_YOU_STUPID_BRO;
            return false;
        }
    }
    for(auto & p : world.player1List){
        if(p->position==action.to){
            result=SECOND_PLAYER_WINS;
            cause=TWO_UNITS_IN_SAME_POSITION_KEEP_THE_SOCIAL_DISTANCING;
            return false;
        }
        if(p->position==action.from){
            pick_a_player=true;
        }
    }
    if(!actionInBound(action)){
        result=SECOND_PLAYER_WINS;
        cause=OUT_OF_BOUND_STAY_WITHIN_THE_HUMAN_REALM;
        return false;
    }
    return pick_a_player;
}
// ITEM 3.a. 4 : this method verifies whether the action performed by 2ndPlayer is legal
// moving towards a mountain/ or a similar position, or out of bounds...
bool validateActionPlayer2(const Action & action, World & world, Result &result,Cause &cause){
    bool pick_a_player=false;
    for(auto & p : world.mountainList){
        if(p->position==action.to) {
            result=FIRST_PLAYER_WINS;
            cause=TRY_TO_CLIMB_A_MOUNT_ARE_YOU_STUPID_BRO;
            return false;
        }
    }

    for(auto & p : world.player2List){
        if(p->position==action.to){
            result=FIRST_PLAYER_WINS;
            cause=TWO_UNITS_IN_SAME_POSITION_KEEP_THE_SOCIAL_DISTANCING;
            return false;
        }
        if(p->position==action.from)
            pick_a_player=true;
    }
    if(!actionInBound(action)){
        result=SECOND_PLAYER_WINS;
        cause=OUT_OF_BOUND_STAY_WITHIN_THE_HUMAN_REALM;
        return false;
    }

    return pick_a_player;

}

/**
 *
 * @param VAction1 legal 1st player move
 * @param VAction2  legal 2nd player move
 * @param world the instance of the move to update
 */
void updateWorld( Action &VAction1, Action &VAction2, World &world){
    if((VAction1.to)==(VAction2.to)){
        world.battleToANewPos(VAction1.from,VAction2.from,VAction1.to);
    }
    else{
     world.moveToANewPos(VAction1.from,VAction1.to);
     world.moveToANewPos(VAction2.from,VAction2.to);
    }
}

/**
 * The return is a pair: action and a boolean whether a timeout happened
 */
std::tuple<Action, bool> waitPlayer(Action (*f)(const World&),  World  &world) {
    auto start = std::chrono::high_resolution_clock::now();

    Action action=f(world);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed = end - start;

    if (elapsed.count() > TIMEOUT) // if time > 0.3 s
        return {action, true}; // player failed to answer in less than 400 ms
    else return {action, false};
}

/**
 *
 * @param world instance of the world
 * @param result store the result of the actions
 * @param cause if there is a loss : store the reason
 * @param validateAction1 whether action 1 is valid
 * @param validateAction2 whether action 2 is valid
 */
void determineResultAndCause(const World & world, Result &result, Cause & cause, bool validateAction1,bool validateAction2 ){
    if(!validateAction1 && !validateAction2){
        result=TIE;
    }
    else{
        if(validateAction1){
            result=FIRST_PLAYER_WINS;
        }
        else{
            result=SECOND_PLAYER_WINS;
        }
    }
}

//ITEM 3.d : a unique feature : This method prints the result of the match as well as states : number of rounds,kills,survivors of each player


void statics(const World & world, Result & result, Cause  & cause, int rounds){
    cout<<"----------------------- GAME OVER -----------------------"<<endl;
    cout<<endl;
    cout<<"FIRST PLAYER                                SECOND PLAYER"<<endl;
    cout<<"------------------------  RESULT  -----------------------"<<endl;
    cout<<endl;
    if(result==TIE){
        cout<<"-----------------------  TIE  ----------------------"<<endl;
    }
    else{
        if(result==FIRST_PLAYER_WINS){
            cout<<"WINNER                                            LOSER"<<endl;
        }
        else {
            cout<<"LOSER                                            WINNER"<<endl;
        }
        cout<<endl;
        switch (cause){
            case OUT_OF_BOUND_STAY_WITHIN_THE_HUMAN_REALM :{
                cout<<"      OUT_OF_BOUND_STAY_WITHIN_THE_HUMAN_REALM      "<<endl;
                break;
            }
            case TIMEOUT_WE_ARE_IN_THE_AGE_OF_SPEED:{
                cout<<"         TIMEOUT_WE_ARE_IN_THE_AGE_OF_SPEED         "<<endl;
                break;
            }
            case TRY_TO_CLIMB_A_MOUNT_ARE_YOU_STUPID_BRO :{
                cout<<"         TRY_TO_CLIMB_A_MOUNT_ARE_YOU_STUPID        "<<endl;
                break;
            }

            case THE_ENEMY_FLAG_IS_OURS:{
                cout<<"               THE_ENEMY_FLAG_IS_OURS               "<<endl;
                break;
            }
            default:{
                cout<<"  TWO_UNITS_IN_SAME_POSITION_KEEP_THE_SOCIAL_DISTANCING  "<<endl;
            }
        }
    }
    cout<<endl;
    unsigned int survivors1=world.player1List.size()-1,survivors2=world.player2List.size()-1;
    unsigned int kills1=30-survivors1,kills2=30-survivors2;
    cout<<"------------------------ "<<rounds<<" rounds -----------------------"<<endl;
    cout<<endl;
    cout<<"----------------------    KILLS    -----------------------"<<endl;
    cout<<endl;

    cout<<kills1<<" -------------------             ------------------ "<<kills2<<endl;
    cout<<endl;

    cout<<"-------------------    SURVIVORS    --------------------"<<endl;
    cout<<endl;

    cout<<survivors1<<" -------------------             ------------------ "<<survivors2<<endl;
    cout<<endl;

}

//  This main has been commented on purpose
// due to the initial set up the possibility of making an illegal move randomly is quite high
// The game may end quite soon
// Please uncomment this main where the 2nd player makes trivial moves so I can demonstrated the basic strategy I though of for the 1st Player.


//int main(){
//    World world;
//    world.setUp();
//    int count=0;
//    Result result;
//    Cause cause;
//    bool endGame = false;
//    while (!endGame) {
//        auto[action1, timeout1] = waitPlayer(actionPlayerOne, world);
//        auto[action2, timeout2] = waitPlayer(actionPlayerTwoTrivial, world);
//        if (timeout1 || timeout2) {
//            endGame = true;
//
//            if(timeout1 && timeout2){
//                result=TIE;
//            }
//            else{
//                if(timeout1){
//                    result=SECOND_PLAYER_WINS;
//                }
//                else{
//                    result=FIRST_PLAYER_WINS;
//                }
//                cause=TIMEOUT_WE_ARE_IN_THE_AGE_OF_SPEED;
//            }
//
//        } else {
//            bool validate1= validateActionPlayer1(action1,world,result,cause);
//            bool validate2= validateActionPlayer2(action2,world,result,cause);
//            if(validate1 && validate2){
//                updateWorld(action1,action2,world);
//                world.displayWorld();
//                cout<<endl;
//                if(world.firstWin()){
//                    result=FIRST_PLAYER_WINS;
//                    cause=THE_ENEMY_FLAG_IS_OURS;
//                    endGame=true;
//                }
//                if(world.secondWin()){
//                    result=SECOND_PLAYER_WINS;
//                    cause=THE_ENEMY_FLAG_IS_OURS;
//                    endGame=true;
//                }
//            }
//            else{
//                determineResultAndCause(world,result,cause,validate1,validate2);
//                endGame=true;
//            }
//
//        }
//        count++;
//        std::this_thread::sleep_for(500ms);
//    }
//    statics(world,result,cause,count);
//    return 0;
//}






int main() {
    World world;
    world.setUp();
    int count=0;
    Result result;
    Cause cause;
    bool endGame = false;
    while (!endGame) {
        auto[action1, timeout1] = waitPlayer(actionPlayerOne, world);
        auto[action2, timeout2] = waitPlayer(actionPlayerTwo, world);
        if (timeout1 || timeout2) {
            endGame = true;
            if(timeout1 && timeout2){
                result=TIE;
            }
            else{
                if(timeout1){
                    result=SECOND_PLAYER_WINS;
                }
                else{
                    result=FIRST_PLAYER_WINS;
                }
                cause=TIMEOUT_WE_ARE_IN_THE_AGE_OF_SPEED;
            }

        } else {
            bool validate1= validateActionPlayer1(action1,world,result,cause);
            bool validate2= validateActionPlayer2(action2,world,result,cause);
            if(validate1 && validate2){
                updateWorld(action1,action2,world);
                world.displayWorld();
                cout<<endl;
                if(world.firstWin()){
                    result=FIRST_PLAYER_WINS;
                    cause=THE_ENEMY_FLAG_IS_OURS;
                    endGame=true;
                }
                if(world.secondWin()){
                    result=SECOND_PLAYER_WINS;
                    cause=THE_ENEMY_FLAG_IS_OURS;
                    endGame=true;
                }
            }
            else{
                determineResultAndCause(world,result,cause,validate1,validate2);
                endGame=true;
            }

        }
        count++;
        std::this_thread::sleep_for(500ms);
    }
    statics(world,result,cause,count);
    return 0;
}












