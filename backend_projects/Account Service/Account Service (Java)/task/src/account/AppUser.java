package account;


import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.data.repository.CrudRepository;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collection;
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
    private String password;

    public AppUserRegistryRequest(String firstName, String lastName, String email, String password) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
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
        return email;
    }

    public String getPassword() {
        return password;
    }
}


// IMPORTANT: MAKE SURE TO PASS THE @Entity annotation so that JPA knows
// it represents a table

// EACH entity must have at least one field with the @Id annotation
@Entity
public class AppUser {
    // possibly using the embeddable thingy
    // to work with first and last names as a single entity...
    @JsonProperty("name")
    private String firstName;
    @JsonProperty("lastname")
    private String lastName;

    @Id
    private String email;

    // the password should be written :Json to obj
    // but not read: obj to json
    @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
    private String password;

    public AppUser(String firstName, String lastName, String email, String password) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.password = password;
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
    public Optional<AppUser> findByEmail(String email);
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


// let's add the User Controller
@RestController
@Validated // used to verify Request Bodies
class UserController {

    private final UserRepository userRepo;

    @Autowired
    public UserController(UserRepository userRepo) {
        this.userRepo = userRepo;
    }

    @Bean(name="passwordEncoder") // will be used for any user related encryption / decryption processes
    public PasswordEncoder byteEncoder(){
        return new BCryptPasswordEncoder();
    }

    @Bean(name="userObjectMapper")
    public ObjectWriter userJsonWriter() {
        return new ObjectMapper().writerWithDefaultPrettyPrinter();
    }


    @PostMapping("api/auth/signup")
    public String signUpUser(@Valid @RequestBody AppUserRegistryRequest request) throws JsonProcessingException {
        // make sure the email does not already exist
//        if (this.userRepo.findByEmail(request.getEmail()).isPresent()) {
//            throw new ExistingIdException("There is already a user with the email " + request.getEmail());
//        }

        // initialize the user object
        AppUser appUser = new AppUser(request.getFirstName(),
                request.getLastName(),
                request.getEmail(),
                this.byteEncoder().encode(request.getPassword())
        );

//        // save the user to the database
//        this.userRepo.save(appUser);

        // return the user representation
        return this.userJsonWriter().writeValueAsString(appUser);

    }
}

