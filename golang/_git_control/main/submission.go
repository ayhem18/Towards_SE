package main

import (
	// "_git_control/utils"
	"bufio"
	"crypto/sha256"
	"fmt"
	"io"
	"log"
	"os"
	"path"
	"strings"
    "hash"
)

// add the functions that were written on different files

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


func GetPathBasename(file_path string) string {
	file_path = strings.ReplaceAll(file_path, "\\", "//")
	return path.Base(file_path)
}


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
	// create the .vsc directory 
	os.Mkdir(controller_obj.vsc_dir, os.ModePerm)
	// make the commits directory
	os.MkdirAll(controller_obj.commits_dir_path, os.ModePerm)

	// create the files
    files := []string{controller_obj.config_file_path, controller_obj.index_file_path, controller_obj.log_file_path}

	for _, f := range files {
		// call the os.Create() function only if the file is yet to be created. Otherwise, it will be truncated..
		if _, err := os.Stat(f); err != nil {
			file, _ := os.Create(f)
			file.Close()
		}
	}

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

	// check if the file exists
	if _, err := os.Stat(*argument); err != nil {	
		return fmt.Sprintf("Can't find '%s'.", *argument)
	}
	
	file, _ := os.OpenFile(ctr_obj.index_file_path, os.O_APPEND|os.O_RDWR, os.ModePerm)
	defer file.Close()

	fmt.Fprintln(file, *argument)

	return fmt.Sprintf("The file '%s' is tracked.", *argument)
}


func (ctr_obj Controler) config_message_display_user(full_msg bool) string {
	// read the 'index.txt' file
	file, err := os.Open(ctr_obj.config_file_path)
	
	if err != nil {
		log.Fatal(err)
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)

	// supposedly there is only one user
	
	if scanner.Scan() {
		if full_msg {
			return fmt.Sprintf("The username is %s.", scanner.Text())
		}
		return scanner.Text()
	}

	return _NO_CURRENT_USER
} 


func (ctr_obj Controler) config_message(argument* string) string {
	if argument == nil {
		return ctr_obj.config_message_display_user(true)
	}
	// overwrite the user
	file, _ := os.Create(ctr_obj.config_file_path)
	fmt.Fprintln(file, *argument)
	return fmt.Sprintf("The username is %s.", *argument)
}

func get_hash(s string) string {
	enc_obj := sha256.New()	
    // at this point create the hash for the commit_msg 
    enc_obj.Write([]byte(s))
    return  fmt.Sprintf("%x", enc_obj.Sum(nil))
}


func (ctr_obj Controler) get_last_commit_id() string{
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

	return last_commit_id
}


func (ctr_obj Controler) fetch_last_commit_version(commit_id string) map[string]string{
    commit_dir := path.Join(ctr_obj.commits_dir_path, commit_id)

    // iterate through the last commit dir
    file2hash := make(map[string]string);

    committed_files, _ := os.ReadDir(commit_dir)

    // create an encryption object
    enc_obj := sha256.New()

    for _, file_entry := range(committed_files) {
		file_base_name := file_entry.Name()
        copy_file_to_hash(&enc_obj, path.Join(commit_dir, file_base_name))
        file2hash[file_base_name] = fmt.Sprintf("%x", enc_obj.Sum(nil)) 
        // reset the encoder 
        enc_obj.Reset()
    } 
    
    return file2hash
}


func (ctr_obj Controler) check_changes() bool {
	last_commit_id := ctr_obj.get_last_commit_id()

	// if no commit has been made so far
	if last_commit_id == "" {
		return false
	}

	// get the tracked files
    tracked_files := ctr_obj.get_tracked_files()

    // get the hashed version of the repository from last commit
	// a map with files tracked from the last commit with their hashes
	last_commit_hash := ctr_obj.fetch_last_commit_version(last_commit_id)

	// createa an encoding object
    enc_obj := sha256.New()

    var no_change bool = true;

	// iterate through the tracked files
	for _, t_file := range tracked_files {
		t_file_basename := GetPathBasename(t_file)
		// check if the basename is not present in the hashing
		if _, ok := last_commit_hash[t_file_basename]; ! ok {
			return false
		}
		// at this point check if the hashing is the same
		// get the old hash from the map
		old_hash := last_commit_hash[t_file_basename]

		// calculate the new has
		copy_file_to_hash(&enc_obj, t_file)
		new_hash := fmt.Sprintf("%x", enc_obj.Sum(nil))
		enc_obj.Reset()

		if new_hash != old_hash {
			no_change = false
			break
		} 
	}

	return no_change
}


func (ctr_obj Controler) build_commit_dir(commit_msg string) string {
	tracked_files := ctr_obj.get_tracked_files()
    enc_obj := sha256.New()

    // at this point create the hash for the commit_msg 
    enc_obj.Write([]byte(commit_msg))
    commit_msg_hash := fmt.Sprintf("%x", enc_obj.Sum(nil))

	// create the directory to save the local copy of the directory
    new_commit_dir := path.Join(ctr_obj.commits_dir_path, commit_msg_hash)
    os.MkdirAll(new_commit_dir, os.ModePerm)

    // copy all files
    for _, t_file := range tracked_files {
        // open the original file
        source_file, e1 := os.Open(t_file)		
		if e1 != nil {
			log.Fatal(e1)
		}
        defer source_file.Close()
		
		// the Base function does not work for Windowns ))
		// replace `backslashes` with `forward slashes`
		t_file = strings.ReplaceAll(t_file, "\\", "//")
        des_file, e2 := os.Create(path.Join(new_commit_dir, GetPathBasename(t_file)))

		if e2 != nil {
			log.Fatal(e2)
		}
		defer des_file.Close()

        _, err := io.Copy(des_file, source_file)
		if err != nil {
			log.Fatal(err)
		}
	}

	return new_commit_dir
}


func (ctr_obj Controler) create_commit(commit_msg string) string{  
	no_change := ctr_obj.check_changes()

	if no_change {
        return "Nothing to commit."
    }

	new_commit_dir := ctr_obj.build_commit_dir(commit_msg)

    // create an extra file inside the commit directory to save the commit information
    commit_info_txt_file, _ := os.Create(path.Join(new_commit_dir, "__commit_info.txt"))	
	defer commit_info_txt_file.Close()

	// append the commit_id to the log file
	log_file, _ := os.OpenFile(ctr_obj.log_file_path, os.O_APPEND|os.O_RDWR, os.ModePerm)
	defer log_file.Close()

	// add the commit hash to the log file
	commit_hash := get_hash(commit_msg)
	fmt.Fprintln(log_file, commit_hash)

	// build the commit log in a slice to copy it to the file
	commit_info_str := fmt.Sprintf("Author: %s\n%s", ctr_obj.config_message_display_user(false), commit_msg)
	fmt.Fprint(commit_info_txt_file, commit_info_str)

	return "Changes are committed." 
}


func (ctr_obj Controler) build_commit_log(commit_id string) string {
	// find the commit dir
	commit_dir := path.Join(ctr_obj.commits_dir_path, commit_id)
	// read the commit info
    commit_info_txt_file := path.Join(commit_dir, "__commit_info.txt")

	commit_info_bytes, err := os.ReadFile(commit_info_txt_file)

	if err != nil {
		log.Fatal(err)
	}

	commit_info := string(commit_info_bytes)
	
	return fmt.Sprintf("commit %s\n%s", commit_id, commit_info)
}

func (ctr_obj Controler) log_command() {
	commit_ids := make([]string, 0)
	// read the log text file
	file, _ := os.Open(ctr_obj.log_file_path)
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		commit_ids = append(commit_ids, scanner.Text())
	}

	if len(commit_ids) == 0 {
		fmt.Println("No commits yet.")
		// make sure to exit the function
		return 
	}


	for i := len(commit_ids) - 1; i >= 0; i-- {
		fmt.Println(ctr_obj.build_commit_log(commit_ids[i]))
		if i > 0 {
			fmt.Println()
		}
	}

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

	case "commit": 
		
		if len(args) < 3 {
			fmt.Println("Message was not passed.")
		}else{
			fmt.Println(ctr_obj.create_commit(args[2]))
		}

	case "log":
		ctr_obj.log_command()

	default:
		fmt.Println(help_message(command))
	}

}
