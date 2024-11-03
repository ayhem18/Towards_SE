package engine;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.web.SecurityFilterChain;


// first  add the authorizations
@Configuration
class HttpSecurityConfig {
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.httpBasic(Customizer.withDefaults())
            // added this line of code from the following lesson:
            // https://hyperskill.org/learn/step/3243
            .csrf(AbstractHttpConfigurer::disable)//.headers(cfg -> cfg.frameOptions().disable())
            .authorizeHttpRequests(
                                      auth -> auth
                                              .regexMatchers(HttpMethod.POST, "/api/register").permitAll()
                                              .regexMatchers(HttpMethod.POST, "/actuator/shutdown").permitAll() // leaving this method without authentication
                                              .anyRequest().authenticated()

//                          .anyRequest().authenticated() // any request going forward would require authentication
                );

//                    auth -> auth.regexMatchers(HttpMethod.POST, "/*").permitAll()
//                    .regexMatchers(HttpMethod.GET, "/*").permitAll()


        return http.build();
    }
}
