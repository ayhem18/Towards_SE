package com.example.quizz_app;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@SpringBootApplication
@RestController
public class QuizzAppApplication {

	// using a thread safe collection such as ConcurrentHashMap
	private final ConcurrentHashMap<Integer, Car> carMap = new ConcurrentHashMap<>();

	public static void main(String[] args) {
		SpringApplication.run(QuizzAppApplication.class, args);
	}


	@PostMapping("/car")
	public String carPostEndpointBody(@RequestBody Car car) {
		if (this.carMap.containsKey(car.getId())) {
			return "There is already a car with id " + car.getId();
		}
		this.carMap.put(car.getId(), car);
		return "The car is added successfully";
	}

	@GetMapping("/car/{car_id}/")
	public String carGetEndpointPath(@PathVariable int car_id) {
		ObjectMapper obj = new ObjectMapper();
		try {
			Car c = this.carMap.get(car_id);
			if (c == null) {
				throw new NoSuchElementException();
			}
			return obj.writerWithDefaultPrettyPrinter().writeValueAsString(this.carMap.get(car_id));
		}
		catch (NoSuchElementException e) {
			return "there is no car with id " + car_id + " saved in the database";
		}

		catch (Exception e) {
			return "Some error happened";
		}
	}

	@Component
	class Runner implements ApplicationRunner {
		private final CarRepository repo;

		@Autowired
		Runner(CarRepository carRepo) {
			this.repo = carRepo;
		}

		@Override
		public void run(ApplicationArguments args) throws Exception {
			// find the very first car added to the database...
			try {
				Car car = this.repo.findById(1).orElseThrow(NoSuchFieldError::new);
				System.out.println("The first car in the database " + car.toString());
				// delete all elements
				this.repo.deleteAll();

			}

			catch (NoSuchElementException e){
				System.out.println("SEEMS THAT The database is empty");
			}

			long count = repo.count();
			System.out.println("\nThe number of records in the database is " + count + "\n");
			
			Car c = new Car(
					((Long) count).intValue(), 
					"shitty_car", 
					2001);
			
			this.repo.save(c);
			System.out.println("\nThe number of records in the database is " + repo.count() + "\n");

		}
	}

}
