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

class Car {
    private int id;
    private String name;
    private Integer companyId;

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Integer getCompanyId() {
        return companyId;
    }

    public Car(int id, String name, Integer companyId) {
        this.id = id;
        this.name = name;
        this.companyId = companyId;
    }
}

class Customer {
    private int id;
    private String name;
    private Integer carId;

    public Customer(int id, String name, Integer carId) {
        this.id = id;
        this.name = name;
        this.carId = carId;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Integer getCarId() {
        return carId;
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

    public Company getCompanyById(int id) throws Exception {
        String createCompanySQL = "SELECT * from Company where id = ?;";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st = conn.prepareStatement(createCompanySQL))
        {
            conn.setAutoCommit(true);
            st.setObject(1, id);
            ResultSet rs = st.executeQuery();
            rs.next();
            return new Company(rs.getInt("id"), rs.getString("name"));

        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        }
    }

    public List<Car> listCompanyCars(String companyName) throws Exception {
        String getCarsSQl = "SELECT * from CAR where company_id = (SELECT ID from COMPANY WHERE name = ?) and rented = False;";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st = conn.prepareStatement(getCarsSQl))
        {
            List<Car> result = new ArrayList<>();
            conn.setAutoCommit(true);

            // add the company name to the SQL query
            st.setObject(1, companyName);
            ResultSet rs = st.executeQuery();

            while (rs.next()) {
                result.add(new Car(rs.getInt("id"), rs.getString("name"), rs.getInt("company_id")));
            }
            return result;

        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public Car getCarByName(String carName) throws Exception {
        String createCompanySQL = "SELECT * from Car where name = ?;";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st = conn.prepareStatement(createCompanySQL))
        {
            conn.setAutoCommit(true);
            st.setObject(1, carName);
            ResultSet rs = st.executeQuery();
            rs.next();
            return new Car(rs.getInt("id"), rs.getString("name"), rs.getInt("company_id"));

        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        }
    }

    public Car getCarById(int id) throws Exception {
        String createCompanySQL = "SELECT * from Car where id = ?;";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st = conn.prepareStatement(createCompanySQL))
        {
            conn.setAutoCommit(true);
            st.setObject(1, id);
            ResultSet rs = st.executeQuery();
            rs.next();
            return new Car(rs.getInt("id"), rs.getString("name"), rs.getInt("company_id"));

        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        }
    }

    public void createCar(String companyName, String carName) {
        String findCompanyNameSQL = "SELECT id from COMPANY WHERE name = ?;";
        String createCompanySQL = "INSERT INTO CAR (name, company_id) VALUES (?, ?)";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st1 = conn.prepareStatement(findCompanyNameSQL);
             PreparedStatement st2 = conn.prepareStatement(createCompanySQL)
        )

        {
            conn.setAutoCommit(true);

            // extract the company ID
            st1.setObject(1, companyName);
            ResultSet rs = st1.executeQuery();
            rs.next();
            int companyID = rs.getInt("id");

            // add the car
            st2.setObject(1, carName);
            st2.setObject(2, companyID);
            st2.executeUpdate();

        } catch (SQLException e) {
            e.printStackTrace();
        }

    }

    public void createCustomer(String customerName) {
        // create a prepared statement
        String createCompanySQL = "INSERT INTO CUSTOMER (name) VALUES (?)";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st = conn.prepareStatement(createCompanySQL))
        {
            conn.setAutoCommit(true);
            st.setObject(1, customerName);
            st.executeUpdate();

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public List<Customer> listCustomers() {
        String createCompanySQL = "SELECT * from Customer ORDER BY id;";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st = conn.prepareStatement(createCompanySQL))
        {
            List<Customer> result = new ArrayList<>();
            conn.setAutoCommit(true);
            ResultSet rs = st.executeQuery();
            while (rs.next()) {
                result.add(new Customer(rs.getInt("id"), rs.getString("name"), (Integer) rs.getObject(3)));
            }

            return result;

        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException(e.getMessage());
        }
    }

    public Customer getCustomerByName(String customerName) {
        String createCompanySQL = "SELECT * from Customer where name = ?;";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st = conn.prepareStatement(createCompanySQL))
        {
            conn.setAutoCommit(true);
            st.setObject(1, customerName);
            ResultSet rs = st.executeQuery();
            rs.next();
            return new Customer(rs.getInt("id"), rs.getString("name"), (Integer) rs.getObject(3));

        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        }
    }

    public Customer rent(String customerName, Integer carId, boolean isRent) {
        String updateCarSql = "UPDATE CAR SET rented = ? where id = ? ";
        String updateClientSql = "UPDATE CUSTOMER SET rented_car_id = ? where name = ? ";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st1 = conn.prepareStatement(updateClientSql);
             PreparedStatement st2 = conn.prepareStatement(updateCarSql);
             )
        {
            conn.setAutoCommit(true);

            // assign the car to the client
            st1.setObject(1, carId);
            st1.setObject(2, customerName);
            st1.executeUpdate();

            // make sure to assign false to the car
            st2.setObject(1, isRent);
            st2.setObject(2, carId);
            st2.executeUpdate();

            return getCustomerByName(customerName);
        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        }
    }

    public Customer returnCar(String customerName, int carId) {
        String updateClientSql = "UPDATE CUSTOMER SET rented_car_id = null where name = ? ";
        String updateCarSql = "UPDATE CAR SET rented = false where id = ? ";

        try (Connection conn = DriverManager.getConnection(this.dbUrl);
             PreparedStatement st1 = conn.prepareStatement(updateClientSql);
             PreparedStatement st2 = conn.prepareStatement(updateCarSql);
        )
        {
            conn.setAutoCommit(true);

            // assign the car to the client
            st1.setObject(1, customerName);
            st1.executeUpdate();

            // make sure to assign false to the car
            st2.setObject(1, carId);
            st2.executeUpdate();

            return getCustomerByName(customerName);
        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        }
    }
}


class UserInterface {
    private final Scanner scanner;

    public UserInterface() {
        this.scanner = new Scanner(System.in);
    }

    private List<Car> listCompanyCars(DBClient client, String companyName) throws  Exception {
        // find the list of company cars
        List<Car> carNames = client.listCompanyCars(companyName);

        if (carNames.isEmpty()) {
            System.out.println("The car list is empty!\n");
            return List.of();
        }

        System.out.println(companyName + " cars:");
        int counter = 1;
        for (Car c : carNames) {
            System.out.println(counter + ". " + c.getName());
            counter += 1;
        }
        System.out.println("0. Back");
        System.out.println();
        return carNames;
    }

    private void createCar(DBClient client, String companyName) throws Exception {
        System.out.println("Enter the car name:");
        String carName = scanner.nextLine();
        client.createCar(companyName, carName);
        System.out.println("The car was added!");
    }


    private void companyMenu(DBClient client, String companyName) throws Exception{
        System.out.println("'" + companyName +  "' company:");

        while (true) {
            System.out.println("1. Car list\n" +
                    "2. Create a car\n" +
                    "0. Back");
            int choice = Integer.parseInt(scanner.nextLine());

            if (choice == 0) {
                return ;
            }

            if (choice == 1) {
                listCompanyCars(client, companyName);
            }

            else if (choice == 2) {
                createCar(client, companyName);
            }
        }
    }


    private void listCompaniesOption(DBClient client) throws Exception {
        List<String> cs = client.listCompanies();
        if (cs.isEmpty()) {
            System.out.println("The company list is empty!\n");
            return;
        }

        System.out.println("Choose a company:");
        int counter = 1;
        for (String c : cs) {
            System.out.println(counter + ". " + c);
            counter += 1;
        }
        System.out.println(("0. Back"));

        int choice = Integer.parseInt(scanner.nextLine());
        if (choice == 0) {
            return ;
        }

        String cN = cs.get(choice - 1);

        companyMenu(client, cN);
    }

    private void createCompanyOption(DBClient client) {
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
                this.createCompanyOption(client);
            }
            else if (choice == 1) {
                this.listCompaniesOption(client);
            }
            else {
                return;
            }
        }
    }

    private Car rent(DBClient client) throws Exception {
        List<String> cs = client.listCompanies();
        if (cs.isEmpty()) {
            System.out.println("The company list is empty!\n");
            return null;
        }

        System.out.println("Choose a company:");
        int counter = 1;
        for (String c : cs) {
            System.out.println(counter + ". " + c);
            counter += 1;
        }
        System.out.println(("0. Back"));

        int choice = Integer.parseInt(scanner.nextLine());
        if (choice == 0) {
            return null;
        }

        String companyName = cs.get(choice - 1);

        List<Car> cars = listCompanyCars(client, companyName);

        if (cars.isEmpty()) {
            return null;
        }
        choice = Integer.parseInt(scanner.nextLine());

        if (choice == 0) {
            return null;
        }
        // let's see how it goes
        return cars.get(choice - 1);
    }

    private void customerMenu(DBClient client, String customerName) throws Exception{
        Customer c = client.getCustomerByName(customerName);
        while (true) {
            System.out.println("1. Rent a car\n" +
                    "2. Return a rented car\n" +
                    "3. My rented car\n" +
                    "0. Back");
            int choice = Integer.parseInt(scanner.nextLine());
            if (choice == 0) {
                return;
            }
            else if (choice == 2) {
                if (c.getCarId() == null) {
                    System.out.println("You didn't rent a car!");
                }
                else {
                    c = client.returnCar(c.getName(), c.getCarId());
                    System.out.println("You've returned a rented car!");
                }
            }
            else if (choice == 3) {
                if (c.getCarId() == null) {
                    System.out.println("You didn't rent a car!");
                }
                else {
                    // extract the Car object
                    Car rentedCar = client.getCarById(c.getCarId());
                    Company company = client.getCompanyById(rentedCar.getCompanyId());
                    System.out.println("Your rented car: ");
                    System.out.println(rentedCar.getName());
                    System.out.println("Company");
                    System.out.println(company.getName());
                    System.out.println();
                }
            }
            else {
                // option 1
                if (c.getCarId() != null) {
                    System.out.println("You've already rented a car!");
                }
                else {
                    Car carToRent = rent(client);
                    if (carToRent != null) {
                        c = client.rent(customerName, carToRent.getId(), true);
                        System.out.println("You rented '" + carToRent.getName() + "'");
                    }
                }
            }
        }
    }


    private void listCustomers(DBClient client) throws Exception{
        List<Customer> customers = client.listCustomers();
        if (customers.isEmpty()) {
            System.out.println("The customer list is empty!\n\n");
            return;
        }

        int counter = 1;
        for (Customer c : customers) {
            System.out.println(counter + ". " + c.getName());
            counter += 1;
        }
        int choice = Integer.parseInt(scanner.nextLine());
        String customerName = customers.get(choice - 1).getName();

        customerMenu(client, customerName);
    }


    private void createCustomerOption(DBClient client) throws Exception{
        System.out.println("Enter the customer name: ");
        String customerName = this.scanner.nextLine();
        client.createCustomer(customerName);
        System.out.println("The customer was added!");
    }


    public  void mainLoop(String dbUrl) throws Exception{
        DBClient client = new DBClient(dbUrl);
        while (true) {
            System.out.println("1. Log in as a manager\n" +
                    "2. Log in as a customer\n" +
                    "3. Create a customer\n" +
                    "0. Exit");
            int choice = Integer.parseInt(scanner.nextLine());
            if (choice == 1) {
                managerMenu(client);
            }
            else if (choice == 2) {
                listCustomers(client);
            }

            else if (choice == 3) {
                createCustomerOption(client);
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

            // create the company table
            String companySql = "CREATE TABLE IF NOT EXISTS COMPANY " +
                    "(ID INT AUTO_INCREMENT PRIMARY KEY, " +
                    " NAME VARCHAR UNIQUE NOT NULL); ";

            st.executeUpdate(companySql);

            // create the car table
            String carSql = "CREATE TABLE IF NOT EXISTS CAR (" +
                    "ID INT AUTO_INCREMENT PRIMARY KEY, " +
                    "NAME VARCHAR UNIQUE NOT NULL, " +
                    "COMPANY_ID INT NOT NULL," +
                    "RENTED boolean DEFAULT FALSE," +
                    "FOREIGN KEY (COMPANY_ID) REFERENCES COMPANY (ID)" +
                    ");";

            st.execute(carSql);

            // create the customer table

//            String sql = "DROP TABLE IF EXISTS CUSTOMER;";
//            st.executeUpdate(sql);

            String customerSql = "CREATE TABLE IF NOT EXISTS CUSTOMER (" +
                    "ID INT AUTO_INCREMENT PRIMARY KEY, " +
                    "NAME VARCHAR UNIQUE NOT NULL, " +
                    "RENTED_CAR_ID INT ," +
                    "FOREIGN KEY (RENTED_CAR_ID) REFERENCES CAR (ID)" +
                    ");";

            st.execute(customerSql);


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
    }
}