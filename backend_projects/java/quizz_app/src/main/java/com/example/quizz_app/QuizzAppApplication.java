package com.example.quizz_app;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.validation.Valid;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@SpringBootApplication
@RestController
@Validated
public class QuizzAppApplication {

	public static void main(String[] args) {
		SpringApplication.run(QuizzAppApplication.class, args);
	}

	// let's remember how to work with databases
	// 1. define a private field in the class
	private final CarRepository<Integer, Car> repo;
	// 2. define a constructor that would receive the repo interface
	@Autowired
	// basically Spring boot will pass the object created during startup time to the constructor
	public QuizzAppApplication(CarRepository<Integer, Car> repo) {
		this.repo = repo;
	}

	@PostMapping("/api/car/")
	public String carPost(@Valid @RequestBody Car car) throws JsonProcessingException {
		try {
			this.repo.save(car);
			return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(car);
		} catch (RuntimeException e ){
			throw new IdAlreadyExists(car.getId());
		}
	}

	@GetMapping("/api/car/{car_id}/")
	public String carGet(@PathVariable int car_id) throws JsonProcessingException{
		Car car = this.repo.findById(car_id).orElseThrow(() -> new NoExistingIdException(car_id));
		return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(car);
	}

	@GetMapping("/api/car/")
	public String getAllCars() throws JsonProcessingException {
		return new ObjectMapper().writerWithDefaultPrettyPrinter().writeValueAsString(this.repo.findAll());
	}

 	@GetMapping("/api/car/clear/")
	public String carClear() {
		this.repo.deleteAll();
		long count = this.repo.count();
		return "the number of records in the database is " + ((Long) count).intValue();
	}
}


