package utils

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


type S struct { // this accessible because the struct name is Capitalized...
	AccF1 string; // this will be accessible from anywhere in the main.go file
	AccF2 string; // this won't be accessible; even for declaration
}
