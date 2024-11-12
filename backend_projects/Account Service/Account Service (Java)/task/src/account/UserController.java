package account;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

// let's add the User Controller
@RestController
@Validated // used to verify Request Bodies
public class UserController {

    private final UserRepository userRepo;

    @Autowired
    public UserController(UserRepository userRepo) {
        this.userRepo = userRepo;
    }

    @Bean(name="userPasswordEncoder") // will be used for any user related encryption / decryption processes
    public PasswordEncoder byteEncoder(){
        return new BCryptPasswordEncoder();
    }

    @Bean(name="userObjectMapper")
    public ObjectWriter userJsonWriter() {
        return new ObjectMapper().writerWithDefaultPrettyPrinter();
    }


    @PostMapping("api/auth/signup")
    public String signUpUser(@Valid @RequestBody AppUserRegistryRequest request) throws JsonProcessingException {

        // if I want to impose the case-insensitivity, one way is to process only lowercase versions
        // but that's very error-prone...
        if (this.userRepo.findByEmail(request.getEmail()).isPresent()) {
            throw new ExistingIdException("There is already a user with the email " + request.getEmail());
        }

        // initialize the user object
        AppUser appUser = new AppUser(request.getFirstName(),
                request.getLastName(),
                request.getEmail(),
                this.byteEncoder().encode(request.getPassword())
        );

        // save the user to the database
        this.userRepo.save(appUser);

        // return the user representation
        return this.userJsonWriter().writeValueAsString(appUser);

    }

    @GetMapping("/api/empl/payment")
    public String getUserId(@AuthenticationPrincipal UserDetails details) throws JsonProcessingException {
        // no need to worry about the get method since the user is guaranteed to exist
        // otherwise it would not be authenticated...
        AppUser currentUser = this.userRepo.findByEmail(details.getUsername()).get();
        return this.userJsonWriter().writeValueAsString(currentUser);
    }
}

