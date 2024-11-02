package com.example.quizz_app;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

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
	private final UserDetailsService usersService;
	// 2. define a constructor that would receive the repo interface
	@Autowired
	// basically Spring boot will pass the object created during startup time to the constructor

	// The @Qualifier annotation might require a bit more typing, but it might save a lot of headache
	// trying to figure out whether the correct bean is called or not
	public QuizzAppApplication(CarRepository<Integer, Car> repo,
							   @Qualifier("userDetailsProvider") UserDetailsService userDetailsService) {
		this.repo = repo;
		this.usersService = userDetailsService;
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

	@GetMapping("api/user")
	public String getUsers()
			throws JsonProcessingException{
		List<String> usernames = List.of("user1", "user2", "user3");

		// map each user to their user details
		List<UserDetails> users = usernames.stream().map(
                this.usersService::loadUserByUsername).collect(Collectors.toList());

		return (new ObjectMapper()).writerWithDefaultPrettyPrinter().writeValueAsString(users);
	}

    @Bean // if a function is not annotated as @Bean, the object won't be created in boot-time.
    public CommandLineRunner cla(@Qualifier("customer1") Customer customer1,
                                 @Qualifier("customer2") Customer customer2,
                                 @Qualifier("sc1") SpecialCustomer sc1,
                                 @Qualifier("sc2") SpecialCustomer sc2,
                                 @Autowired CustomerUnion cu) {
        return args -> {
            System.out.println("\n");

            System.out.println("This is the first Customer: " + customer1);
            System.out.println("This is the second Customer: " + customer2);

            System.out.println("This is the first Special Customer: " + sc1);
            System.out.println("This is the second Special Customer: " + sc2);

            System.out.println(cu.unionRep());

            System.out.println("\n");

        };
    }

    // this code would work only if there were a single customer...
//    @Bean
//    public CommandLineRunner cla(@Autowired Customer customer) {
//        return args -> {
//            System.out.println("This is the first Customer: " + customer);
//        };
//    }

}
