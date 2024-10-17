package com.example.quizz_app;

import com.fasterxml.jackson.databind.ObjectMapper;

public class Car {
    private static int CAR_COUNT = 0;
    private final String name;
    private final int year;
    private int car_id; // keeps track for all the car objects that were created in the program so far...

    public Car(String n, int y) {
        Car.CAR_COUNT += 1;
        this.car_id = Car.CAR_COUNT;
        this.name = n;
        this.year = y;
    }


    public String getName() {
        return name;
    }

    public int getYear() {
        return year;
    }

    public int getCar_id() {
        return car_id;
    }
}



class Main {    public static void main(String[] args) {
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

