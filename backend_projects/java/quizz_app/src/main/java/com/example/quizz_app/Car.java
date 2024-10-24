package com.example.quizz_app;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.persistence.*;
import org.springframework.data.repository.CrudRepository;

// let's start by making this class an entity
@Entity
@Table(name="Car") //  the Car Objects will be stored in a table called "Car"
public class Car {
    @Id // annotation to identify the primary key in a table
    private int id;

    private String name;
    private int year;

    public Car(int id, String n, int y) {
        this.id = id; // for the moment pass the id, because I have no clue how to run the application without doing so...
        this.name = n;
        this.year = y;
    }

    public Car() {};

    public String getName() {
        return name;
    }

    public int getYear() {
        return year;
    }

    public int getId() {
        return id;
    }

    public String toString() {
        return "Car(" + this.id + ", " + this.name + ", " + this.year + ")";
    }
}


//define a repository to create, delete and update cars
interface CarRepository extends CrudRepository<Car, Integer> {

};

