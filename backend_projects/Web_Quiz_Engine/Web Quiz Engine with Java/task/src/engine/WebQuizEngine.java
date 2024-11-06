package engine;

import com.fasterxml.jackson.core.JsonProcessingException;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.context.annotation.Bean;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import com.fasterxml.jackson.databind.ObjectMapper;


import java.util.*;



@SpringBootApplication
@RestController // this is necessary for the app to intercept the api requests...
@Validated // the input data can be validated using annotations: https://hyperskill.org/learn/step/9355
public class WebQuizEngine {
    private final QuizRepository quizRepo;
    private final UserRepo userRepo;
    private final int quizPerPage;


    private static final String correctStringFeedback = "Congratulations, you're right!";
    private static final String wrongStringFeedback = "Wrong answer! Please, try again.";

    @Autowired // funny enough the "QuizRepository" is only an interface.
    // however using the repo object created at startup time I can use it without explicit initialization...
    public WebQuizEngine(QuizRepository repo, UserRepo userRepo) {
        this.quizRepo = repo;
        this.userRepo = userRepo;
        this.quizPerPage = 10; // according to the last stage requirements...
    }

    public static void main(String[] args) {
        SpringApplication.run(WebQuizEngine.class, args);
    }

    @GetMapping("api/quizzes/all")
    public String getAllQuizzes() throws JsonProcessingException {
        return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(this.quizRepo.findAll());
    }

    @GetMapping("/api/quizzes")
    public String getQuizzesPaginated(@RequestParam int pageNumber) throws JsonProcessingException {
        // create the PageRequest object to set the page number
        return (new ObjectMapper()).
                writerWithDefaultPrettyPrinter().
                writeValueAsString(
                        this.quizRepo.findAll(PageRequest.of(pageNumber, this.quizPerPage))
                );
    }


    @PostMapping("api/quizzes")
    public String addQuiz(@AuthenticationPrincipal UserDetails details,
                          @RequestBody @Valid Quiz quiz) // add the @Valid annotation to validate the request body
    throws JsonProcessingException {
        try {
            this.quizRepo.save(quiz);
            // extract the user (the user has already been authenticated, so it exists...)
            User user = this.userRepo.findUserByEmail(details.getUsername()).get();
            user.addQuiz(quiz);

            // make sure to save the update on the database level
            this.userRepo.save(user);

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


    @DeleteMapping("api/quizzes/{id}")
    public ResponseEntity<String> deleteQuizById(
            @AuthenticationPrincipal UserDetails details,
            @PathVariable(value="id") int id)
            throws JsonProcessingException
    {
        Quiz q = this.quizRepo.findById(id).orElseThrow(
                () -> new NoSuchIdException("There is no quiz with the id " + id));

        User user = this.userRepo.findUserByEmail(details.getUsername()).get();

        if (! user.createdQuiz(q)) {
            throw new NonUserQuizException("The user " + user.getEmail() + " did not create the quiz " + q.getId() + " and hence cannot delete it");
        }
        String return_string = "Quiz " + q.getId() + " successfully deleted";

        this.quizRepo.deleteById(q.getId());

        return new ResponseEntity<>(return_string, HttpStatus.NO_CONTENT);
    }


    @PostMapping("/api/register")
    public String userRegisterEndpoint(@RequestBody @Valid UserRegisterRequest req) {
        // I did not find a way to throw an exception with the "ifPresent" method of the Optional class
        try {
            this.userRepo.findUserByEmail(req.getEmail()).get();
        } catch (NoSuchElementException e ) {
            // create the user
            User user = new User(req.getEmail(), this.passwordEncoder().encode(req.getPassword()));
            this.userRepo.save(user);
            int count = ((Long) this.userRepo.count()).intValue();
            return "user with email " + user.getEmail() + " was added successfully. Total number of users: " + count;
        }
        throw new ExistingIdException("There is already a user with the email `" + req.getEmail() + "`");
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
