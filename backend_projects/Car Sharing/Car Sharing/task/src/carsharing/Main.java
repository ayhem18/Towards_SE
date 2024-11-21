package carsharing;

import java.io.File;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


class Company {
    private int id;
    private String name;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Company(int id, String name) {
        this.id = id;
        this.name = name;
    }
}


class DBClient {
    private String dbUrl;

    public DBClient(String dbUrl) {
        this.dbUrl = dbUrl;
    }

    public boolean createCompany(String name) {
        // create a prepared statement
        String createCompanySQL = "INSERT INTO COMPANY (name) VALUES (?)";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
            PreparedStatement st = conn.prepareStatement(createCompanySQL))
        {
            conn.setAutoCommit(true);
            st.setObject(1, name);
            st.executeUpdate();
            return true;

        } catch (SQLException e) {
            e.printStackTrace();
        }
        return false;
    }

    public List<String> listCompanies() throws Exception{
        String createCompanySQL = "SELECT * from COMPANY ORDER BY id;";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st = conn.prepareStatement(createCompanySQL))
        {
            List<String> result = new ArrayList<>();
            conn.setAutoCommit(true);
            ResultSet rs = st.executeQuery();

            while (rs.next()) {
                result.add(rs.getString("name"));
            }
            return result;

        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public void check() throws  Exception{
        String createCompanySQL = "SELECT * from INFORMATION_SCHEMA.CONSTRAINTS";
        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st = conn.prepareStatement(createCompanySQL))
        {
            conn.setAutoCommit(true);
            ResultSet rs = st.executeQuery();

            while (rs.next()) {
                System.out.println((rs.getString("TABLE_NAME")));
            }

        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }

    }
}


class UserInterface {
    private final Scanner scanner;

    public UserInterface() {
        this.scanner = new Scanner(System.in);
    }

    private void listCompanies(DBClient client) throws Exception{
        System.out.println("Company list:");
        List<String> cs = client.listCompanies();
        if (cs.isEmpty()) {
            System.out.println("The company list is empty!\n");
            return;
        }
        int counter = 1;
        for (String c: cs) {
            System.out.println(counter + ". " + c);
            counter += 1;
        }
        System.out.println();
    }

    private void createCompany(DBClient client) {
        System.out.println("Enter the company name:");
        String companyName = scanner.nextLine();
        client.createCompany(companyName);
        System.out.println("The company was created!\n");
    }

    private void managerMenu(DBClient client) throws Exception {
        while (true) {
            System.out.println("1. Company list\n" +
                    "2. Create a company\n" +
                    "0. Back");
            int choice = Integer.parseInt(scanner.nextLine());

            if (choice == 2) {
                this.createCompany(client);
            }
            else if (choice == 1) {
                this.listCompanies(client);
            }
            else {
                return;
            }
        }
    }

    public  void mainLoop(String dbUrl) throws Exception{
        DBClient client = new DBClient(dbUrl);
        while (true) {
            System.out.println("1. Log in as a manager\n" +
                    "0. Exit");
            int choice = Integer.parseInt(scanner.nextLine());
            if (choice == 1) {
                managerMenu(client);
            }
            else {
                return;
            }
        }
    }
}


public class Main {

    static final String JDBC_DRIVER = "org.h2.Driver";
    static final String DB_URL = "jdbc:h2:";

    public static String setup(String[] args) throws Exception{
        String mainPath = "./src/carsharing/db/";

        File dir = new File(mainPath);
        dir.mkdirs();

        String dbPath, path;
        if (args.length > 1 && args[0].equals("-databaseFileName")) {
            path = mainPath + args[1] + ".mv.db";
            dbPath = DB_URL + mainPath + args[1];
        }
        else {
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
            throw e;
        }

        System.out.println(dbPath);

        try (Connection conn =DriverManager.getConnection(dbPath);
             Statement st = conn.createStatement();
        ) {
            conn.setAutoCommit(true);
            String sql = "CREATE TABLE IF NOT EXISTS COMPANY " +
                    "(ID INT AUTO_INCREMENT PRIMARY KEY, " +
                    " NAME VARCHAR UNIQUE NOT NULL); ";

            st.executeUpdate(sql);

        } catch (SQLException e) {
            throw e;
        }
        return dbPath;
    }


    public static void main(String[] args) throws Exception{
        // call the setup function
        String dbUrl = setup(args);
        UserInterface ui = new UserInterface();
        ui.mainLoop(dbUrl);
//        DBClient client = new DBClient(dbUrl);
//
//        client.check();
    }
}