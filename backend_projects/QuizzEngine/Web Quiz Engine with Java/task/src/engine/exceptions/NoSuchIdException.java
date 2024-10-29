package engine.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class NoSuchIdException extends RuntimeException{
    public NoSuchIdException(String message) {
        super(message);
    }
}
