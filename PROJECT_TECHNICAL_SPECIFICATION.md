# Supply Chain Product Tracking System - Technical Specification & Architecture Document

This document provides a comprehensive technical breakdown of the current Node.js/Express backend system, database architecture, API specifications, and the migration blueprint for transitioning to a **Spring Boot REST API** while maintaining 100% backward compatibility.

---

## 1. Project Overview

- **Project Name:** Supply Chain Product Tracking System
- **Current Role:** Backend RESTful API Service
- **Core Functionality:** Tracking products across supply chain stages (`Manufactured` → `Shipped` → `Delivered`), allowing product registration, status transitions, retrieval, and lifecycle management.
- **Current Port:** `5000`
- **Default Base URL:** `http://localhost:5000`

---

## 2. Current Technology Stack

### Runtime & Core Framework
- **Runtime:** Node.js (CommonJS modules)
- **Framework:** Express.js (`^5.2.1`)
- **Database Driver:** `pg` (node-postgres `^8.18.0`) using connection pooling (`pg.Pool`)

### Installed Dependencies & Purpose
| Package | Version | Purpose in Existing Codebase |
| :--- | :--- | :--- |
| `express` | `^5.2.1` | HTTP Web server and routing framework |
| `pg` | `^8.18.0` | PostgreSQL client for connection pooling and SQL queries |
| `dotenv` | `^17.2.3` | Loads environment variables from `.env` |
| `cors` | `^2.8.6` | Cross-Origin Resource Sharing middleware (installed for client integration) |
| `body-parser`| `^2.2.2` | Request body parsing (used via `express.json()`) |
| `jsonwebtoken`| `^9.0.3`| JWT support (installed in dependencies for authentication) |
| `bcryptjs` | `^3.0.3` | Password hashing utility (installed in dependencies for user credential security) |

---

## 3. Database Architecture & Schema

### PostgreSQL Connection Configuration (`config/db.js`)
The application currently connects to PostgreSQL using the following environment variables:
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT` (Default PostgreSQL port: `5432`)
- `DB_NAME`

### Inferred Database Schema: `products` Table

Based on direct raw SQL queries in `server.js`:
```sql
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    origin VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Manufactured'
);
```

#### Fields Description:
- **`id`** (`SERIAL` / `BIGSERIAL`, Primary Key): Auto-incrementing unique product identifier.
- **`name`** (`VARCHAR` / `TEXT`): Name or description of the product (e.g., `"Laptop"`, `"Coffee Beans"`).
- **`origin`** (`VARCHAR` / `TEXT`): Location or facility where product originated (e.g., `"Factory A"`, `"Warehouse 3"`).
- **`status`** (`VARCHAR`): Current supply chain milestone (`Manufactured` → `Shipped` → `Delivered`).

---

## 4. API Endpoints Specification (Current Contracts)

All endpoints exchange data in `application/json` format.

### 4.1. Health Check
- **Route:** `GET /`
- **Response:** Plain text: `"Server is running!"`
- **Status Code:** `200 OK`

---

### 4.2. Get All Products
- **Route:** `GET /products`
- **Description:** Fetches all products stored in the database.
- **SQL Executed:** `SELECT * FROM products`
- **Response (200 OK):**
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
- **Error Response (500 Internal Server Error):**
  `"Error fetching products"`

---

### 4.3. Create Product
- **Route:** `POST /products`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "name": "Industrial Sensor",
    "origin": "Plant Dallas",
    "status": "Manufactured"
  }
  ```
- **SQL Executed:**
  `INSERT INTO products (name, origin, status) VALUES ($1, $2, $3) RETURNING *`
- **Response (200 OK / 201 Created):**
  ```json
  {
    "id": 3,
    "name": "Industrial Sensor",
    "origin": "Plant Dallas",
    "status": "Manufactured"
  }
  ```
- **Error Response (500 Internal Server Error):**
  `"Error creating product"`

---

### 4.4. Update Product Status
- **Route:** `PUT /products/:id/status`
- **Path Variable:** `id` (integer)
- **Headers:** `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "status": "Shipped"
  }
  ```
- **SQL Executed:**
  `UPDATE products SET status = $1 WHERE id = $2 RETURNING *`
- **Response (200 OK):**
  ```json
  {
    "id": 3,
    "name": "Industrial Sensor",
    "origin": "Plant Dallas",
    "status": "Shipped"
  }
  ```
- **Error Response (500 Internal Server Error):**
  `"Error updating status"`

---

### 4.5. Delete Product (Documented in README / Planned)
- **Route:** `DELETE /products/:id`
- **Path Variable:** `id` (integer)
- **Target SQL:** `DELETE FROM products WHERE id = $1`
- **Target Response:** Confirmation message or 204 No Content.

---

## 5. Architectural & Behavioral Characteristics

1. **State & Lifecycle Workflow:**
   Products move through a sequential status workflow:
   `Manufactured` ➔ `Shipped` ➔ `Delivered` (with extensible custom states).

2. **Error Handling:**
   Currently uses standard `try-catch` blocks returning 500 status codes with textual error feedback.

3. **Port & Connectivity:**
   Express currently listens on `PORT = 5000`. When migrating to Spring Boot, the server can be configured to run on port `5000` via `server.port=5000` to prevent breaking frontend clients.

4. **Security & Future Scope (Present in dependencies):**
   `jsonwebtoken` and `bcryptjs` are present in `package.json`, indicating intent for future or planned authentication/authorization layers (e.g. Spring Security + JWT).

---

## 6. Spring Boot Target Architecture Mapping

To migrate this Node.js/Express backend to Spring Boot seamlessly without altering external client interfaces:

### Proposed Target Tech Stack:
- **Language:** Java 17 or Java 21
- **Framework:** Spring Boot 3.x (`spring-boot-starter-web`, `spring-boot-starter-data-jpa`, `spring-boot-starter-validation`)
- **Database Driver:** `org.postgresql:postgresql`
- **ORM / Persistence:** Hibernate / Spring Data JPA
- **Build Tool:** Maven (`pom.xml`) or Gradle (`build.gradle`)
- **Utilities:** Lombok (optional for cleaner getters/setters/constructors)

### Target Package & Layer Structure:
```
com.producttracking/
├── ProductTrackingApplication.java      // Application Entry Point
├── config/
│   └── CorsConfig.java                  // Cross-Origin Resource Sharing setup
├── controller/
│   ├── RootController.java              // GET / -> Health check
│   └── ProductController.java           // /products endpoints
├── model/entity/
│   └── Product.java                     // JPA Entity mapping 'products' table
├── dto/
│   ├── ProductRequestDto.java           // Payload for POST /products
│   └── StatusUpdateDto.java             // Payload for PUT /products/{id}/status
├── repository/
│   └── ProductRepository.java           // JpaRepository<Product, Long>
├── service/
│   ├── ProductService.java              // Business interface
│   └── impl/ProductServiceImpl.java     // Business logic implementation
└── exception/
    ├── ResourceNotFoundException.java   // Custom 404 handler
    └── GlobalExceptionHandler.java      // @ControllerAdvice for uniform error responses
```

### Target Configuration (`src/main/resources/application.properties`):
```properties
server.port=5000

spring.datasource.url=jdbc:postgresql://${DB_HOST:localhost}:${DB_PORT:5432}/${DB_NAME:product_tracking}
spring.datasource.username=${DB_USER:postgres}
spring.datasource.password=${DB_PASSWORD:postgres}
spring.datasource.driver-class-name=org.postgresql.Driver

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```

---

## 7. Key Requirements for Migration Prompt
When generating your prompt for ChatGPT:
1. **Preserve exact API routes, request bodies, and JSON response formats** (`GET /`, `GET /products`, `POST /products`, `PUT /products/{id}/status`, `DELETE /products/{id}`).
2. **Maintain database schema compatibility** with table `products` (`id`, `name`, `origin`, `status`).
3. **Configure default port to `5000`** so frontend integrations remain intact.
4. **Environment variable parity** (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`).
5. **Include standard CORS configuration** for local development and client consumption.
