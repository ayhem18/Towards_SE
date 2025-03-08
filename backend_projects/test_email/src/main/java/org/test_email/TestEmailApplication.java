package org.test_email;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class TestEmailApplication implements CommandLineRunner {

	@Autowired
	private EmailSenderService emailSenderService;

	public static void main(String[] args) {
		SpringApplication.run(TestEmailApplication.class, args);
	}

    @Override
    public void run(String... args) {
		System.out.println("Running the application. Sending an email");

		this.emailSenderService.sendEmail(
			"bouabidayhem@gmail.com",
			"ayhembouabid@yandex.com",
			"Test Email",
			"This email was sent by a Spring Boot Application"
		);
	}

}

