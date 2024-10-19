package com.example.quizzz;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import com.fasterxml.jackson.databind.ObjectMapper;


import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

// let's start with something very simple
@JsonPropertyOrder({"id", "title", "text", "options"}) // setting the order of serialization
class Question {
	private static int QUIZ_COUNT = 0;
	private final int id;

	private final String title;
	private final  String text;
	private final  List<String> options;

	// according to
	// https://stackoverflow.com/questions/12505141/only-using-jsonignore-during-serialization-but-not-deserialization
	// this means the property will be ignored during serialization (to Json), but considered during deserialization
	// to the original format
	@JsonProperty(access=JsonProperty.Access.WRITE_ONLY)
	private final  int answer;


	public Question(String title,
					String text,
					List<String> options,
					int answer) {
		this.title = title;
		this.text = text;
		this.options = options;
		this.answer = answer;
		QUIZ_COUNT += 1;
		this.id = QUIZ_COUNT;
	}

	public int getId() {
		return id;
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

	public int getAnswer() {
		return answer;
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

@ResponseStatus(code = HttpStatus.BAD_REQUEST)
class NoExistingIdException extends RuntimeException {
	private static String defaultErrorMessageFormatter(int id) {
		return "There is no quiz with the id " + id;
	}

	public NoExistingIdException(int id) {
		super(NoExistingIdException.defaultErrorMessageFormatter(id));
	}
}



@SpringBootApplication
@RestController // this is necessary for the app to intercept the api requests...
public class QuizEngineApplication {
	// updating the controller

	private static final ConcurrentHashMap<Integer, Question> QUESTIONS_MAP = new ConcurrentHashMap<>();

	private static final String correctStringFeedback = "Congratulations, you're right!";
	private static final String wrongStringFeedback = "Wrong answer! Please, try again.";


	public static void main(String[] args) {
		SpringApplication.run(QuizEngineApplication.class, args);
	}

	@GetMapping("api/quizzes")
	public String GetQuiz() {
		try {
			return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(QUESTIONS_MAP.values());
		} catch (JsonProcessingException e) {
			return e.toString();
		}
	}

	@PostMapping("api/quizzes")
	public String addQuiz(@RequestBody Question question) {
		// extract the id
		int question_id = question.getId();
		// add the question
		QUESTIONS_MAP.put(question_id, question);
		try {
			return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(question);
		} catch (JsonProcessingException e) {
			return e.toString();
		}
	}

	@GetMapping("api/quizzes/{id}")
	public String getQuizById(@PathVariable(value="id") int id) {
		if (! QUESTIONS_MAP.containsKey(id)) {
			throw new NoExistingIdException(id);
		}

		try {
			return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(QUESTIONS_MAP.get(id));
		} catch (JsonProcessingException e) {
			return e.toString();
		}
	}

	@PostMapping("api/quizzes/{id}/solve")
	public String AnswerQuiz(@PathVariable(value = "id") int id,
							@RequestParam(name = "answer") int answer_index) {

		if (! QUESTIONS_MAP.containsKey(id)) {
			throw new NoExistingIdException(id);
		}

		boolean success = answer_index == QuizEngineApplication.QUESTIONS_MAP.get(id).getAnswer();
		ServerResponse res = new ServerResponse(success,
				success ? QuizEngineApplication.correctStringFeedback: QuizEngineApplication.wrongStringFeedback);

		try {
			return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(res);
		} catch (JsonProcessingException e) {
			return e.toString();
		}
	}


	@GetMapping("api/quizzes/{id}/__get")
	public int getQuizAnswer(@PathVariable(value = "id") int id) {

		if (! QUESTIONS_MAP.containsKey(id)) {
			throw new NoExistingIdException(id);
		}

		int answer = QUESTIONS_MAP.get(id).getAnswer();
		System.out.println(answer);
		return answer;
	}

}
