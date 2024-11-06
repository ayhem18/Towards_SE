package engine;

// in this file I will implement the necessary mechanisms to add users

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.repository.CrudRepository;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Component;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.util.*;


// create a wrapper around the request sent by the user
// need to if Jackson works with Record classes
class UserRegisterRequest {
    @NotNull
    @Pattern(regexp = ".+@.+\\..+", message="The username should correspond to an email: <username>@<domain>.<org>")
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
    public String getEmail() {
        return email;
    }
    public String getPassword() {
        return password;
    }
}


@Entity
@Table(name="app_users")
public class User {
    @Id // signals to JPA that the "email" field is the class primary key
    private String email;
    private String passwordEncoded;


    // the name here can be anything (make sure it is not present in any of the two tables...)
    // https://codingnomads.com/spring-data-jpa-joincolumn-configuration
    @OneToMany
    @JoinColumn(name="user_quiz")

    private List<Quiz> quizzes = new ArrayList<>();


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

    public void addQuiz(Quiz q) {
        this.quizzes.add(q);
    }

    public boolean createdQuiz(Quiz q) {
        return this.quizzes.contains(q);
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
