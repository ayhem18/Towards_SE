//import org.junit.jupiter.api.Test;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.beans.factory.annotation.Qualifier;
//import org.springframework.boot.test.context.SpringBootTest;
//import org.springframework.security.crypto.password.PasswordEncoder;
//
//import java.util.List;
//
//import static org.assertj.core.api.Assertions.assertThat;
//import static org.junit.jupiter.api.Assertions.assertFalse;
//import static org.junit.jupiter.api.Assertions.assertTrue;
//
//// check https://hyperskill.org/learn/step/27507
//// SpringBootTest looks for @SpringBootApplication.\
////@SpringBootTest(classes= UserController.class)
////class  TestPasswordEncoder{
////
////    private final PasswordEncoder pe;
////
////    @Autowired
////    public TestPasswordEncoder(@Qualifier("userPasswordEncoder") PasswordEncoder pe) {
////        this.pe = pe;
////    }
////
////    @Test
////    void passwordEncoderTest1() {
////        List<String> p1 = List.of("pass1", "pass1", "pass1");
////        List<String> p2 = List.of("pass2", "pass2", "pass2");
////
////        // encode each of these passwords
////        List<String> p1Encoded = p1.stream().map(this.pe::encode).toList();
////        List<String> p2Encoded = p2.stream().map(this.pe::encode).toList();
////
////        for (int i = 0; i < p1Encoded.size(); i++) {
////            for (int j = i; j < p1Encoded.size(); j++) {
////                // the encoded passwords should different (due to salt)
////                assertThat(p1Encoded.get(i)).isNotEqualTo(p1Encoded.get(j));
////                // the matches method on the other hand should work
////
////                assertThat(p1Encoded.get(i)).isNotEqualTo(p1Encoded.get(j));
////                assertTrue(this.pe.matches(p1Encoded.get(i), p1Encoded.get(j)));
////            }
////        }
////
////        for (String p1e: p1Encoded) {
////            for (String p2e: p2Encoded) {
////                assertFalse(this.pe.matches(p1e, p2e));
////            }
////        }
////    }
////
////
////
////}