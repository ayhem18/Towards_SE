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
import org.springframework.security.crypto.factory.PasswordEncoderFactories;
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

    @Bean
    public UserDetailsService userDetailsService() {
        // saving the users in memory
        UserDetails user1 = User.withUsername("user1")
                .password(this.pe.encode("pass1"))
                .roles()
                .build();

        UserDetails user2 = User
//                .withDefaultPasswordEncoder() // deprecated
                .withUsername("user2")
                .password(this.pe.encode("pass2"))
                .roles()
                .build();

        return new InMemoryUserDetailsManager(user1, user2);
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        // the requestMatchers should be called from specific pattern to general ones
        HttpSecurity h = http.authorizeHttpRequests(
                mr -> mr.requestMatchers("/**").hasAnyRole("rol1", "rol2", "no Role") // this mean
                        .anyRequest().denyAll() // deny any request to any internal endpoint for example
        );

        return h.httpBasic(Customizer.withDefaults()) // enable the default http settings
                .csrf(AbstractHttpConfigurer::disable) // disable the csrf thingy for now
                .build();
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