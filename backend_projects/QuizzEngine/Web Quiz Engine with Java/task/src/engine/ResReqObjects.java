package engine;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

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
    private final List<Integer> userAnswers;

    public QuizAnswerRequest(List<Integer> answer) {
        this.userAnswers = answer;
        // sort the user's answers
        Collections.sort(this.userAnswers);
    }

    public QuizAnswerRequest() {
        this.userAnswers = new ArrayList<>();
    }

    public boolean correctAnswers(List<Integer> real_answers) {
        List<Integer> real_answers_copy = new ArrayList<>();
        Collections.copy(real_answers_copy, real_answers);
        Collections.sort(real_answers_copy);
        return real_answers_copy.equals(this.userAnswers);
    }

//    @JsonProperty("answer")
    public List<Integer> getUserAnswers() {
        return this.userAnswers;
    }

//    public void setUserAnswers(List<Integer> userAnswers) {
//        this.userAnswers = userAnswers;
//    }

}