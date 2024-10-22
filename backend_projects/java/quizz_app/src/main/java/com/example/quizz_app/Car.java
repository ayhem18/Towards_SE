package com.example.quizz_app;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.persistence.*;
import org.springframework.data.repository.CrudRepository;

// let's start by making this class an entity
@Entity
@Table(name="Car") //  the Car Objects will be stored in a table call "Car"
public class Car {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private int id;

    private String name;
    private int year;

    public Car(String n, int y) {
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
}


//define a repository to create, delete and update cars
interface CarRepository extends CrudRepository<Car, Integer> {

};
