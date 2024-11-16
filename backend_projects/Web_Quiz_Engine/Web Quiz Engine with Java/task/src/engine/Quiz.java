package engine;


import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.PagingAndSortingRepository;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.*;


// annotations for JPA
@Entity
@Table(name="Quizzes")

// Jackson properties for better display
@JsonPropertyOrder({"id", "title", "text", "options"}) // setting the order of serialization
public class Quiz {
    @Id // make sure to set the id for the Quiz table
    @GeneratedValue(strategy = GenerationType.IDENTITY) // auto increment ids...
    @Column(name="quiz_id") // setting the name in the database
    private  int id;

    @NotBlank // this means the string can neither be null not empty (with only white spaces...)
    private  String title;

    @NotBlank
    private   String text;

    @NotNull // setting the notNull requirement is indeed helpful...
    @Size(min=2) // at least 2 options

    @ElementCollection // the list of questions will be saved in a different table in th database (good practice, I guess)
    private  List<String> options;

    @JsonProperty(access=JsonProperty.Access.WRITE_ONLY) // a property to write the answer field without reading it
    @ElementCollection // adding the @ElementCollection notation to make the field work in the database
    private  List<Integer> answer;

    public Quiz(String title,
                String text,
                List<String> options,
                List<Integer> answer) {
        this.title = title;
        this.text = text;
        this.options = options;

        if (answer == null) {
            answer = new ArrayList<>();
        }
        this.answer = answer;
    }

     // adding a default constructor cause it fixes some bugs...
     public Quiz() {

     }

    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getText() {
        return text;
    }

    public List<String> getOptions() {
        return options;
    }

    public List<Integer> getAnswer() {
        return this.answer;
    }

    @Override
    public boolean equals(Object obj) {
        if (! (obj instanceof Quiz)) {
            return false;
        }
        return ((Quiz) obj).getId() == this.id;
    }
}

// CrudRepository provides the basic Crud Operations while PagingAndSortingRepository
// offers the sorting and pagination functionalities
interface QuizRepository extends CrudRepository<Quiz, Integer>, PagingAndSortingRepository<Quiz, Integer> { };


@Embeddable
class QuizCompletionKey implements Serializable {
    @Column(name="username")
    private String email;

    @Column(name="quiz_id")
    private int id;

    private LocalDateTime completionTime;

    public QuizCompletionKey(String email, int id, LocalDateTime ct) {
        this.email = email;
        this.id = id;
        this.completionTime = ct;
    }

    public QuizCompletionKey() {
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof QuizCompletionKey that)) return false;
        return id == that.id
                && this.email.equals(that.email) &&
                Objects.equals(completionTime, that.completionTime);
    }

    @Override
    public int hashCode() {
        return Objects.hash(email, id, completionTime);
    }
}


@Entity
@Table(name="quiz_completions")
@JsonPropertyOrder({"id", "completedAt"}) // stting the order of the Json representation
class QuizCompletion {

    @JsonProperty(access=JsonProperty.Access.WRITE_ONLY)  // the completion object should not contain the key
    @EmbeddedId
    private QuizCompletionKey key;

    // the quiz field will be named "id" in the JSON representation
    @JsonProperty("id")
    //database annotations
    @ManyToOne()
    @MapsId("id")
    private Quiz quiz;

    // annotations for JSON serialization
    @JsonProperty(access=JsonProperty.Access.WRITE_ONLY)  // the completion object not should contain user information
    // annotations for the database
    @ManyToOne()
    @MapsId("email")
    private User user;

    // https://www.geeksforgeeks.org/deserialize-java-8-localdatetime-with-jacksonmapper/
    // the default Jackson Package does not serialize POJOs of type LocalDateTime
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    // the Sort class uses the table column and hence it helps to set the name to make sure the mapping is done correctly
    @Column(name="completedAt")
    private LocalDateTime completedAt;

    public QuizCompletion(Quiz quiz, User user) {
        this.quiz = quiz;
        this.user = user;
        this.completedAt = LocalDateTime.now();
        this.key = new QuizCompletionKey(user.getEmail(), quiz.getId(), this.completedAt);
    }

    public QuizCompletion() {

    }

    // getters
    public QuizCompletionKey getKey() {
        return key;
    }

    public Quiz getQuiz() {
        return quiz;
    }

    public User getUser() {
        return user;
    }

    public LocalDateTime getCompletedAt() {
        return completedAt;
    }

    // since only the quiz id should be serialized and not the entire object
    // one solution is to have a method that returns only the part needed out of the quiz: in this case the id
    // in general, this function can return a hashmap with different properties... (this idea needs to be tested)
    // check: https://www.baeldung.com/jackson-annotations#bd-jackson-serialization-annotations
    @JsonGetter("id")
    public int getQuizId() {
        return this.quiz.getId();
    }

}

//create a CRUD repository for quiz completions
interface QuizCompletionRepo extends CrudRepository<QuizCompletion, QuizCompletionKey>,
        PagingAndSortingRepository<QuizCompletion, QuizCompletionKey> {

    // a function to find all quizCompletions by user
    List<QuizCompletion> findByUser(User user);
    // find all the quizzes completed by a given user
    Page<QuizCompletion> findByUser(User user, Pageable pageable);
    // find all the quizCompletion instances involving a given quiz
    void deleteByQuiz(Quiz q);
};


/**
 * Observable interface
 **/
interface Observable {

    void addObserver(Observer observer);

    void removeObserver(Observer observer);

    void notifyObservers();
}

/**
 * Concrete Observable - Rockstar Games
 **/
//class RockstarGames implements Observable {
//
//    public String releaseGame;
//    private List<Observer> observers = new ArrayList<>();
//
//    public void release(String releaseGame) {
//        this.releaseGame = releaseGame;
//        notifyObservers();
//    }
//
//    @Override
//    public void addObserver(Observer observer) {
//            this.observers.add(observer);
//    }
//
//    @Override
//    public void removeObserver(Observer observer) {
//        this.observers.remove(observer);
//    }
//
//    @Override
//    public void notifyObservers() {
//        for (Observer observer : observers) {
//            System.out.println("Notification for gamer : " + observer);
//            observer.update(releaseGame);
//        }
//    }
//}

/**
 * Observer interface
 **/
interface Observer {

    public void update(String domain);
}

/**
 * Concrete observer - Gamer
 **/
//class Gamer implements Observer {
//
//    private String name;
//    private Set<String> games = new HashSet<>();
//
//    public Gamer(String name) {
//        this.name = name;
//    }
//
//    @Override
//    public void update(String game) {
//        buyGame(game);
//    }
//
//    public void buyGame(String game) {
//        System.out.println(name + " says : \"Oh, Rockstar releases new game " + game + " !\"");
//        games.add(game);
//    }
//
//    @Override
//    public String toString() {
//        return this.name;
//    }
//}
//
//class Main {
//    public static void main(String[] args) {
//        final Scanner scanner = new Scanner(System.in);
//
//        String game = null;
//
//        RockstarGames rockstarGames = new RockstarGames();
//
//        Gamer garry = new Gamer("Garry Rose");
//        Gamer peter = new Gamer("Peter Johnston");
//        Gamer helen = new Gamer("Helen Jack");
//
//        rockstarGames.addObserver(garry);
//        rockstarGames.addObserver(peter);
//        rockstarGames.addObserver(helen);
//
//        game = scanner.nextLine();
//        rockstarGames.release(game);
//
//        scanner.close();
//    }
//}


class RockstarGames implements Observable {

    public String releaseGame;
    private List<Observer> observers = new ArrayList<>();

    public void release(String releaseGame) {
        this.releaseGame = releaseGame;
        notifyObservers();
    }

    @Override
    public void addObserver(Observer observer) {
        this.observers.add(observer);
    }

    @Override
    public void removeObserver(Observer observer) {
        this.observers.remove(observer);
    }

    @Override
    public void notifyObservers() {
        for (Observer observer : observers) {
            System.out.println("Inform message to : " + observer);
            observer.update(releaseGame);
        }
    }
}

/** Observer */

/** Concrete Observer */
class Gamer implements Observer{

    private String name;
    private String reaction;
    private Set<String> games = new HashSet<>();

    public Gamer(String name, String reaction) {
        this.reaction = reaction;
        this.name = name;
    }

    /* write your code here ... */
    @Override
    public void update(String game) {
        buyGame(game);
    }


    public void buyGame(String game) {
        games.add(game);
        System.out.println(this.name + " says: " + reaction);
    }

    @Override
    public String toString() {
        return this.name;
    }
}

/** Main Class */

class Main {
    public static void main(String[] args) {

        final Scanner scanner = new Scanner(System.in);

        RockstarGames rockStarGames = new RockstarGames();

        Gamer garry = new Gamer("Garry Rose", "I want to pre-order");
        Gamer peter = new Gamer("Peter Johnston", "Pinch me...");
        Gamer helen = new Gamer("Helen Jack", "Jesus, it's new game from Rockstar!");

        /* write your code here ... */
        rockStarGames.addObserver(garry);
        rockStarGames.addObserver(peter);
        rockStarGames.addObserver(helen);

        String game = scanner.nextLine();
        System.out.println("It's happened! RockstarGames releases new game - " + game + "!");

        rockStarGames.release(game);
        /* write your code here ... */
        scanner.close();
    }
}