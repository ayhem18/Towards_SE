package account;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import jakarta.validation.ConstraintViolationException;
import org.apache.coyote.Response;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import java.time.LocalDateTime;


class ExistingIdException extends RuntimeException{
    public ExistingIdException(String message) {
        super(message);
    }
}


class NoSuchIdException extends RuntimeException{
    public NoSuchIdException(String message) {
        super(message);
    }
}


class BreachedPasswordException extends RuntimeException {
    public BreachedPasswordException() {
        super("The password is in the hacker's database!");
    }
}

class InvalidPasswordException extends RuntimeException {
    public InvalidPasswordException(String message) {
        super(message);
    }
}

class OldNewPasswordsMatch extends RuntimeException {
    public OldNewPasswordsMatch() {
        super("The passwords must be different!");
    }
}


// make it JSON serializable with the jackson annotations
// Passing non JSON-Serializable object to the ResponseEntity class would raise
//HttpMediaTypeNotAcceptableException
@JsonPropertyOrder({"statusCode", "timestamp", "message", "description"})
class CustomErrorMessage {

    private int statusCode;

    private LocalDateTime timestamp;

    private String message;

    private String description;

    public CustomErrorMessage(
            int statusCode,
            LocalDateTime timestamp,
            String message,
            String description) {

        this.statusCode = statusCode;
        this.timestamp = timestamp;
        this.message = message;
        this.description = description;
    }

    public CustomErrorMessage() {};

    public int getStatusCode() {
        return statusCode;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public String getMessage() {
        return message;
    }

    public String getDescription() {
        return description;
    }
}

@ControllerAdvice
public class ControllerExceptionHandler extends ResponseEntityExceptionHandler {
    private ResponseEntity<CustomErrorMessage> handle(
            RuntimeException e, WebRequest request, HttpStatus s) {
        CustomErrorMessage body = new CustomErrorMessage(
                s.value(),
                LocalDateTime.now(),
                e.getMessage(),
                request.getDescription(false));
        return new ResponseEntity<>(body, s);
    }


    // make sure the Class in the @exceptionHandler annotation is the same as in the signature
    @ExceptionHandler(ExistingIdException.class)
    public ResponseEntity<CustomErrorMessage> handleExistingIdException(
            ExistingIdException e, WebRequest request) {
        return handle(e, request, HttpStatus.BAD_REQUEST);
    }


    @ExceptionHandler(NoSuchIdException.class)
    public ResponseEntity<CustomErrorMessage> handleNoSuchIdFoundException(
            NoSuchIdException e, WebRequest request) {

        return handle(e, request, HttpStatus.NOT_FOUND);
    }

    // custom exception handlers must be public to be accessed
    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<CustomErrorMessage> handleConstraintViolationException(
            ConstraintViolationException e, WebRequest request) {
        return handle(e, request, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(BreachedPasswordException.class)
    public ResponseEntity<CustomErrorMessage> handleBreachedPasswordException(
            BreachedPasswordException e, WebRequest request) {
        return handle(e, request, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(InvalidPasswordException.class)
    public ResponseEntity<CustomErrorMessage> handleInvalidPasswordException(
            InvalidPasswordException e, WebRequest request) {
        return handle(e, request, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(OldNewPasswordsMatch.class)
    public ResponseEntity<CustomErrorMessage> handleOldNewPasswordsMatch(
            OldNewPasswordsMatch e, WebRequest request) {
        return handle(e, request, HttpStatus.BAD_REQUEST);
    }

    // overload the built-in exceptions
    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
            MethodArgumentNotValidException ex,
            HttpHeaders headers,
            HttpStatusCode status,
            WebRequest request) {
        CustomErrorMessage c = new CustomErrorMessage(status.value(),LocalDateTime.now(), ex.getMessage(), request.getDescription(false));
        return new ResponseEntity<>(c, headers, status);
    }

}
