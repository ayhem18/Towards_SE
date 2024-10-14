package com.example.quizz_app;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.quizz_app.Car;

@SpringBootApplication
@RestController
public class QuizzAppApplication {

	public static void main(String[] args) {
		SpringApplication.run(QuizzAppApplication.class, args);
	}

	@GetMapping("/hello")
	public String hello(@RequestParam(value = "name", defaultValue="World") String name) {
		return "mind your own business";
	}

	 @GetMapping("/car")
	 public String carEndpoint(@RequestParam(value = "name", defaultValue="Jaguar") String name,
	 						  @RequestParam(value = "year", defaultValue="2002") int year) {

		Car c = new Car(name, year);
		ObjectMapper obj = new ObjectMapper();
		try {
			return obj.writeValueAsString(c);
		}catch (Exception e) {
			return "Some error happened";
		}
	 }

}
