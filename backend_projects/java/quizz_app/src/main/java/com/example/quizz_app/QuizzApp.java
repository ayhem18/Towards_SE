package com.example.quizz_app;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.*;

import java.util.NoSuchElementException;
import java.util.concurrent.ConcurrentHashMap;

// this class os a simple demonstration of using in-memory storage...

//@SpringBootApplication
//@RestController
//public class QuizzApp {
//
//	// using a thread safe collection such as ConcurrentHashMap
//	private final ConcurrentHashMap<Integer, Car> carMap = new ConcurrentHashMap<>();
//
//	public static void main(String[] args) {
//		SpringApplication.run(QuizzApp.class, args);
//	}
//
//
//	@PostMapping("/car")
//	public String carPostEndpointBody(@RequestBody Car car) {
//		if (this.carMap.containsKey(car.getId())) {
//			return "There is already a car with id " + car.getId();
//		}
//		this.carMap.put(car.getId(), car);
//		return "The car is added successfully";
//	}
//
//	@GetMapping("/car/{car_id}/")
//	public String carGetEndpointPath(@PathVariable int car_id) {
//		ObjectMapper obj = new ObjectMapper();
//		try {
//			Car c = this.carMap.get(car_id);
//			if (c == null) {
//				throw new NoSuchElementException();
//			}
//			return obj.writerWithDefaultPrettyPrinter().writeValueAsString(this.carMap.get(car_id));
//		}
//		catch (NoSuchElementException e) {
//			return "there is no car with id " + car_id + " saved in the database";
//		}
//
//		catch (Exception e) {
//			return "Some error happened";
//		}
//	}
//
//}
