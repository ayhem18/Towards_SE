package engine.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.FORBIDDEN)
public class NonUserQuizException extends RuntimeException{
    public NonUserQuizException(String message) {
        super(message);
    }
}
