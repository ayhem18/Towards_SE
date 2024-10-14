package com.example.quizz_app;

import com.fasterxml.jackson.databind.ObjectMapper;

public class Car {
    private final String name;
    private final int year;


    public Car(String n, int y) {
        this.name = n;
        this.year = y;
    }


    public String getName() {
        return name;
    }

    public int getYear() {
        return year;
    }
}



class Main {
    public static void main(String[] args) {
        Car c = new Car("car_name", 10);
        ObjectMapper obj = new ObjectMapper();
        try {
            System.out.println(obj.writeValueAsString(c));
        }
        catch (Exception e) {
            System.out.println(e);
        }
    }
}
