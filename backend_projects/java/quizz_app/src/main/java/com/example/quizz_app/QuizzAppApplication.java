package com.example.quizz_app;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.web.bind.annotation.*;
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;

import java.util.concurrent.ConcurrentHashMap;

@SpringBootApplication
@RestController
public class QuizzAppApplication {

	// using a thread safe collection such as ConcurrentHashMap
	private final ConcurrentHashMap<Integer, Car> carMap = new ConcurrentHashMap<>();

	public static void main(String[] args) {
		SpringApplication.run(QuizzAppApplication.class, args);
	}


//	 @PostMapping("/car")
//	 public String carPostEndpoint(@RequestParam(value = "name") String name,
//							   @RequestParam(value = "year") int year) {
//		 Car c = new Car(name, year);
//		 this.carMap.put(c.getCar_id(), c);
//		 return "Car added successfully";
//	 }


	@PostMapping("/car")
	public String carPostEndpointBody(@RequestBody Car car) {
		if (this.carMap.containsKey(car.getCar_id())) {
			return "There is already a car with id " + car.getCar_id();
		}
		this.carMap.put(car.getCar_id(), car);
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

	// you can also use path variables
	@GetMapping("/car")
	public List<Car> allCarsEndpoint(){
		return new ArrayList<>(this.carMap.values());
	}


}
