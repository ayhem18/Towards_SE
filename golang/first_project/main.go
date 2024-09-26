package main
import "fmt"



// the project is so plain so far... 

func main() {
	var score int = 0;
	var average float32 = 0.0;

	for i:= 0; i < 3; i++ {
		fmt.Scan(&score)
		average += float32(score);
	}

	// make sure to actually average the score
	average = average / 3

	fmt.Println(average)

	if average >= 60 {
		fmt.Println("Congratulations, you are accepted!")
	} else {
		fmt.Println("We regret to inform you that we will not be able to offer you admission.")
	}
}


