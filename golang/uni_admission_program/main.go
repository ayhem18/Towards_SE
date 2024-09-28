package main

import (
	"bufio"
	"log"
	"os"
	"path"
	"sort"
	"strconv"
	"strings"

	// "sort"
	"fmt"
	"slices"
)

// the project is too simple to say the least...

type Student struct {
	first_name string;
	last_name string;
	gpa float64;

	priorities []string;

}

func student_full_name(s Student) string {
	return s.first_name + " " + s.last_name
}


func get_integer_input() (int, int) {

	// let's try to use a different way to read the input
	scanner := bufio.NewScanner(os.Stdin) // the scanner reads line by line by default

	// scan 2 numbers
	scanner.Scan()
	total_applicants, err := strconv.Atoi(scanner.Text())	
	if err != nil {
		log.Fatal(err)
	}

	scanner.Scan()
	successful_applicants, err := strconv.Atoi(scanner.Text())	
	if err != nil {
		log.Fatal(err)
	}
	
	// fmt.Println("total and successful applications ", total_applicants, successful_applicants)
	return total_applicants, successful_applicants
}

// func get_students_input(total_applicants int) []Student {
// 	// the slices will have 'total_applicants' elements with default values
// 	students := make([]Student, total_applicants) 

// 	var scanner = bufio.NewScanner(os.Stdin)

// 	for v:=0; v < total_applicants; v ++ {
// 		scanner.Scan()
// 		app_info_str := scanner.Text()
// 		app_info := strings.Split(strings.TrimSpace(app_info_str), " ")
// 		// convert the gpa to the float datatype
// 		gpa_float, _ := strconv.ParseFloat(app_info[2], 32)	
// 		// save the student
// 		students[v] = Student{app_info[0], app_info[1], gpa_float}
// 	}

// 	return students
// }


// func enroll_students() {
// 	total_applicants, successful_applicants := get_integer_input()

// 	students := get_students_input(total_applicants)

// 	// sort students
// 	sort.Slice(students, 
// 		func (i int , j int) bool{
// 			if students[i].gpa == students[j].gpa {
// 				i_full_name := student_full_name(students[i])
// 				j_full_name := student_full_name(students[j])
				
// 				return i_full_name <= j_full_name
// 			}

// 			return students[i].gpa > students[j].gpa
// 		})
	
// 	fmt.Println("Successful applicants:")
// 	for k := 0; k < successful_applicants; k++ {
// 		fmt.Println(student_full_name(students[k]))
// 	}
// }


func get_students() map[int]Student {
	// first read the file
	app_list_path := path.Join("first_project", "applicant_list.txt")

	file, err := os.Open(app_list_path)
	
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	
	var index2app = make(map[int]Student)

	var counter = 0

	for scanner.Scan() {
		// read the input
		app_info_str := scanner.Text()
		app_info := strings.Split(strings.TrimSpace(app_info_str), " ")
		// convert the gpa string to a float value
		gpa_float, _ := strconv.ParseFloat(app_info[2], 32)
		// create a list to save the values	
		app_priorities := make([]string, 3)
		copy(app_priorities, app_info[3:])
		// create a Student object to add it to the list
		index2app[counter] = Student{app_info[0], app_info[1], gpa_float, app_priorities}

		counter += 1
	}

	return index2app
}




func enroll_per_round(
					  ads_per_department int,
					  final_ads *map[string][]int,
					  current_apps *map[int]Student,
					  round_number int) {
	
	// admissions per round
	ads_per_round := make(map[string][]int, 4)
	
	// itereate through
	for app_index, app := range(*current_apps) {
		app_priority := app.priorities[round_number]
		if _, ok := ads_per_round[app_priority]; ! ok{
			ads_per_round[app_priority] = make([]int, 0) 
		}
		ads_per_round[app_priority] = append(ads_per_round[app_priority], app_index)
	}

	// sort the applicants for the current round
	for dep_name := range ads_per_round {
		
		sort.Slice(ads_per_round[dep_name], 
		func (i int , j int) bool{
			student_i , student_j := (*current_apps)[ads_per_round[dep_name][i]], (*current_apps)[ads_per_round[dep_name][j]]

			if student_i.gpa == student_j.gpa {
				i_full_name := student_full_name(student_i)
				j_full_name := student_full_name(student_j)
				
				return i_full_name <= j_full_name
			}

			return student_i.gpa > student_j.gpa
		})
	}

	for dep_name, already_acc_app:= range *final_ads {
		dep_acc_student_round := ads_per_department - len(already_acc_app)

		accepted_students := ads_per_round[dep_name][0:dep_acc_student_round]

		for i := range accepted_students {
			delete(*current_apps, i)
		}

		(*final_ads)[dep_name] = slices.Concat((*final_ads)[dep_name], accepted_students) 	
	}
}


func main() {
	index2app := get_students()
	fmt.Println(index2app)
}
