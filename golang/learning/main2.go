package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)


func func_calls_anonymous_func(num int, 
	fn func (x string) string) string {
		// basically this function accepts an int "num" and a function 'fn' that accepts a string 'x' and returns a string. The oustide function returns a string...
	return fn(strconv.Itoa(num))
}



type Team struct {
	Name   string
	Points int
}

func sort_teams() {

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


func work_with_bufio_scanner() {
	var scanner = bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		line := scanner.Text()
		fmt.Println(line) // we can stop the loop with the C^Z
	}
}	



func main() {
work_with_bufio_scanner()
}
