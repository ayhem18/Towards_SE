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
