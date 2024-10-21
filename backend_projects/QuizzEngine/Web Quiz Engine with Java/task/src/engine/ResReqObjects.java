package engine;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

import javax.validation.constraints.NotNull;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

// got to find different approaches to create Json like responses than just creating random objects
class ServerResponse {
    private final boolean  success;
    private final String feedback;

    public ServerResponse(boolean success, String feedback) {
        this.success = success;
        this.feedback = feedback;
    }

    // jackson fails without getters
    public boolean isSuccess() {
        return success;
    }

    public String getFeedback() {
        return feedback;
    }
}


class QuizAnswerRequest {

    @JsonProperty("answer")
    @NotNull
    private List<Integer> userAnswer;

    public QuizAnswerRequest(List<Integer> answer) {
        this.userAnswer = answer;
    }

    // without the default constructor, something crushes somewhere...
    public QuizAnswerRequest() {
        this.userAnswer = new ArrayList<>();
    }

    public boolean correctAnswers(List<Integer> real_answers) {
        List<Integer> real_answers_copy = new ArrayList<>(real_answers); // set the capacity
        Collections.sort(real_answers_copy);
        return real_answers_copy.equals(this.userAnswer);
    }

    @JsonProperty("answer")
    public List<Integer> getUserAnswers() {
        return this.userAnswer;
    }
    @JsonProperty("answer")
    public void setUserAnswers(List<Integer> userAnswers) {
        // so apparently the Jackson library does not operate with Constructors but rather getters and setters
        // including the sorting in the constructor saves an unsorted list of answers as is
        // on the other hand adding the Collections.sort() call in the setter method
        // ends up sorting the user answers
        this.userAnswer = userAnswers;
        // make sure to sort
        Collections.sort(this.userAnswer);
    }

}