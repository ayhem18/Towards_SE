package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"

	// "log"
	// "path/filepath"
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



func read_file(file_path string) {	
	// read a file
	file, err := os.Open(file_path)

	if err != nil {
		log.Fatal(err)
	}

	// create a scanner
	scanner := bufio.NewScanner(file)

	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
}



func factorial(num int64) int64 {
	res := int64(1)
	for i := int64(1); i <= num; i++ {
		res *= i
	}
	return res
}


func main() {
	var t = make([]int, 5)
	fmt.Println(len(t), cap(t))
}

