package engine;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import com.fasterxml.jackson.databind.ObjectMapper;


import java.util.ArrayList;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Null;
import javax.validation.constraints.Size;
import java.util.concurrent.ConcurrentHashMap;


// I don't understand why Jackson works with the constructor of the Question class
// while it doesn't with the AnswerResponseObject class

@JsonPropertyOrder({"id", "title", "text", "options"}) // setting the order of serialization
class Question {
    private static int QUIZ_COUNT = 0;
    private final int id;

    @NotBlank // this means the string can neither be null not empty (with only white spaces...)
    private final String title;
    @NotBlank
    private final  String text;

    @NotNull // setting the notNull requirement is indeed helpful...
    @Size(min=2) // at least 2 options
    private final  List<String> options;

    // according to
    // https://stackoverflow.com/questions/12505141/only-using-jsonignore-during-serialization-but-not-deserialization
    // this means the property will be ignored during serialization (to Json), but considered during deserialization
    // to the original format

    //    @NotNull
    @JsonProperty(access=JsonProperty.Access.WRITE_ONLY)
    private final List<Integer> answer;

    public Question(String title,
                    String text,
                    List<String> options,
                    List<Integer> answer) {
        this.title = title;
        this.text = text;
        this.options = options;

        if (answer == null) {
            answer = new ArrayList<>();
        }
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

    public List<Integer> getAnswer() {
        return this.answer;
    }
}



@SpringBootApplication
@RestController // this is necessary for the app to intercept the api requests...
@Validated // the input data can be validated using annotations: https://hyperskill.org/learn/step/9355
public class WebQuizEngine {
    private static final ConcurrentHashMap<Integer, Question> QUESTIONS_MAP = new ConcurrentHashMap<>();

    private static final String correctStringFeedback = "Congratulations, you're right!";
    private static final String wrongStringFeedback = "Wrong answer! Please, try again.";

    public static void main(String[] args) {
        SpringApplication.run(WebQuizEngine.class, args);
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
    public String addQuiz(@Valid @RequestBody Question question) { // add the @Valid annotation to validate the request body
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
    public String AnswerQuiz(@PathVariable(value = "id") int id, @RequestBody QuizAnswerRequest userAnswer) {

        if (! QUESTIONS_MAP.containsKey(id)) {
            throw new NoExistingIdException(id);
        }

        boolean success = userAnswer.correctAnswers(QUESTIONS_MAP.get(id).getAnswer());
        ServerResponse res = new ServerResponse(success,
                success ? WebQuizEngine.correctStringFeedback: WebQuizEngine.wrongStringFeedback);

        try {
            return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(res);
        } catch (JsonProcessingException e) {
            return e.toString();
        }
    }


    @GetMapping("api/quizzes/{id}/__get")
    public List<Integer> getQuizAnswer(@PathVariable(value = "id") int id) {

        if (! QUESTIONS_MAP.containsKey(id)) {
            throw new NoExistingIdException(id);
        }

        List<Integer> answer = QUESTIONS_MAP.get(id).getAnswer();
//        System.out.println(answer);
        return answer;
    }

}