package carsharing;
import java.io.File;
import java.nio.file.Paths;
import java.sql.*;

public class Main {

    static final String JDBC_DRIVER = "org.h2.Driver";
    static final String DB_URL = "jdbc:h2:";
    public static void main(String[] args){

//        String mainPath = System.getProperty("user.dir");
//        mainPath = Paths.get(mainPath,  "src", "carsharing", "db").toString();

        String mainPath = "./src/carsharing/db/";

        File dir = new File(mainPath);
        dir.mkdirs();

        String dbPath, path;
        if (args.length > 1 && args[0].equals("-databaseFileName")) {
//            path = Paths.get(mainPath, args[1] + ".mv.db").toString();
//            dbPath = DB_URL + Paths.get(mainPath, args[1]);

            path = mainPath + args[1] + ".mv.db";
            dbPath = DB_URL + mainPath + args[1];
        }
        else {
//            path = Paths.get(mainPath, "test_db.mv.db").toString();
//            dbPath = DB_URL + Paths.get(mainPath, "test_db");
            path = mainPath +  "test_db.mv.db";
            dbPath = DB_URL + mainPath + "test_db" ;
        }

        System.out.println(path);
        File f = new File(path);
        try {
            // only create the file when it does not exist
            if (! f.exists()) {
                f.createNewFile();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println(dbPath);

        try (Connection conn =DriverManager.getConnection(dbPath);
             Statement st = conn.createStatement();
        ) {
            conn.setAutoCommit(true);
            String sql = "CREATE TABLE IF NOT EXISTS COMPANY " +
                    "(ID INT not NULL, " +
                    " NAME VARCHAR_IGNORECASE, " +
                    " PRIMARY KEY ( id ));";

            st.executeUpdate(sql);


        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}