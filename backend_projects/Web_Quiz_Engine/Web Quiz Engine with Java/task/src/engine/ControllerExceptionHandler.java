package engine;

import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import jakarta.validation.ConstraintViolationException;
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


//@ResponseStatus(HttpStatus.BAD_REQUEST)
class ExistingIdException extends RuntimeException{
    public ExistingIdException(String message) {
        super(message);
    }
}

//@ResponseStatus(HttpStatus.FORBIDDEN)
class NonUserQuizException extends RuntimeException{
    public NonUserQuizException(String message) {
        super(message);
    }
}

//@ResponseStatus(HttpStatus.NOT_FOUND)
class NoSuchIdException extends RuntimeException{
    public NoSuchIdException(String message) {
        super(message);
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
        System.out.println("\n\nHandling the exception with message: " + e.getMessage() + "\n\n");

        CustomErrorMessage body = new CustomErrorMessage(
                s.value(),
                LocalDateTime.now(),
                e.getMessage(),
                request.getDescription(false));

        return new ResponseEntity<>(body, s);
    }

    @ExceptionHandler(ExistingIdException.class)
    protected ResponseEntity<CustomErrorMessage> handleExistingIdException(
            ExistingIdException e, WebRequest request) {
        return handle(e, request, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(NonUserQuizException.class)
    protected ResponseEntity<CustomErrorMessage> handleNonUserQuizException(
            ExistingIdException e, WebRequest request) {
        return handle(e, request, HttpStatus.FORBIDDEN);
    }

    @ExceptionHandler(NoSuchIdException.class)
    protected ResponseEntity<CustomErrorMessage> handleNoSuchIdFoundException(
            ExistingIdException e, WebRequest request) {

        return handle(e, request, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(ConstraintViolationException.class)
    protected ResponseEntity<CustomErrorMessage> handleConstraintViolationException(
            ExistingIdException e, WebRequest request) {
        return handle(e, request, HttpStatus.BAD_REQUEST);
    }

    // overload the built-in exceptions
    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
            MethodArgumentNotValidException ex,
            HttpHeaders headers,
            HttpStatusCode status,
            WebRequest request) {

        System.out.println("\n\nNo Valid Argument: " + ex.getMessage() + "\n\n");

        CustomErrorMessage c = new CustomErrorMessage(status.value(),LocalDateTime.now(), ex.getMessage(), request.getDescription(false));

        return new ResponseEntity<>(c, headers, status);
    }

}
