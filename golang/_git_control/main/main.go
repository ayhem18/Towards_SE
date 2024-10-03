package main

import (
	"fmt"
	// "_git_control/utils"
	"os"
	"strings"
)


func LongestString(slice []string) string {
	var longest_str string = "";
	var length int = -1;

	for _, s := range(slice) {
		if length == -1 {
			longest_str = s 
			length  = len(s)
		}

		if len(s) > length {
			longest_str = s
			length = len(s)
		}

	}
	return longest_str
}


func help_message(command string) string {
	cs := []string {"help", "config", "add", "log", "commit", "checkout"}
	length := len(LongestString(cs))

	command_help_str := map[string]string{
		"help": "These are SVCS commands:",
		"config": "Get and set a username.",
		"add": "Add a file to the index.",
		"log": "Show commit logs.",
		"commit": "Save changes.",
		"checkout": "Restore a file.",
	}

	// first check if the command is in the dictionary
	if _, ok := command_help_str[command]; ! ok {
		return "'" + command + "'"+ " is not a SVCS command."
	}

	if command == "help" {
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

	return command_help_str[command]
}



func main() {
	args := os.Args

	var command string;

	if len(args) == 1 {
		command = "help";
	} else {
		command = strings.ReplaceAll(args[1], "-", "",)			
	}
	fmt.Println(help_message(command))
	
}
