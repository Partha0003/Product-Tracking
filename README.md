# Supply Chain Product Tracking System - Spring Boot REST API

A robust, enterprise-grade **Java Spring Boot 3.x** RESTful API for tracking products across supply chain milestones (`Manufactured` → `Shipped` → `Delivered`), migrated from Node.js/Express with 100% API contract and PostgreSQL database compatibility.

---

## 🚀 Tech Stack

- **Language:** Java 21
- **Framework:** Spring Boot 3.3.5
  - `spring-boot-starter-web` (REST API & MVC)
  - `spring-boot-starter-data-jpa` (Hibernate ORM & Spring Data)
  - `spring-boot-starter-validation` (Jakarta Bean Validation)
- **Database:** PostgreSQL (with `org.postgresql:postgresql` driver)
- **Testing:** JUnit 5, Mockito, Spring Boot Test, MockMvc, H2 Database (for automated test isolation)
- **Build Tool:** Apache Maven
- **Port:** `5000` (Maintains compatibility with existing frontend applications)

---

## 📁 Project Architecture

```
Product-Tracking-System-main/
├── src/
│   ├── main/
│   │   ├── java/com/producttracking/
│   │   │   ├── ProductTrackingApplication.java        # Spring Boot Entry Point
│   │   │   ├── config/
│   │   │   │   └── CorsConfig.java                    # Global CORS Configuration
│   │   │   ├── controller/
│   │   │   │   ├── RootController.java                # GET / (Health Check)
│   │   │   │   └── ProductController.java             # /products Endpoints
│   │   │   ├── dto/
│   │   │   │   ├── ProductRequestDto.java             # Product creation payload
│   │   │   │   └── StatusUpdateDto.java               # Status update payload
│   │   │   ├── entity/
│   │   │   │   └── Product.java                       # JPA Entity mapped to 'products' table
│   │   │   ├── repository/
│   │   │   │   └── ProductRepository.java             # Spring Data JPA Repository
│   │   │   ├── service/
│   │   │   │   ├── ProductService.java                # Service Interface
│   │   │   │   └── impl/ProductServiceImpl.java       # Business Logic Implementation
│   │   │   └── exception/
│   │   │       ├── ResourceNotFoundException.java     # Custom 404 Exception
│   │   │       └── GlobalExceptionHandler.java        # @RestControllerAdvice Error Handling
│   │   └── resources/
│   │       └── application.properties                 # PostgreSQL & Server Configuration
│   └── test/
│       ├── java/com/producttracking/
│       │   ├── ProductTrackingApplicationTests.java   # Context Loading Verification
│       │   ├── controller/
│       │   │   ├── RootControllerTest.java            # Health Check MockMvc Tests
│       │   │   └── ProductControllerTest.java         # All 5 Endpoints MockMvc Tests
│       │   └── service/
│       │       └── ProductServiceTest.java            # Business Logic & Lifecycle Tests
│       └── resources/
│           └── application.properties                 # H2 in-memory test configuration
├── .env.example                                       # Documented Environment Variables
├── pom.xml                                            # Maven Build Configuration
└── README.md
```

---

## 🗄️ Database Configuration & Schema

The application maps directly to the existing PostgreSQL `products` table without dropping or modifying existing records:

```sql
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    origin VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Manufactured'
);
```

### Environment Variables

Configure database credentials via environment variables or a `.env` file (refer to `.env.example`):

| Variable | Description | Default Value |
| :--- | :--- | :--- |
| `DB_HOST` | Database host address | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | `product_tracking` |
| `DB_USER` | Database username | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` |

---

## 📡 API Endpoints & Contracts

All endpoints are hosted on `http://localhost:5000`.

### 1. Health Check
- **Endpoint:** `GET /`
- **Response Status:** `200 OK`
- **Response Body (`text/plain`):**
  ```
  Server is running!
  ```

---

### 2. Retrieve All Products
- **Endpoint:** `GET /products`
- **Response Status:** `200 OK`
- **Response Body (`application/json`):**
  ```json
  [
    {
      "id": 1,
      "name": "Mechanical Keyboard",
      "origin": "Assembly Plant 1",
      "status": "Manufactured"
    },
    {
      "id": 2,
      "name": "Smart Monitor",
      "origin": "Factory B",
      "status": "Shipped"
    }
  ]
  ```

---

### 3. Register a New Product
- **Endpoint:** `POST /products`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "name": "Industrial Sensor",
    "origin": "Plant Dallas",
    "status": "Manufactured"
  }
  ```
  *(Note: `status` is optional and defaults to `"Manufactured"` if omitted).*
- **Response Status:** `200 OK`
- **Response Body:**
  ```json
  {
    "id": 3,
    "name": "Industrial Sensor",
    "origin": "Plant Dallas",
    "status": "Manufactured"
  }
  ```

---

### 4. Update Product Status
- **Endpoint:** `PUT /products/{id}/status`
- **Path Parameter:** `id` (numeric ID)
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "status": "Shipped"
  }
  ```
  *(Note: Protects `name` and `origin` from accidental modification; only `status` is updated).*
- **Response Status:** `200 OK`
- **Response Body:**
  ```json
  {
    "id": 3,
    "name": "Industrial Sensor",
    "origin": "Plant Dallas",
    "status": "Shipped"
  }
  ```

---

### 5. Delete a Product
- **Endpoint:** `DELETE /products/{id}`
- **Path Parameter:** `id` (numeric ID)
- **Response Status:** `200 OK`
- **Response Body:**
  ```json
  {
    "message": "Product deleted successfully"
  }
  ```

---

## 🧪 Testing

The test suite contains **22 automated tests** across all controller endpoints, service logic, lifecycle rules, and error conditions using JUnit 5, Mockito, and Spring Boot MockMvc.

To execute tests:
```bash
mvn test
```

---

## 🏃 Running the Application

### Option 1: Run with Local Standalone Profile (Zero Setup Required)
If you do not have PostgreSQL running right now, you can immediately start the application with an in-memory database:

In PowerShell:
```powershell
mvn spring-boot:run '-Dspring-boot.run.profiles=local'
```

In Command Prompt (cmd) / Bash:
```bash
mvn spring-boot:run -Dspring-boot.run.profiles=local
```

---

### Option 2: Run with PostgreSQL (Default)

#### 1. Start PostgreSQL Database
If you have Docker Desktop installed, start PostgreSQL in one command using the included `docker-compose.yml`:
```bash
docker compose up -d
```
Or start your locally installed PostgreSQL service on port `5432` with a database named `product_tracking`.

#### 2. Start the Application
```powershell
mvn spring-boot:run
```

---

### Option 3: Package & Run Executable JAR
```powershell
mvn clean package -DskipTests
java -jar target/product-tracking-system-1.0.0.jar
```

The server listens on port **`5000`** at **`http://localhost:5000`**.
