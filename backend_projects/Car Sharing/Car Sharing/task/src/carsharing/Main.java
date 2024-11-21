package carsharing;

import java.io.File;
import java.nio.file.Paths;
import java.sql.*;

public class Main {

    static final String JDBC_DRIVER = "org.h2.Driver";
    static final String DB_URL = "jdbc:h2:";
//    static final String Path = "./src/carsharing/db";

    public static void main(String[] args){

        String mainPath = System.getProperty("user.dir");
        mainPath = Paths.get(mainPath,  "src", "carsharing", "db").toString();

        // "Car Sharing", "task",
        File dir = new File(mainPath);
        dir.mkdirs();

        String dbPath, path;
        if (args.length > 1 && args[0].equals("-databaseFileName")) {
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
            // only try to create the file when it does not already exist
            if (! f.exists()) {
                f.createNewFile();
            }
//            else {
//                System.out.println("Creating a connection to the database");
//                Connection con = DriverManager.getConnection(dbPath);
//                if (con == null) {
//                    throw new Exception();
//                }
//            }
        } catch (Exception e) {
            e.printStackTrace();
        }



        Connection conn = null;
        Statement st = null;

        try {
            conn = DriverManager.getConnection(dbPath);
            conn.setAutoCommit(true);

            st = conn.createStatement();
            String sql = "CREATE TABLE IF NOT EXISTS COMPANY " +
                    "(ID INT not NULL, " +
                    " NAME VARCHAR_IGNORECASE, " +
                    " PRIMARY KEY ( id ));";

            st.executeUpdate(sql);
//            st.executeUpdate("INSERT INTO COMPANY " +
//                    "VALUES (1, 'n1')," +
//                    "(2, 'n2'), " +
//                    "(3, 'n3');");


        } catch (SQLException e) {
            e.printStackTrace();
        }

        finally {
            if (st != null) {
                try {
                    st.close();
                } catch ( SQLException e) {
                     st = null;
                }
            }

            if (conn != null) {
                try {
                    conn.close();
                } catch ( SQLException e) {
                     conn = null;
                }
            }
        }

    }
}