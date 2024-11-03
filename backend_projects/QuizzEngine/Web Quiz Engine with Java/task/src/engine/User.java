package engine;

// in this file I will implement the necessary mechanisms to add users

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import engine.exceptions.ExistingIdException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;;
import org.springframework.data.repository.CrudRepository;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import javax.persistence.*;
import javax.validation.Valid;
import javax.validation.constraints.Email;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.util.Collection;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;




// create a wrapper around the request sent by the user
// need to if Jackson works with Record classes
class UserRegisterRequest {
    @NotNull
    @Email // verify whether the user is passing an email-like string
    private String email;

    @NotNull
    @Size(min=5) // the password must be of at least 5 characters
    private String password;

    public UserRegisterRequest(String email, String password) {
        this.email = email;
        this.password = password;
    }

    public UserRegisterRequest() {

    }

    // getters for the Jackson package...
    public @NotNull @Email String getEmail() {
        return email;
    }
    public @NotNull @Size(min = 5) String getPassword() {
        return password;
    }
}


@Entity
@Table(name="User")
public class User {
    @Id // signals to JPA that the "email" field is the class primary key
    private String email;
    private String passwordEncoded;

    public User(String email, String passwordEncoded) {
        this.email = email;
        this.passwordEncoded = passwordEncoded;
    }

    public User() {
    }

    // getters and setters
    public String getEmail() {
        return email;
    }

    public String getPasswordEncoded() {
        return passwordEncoded;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setPasswordEncoded(String passwordEncoded) {
        this.passwordEncoded = passwordEncoded;
    }
}

// create a user CRUD repository
interface UserRepo extends CrudRepository<User, String> {
    // add a method to load user by email
    Optional<User> findUserByEmail(String email);
}


// the UserDetailsService class returns an implementation of the UserDetails interface
// userDetails basically is a mechanism to control access to the user's information
class UserDetailsImp implements UserDetails {
    private final User user;
    public UserDetailsImp(User user) {
        this.user = user;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        // for the moment users do not have authorities
        return List.of();
    }

    @Override
    public String getPassword() {
        return user.getPasswordEncoded();
    }

    @Override
    public String getUsername() {
        return user.getEmail();
    }

    // if this function returns False, the corresponding user will not be authorized !!!!
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    // if this function returns False, the corresponding user will not be authorized !!!!
    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    // if this function returns False, the corresponding user will not be authorized !!!!
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}


// in order to use SpringSecurity built-in authentication mechanisms
// need to have a UserDetailService Bean object
@Component
class UserDetailServiceImp implements UserDetailsService {
    private final UserRepo repo;

    @Autowired // the autowired can be omitted, but why would I do such a thing ??
    public UserDetailServiceImp(UserRepo repo) {
        this.repo = repo;
    }

    @Override
    public UserDetails loadUserByUsername(String userIdentifier) throws UsernameNotFoundException {
        // the idea here is simple
        System.out.println("\nTHE loadUserByUsername is called with the argument: " + userIdentifier + "\n");

        User user = repo.findUserByEmail(userIdentifier).
                orElseThrow(() -> new UsernameNotFoundException("There is no user with the email " + userIdentifier));



        // wrap the user in a userDetails object
        return new UserDetailsImp(user);
    }
}


// let's add a controller for the users
//@RestController
//@Validated
//class UserController {
//    // one crucial remark is that Interface fields can cause issues if not injected by
//    // constructor or field DI
//    private final UserRepo userRepo;
//
//    @Autowired
//    public UserController(UserRepo repo){
//        this.userRepo = repo;
//    }
//
//    @PostMapping("/api/register")
//    public String userRegisterEndpoint(@Valid @RequestBody UserRegisterRequest req) {
//        // I did not find a way to throw an exception with the "ifPresent" method of the Optional class
//
//        try {
//            this.userRepo.findUserByEmail(req.getEmail()).get();
//        } catch (NoSuchElementException e ) {
//            // create the user
//            User user = new User(req.getEmail(), this.passwordEncoder().encode(req.getPassword()));
//            this.userRepo.save(user);
//            int count = ((Long) this.userRepo.count()).intValue();
//            return "user with email " + user.getEmail() + " was added successfully. Total number of users: " + count;
//        }
//        throw new ExistingIdException("There is already a user with the email " + req.getEmail());
//    }
//
//    @GetMapping("/api/hidden/users")
//    public String getAllUsers() throws JsonProcessingException {
//        return new ObjectMapper().writerWithDefaultPrettyPrinter().writeValueAsString(this.userRepo.findAll());
//    }
//
//    @Bean
//    public PasswordEncoder passwordEncoder() {
//        return new BCryptPasswordEncoder();
//    }
//
//}

