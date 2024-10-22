package com.example.quizz_app;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Random;


// a class where I save the

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
