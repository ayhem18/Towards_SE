package com.example.quizz_app;

import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.encrypt.AesBytesEncryptor;
import org.springframework.security.crypto.encrypt.BytesEncryptor;
import org.springframework.security.crypto.encrypt.Encryptors;
import org.springframework.security.crypto.encrypt.TextEncryptor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

// the main goal of this class is to play around with the theory presented in Jetbrains Courses

//@Component
//class CryptEx implements CommandLineRunner {
//    public void runHashers(){
//
//        // let's start with a few hashers
//        // this is a good hasher for the passwords...
//        PasswordEncoder bCryptEncoder = new BCryptPasswordEncoder(10);
//
//        String rawPassword = "password";
//        String firstEncodedPassword = bCryptEncoder.encode(rawPassword);
//        String secondEncodedPassword = bCryptEncoder.encode(rawPassword);
//
//        System.out.println("The bcrypt hasher uses salt internally so each independent encoding will lead to a different result");
//        System.out.println(firstEncodedPassword.equals(secondEncodedPassword));
//
//        System.out.println("use the matches method instead...");
//        System.out.println(bCryptEncoder.matches(rawPassword, firstEncodedPassword));
//
//        System.out.println("use the matches method instead...");
//        System.out.println(bCryptEncoder.matches(rawPassword, firstEncodedPassword));
//    }
//
//    public void runEncoders() {
//        // use this to encrypt passwords
//        // let's start with a few hashers
//        TextEncryptor te = Encryptors.text("password",
//                "8560b4f4b3" // the salt must be hex-encoded
//        );
//
//        String password_encrypted = te.encrypt("password");
//        String p = te.decrypt((password_encrypted));
//
//        System.out.println(p.equals("password"));
//    }
//
//    @Override
//    public void run(String... args) throws Exception {
//        runEncoders();
//    }
//}
//
