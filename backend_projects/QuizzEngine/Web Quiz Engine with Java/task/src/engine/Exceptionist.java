package engine;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;


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

}


// a custom exception for non-existing ids
@ResponseStatus(HttpStatus.NOT_FOUND)
class NoExistingIdException extends RuntimeException {
    private static String defaultErrorMessageFormatter(int id) {
        return "There is no quiz with the id " + id;
    }

    public NoExistingIdException(int id) {
        super(NoExistingIdException.defaultErrorMessageFormatter(id));
    }
}


@ControllerAdvice
public class Exceptionist {

    // using this method leads to return the 500 status code all the time

//    @ExceptionHandler(NoExistingIdException.class)
//    public ResponseEntity<CustomErrorMessage> handleNotFoundExceptions(
//            NoExistingIdException e, WebRequest request) {
//
//        CustomErrorMessage body = new CustomErrorMessage(
//                HttpStatus.NOT_FOUND.value(),
//                LocalDateTime.now(),
//                e.getMessage(),
//                request.getDescription(false));
//
//        return new ResponseEntity<>(body, HttpStatus.NOT_FOUND);
//    }

    // let's add a control Device
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<CustomErrorMessage> handleBadRequestExceptions(
            RuntimeException e, WebRequest request) {

        CustomErrorMessage body = new CustomErrorMessage(
                HttpStatus.BAD_REQUEST.value(),
                LocalDateTime.now(),
                e.getMessage(),
                request.getDescription(true));

        return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
    }


}

