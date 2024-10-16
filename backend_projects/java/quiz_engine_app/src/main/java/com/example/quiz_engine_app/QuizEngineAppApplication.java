package com.example.quiz_engine_app;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.web.bind.annotation.*;
import com.fasterxml.jackson.databind.ObjectMapper;


import java.util.List;

// let's start with something very simple
@JsonPropertyOrder({"title", "title", "options"}) // setting the order of serialization
@JsonIgnoreProperties({"answer_index"}) // ignoring the answer index
class Question {
	private final String title;
	private final  String text;
	private final  List<String> options;
	private final  int answer_index;

	public Question(String title, String text, List<String> options, int answer_index) {
		this.title = title;
		this.text = text;
		this.options = options;
		this.answer_index = answer_index;
	}

	public String getTitle() {
		return title;
	}

	public String getText() {
		return text;
	}

	public List<String> getOptions() {
		return options;
	}

	public int getAnswer_index() {
		return answer_index;
	}
}

// got to find different approaches to create Json like responses than just creating random objects

class ServerResponse {
	private final boolean  success;
	private final String feedback;

	public ServerResponse(boolean success, String feedback) {
		this.success = success;
		this.feedback = feedback;
	}

	// jackson fails without getters
	public boolean isSuccess() {
		return success;
	}

	public String getFeedback() {
		return feedback;
	}
}



@SpringBootApplication
@RestController // this is necessary for the app to intercept the api requests...
public class QuizEngineAppApplication {

	private static final List<Question> questions = List.of(
			new Question("The Java Logo",
					"What is depicted on the Java logo?",
					List.of("Robot","Tea leaf","Cup of coffee","Bug"),
					2
					)
	);

	private static final String correctStringFeedback = "Congratulations, you're right!";
	private static final String wrongStringFeedback = "Wrong answer! Please, try again.";


	public static void main(String[] args) {
		SpringApplication.run(QuizEngineAppApplication.class, args);
	}

	@GetMapping("api/quiz")
	public String GetQuiz() {
		// create the object Mapper
		ObjectMapper mapper = new ObjectMapper();
		// the main idea here is to return a description of the quiz question
		try{
			return mapper.writerWithDefaultPrettyPrinter().writeValueAsString(QuizEngineAppApplication.questions.get(0));
		} catch (JsonProcessingException e) {
        	return "some error happened";
		}
    }


	@PostMapping("api/quiz")
	public String AnswerQuiz(@RequestParam(name = "answer") int answer_index) {
		boolean success = answer_index == QuizEngineAppApplication.questions.get(0).getAnswer_index();
		ServerResponse res = new ServerResponse(success,
				success ? QuizEngineAppApplication.correctStringFeedback: QuizEngineAppApplication.wrongStringFeedback);
		try {
			return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(res);
		} catch (JsonProcessingException e) {
			return e.toString();
		}
	}

}
