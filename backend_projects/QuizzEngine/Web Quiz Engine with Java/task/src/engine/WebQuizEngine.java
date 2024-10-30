package engine;

import com.fasterxml.jackson.core.JsonProcessingException;
import engine.exceptions.ExistingIdException;
import engine.exceptions.NoSuchIdException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.context.annotation.Bean;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import com.fasterxml.jackson.databind.ObjectMapper;

import javax.validation.Valid;
import java.util.NoSuchElementException;

@SpringBootApplication
@RestController // this is necessary for the app to intercept the api requests...
@Validated // the input data can be validated using annotations: https://hyperskill.org/learn/step/9355
public class WebQuizEngine {
    private final QuizRepository quizRepo;
    private final UserRepo userRepo;

    private static final String correctStringFeedback = "Congratulations, you're right!";
    private static final String wrongStringFeedback = "Wrong answer! Please, try again.";

    @Autowired // funny enough the "QuizRepository" is only an interface.
    // however using the repo object created at startup time I can use it without explicit initialization...
    public WebQuizEngine(QuizRepository repo, UserRepo userRepo) {
        this.quizRepo = repo;
        this.userRepo = userRepo;
    }

    public static void main(String[] args) {
        SpringApplication.run(WebQuizEngine.class, args);
    }

    @GetMapping("api/quizzes")
    public String GetAllQuizzes() throws JsonProcessingException {
        return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(this.quizRepo.findAll());
    }

    @PostMapping("api/quizzes")
    public String addQuiz(@Valid @RequestBody Quiz quiz) // add the @Valid annotation to validate the request body
    throws JsonProcessingException {
        // save the new quiz
        try {
            this.quizRepo.save(quiz);
            return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(quiz);

        }catch (RuntimeException e) {
            throw new ExistingIdException("There is already a quiz with the id " + quiz.getId());
        }
    }

    @GetMapping("api/quizzes/{id}")
    public String getQuizById(@PathVariable(value="id") int id) throws JsonProcessingException{
        Quiz q = this.quizRepo.findById(id).orElseThrow(
                () -> new NoSuchIdException("There is no quiz with the id " + id));

        return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(q);
    }

    @PostMapping("api/quizzes/{id}/solve")
    public String answerQuiz(@PathVariable(value = "id") int id,
                             @RequestBody QuizAnswerRequest userAnswer) throws JsonProcessingException {
        // the exception will be thrown
        Quiz q = this.quizRepo.findById(id).orElseThrow(() ->
                new NoSuchIdException("There is no quiz with the id " + id));

        // determine whether the answer is correct
        boolean success = userAnswer.correctAnswers(q.getAnswer());
        // prepare the object
        ServerResponse res = new ServerResponse(success,
                success ? WebQuizEngine.correctStringFeedback: WebQuizEngine.wrongStringFeedback);

        return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(res);
    }


    @GetMapping("api/quizzes/clear")
    public String clearQuizzes() {
        this.quizRepo.deleteAll();
        int count = ((Long) this.quizRepo.count()).intValue();
        return "the number of quizzes in the database " + count;
    }



    @PostMapping("/api/user")
    public String userRegisterEndpoint(@Valid @RequestBody UserRegisterRequest req) {
        // I did not find a way to throw an exception with the "ifPresent" method of the Optional class

        try {
            this.userRepo.findUserByEmail(req.getEmail()).get();
        } catch (NoSuchElementException e ) {
            // create the user
            User user = new User(req.getEmail(), this.passwordEncoder().encode(req.getPassword()));
            this.userRepo.save(user);
            int count = ((Long) this.quizRepo.count()).intValue();
            return "user with email " + user.getEmail() + " was added successfully. Total number of users: " + count;
        }
        throw new ExistingIdException("There is already a user with the email " + req.getEmail());
    }

    @GetMapping("/api/hidden/users")
    public String getAllUsers() throws JsonProcessingException {
        return new ObjectMapper().writerWithDefaultPrettyPrinter().writeValueAsString(this.userRepo.findAll());
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

//    @GetMapping("api/quizzes/{id}/__get")
//    public List<Integer> getQuizAnswer(@PathVariable(value = "id") int id) {
//
//        if (! QuizS_MAP.containsKey(id)) {
//            throw new NoExistingIdException(id);
//        }
//
//        List<Integer> answer = QuizS_MAP.get(id).getAnswer();
////        System.out.println(answer);
//        return answer;
//    }

}