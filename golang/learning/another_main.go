package main

import (
	"fmt"
	"path"
	// "log"
	// "os"
	// "path/filepath"
	// "bufio"
	"strings"

)

// func read_file_size() {
//     var availableSize, size, filesCount int64
//     fmt.Scan(&availableSize)

// 	current_dir, _ := os.Getwd()
// 	mod_go_file := filepath.Join(current_dir, "go.mod")
// 	fileInfo, err := os.Stat(mod_go_file)

//     if err != nil {
//         log.Fatal(err)
//     }

// 	file_size := fileInfo.Size()

//     for {
//         size += file_size
//         if size > availableSize {
//             break
//         }
//         filesCount++
//     }

//     fmt.Println(filesCount)

// }






func main() {
	// var famousPwd string
	// fmt.Scanln(&famousPwd)

	// // Use the correct function to create 'new' MD5 Hash and SHA-256 Hash interfaces below:
	// md5Hash := md5.New()
	// sha256Hash := sha256.New()

	// // Call the correct method that adds the 'famousPwd' to the hash that will be calculated:
	// md5Hash.Write([]byte(famousPwd))
	// sha256Hash.Write([]byte(famousPwd))

	// // Call the method that returns the computed hash slice
	// // And print the hash in hexadecimal notation below:
	// fmt.Printf("%x\n", md5Hash.Sum(nil))
	// fmt.Printf("%x\n", sha256Hash.Sum(nil))

	f := strings.ReplaceAll(".\\learning\\main2.go", "\\", "//")
	fmt.Println(path.Base(f))

}
