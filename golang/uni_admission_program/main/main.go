package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path"
	"sort"
	"strconv"
	"strings"
	"math"
)


func avg_slice(num_slice []int) float64 {
	var total float64 = 0.0
	for _, val := range(num_slice) {
		total += float64(val)
	}

	return total / float64(len(num_slice))
}

type Student struct {
	first_name string;
	last_name string;
	// gpa float64;

	// exam results
	exam_scores map[string][]int;
	entrance_score int;
	priorities []string;
}


func (s Student) full_name() string{
	return s.first_name + " " + s.last_name
}

func (s Student) student_best_score(dep string) float64 {
	avg_finals := avg_slice(s.exam_scores[dep])
	return math.Max(float64(s.entrance_score), avg_finals)
}


func get_students(app_list_path string) map[int]Student {

	file, err := os.Open(app_list_path)
	
	if err != nil {
		log.Fatal(err)
	}

	// close the file at the end of the function 
	defer file.Close()

	scanner := bufio.NewScanner(file)
	
	var index2app = make(map[int]Student)

	var counter = 0

	// just to remember: 0 -> Physics, 1: chemistry, 2 math, 3 computer science
	
	// departments and subjects

	// physics: physics and math
	// math: math 
	// chemistry: chemistry
	// engineering: cs and math
	// biotech: chemistry and physics

	// by subject: 0, physics affects physics and biotech
	// chemistry 1 affects chemistry and biotech
	// math affects math, physics and engineering
	// cs: affects engineering

	exam_index_2_dep := map[int][]string {0: {"Physics", "Biotech"}, 1: {"Biotech", "Chemistry"}, 2 : {"Mathematics", "Physics", "Engineering"}, 3: {"Engineering"}}

	for scanner.Scan() {
		// read the input
		app_info_str := scanner.Text()
		app_info := strings.Split(strings.TrimSpace(app_info_str), " ")

		// extract the exam results
		exam_scores := make(map[string][]int)
		// exam_scores := make([]int, 4)

		for i, score := range(app_info[2:6]) {
			// convert each score to an integer
			score_int, err := strconv.Atoi(score)
			if err != nil {
				log.Fatal(err)
			}
			for _, dep := range(exam_index_2_dep[i]) {
				if _, ok := exam_scores[dep]; ! ok {
					exam_scores[dep] = make([]int, 0)
				}
				exam_scores[dep] = append(exam_scores[dep], score_int)
			}
		}

		// convert the gpa string to a float value
		entrance_score, _ := strconv.Atoi(app_info[6])

		// create a list to save the values	
		app_priorities := make([]string, 3)
		copy(app_priorities, app_info[7:])

		// create a Student object to add it to the list
		index2app[counter] = Student{app_info[0], app_info[1], exam_scores, entrance_score, app_priorities}

		counter += 1
	}

	return index2app
}



func enroll_per_round(
					  students_per_department int,
					  round_number int,
					  final_admissions *map[string][]Student,
					  current_round_applicants *map[int]Student,) {
	
	// admissions per round
	round_admissions := make(map[string][]int, 4)
	
	// itereate through the current students
	for app_index, app := range(*current_round_applicants) {
		// extract the applicant priority (depending on the admission round)
		app_priority := app.priorities[round_number]

		// check if the department has been added
		if _, ok := round_admissions[app_priority]; ! ok{
			round_admissions[app_priority] = make([]int, 0) 
		}
		round_admissions[app_priority] = append(round_admissions[app_priority], app_index)
	}

	// sort the applicants for the current round
	for dep_name := range round_admissions {
		
		sort.Slice(round_admissions[dep_name], 
		func (i int , j int) bool{
			student_i , student_j := (*current_round_applicants)[round_admissions[dep_name][i]], (*current_round_applicants)[round_admissions[dep_name][j]]

			student_i_avg_score := student_i.student_best_score(dep_name) 
			student_j_avg_score := student_j.student_best_score(dep_name)  

			if student_i_avg_score == student_j_avg_score {
				i_full_name := student_i.full_name()
				j_full_name := student_j.full_name()
				
				return i_full_name <= j_full_name
			}

			return student_i_avg_score > student_j_avg_score
		})
	}

	for dep_name, already_acc_app:= range *final_admissions {
		// calculate the number of students to be accepted to the specific department 
		// in the given admission round
		dep_acc_student_round := int(students_per_department - len(already_acc_app))

		// make sure the number of elements does not exceed the length of the current number of admitted students...
		dep_acc_student_round = min (dep_acc_student_round, len(round_admissions[dep_name]))

		// extract them
		accepted_students_indices := round_admissions[dep_name][0:dep_acc_student_round]

		accepted_students := make([]Student, len(accepted_students_indices))

		// delete them from the list of applicants
		for slice_index, student_index := range accepted_students_indices {
			accepted_students[slice_index] = (*current_round_applicants)[student_index]			
			delete(*current_round_applicants, student_index)
		}

		// add the list of this round students to the final admission list
		(*final_admissions)[dep_name] = append((*final_admissions)[dep_name], accepted_students...)
	}
}


func enroll_students(app_list_path string) map[string][]Student{
	var students_per_dep int = 4 ;
	fmt.Scan(&students_per_dep)

	// get the students
	index2app := get_students(app_list_path)

	// create the final admission mapping between departments and applicants
	final_admissions := make(map[string][]Student)

	deps := []string{"Mathematics", "Physics", "Biotech", "Chemistry", "Engineering"}

	for _, d := range(deps) {
		final_admissions[d] = make([]Student, 0)
	}

	for p:=0; p < 3; p++ {
		enroll_per_round(students_per_dep, 
						p, 
						&final_admissions, 
						&index2app)
	}


	for _, d := range(deps) {
		sort.Slice(final_admissions[d], 		
			func (i int , j int) bool{
			student_i, student_j := final_admissions[d][i], final_admissions[d][j]
			
			student_i_avg_score, student_j_avg_score := student_i.student_best_score(d), student_j.student_best_score(d)

			if student_i_avg_score == student_j_avg_score {
				i_full_name := student_i.full_name()
				j_full_name := student_j.full_name()
				
				return i_full_name <= j_full_name
			}

			return student_i_avg_score > student_j_avg_score
		}) 
	}

	return final_admissions

}


func main() {
	// first read the file
	// app_list_path := path.Join("main", "test_case1.txt")
	current_dir, _ := os.Getwd()
	app_list_path := path.Join(current_dir, "applicants.txt")

	// fmt.Println(index2app)
	final_admissions := enroll_students(app_list_path)	

	deps := []string{"Biotech", "Chemistry", "Engineering", "Mathematics", "Physics"}

	for dep_index, d := range deps {
		dep_file_name := strings.ToLower(d) + ".txt"
		dep_file_path := path.Join(current_dir, dep_file_name)
		
		file, err := os.Create(dep_file_path)
		
		if err != nil {
			log.Fatal(err)
		}

		// don't forget this function
		defer file.Close()

		// fmt.Println(d)
		department_students := final_admissions[d]

		for _, s := range(department_students) {
			fmt.Printf("%s %s %.1f\n", s.first_name, s.last_name, s.student_best_score(d))
			fmt.Fprintf(file, "%s %s %.1f\n", s.first_name, s.last_name, s.student_best_score(d))
		}

		// leave a space between consecutive departments: (except the last one...) 
		if dep_index != 4 {
			fmt.Println()
		}		
	}
}
