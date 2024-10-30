package com.example.quizz_app;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
class BeanPasswordEncoder {
    // this way the encoder will be a singleton object (hence the same salt and the same validation mechanism)
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(10);
    }
}


// this class works as expected
@Configuration
class SecurityConfig {
    private final PasswordEncoder pe;

    @Autowired
    SecurityConfig(PasswordEncoder passwordEncoder) {
        this.pe = passwordEncoder;
    }

    @Bean(name="userDetailsProvider")
    public UserDetailsService userDetailsService() {
        // saving the users in memory
        UserDetails user1 = User.withUsername("user1")
                .password("pass1") // store the raw password to see if the issue is with the encoding
                .roles("role1")
                .build();

        UserDetails user2 = User
//                .withDefaultPasswordEncoder() // deprecated
                .withUsername("user2")
                .password("pass2") // store the raw password to see if the issue is with the encoding
                .roles("role2")
                .build();

        UserDetails user3 = User
                .withUsername("user3")
                .password(this.pe.encode("pass3"))
                .roles() // has no roles, so he should not be authenticated
                .build();

        return new InMemoryUserDetailsManager(user1, user2, user3);
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        // the requestMatchers should be called from specific to general patterns

        return
                http.httpBasic(Customizer.withDefaults())
                .csrf(AbstractHttpConfigurer::disable)
                .authorizeHttpRequests(
//                        auth -> auth.anyRequest().permitAll()
                        auth -> auth.requestMatchers("/api/car/clear").authenticated().
                                anyRequest().permitAll()
                ).build();
    }
}

//@Configuration
//class SecurityConfig {
//    // saving the users in-memory
//    @Bean
//    public UserDetailsService userDetailsService() {
//        UserDetails user1 = User.withUsername("user1")
//                .password(this.passwordEncoder().encode("pass1"))
//                .roles()
//                .build();
//
//        UserDetails user2 = User
////                .withDefaultPasswordEncoder() // deprecated
//                .withUsername("user2")
//                .password(this.passwordEncoder().encode("pass2"))
//                .roles()
//                .build();
//
//        return new InMemoryUserDetailsManager(user1, user2);
//    }
//
//    public PasswordEncoder passwordEncoder() {
//        // returning a delegated password encoder works (recommended by the Hyperskill course)
//        // return PasswordEncoderFactories.createDelegatingPasswordEncoder();
//
//        // let's explore another way that is unlikely to work
//        // this actually still works somehow...
//        return new BCryptPasswordEncoder();
//    }
//}