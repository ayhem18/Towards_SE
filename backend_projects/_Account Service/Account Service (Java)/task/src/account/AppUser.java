package account;

import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.data.repository.CrudRepository;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Optional;


class AppUserRegistryRequest {
    @NotBlank
    @JsonProperty("name")
    private String firstName;
    @JsonProperty("lastname")
    @NotBlank
    private String lastName;

    @NotBlank
    @Pattern(regexp = ".+@acme\\.com$", message="The username should correspond to an email: <username>@<domain>.<org>")
    private String email;

    @NotBlank
//    @SecurePasswordConstraint() // the password will be validated from now on...
    private String password;

    public AppUserRegistryRequest(String firstName, String lastName, String email, String password) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email.toLowerCase();
        this.password = password;
    }

    // add a no arg constructor just in case
    public AppUserRegistryRequest() {}

    @JsonGetter("name")
    public String getFirstName() {
        return firstName;
    }

    @JsonGetter("lastname")
    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email.toLowerCase();
    }

    public String getPassword() {
        return password;
    }
}




// IMPORTANT: MAKE SURE TO PASS THE @Entity annotation so that JPA recognizes it as a database TABLE
@Entity
public class AppUser {

    private static long NUM_USERS = 0;

    // https://stackoverflow.com/questions/277630/hibernate-jpa-sequence-non-id
    //  @Generated(event = EventType.INSERT)
    // it did not work as expected ...
    private long id;

    // possibly using the embeddable thingy
    // to work with first and last names as a single entity...
    @JsonProperty("name")
    private String firstName;
    @JsonProperty("lastname")
    private String lastName;

    // EACH entity must have at least one field with the @Id annotation
    @Id
    private String email;

    // the password should be written :Json to obj
    // but not read: obj to json
    @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
    private String password;

    public AppUser(String firstName, String lastName, String email, String password) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email.toLowerCase();
        this.password = password;
        this.id = NUM_USERS;
        NUM_USERS += 1;
    }

    // add a no arg constructor just in case
    public AppUser() {}

    @JsonGetter("name")
    public String getFirstName() {
        return firstName;
    }

    @JsonGetter("lastname")
    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public String getPassword() {
        return password;
    }

    public long getId() {
        return id;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}

class UserDetailsImp implements UserDetails {

    private final AppUser user;

    public UserDetailsImp(AppUser user) {
        this.user = user;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of();
    }

    @Override
    public String getPassword() {
        return user.getPassword();
    }

    @Override
    public String getUsername() {
        return user.getEmail();
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}

// need a CrudRepository to extract users
interface UserRepository extends CrudRepository<AppUser, String> {
    Optional<AppUser> findByEmail(String email);
}


@Component
class AppUserDetailService implements UserDetailsService  {
    private final UserRepository userRepo;

    @Autowired
    public AppUserDetailService(UserRepository userRepo) {
        this.userRepo = userRepo;
    }

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        AppUser user = userRepo.findByEmail(email).orElseThrow(
                () -> new UsernameNotFoundException("There is no user with the email: " + email)
        );
        return new UserDetailsImp(user);
    }
}



@RestController
@Validated // used to verify Request Bodies
class UserController {

    private final PasswordValidator passwordValidator;
    private final UserRepository userRepo;

    @Autowired
    public UserController(UserRepository userRepo, PasswordValidator pv) {
        this.userRepo = userRepo;
        this.passwordValidator = pv;
    }


    @Bean(name = "userObjectMapper")
    public ObjectWriter userJsonWriter() {
        return new ObjectMapper().writerWithDefaultPrettyPrinter();
    }

    @PostMapping("api/auth/signup")
    public String signUpUser(@Valid @RequestBody AppUserRegistryRequest request) throws JsonProcessingException {
        // the least error-prone approach I found so far is just converting all emails to lower-case
        // inside every component that works with the User object
        // The User and UserRegisterRequest classes

        if (this.userRepo.findByEmail(request.getEmail()).isPresent()) {
            throw new ExistingIdException("There is already a user with the email " + request.getEmail());
        }

        // initialize the user object
        AppUser appUser = new AppUser(request.getFirstName(),
                request.getLastName(),
                request.getEmail(),
                this.passwordValidator.encode(request.getPassword()) // calling the passwordValidator.encode() method ensures the password satisfy the security requirements
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

    @PostMapping("api/auth/changepass")
    @Transactional
    public String changePasswords(@AuthenticationPrincipal UserDetails details,
                                  @Valid @RequestBody ChangePasswordRequest request) throws JsonProcessingException{

        // make sure the new password is different from the current one
        AppUser currentUser = this.userRepo.findByEmail(details.getUsername()).get();

        if (this.passwordValidator.match(request.getNewPassword(), currentUser.getPassword())) {
            // make sure the passwords are indeed different
            throw new OldNewPasswordsMatch();
        }
        // encode while satisfying the security requirements
        String newPasswordEncoded = this.passwordValidator.encode(request.getNewPassword());
        currentUser.setPassword(newPasswordEncoded);
        this.userRepo.save(currentUser);

        HashMap<String, String> res = new HashMap<>();
        res.put("email", details.getUsername());
        res.put("status", "The password has been updated successfully");
        return this.userJsonWriter().writeValueAsString(res);

    }
}

