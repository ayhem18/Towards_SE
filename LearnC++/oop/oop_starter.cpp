# include <iostream>
# include "oop_starter.h"

void print_ball(const Ball ball_obj) {
    // since the argument ball_obj is passed by value (without the & symbol), then
    // the function inside is not acting on the original object but a copy and the
    // copy constructor will be called:
    // basically ball_obj = copy_constructor(ball_obj)
    std:: cout << "Ball (" << ball_obj.getColor() << " " << ball_obj.getRadius() << ") printed\n";
}

//void print_ball(const Ball& ball_obj) {
//    // here we're dealing with a reference to the original object passed
//    std:: cout << "Ball (" << ball_obj.getColor() << " " << ball_obj.getRadius() << ") printed\n";
//}
