package com.example.quizz_app;


import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;

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

@ResponseStatus(HttpStatus.BAD_REQUEST)
class IdAlreadyExists extends RuntimeException {
    private static String defaultErrorMessageFormatter(int id) {
        return "There is already a quiz with the id " + id;
    }

    public IdAlreadyExists(int id) {
        super(IdAlreadyExists.defaultErrorMessageFormatter(id));
    }
}



class CustomErrorMessage {
    private final int statusCode;
    private final LocalDateTime timestamp;
    private final String message;
    private final String description;

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

// a controllerAdvice intercepts errors raised by all controllers in the app
@ControllerAdvice
class Exceptionist {
    @ExceptionHandler (JsonProcessingException.class)
    public ResponseEntity<CustomErrorMessage> handleJsonProcessingErrors(
            JsonProcessingException e, WebRequest w) {

        CustomErrorMessage body = new CustomErrorMessage(
                HttpStatus.BAD_REQUEST.value(),
                LocalDateTime.now(),
                "This is a Json Processing error: " + e.getMessage(),
                w.getDescription(true));

        return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
    }

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
