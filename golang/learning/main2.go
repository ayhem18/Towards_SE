package main

import (
	"fmt"
	"strconv"
	"sort"
)


func func_calls_anonymous_func(num int, 
	fn func (x string) string) string {
		// basically this function accepts an int "num" and a function 'fn' that accepts a string 'x' and returns a string. The oustide function returns a string...
	return fn(strconv.Itoa(num))
}


// func main() {
// 	func(msg string) {
// 		fmt.Println(msg)
// 	}("Hello, World!")
// }


type Team struct {
	Name   string
	Points int
}

func main() {
	teams := []Team{
		{"Borussia Dortmund", 64},
		{"Bayern Munich", 78},
		{"RB Leipzig", 65},
		{"Vfl Wolfsburg", 61},
	}

	// Implement the logic within the sort.Slice() function below to sort the teams slice!
    sort.Slice(teams, func(i, j int) bool {
        return teams[i].Points >teams[j].Points
    })

    // Do not delete the output line!
	fmt.Println(teams)
}
