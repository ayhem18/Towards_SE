package main // the executable package must be named name and it must have a main function: the program entry point

import (
	// "errors"
	"fmt"
)

// finally something a little bit more interesting...
// fucking pointers
func pointer_main() {
    // var x string = "Ayhem"
    
    var x int = 0

    for true {
        if x < 10 {
            x += 1
        } else { // believe it or not the 'else' keyword must be on the same line as the closing '}' of the 'if' statement
            break;
        }
    }

    fmt.Println("final value of 'x'", x)

    var p = new(string); 
    *p = "my string";


    fmt.Println("The string ", *p, " is saved in the memory address ", p)
}

func slices_main() {
    // var a, b, c int

	// fmt.Scanln(&a, &b, &c)

    // s := [3]int{0, 0, 0}; 

    // fmt.Println(s)

    // a slice with capacity 10 and 5 elements
    s1:= make([]int, 5, 10);
    fmt.Println("length", len(s1), ",capacity", cap(s1)) // should print 5, 10
    s1 = append(s1, 10)
    fmt.Println("length", len(s1), ",capacity", cap(s1)) // should print 6, 10


    s2:= make([]int, 5);
    fmt.Println("length", len(s2), ",capacity", cap(s2)) // should print 5, 5
    s2 = append(s2, 10)
    fmt.Println("length", len(s2), ",capacity", cap(s2)) // prints 6 and 10:
    // it seems like it is doubling the current capacity



    // add more values: setting values manually using values larger than len(slice)
    // raises an error
    // for j:=len(s2); j < cap(s2); j++ {
    //     s2[j] = 10;
    // }


    current_s2_length := len(s2)
    current_s2_cap := cap(s2)

    for v:=0;  v < current_s2_cap - current_s2_length; v++ { // make sure not not use the len() and cap() function in a loop that changes a slice, as these values are evaluated at each iteration
        s2 = append(s2, v)
    }

    // now s2 reached its full capacity
    fmt.Println("after setting all the elements")
    fmt.Println("length", len(s2), ",capacity", cap(s2)) // should print 10, 10
    s2 = append(s2, 10)
    fmt.Println("length", len(s2), ",capacity", cap(s2)) // print 11, 20 ???
}


func slices_main_2() {
	var num1, num2, num3 int
	fmt.Scanln(&num1, &num2, &num3)
	intSlice := []int{num1, num2, num3}

    // slice is the Golanguage implementation of ArrayList

    for _, v:= range(intSlice) { // range is basically the same as enumerate in python 
        fmt.Println(v * 2)
    }

}


// create a struct type
type Pokemon struct {
	Name   string
	Number int
    Level  int
}


type Country struct {
    Name string
    Capital string
    Currency string
}


func updateRapper(fName *string, lName* string) string{
    *fName = "Mac"    // do not change the name!
	*lName = "Miller" // do not change the last name!
    return *fName + " " + *lName;
}


// func main() {
// }
