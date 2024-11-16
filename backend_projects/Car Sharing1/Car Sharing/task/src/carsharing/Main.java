package carsharing;

import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class Main {

//    static final String JDBC_DRIVER = "org.h2.Driver";
    static final String DB_URL = "jdbc:h2:";
//    static final String Path = "./src/carsharing/db";

    public static void main(String[] args) throws Exception{
        // write your code here
        String mainPath = System.getProperty("user.dir");
        mainPath = Paths.get(mainPath, "src", "carsharing", "db").toString();

        File dir = new File(mainPath);
        dir.mkdirs();

        String dbPath, path;
        if (args.length > 1) {
            path = Paths.get(mainPath, args[1] + ".mv.db").toString();
//            dbPath = DB_URL + Paths.get("./src/carsharing/db", args[1]);
            dbPath = DB_URL + Paths.get(mainPath, args[1]);
        }
        else {
            path = Paths.get(mainPath, "test_db.mv.db").toString();
//            dbPath = DB_URL + Paths.get("./src/carsharing/db", "test_db");
            dbPath = DB_URL + Paths.get(mainPath, "test_db");
        }

        System.out.println(path);
        File f = new File(path);
        try {
            f.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
        }

        try (Connection conn = DriverManager.getConnection(dbPath);
             Statement st = conn.createStatement()) {

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