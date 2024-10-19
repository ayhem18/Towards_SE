package com.example.quizz_app;

import java.util.Random;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.*;

import java.util.*;

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
	private final ComponentClass c;

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
		System.out.println("\n\nSetting the first call for the Component Class field\n\n");
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


@Component
@Scope(value="prototype")
class CompClass {
	private final List<String> objsList;
	private final Random randObject;

	public CompClass() {
		this.objsList = List.of("an even bigger shit", "Shit", "another shit", "Hello", "oh shit", "damn shit", "fuck shit");
		this.randObject = new Random();
	}

	public String getObject() {
		int val = this.randObject.nextInt(this.objsList.size());
		return this.objsList.get(val);
	}
}

@Component
class YetAnotherComp {
	private final CompClass c1;
	private final CompClass c2;
	private final boolean same;


	public YetAnotherComp(@Autowired CompClass c1, @Autowired CompClass c2) {
		this.c1 = c1;
		this.c2 = c2;
		this.same = (this.c1 == this.c2);

	}

	public String function() {
		return c1.getObject() + "_" + c2.getObject() + "_" + this.same;
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
	public String ComponentPoint(@Autowired CompClass c){
		return c.getObject();
	}

	@Bean
	@GetMapping("call2")
	public String ComponentPoint2(@Autowired YetAnotherComp c){
		return c.function();
	}

}
