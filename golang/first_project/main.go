package main

import (
	"bufio"
	"fmt"
	// "log"
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


func enroll_students() {
	var total_applicants int;
	var successful_applicants int;

	fmt.Scan(&total_applicants)
	fmt.Scan(&successful_applicants)
	reader := bufio.NewReader(os.Stdin)
	// read the last newline character from the fmt.Scan function
	reader.ReadString('\n')

	// the slices will have 'total_applicants' elements with default values
	students := make([]Student, total_applicants) 
	
	for v:=0; v < total_applicants; v ++  {
		reader := bufio.NewReader(os.Stdin)

		app_info_str, _ := reader.ReadString('\n')

		app_info := strings.Split(strings.ToLower(strings.TrimSpace(app_info_str)), " ")

		// fmt.Println("app number ", v + 1, app_info)

		// convert the gpa to the float datatype
		gpa_float, _ := strconv.ParseFloat(app_info[2], 32)	

		// save the student
		students[v] = Student{app_info[0], app_info[1], gpa_float}
	}

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


