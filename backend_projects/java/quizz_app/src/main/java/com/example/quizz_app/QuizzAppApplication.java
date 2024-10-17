package com.example.quizz_app;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.NoSuchElementException;

import java.util.concurrent.ConcurrentHashMap;


// a class that is created in startup time
@Configuration
class BeanClass {
	@Bean(name = "ad1")
	public String getAddress(){
		return "ad1";
	}

	@Bean(name = "ad2")
	public String getAnotherAddress() {
		return "Well this object was created in boot time";
	}
}

@Component
class ComponentClass  {
	@Bean
	public String call(@Qualifier("ad1") String address) {
		return address;
	}
}

@Component
class ComponentWrapper implements CommandLineRunner {
	// this mean that the Component class will be created an
	private ComponentClass c;

	public ComponentWrapper(@Autowired ComponentClass instance) {
		this.c = instance;
	}

	@Bean
	public String getCallCountSquared(@Qualifier("ad1") String ad) {
		String s = this.c.call(ad);
		return s + " " + s;
	}

	@Override
	public void run(String... args) throws Exception {
		System.out.println("\n\nSetting the first call for the Component Class field");
	}
}


@Component
class AnotherComponent {
	private final int CompanyID = 1000221993;
	private final String CompanyLogo = "CompanyLogo";

	public String companyKey() {
		return this.CompanyLogo + "__" + this.CompanyID;
	}

	public String getLogoSubstring(int index) {
		index = index % this.CompanyLogo.length();
		return this.CompanyLogo.substring(0, index);
	}
}


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

	@Bean // have to add "Bean" to work with Bean objects; use annotations to communicate / pass the objects
	@GetMapping("bean")
	public String BeanEndpoint(@Qualifier("ad1") String add) {
		// basically returning an object that was created when the application boots up
		return add;
	}

	@Bean
	@GetMapping("bean2")
	// have to add "Bean" to work with Bean objects; use annotations to communicate / pass the objects
	public String BeanEndpoint2(@Qualifier("ad2") String add) {
		// basically returning an object that was created when the application boots up
		return add;
	}

	@Bean
	@GetMapping("call")
	public String ComponentPoint(
			@RequestParam(name = "index") int index,
			@Autowired AnotherComponent ac) {
		return ac.getLogoSubstring(index);
	}

}
