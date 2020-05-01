#include <cstdlib>
#include <iostream>
#include <ctime>


int main() {

    std::srand(std::time(nullptr)); // use current time as seed for random generator
    int random_variable = std::rand();

    if( random_variable %2 == 0){
        std::cout<<"branch1"<<std::endl;
    }else{
        std::cout<<"branch2"<<std::endl;
    }

    return 0;

}
