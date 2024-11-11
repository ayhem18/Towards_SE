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
            .csrf(AbstractHttpConfigurer::disable)
            .authorizeHttpRequests(
                                      auth -> auth
                                              .requestMatchers(HttpMethod.POST, "/api/register").permitAll()
                                              .requestMatchers(HttpMethod.POST, "/actuator/shutdown").permitAll() // leaving this method without authentication
                                              .anyRequest().authenticated()
             );

        return http.build();
    }
}
