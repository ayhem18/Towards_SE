package com.example.quizz_app;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Component;

// let's start by making this class an entity
@Entity
@Table(name="Car") //  the Car Objects will be stored in a table called "Car"
public class Car {

    @Id // annotation to identify the primary key in a table
    @GeneratedValue(strategy = GenerationType.IDENTITY) // basically an incremental variable
    private int id;

    @NotNull
    @NotBlank // enforces the presence of the 'name' field in any Json string with a non-empty value
    private String name;

    @NotNull // enforces the presence of the 'year' field in any Json string with a non-empty value
    @JsonProperty("year")
    // if Spring boot is complaining about a syntax error in the table creation
    // then there is a high chance one of the fields is a reserved keyword: look for [*] in the trace
    // some solutions:
    // https://stackoverflow.com/questions/66333101/how-to-fix-org-h2-jdbc-jdbcsqlsyntaxerrorexception-syntax-error-in-sql-statemen
    private long yearMade;

    public Car(int id, String n, int y) {
        this.id = id; // for the moment pass the id, because I have no clue how to run the application without doing so...
        this.name = n;
        this.yearMade = y;
    }

    public Car(String n, int y) {
        this.name = n;
        this.yearMade = y;
    }

    public Car() {};

    public String getName() {
        return name;
    }

    public long getYearMade() {
        return yearMade;
    }

    public int getId() {
        return id;
    }

    public String toString() {
        return "Car(" + this.id + ", " + this.name + ", " + this.yearMade + ")";
    }
}


//define a repository to create, delete and update cars
@Component
interface CarRepository<T, K> extends CrudRepository<Car, Integer> {

};

