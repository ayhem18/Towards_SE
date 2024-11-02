package com.example.quizz_app;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.stereotype.Component;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;


@Configuration
// a Configuration class just to create String beans
class StringBeanCreator {
	@Bean
	// this is a bean with the name "add1"
	public String add1() {
		return "add1";
	}

	@Bean("address") // although the method name is "add2", using the "name" keyword in the @Bean annotation
	// associated the name "address" wth this bean object
	public String add2() {
		return "address";
	}
}

// usual class definition
class Customer {
	private String name;
	private String address;

	public Customer(String name, String address) {
		this.name = name;
		this.address = address;
	}
	// a no argument constructor is a requirement of Spring Beans
	public Customer() {

	}

	@Override
	public String toString() {
		return "Customer " + this.name + " living at " + this.address;
	}
}

@Configuration
class CustomerBeanCreator {
//	@Bean
//	public Customer customer1(@Autowired String add) {
//		return new Customer("n1", add);
//	}
//
//
//	@Bean
//	public Customer customer2(@Autowired String add) {
//		return new Customer("n2", add);
//	}


	// the commented code should not work because there are at least 2 String Beans
	// Ioc cannot distinguish between both beans solely by the data type
	@Bean
	// we can use the @Primary annotation to determine which bean object to be selected
	// in case of multiple Bean objects of the same type
	public Customer customer1(@Qualifier("add1") String add) {
		return new Customer("n1", add);
	}

	@Bean
	public Customer customer2(@Qualifier("address") String add) {
		return new Customer("n2", add);
	}

}

// this customer class has the same address across all instances
// not necessarily a Bean object
// according to https://hyperskill.org/learn/step/28662
class SpecialCustomer {
	private String name;

	// opting for field injection because using the constructor injection
	// would require passing a string (and that string being injected for every application that calls the constructor...)
	@Qualifier("add1")
	@Autowired
	private String address;

	public SpecialCustomer(String name){
		this.name = name;
	}

	@Override
	public String toString() {
		return "SpecialCustomer{" +
				"name='" + name + '\'' +
				", address='" + address + '\'' +
				'}';
	}
}


@Configuration
class SpecialCustomerBeanCreator {
	// both of these SpecialCustomer instance would have the same address string value

	@Bean
	public SpecialCustomer sc1() {
		return new SpecialCustomer("n1");
	}


	@Bean
	public SpecialCustomer sc2() {
		return new SpecialCustomer("n2");
	}
}


@Component
class CustomerUnion {
	private final Customer c;
	private final SpecialCustomer sc;

	// use the constructor injection
	@Autowired
	public CustomerUnion(@Qualifier("customer1") Customer c, @Qualifier("sc1") SpecialCustomer sc1) {
		this.c = c;
		this.sc = sc1;
	}

	public String unionRep() {
		return "Customers:\n" + this.c.toString() + "\n" + this.sc.toString() + "\n";
	}
}

