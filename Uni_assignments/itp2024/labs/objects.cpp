# include<iostream>
# include "objects.h"

std::ostream& operator << (std::ostream& out, const Box& box) {
    out << "Box(" << box.m_height << ", " << box.m_length << ", " << box.m_width << ")\n";
    return out;
}

std::ostream& operator << (std::ostream& out, Animal& a) {
    out << "My name is " << a.getName() << " and I am " << a.getAge() << "\n";
    out << "I make the following sound " << a.make_sound() << "\n";
    return out;
}
