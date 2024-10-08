package main

import (
	"_git_control/utils"
	"bufio"
	"fmt"
	"log"
	"os"
	"path"
	"strings"
)

type Controler struct{
	vsc_dir string;
	index_file_path string;
	config_file_path string;
}


func (controller_obj Controler) set_up() {
	// create the .vsc directory as well as the files
	os.MkdirAll(controller_obj.vsc_dir, os.ModePerm)

	index_file_path := controller_obj.index_file_path
	config_file_path := controller_obj.config_file_path
	
	// to my understanding, I need to check if the file already exists all the time
	if _, err := os.Stat(index_file_path); err != nil {
		os.Create(index_file_path)
	}

	if _, err := os.Stat(config_file_path); err != nil {
		os.Create(config_file_path)
	}
}


func help_message() string {
	cs := []string {"help", "config", "add", "log", "commit", "checkout"}
	length := len(utils.LongestString(cs))

	command_help_str := map[string]string{
		"help": "These are SVCS commands:",
		"config": "Get and set a username.",
		"add": "Add a file to the index.",
		"log": "Show commit logs.",
		"commit": "Save changes.",
		"checkout": "Restore a file.",
	}

	var result string = ""
	for i := range cs {
		var k string;
		if i == 0 {
			k = ""
		} else {
			k = cs[i] + strings.Repeat(" ", length - len(cs[i])) + "  "
		}

		result += (k + command_help_str[cs[i]] + "\n") 
	}
	return result
}


func (ctr_obj Controler) add_message_display_files() string {
	// read the 'index.txt' file
	file, err := os.Open(ctr_obj.index_file_path)
	
	if err != nil {
		log.Fatal(err)
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)

	tracked_files := make([]string, 0)

	for scanner.Scan() {
		tracked_files = append(tracked_files, scanner.Text())
	}

	if len(tracked_files) == 0 {
		return "Add a file to the index."
	}

	tracked_files = append(([]string{"Tracked files:"}), tracked_files...)

	return strings.Join(tracked_files, "\n")
} 

func (ctr_obj Controler) add_message(argument* string) string {
	// there are three cases for the argument
	// either Nil: which means the the function is called to display the 
	// or a string representing a file name if the file exists: let the user know that is has been added
	// if not let it know that it does not exist

	if argument == nil {
		return ctr_obj.add_message_display_files()
	}

	if _, err := os.Stat(*argument); err != nil {	
		return fmt.Sprintf("Can't find '%s'.", *argument)
	}
	
	file, _ := os.OpenFile(ctr_obj.index_file_path, os.O_APPEND, os.ModePerm)
	defer file.Close()

	fmt.Fprintln(file, *argument)

	return fmt.Sprintf("The file '%s' is tracked.", *argument)
}


func (ctr_obj Controler) config_message_display_users() string {
	// read the 'index.txt' file
	file, err := os.Open(ctr_obj.config_file_path)
	
	if err != nil {
		log.Fatal(err)
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)

	// supposedly there is only one user

	if scanner.Scan() {
		return fmt.Sprintf("The username is %s.", scanner.Text())
	}

	return "Please, tell me who you are."	
} 


func (ctr_obj Controler) config_message(argument* string) string {
	if argument == nil {
		return ctr_obj.config_message_display_users()
	}
	// overwrite the user
	file, _ := os.Create(ctr_obj.config_file_path)
	fmt.Fprintln(file, *argument)
	return fmt.Sprintf("The username is %s.", *argument)
}


func main() {
	current_dir, _ := os.Getwd()
	vcs_dir := path.Join(current_dir, "vsc_dir")
	// build the
	config_path := path.Join(vcs_dir, "config.txt")
	index_path := path.Join(vcs_dir, "index.txt")

	ctr_obj := Controler{vcs_dir, index_path, config_path}

	ctr_obj.set_up()

	args := os.Args

	var command string;

	if len(args) == 1 {
		command = "help";
	} else {
		command = strings.ReplaceAll(args[1], "-", "",)			
	}

	switch command {
	case "help":
		fmt.Println(help_message())
	case "add":
		if len(args) < 3 {
			fmt.Println(ctr_obj.add_message(nil))
		} else {
			fmt.Println(ctr_obj.add_message(&args[2]))
		}
	case "config":
		if len(args) < 3 {
			fmt.Println(ctr_obj.config_message(nil))
			} else {
			fmt.Println(ctr_obj.config_message(&args[2]))
		}
	}

}
