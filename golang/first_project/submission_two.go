package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

// the project is too simple to say the least...

type Student struct {
	first_name string;
	last_name string;
	gpa float64;

}

func student_full_name(s Student) string {
	return s.first_name + " " + s.last_name
}


func get_integer_input() (int, int) {
	var total_applicants int;
	var successful_applicants int;

	fmt.Scan(&total_applicants)
	fmt.Scan(&successful_applicants)

	reader := bufio.NewReader(os.Stdin)
	// read the last newline character from the fmt.Scan function
	reader.ReadString('\n')

	return total_applicants, successful_applicants
}

func get_students_input(total_applicants int) []Student {
	// the slices will have 'total_applicants' elements with default values
	students := make([]Student, total_applicants) 

	var scanner = bufio.NewScanner(os.Stdin)

	v := 0

	for scanner.Scan() {
		app_info_str := scanner.Text()
		app_info := strings.Split(strings.TrimSpace(app_info_str), " ")
		// convert the gpa to the float datatype
		gpa_float, _ := strconv.ParseFloat(app_info[2], 32)	
		// save the student
		students[v] = Student{app_info[0], app_info[1], gpa_float}
		v ++ 
	}

	return students
}


func enroll_students() {
	total_applicants, successful_applicants := get_integer_input()

	students := get_students_input(total_applicants)

	// sort students
	sort.Slice(students, 
		func (i int , j int) bool{
			if students[i].gpa == students[j].gpa {
				i_full_name := student_full_name(students[i])
				j_full_name := student_full_name(students[j])
				
				return i_full_name <= j_full_name
			}

			return students[i].gpa > students[j].gpa
		})
	
	fmt.Println("Successful applicants:")
	for k := 0; k < successful_applicants; k++ {
		fmt.Println(student_full_name(students[k]))
	}
}

func main() {
	enroll_students()	
}


