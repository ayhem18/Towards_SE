# include <iostream>

using namespace std;
int getInteger();

int main() {    
    freopen("r","input.txt",stdin);
    freopen("w","output.txt",stdout);
    std::cout << "We received an integer from a different file: " << getInteger() << " .Hallelujah!!\n"; 
    return 0;
}
