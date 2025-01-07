package account;

/*
This file contains the code for the layer in between the presentation layer and the data layer...
 */

import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.Constraint;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.lang.annotation.*;
import java.util.List;
import java.util.Set;

// create a custom annotation to verify the password
// inspired from https://www.baeldung.com/spring-mvc-custom-validator

//@Documented
//@Constraint(validatedBy = SecurePasswordValidator.class)
//@Target( { ElementType.FIELD })
//@Retention(RetentionPolicy.RUNTIME)
//@interface SecurePasswordConstraint { }
//class SecurePasswordValidator implements ConstraintValidator<SecurePasswordConstraint, String> {
//    private static final Set<String> BREACHED_PASSWORDS = Set.of(
//            "PasswordForJanuary",
//            "PasswordForFebruary",
//            "PasswordForMarch",
//            "PasswordForApril",
//            "PasswordForMay",
//            "PasswordForJune",
//            "PasswordForJuly",
//            "PasswordForAugust",
//            "PasswordForSeptember",
//            "PasswordForOctober",
//            "PasswordForNovember",
//            "PasswordForDecember");
//
//    @Override
//    public void initialize(SecurePasswordConstraint contactNumber) {
//    }
//
//    @Override
//    public boolean isValid(String passwordField,
//                           ConstraintValidatorContext cxt) {
//        // mainly 3 validity conditions
//        // 1. not Null
//        // 2. at least 12 characters long
//        // 3. is not in the list of breached passwords
//        return passwordField != null && passwordField.length() >= 12 && ! BREACHED_PASSWORDS.contains(passwordField);
//    }
//}


@Configuration
class PasswordValidator {
    @Bean(name = "BreachedPasswordsRaw")
    public Set<String> breachedPasswordsRaw() {
        return Set.of(
                "PasswordForJanuary",
                "PasswordForFebruary",
                "PasswordForMarch",
                "PasswordForApril",
                "PasswordForMay",
                "PasswordForJune",
                "PasswordForJuly",
                "PasswordForAugust",
                "PasswordForSeptember",
                "PasswordForOctober",
                "PasswordForNovember",
                "PasswordForDecember");
    }

    @Bean(name = "userPasswordEncoder") // will be used for any user related encryption / decryption processes
    public PasswordEncoder byteEncoder() {
        return new BCryptPasswordEncoder(); // the strength is automatically set to be as large as possible...
    }


    @Bean(name = "BreachedPasswordsEncoded")
    public List<String> breachedPasswordsEncodedBean() {
        return this.breachedPasswordsRaw().stream().map(this.byteEncoder()::encode).toList();
    }

    public String encode(String rawPassword) throws BreachedPasswordException{
        // make sure the string is a valid and not breached
        if (rawPassword.length() < 12) {
            throw new InvalidPasswordException("Password length must be 12 chars minimum!");
        }

        if (this.breachedPasswordsRaw().contains(rawPassword)) {
            throw new BreachedPasswordException();
        }

        return this.byteEncoder().encode(rawPassword);
    }

    public boolean match(String rawPassword, String encodedPassword) {
        return this.byteEncoder().matches(rawPassword, encodedPassword);
    }
}


//class AppUserRegistryRequest {
//    @NotBlank
//    @JsonProperty("name")
//    private String firstName;
//    @JsonProperty("lastname")
//    @NotBlank
//    private String lastName;
//
//    @NotBlank
//    @Pattern(regexp = ".+@acme\\.com$", message="The username should correspond to an email: <username>@<domain>.<org>")
//    private String email;
//
//    @NotBlank
////    @SecurePasswordConstraint() // the password will be validated from now on...
//    private String password;
//
//    public AppUserRegistryRequest(String firstName, String lastName, String email, String password) {
//        this.firstName = firstName;
//        this.lastName = lastName;
//        this.email = email.toLowerCase();
//        this.password = password;
//    }
//
//    // add a no arg constructor just in case
//    public AppUserRegistryRequest() {}
//
//    @JsonGetter("name")
//    public String getFirstName() {
//        return firstName;
//    }
//
//    @JsonGetter("lastname")
//    public String getLastName() {
//        return lastName;
//    }
//
//    public String getEmail() {
//        return email.toLowerCase();
//    }
//
//    public String getPassword() {
//        return password;
//    }
//}


class ChangePasswordRequest {    
    @NotBlank
    @JsonProperty("new_password")
    private String newPassword;

    public ChangePasswordRequest(String newPassword) {
        this.newPassword = newPassword;
    }

    public ChangePasswordRequest() {
    }

    @JsonGetter("new_password")
    public String getNewPassword() {
        return newPassword;
    }
}
