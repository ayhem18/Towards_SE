package account;

import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.repository.CrudRepository;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Component;

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
