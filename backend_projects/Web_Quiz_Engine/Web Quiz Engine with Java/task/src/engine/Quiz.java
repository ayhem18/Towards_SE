package engine;


//import com.fasterxml.jackson.annotation.JsonProperty;
//import com.fasterxml.jackson.annotation.JsonPropertyOrder;
//import org.springframework.data.repository.CrudRepository;
//import org.springframework.data.repository.PagingAndSortingRepository;
//
//import javax.persistence.*;
//import javax.sound.midi.Sequence;
//import javax.validation.constraints.NotBlank;
//import javax.validation.constraints.NotNull;
//import javax.validation.constraints.Size;
//import java.util.ArrayList;
//import java.util.List;
//
//
//
//// annotations for JPA
//@Entity
//@Table(name="Quizzes")
//
//// Jackson properties for better display
//@JsonPropertyOrder({"id", "title", "text", "options"}) // setting the order of serialization
//public class Quiz {
//    @Id // make sure to set the id for the Quiz table
//    @GeneratedValue(strategy = GenerationType.IDENTITY) // auto increment ids...
//    @Column(name="quiz_id") // setting the name in the database
//    private  int id;
//
//    @NotBlank // this means the string can neither be null not empty (with only white spaces...)
//    private  String title;
//    @NotBlank
//    private   String text;
//
//    @NotNull // setting the notNull requirement is indeed helpful...
//    @Size(min=2) // at least 2 options
//
//    @ElementCollection // the list of questions will be saved in a different table in th database (good practice, I guess)
//    private  List<String> options;
//
//    @JsonProperty(access=JsonProperty.Access.WRITE_ONLY) // a property to write the answer field without reading it
//    @ElementCollection // adding the @ElementCollection notation to make the field work in the database
//    private  List<Integer> answer;
//
//    public Quiz(String title,
//                String text,
//                List<String> options,
//                List<Integer> answer) {
//        this.title = title;
//        this.text = text;
//        this.options = options;
//
//        if (answer == null) {
//            answer = new ArrayList<>();
//        }
//        this.answer = answer;
//    }
//
//     // writing a default constructor cause it fixes some bugs...
//     public Quiz() {
//
//     }
//
//    public int getId() {
//        return id;
//    }
//
//    public String getTitle() {
//        return title;
//    }
//
//    public String getText() {
//        return text;
//    }
//
//    public List<String> getOptions() {
//        return options;
//    }
//
//    public List<Integer> getAnswer() {
//        return this.answer;
//    }
//
//    @Override
//    public boolean equals(Object obj) {
//        if (! (obj instanceof Quiz)) {
//            return false;
//        }
//        return ((Quiz) obj).getId() == this.id;
//    }
//}
//
//// CrudRepository provides the basic Crud Operations while PagingAndSortingRepository
//// offers the sorting and pagination functionalities
//interface QuizRepository extends CrudRepository<Quiz, Integer>, PagingAndSortingRepository<Quiz, Integer> {
//
//};
