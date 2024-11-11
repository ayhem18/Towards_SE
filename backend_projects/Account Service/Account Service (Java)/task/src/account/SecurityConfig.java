package account;

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
                                .requestMatchers("/api/auth/signup").permitAll()
                                // the line above will allow any request (with any method) to the endpoint in question
                                // the line below will allow POST requests but deny requests with other methods
                                //.requestMatchers(HttpMethod.POST, "/api/auth/signup").permitAll()
                                .anyRequest().authenticated()
                );

        return http.build();
    }
}
