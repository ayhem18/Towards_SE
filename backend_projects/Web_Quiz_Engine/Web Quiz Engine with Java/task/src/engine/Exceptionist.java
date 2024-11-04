package engine;

//import org.springframework.http.HttpStatus;
//import org.springframework.http.ResponseEntity;
//import org.springframework.web.bind.annotation.ControllerAdvice;
//import org.springframework.web.bind.annotation.ExceptionHandler;
//import org.springframework.web.context.request.WebRequest;
//
//import java.time.LocalDateTime;
//
//
//class CustomErrorMessage {
//    private final int statusCode;
//    private final LocalDateTime timestamp;
//    private final String message;
//    private final String description;
//
//    public CustomErrorMessage(
//            int statusCode,
//            LocalDateTime timestamp,
//            String message,
//            String description) {
//
//        this.statusCode = statusCode;
//        this.timestamp = timestamp;
//        this.message = message;
//        this.description = description;
//    }
//
//}
//
//
//
//@ControllerAdvice
//public class Exceptionist {
//
//    // let's add a control Device
//    @ExceptionHandler(RuntimeException.class)
//    public ResponseEntity<CustomErrorMessage> handleBadRequestExceptions(
//            RuntimeException e, WebRequest request) {
//
//        CustomErrorMessage body = new CustomErrorMessage(
//                HttpStatus.BAD_REQUEST.value(),
//                LocalDateTime.now(),
//                e.getMessage(),
//                request.getDescription(true));
//
//        return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
//    }
//
//}
