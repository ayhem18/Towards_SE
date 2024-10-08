package main

import (
	"_git_control/utils"
	"bufio"
	"crypto/sha256"
	"fmt"
	"io"
	"log"
	"os"
	"path"
	"strings"
    "slices"
    "hash"
)


const _NO_CURRENT_USER = "Please, tell me who you are."

func copy_file_to_hash(enc_obj *hash.Hash, file_path string) {
    // read the file
    file, err := os.Open(file_path)
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()
    // copy the file 
    io.Copy(*enc_obj, file)
}


type Controler struct{
	vsc_dir string;
	index_file_path string;
	config_file_path string;
    log_file_path string;
    commits_dir_path string;
}


func (controller_obj Controler) set_up() {
	// create the .vsc directory as well as the files
    files := []string{controller_obj.config_file_path, controller_obj.index_file_path, controller_obj.log_file_path, controller_obj.commits_dir_path}

    for _, f := range(files) {
        os.MkdirAll(f, os.ModePerm)
    }

	// index_file_path := controller_obj.index_file_path
	// config_file_path := controller_obj.config_file_path
	
	// // to my understanding, I need to check if the file already exists all the time
	// if _, err := os.Stat(index_file_path); err != nil {
	// 	os.Create(index_file_path)
	// }

	// if _, err := os.Stat(config_file_path); err != nil {
	// 	os.Create(config_file_path)
	// }

}


func help_message(command string) string {
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


func (ctr_obj Controler) get_tracked_files()[]string {
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

    return tracked_files
} 


func (ctr_obj Controler) add_message_display_files() string {
    tracked_files := ctr_obj.get_tracked_files()

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
	
	file, _ := os.OpenFile(ctr_obj.index_file_path, os.O_APPEND|os.O_RDWR, os.ModePerm)
	defer file.Close()

	fmt.Fprintln(file, *argument)

	return fmt.Sprintf("The file '%s' is tracked.", *argument)
}



func (ctr_obj Controler) config_message_display_user() string {
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

	return _NO_CURRENT_USER
} 


func (ctr_obj Controler) config_message(argument* string) string {
	if argument == nil {
		return ctr_obj.config_message_display_user()
	}
	// overwrite the user
	file, _ := os.Create(ctr_obj.config_file_path)
	fmt.Fprintln(file, *argument)
	return fmt.Sprintf("The username is %s.", *argument)
}

func (ctr_obj Controler) fetch_last_commit_version() map[string]string{
    // open the log text    
    file, err := os.Open(ctr_obj.log_file_path)

    if (err != nil) {
        log.Fatal(err)
    }

    defer file.Close()

    scanner := bufio.NewScanner(file)

    last_commit_id := ""
    for scanner.Scan() {
        last_commit_id = scanner.Text()  
    }

    last_commit_dir := path.Join(ctr_obj.commits_dir_path, last_commit_id)

    // iterate through the last commit dir
    file2hash := make(map[string]string);

    committed_files, _ := os.ReadDir(last_commit_dir)

    // create an encryption object
    enc_obj := sha256.New()

    for _, file_entry := range(committed_files) {
        copy_file_to_hash(&enc_obj, file_entry.Name())
        file2hash[file_entry.Name()] = fmt.Sprintf("%x", enc_obj.Sum(nil)) 
        // reset the encoder 
        enc_obj.Reset()
    } 
    
    return file2hash
}



func (ctr_obj Controler) create_commit(commit_msg string) string{  
    // get the tracked files
    tracked_files := ctr_obj.get_tracked_files()

    // get the hashed version of the repository from last commit
    last_commit_hash := ctr_obj.fetch_last_commit_version()

    enc_obj := sha256.New()

    var no_change bool = true;

    for file, old_hash := range last_commit_hash {
        if slices.Contains(tracked_files, file) {
            copy_file_to_hash(&enc_obj, file)
            new_hash := fmt.Sprintf("%x", enc_obj.Sum(nil))
            enc_obj.Reset()

            if new_hash != old_hash {
                no_change = false
                break
            } 
        }     
    }

    if no_change {
        return "Nothing to commit."
    }




    // at this point create the hash for the commit_msg 
    enc_obj.Write([]byte(commit_msg))
    commit_msg_hash := fmt.Sprintf("%x", enc_obj.Sum(nil))
    enc_obj.Reset()

    // create the repository
    new_commit_dir := path.Join(ctr_obj.commits_dir_path, commit_msg_hash)
    os.MkdirAll(new_commit_dir, os.ModePerm)

    // copy all files
    for _, t_file := range tracked_files {
        // open the original file
        source_file, _ := os.Open(t_file)
        defer source_file.Close()

        des_file, _ := os.Create(path.Join(ctr_obj.commits_dir_path, t_file))
        defer des_file.Close()

        io.Copy(source_file, des_file)
    }

    // create an extra file
    commit_info_txt_file, _ := os.Create(path.Join(new_commit_dir, "commit_info.txt"))

    io.Copy()

}


func main() {
	current_dir, _ := os.Getwd()
	vcs_dir := path.Join(current_dir, "vcs")

    // build the directory where the files will be saved

	config_path := path.Join(vcs_dir, "config.txt")
	index_path := path.Join(vcs_dir, "index.txt")
    log_path := path.Join(vcs_dir, "log.txt")
    commits_dir_path := path.Join(vcs_dir, "commits")

	ctr_obj := Controler{vsc_dir: vcs_dir,
        index_file_path: index_path,
        config_file_path: config_path,
        log_file_path: log_path,
        commits_dir_path: commits_dir_path,
    }

	ctr_obj.set_up()

	args := os.Args

	var command string;

	if len(args) == 1 {
		command = "help";
	} else {
		command = strings.ReplaceAll(args[1], "-", "",)			
	}

	switch command {
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
	default:
		fmt.Println(help_message(command))
	}
	

}
