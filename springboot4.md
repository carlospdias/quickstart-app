# Spring Boot 4 for Java Developers: What You Need to Know

After more than 20 years of evolution, Spring Framework has reached its seventh generation, and with it comes Spring Boot 4 — officially released in November 2025.

> But here’s the thing: this isn’t just another incremental update with a few new features sprinkled on top. Spring Boot 4 represents a fundamental reimagining of how we build Java applications. The framework has been completely modularized, null safety has been baked into the core, and declarative HTTP clients finally eliminate the boilerplate we’ve all been complaining about. If you’re still running Spring Boot 3, you might be wondering if the upgrade is worth the effort. Spoiler alert: it absolutely is.

-------------

## Table of Contents
 - The Modular Revolution: Why Your Apps Just Got Lighter
 - Game-Changing Features That Actually Matter
 - Migration Strategy: Making the Jump
 - Real-World Implementation Example

## The Modular Revolution: Why Your Apps Just Got Lighter
Remember the days when adding spring-boot-starter-web to your project pulled in configuration classes for every possible integration under the sun? Batch jobs you'd never run, databases you'd never touch, and entire subsystems you didn't even know existed—all sitting there, consuming memory and slowing down your startup time.

Spring Boot 4 fundamentally changes this by splitting the massive auto-configuration module into smaller, focused jars. Think of it like this: before, Spring Boot was like packing for a trip by bringing your entire closet “just in case.” Now, you only pack what you actually need.


What This Means for You
When you add a starter dependency now, you get exactly what that starter needs and nothing more. Add spring-boot-starter-webmvc? You get WebMVC configuration. No batch processing hints, no reactive web configuration, no unnecessary database auto-configuration.

### The practical benefits are immediately noticeable:

 - Faster startup times — Less classpath scanning means your application boots quicker
 - Reduced memory footprint — Fewer configuration classes loaded into memory
 - Cleaner dependency trees — Easier to debug and understand what’s actually in your application
 - Better native image compilation — GraalVM doesn’t need to process unnecessary metadata
Here’s the kicker: as a developer using starter dependencies, you don’t need to change a single line in your pom.xml or build.gradle. The modularization happens behind the scenes, but you reap all the benefits.


## Game-Changing Features That Actually Matter
### Native API Versioning (Finally!)
We’ve all been there — hardcoding version numbers into every URL path like some kind of medieval artisan. Need to support both /v1/users and /v2/users? Better create duplicate controllers. Want to switch from URL-based versioning to header-based? Time to rewrite everything.

Spring Boot 4 introduces a version attribute directly in @RequestMapping and @GetMapping annotations, making API versioning a first-class citizen.

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping(version = "1")
    public List<UserDTO> getUsersV1() {
        return userService.getAllUsersBasic();
    }
    
    @GetMapping(version = "2")
    public List<EnhancedUserDTO> getUsersV2() {
        return userService.getAllUsersWithMetadata();
    }
}

```

You can even configure the versioning strategy globally in application.properties:

```text

# Use header-based versioning
spring.web.api.versioning.strategy=header
spring.web.api.versioning.header-name=X-API-VERSION

# Or stick with URL path versioning
# spring.web.api.versioning.strategy=path
# spring.web.api.versioning.path-prefix=/v

```

## JSpecify Null Safety: Your IDE Becomes Your Safety Net

Spring Framework 7 migrates to JSpecify annotations, providing precise nullness contracts for method parameters, return types, and fields. This isn’t just theoretical — it catches bugs before they reach production.

Think of JSpecify as a traffic light system:

- @Nullable → Red light: this might be null, check it
- @NonNull → Green light: guaranteed to have a value
- @NullMarked → The entire package follows null-safe rules by default


Here’s where it gets powerful. Create a package-info.java file:
```java
@NullMarked
package com.yourcompany.users;
import org.jspecify.annotations.NullMarked;

```

Now every class in that package assumes non-null by default. You only annotate exceptions:

```java
public class UserService {
    
    // Returns are guaranteed non-null
    public User findUser(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
    
    // But this one might return null
    public @Nullable User findUserOptional(Long id) {
        return userRepository.findById(id).orElse(null);
    }
}

```

Your IDE (IntelliJ IDEA 2025.3+) highlights potential null pointer exceptions as you type. No more runtime surprises.

Add the dependency to use it in your own code:

```xml
<dependency>
    <groupId>org.jspecify</groupId>
    <artifactId>jspecify</artifactId>
    <version>1.0.0</version>
</dependency>
```

## Declarative HTTP Clients: RestTemplate’s Modern Replacement
Remember writing this mess with RestTemplate?

```java
// The old way - verbose and painful
RestTemplate restTemplate = new RestTemplate();
HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.APPLICATION_JSON);
HttpEntity<OrderRequest> entity = new HttpEntity<>(orderRequest, headers);

ResponseEntity<OrderResponse> response = restTemplate.exchange(
    "https://api.example.com/orders",
    HttpMethod.POST,
    entity,
    OrderResponse.class
);

```

Spring Boot 4 includes auto-configuration support for HTTP Service Clients, allowing you to annotate plain Java interfaces and have Spring automatically create implementations.

Here’s the new way:

```java
@HttpExchange(url = "https://api.example.com")
public interface OrderClient {
    
    @PostExchange("/orders")
    OrderResponse createOrder(@RequestBody OrderRequest request);
    
    @GetExchange("/orders/{id}")
    OrderResponse getOrder(@PathVariable Long id);
    
    @PutExchange("/orders/{id}")
    OrderResponse updateOrder(@PathVariable Long id, 
                             @RequestBody OrderRequest request);
}

```

Then just inject it like any other Spring bean:
```java
@Service
public class OrderService {
    
    private final OrderClient orderClient;
    
    public OrderService(OrderClient orderClient) {
        this.orderClient = orderClient;
    }
    
    public void processOrder(OrderRequest request) {
        OrderResponse response = orderClient.createOrder(request);
        // Handle response
    }
}
```

Zero boilerplate. Spring handles the implementation, error handling, serialization, and deserialization automatically.

## Built-in Resilience Patterns
Modern applications need to handle failures gracefully. Spring Boot 4 introduces @Retryable and @ConcurrencyLimit annotations:
```java
@Service
@EnableResilientMethods
public class PaymentService {
    
    @Retryable(maxAttempts = 3, backoff = @Backoff(delay = 1000))
    public PaymentResult processPayment(PaymentRequest request) {
        // This will retry up to 3 times with 1s delay
        return externalPaymentGateway.process(request);
    }
    
    @ConcurrencyLimit(maxConcurrentCalls = 10)
    public void generateReport(ReportRequest request) {
        // Only 10 concurrent executions allowed
        // Others will wait or fail fast
    }
}
```

These patterns used to require third-party libraries like Resilience4j. Now they’re baked right in.


## Migration Strategy: Making the Jump
Upgrading to Spring Boot 4 isn’t a Sunday afternoon project, but it’s not as scary as you might think. Here’s your battle plan:


## The Prerequisites
 - Upgrade to Java 17 minimum (Java 21 or 25 recommended)
 - Switch from javax.* to jakarta.* packages — This is the big one
 - Update your dependencies:
 - JUnit 4 → JUnit 5
 - Jackson 2.x → Jackson 3.x
 - Any old Hibernate Validator → Version 9


## The Jakarta Migration

The javax.* to jakarta.* migration affects almost every Spring application. Fortunately, IntelliJ IDEA has built-in refactoring tools:

Find & Replace across your project:

 - import javax.persistence → import jakarta.persistence
 - import javax.servlet → import jakarta.servlet
 - import javax.validation → import jakarta.validation

```java
 // Before
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.validation.constraints.NotNull;

// After
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.validation.constraints.NotNull;

```

## Deprecated Features to Watch
 - No more suffix pattern matching in Spring MVC — /users.json won't work anymore
 - Trailing slash matching removed — /users and /users/ are now different endpoints
 - Spring JCL module retired — Migrated to Apache Commons Logging
 - JUnit 4 support dropped — Time to embrace JUnit 5


## Update Your pom.xml

```xml
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>4.0.1</version>
  </parent>

  <properties>
    <java.version>21</java.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-opentelemetry</artifactId>
    </dependency>
  </dependencies>
```


## Real-World Implementation Example
Let’s build a practical example that showcases Spring Boot 4’s new capabilities: a User Management Service with API versioning, declarative HTTP clients, null safety, and resilience patterns.

### Project Setup

```xml
<!-- pom.xml -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>4.0.1</version>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.jspecify</groupId>
        <artifactId>jspecify</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

### Null-Safe Domain Model

```java
@NullMarked
package com.example.users.domain;

import org.jspecify.annotations.NullMarked;
import org.jspecify.annotations.Nullable;

@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String username;
    private String email;
    
    @Nullable  // Middle name is optional
    private String middleName;
    
    // Getters and setters
}
```

### Versioned API Endpoints

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final UserService userService;
    private final AuditClient auditClient;
    
    // V1: Basic user info
    @GetMapping(value = "/{id}", version = "1")
    public UserDTOV1 getUserV1(@PathVariable Long id) {
        User user = userService.findById(id);
        return new UserDTOV1(user.getUsername(), user.getEmail());
    }
    
    // V2: Enhanced with metadata
    @GetMapping(value = "/{id}", version = "2")
    public UserDTOV2 getUserV2(@PathVariable Long id) {
        User user = userService.findById(id);
        auditClient.logAccess(id, "read");  // Using declarative client
        return new UserDTOV2(
            user.getUsername(), 
            user.getEmail(),
            user.getMiddleName(),  // Nullable field
            LocalDateTime.now()
        );
    }
}

```

### Declarative HTTP Client for Audit Service

```java
@HttpExchange(url = "${audit.service.url}")
public interface AuditClient {
    
    @PostExchange("/audit/logs")
    void logAccess(@RequestParam Long userId, 
                   @RequestParam String action);
    
    @GetExchange("/audit/logs/{userId}")
    List<AuditLog> getUserAuditHistory(@PathVariable Long userId);
}
```

### Resilient Service Layer

```java
@Service
@EnableResilientMethods
public class UserService {
    
    private final UserRepository userRepository;
    private final EmailClient emailClient;
    
    @Retryable(maxAttempts = 3, backoff = @Backoff(delay = 500))
    public void sendWelcomeEmail(User user) {
        // External email service - retry on failure
        emailClient.send(user.getEmail(), "Welcome!");
    }
    
    @ConcurrencyLimit(maxConcurrentCalls = 20)
    public List<User> searchUsers(String query) {
        // Rate-limited expensive operation
        return userRepository.searchByQuery(query);
    }
    
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

### Configuration

```sh
# application.properties

# API Versioning Strategy
spring.web.api.versioning.strategy=header
spring.web.api.versioning.header-name=X-API-VERSION
# External Service URLs
audit.service.url=https://audit.example.com
# Database
spring.datasource.url=jdbc:postgresql://localhost:5432/userdb
spring.jpa.hibernate.ddl-auto=validate
```


Links

 - https://www.youtube.com/watch?v=6_Y41z7OIv8&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK
 - https://www.youtube.com/watch?v=KmNAqlaKwjw&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK&index=3
 - https://www.youtube.com/watch?v=91xVrWlzIe4&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK&index=5
 - https://www.youtube.com/watch?v=s_kmDbitE8s&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK&index=6
 - https://www.youtube.com/watch?v=CT1wGTwOfg0&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK&index=7
 - https://www.youtube.com/watch?v=4cvP_qroLH4&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK&index=8
 - https://www.youtube.com/watch?v=QlGnaRoujL8&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK&index=10
 - https://www.youtube.com/watch?v=dPM8n0uNhes&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK&index=11
 - https://www.youtube.com/watch?v=qjo2tYf01xo&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK&index=12
 - https://www.youtube.com/watch?v=yh760wTFL_4&list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK&index=13
 
 - https://www.youtube.com/watch?v=59twysAveKI


## Outras fontes
https://www.danvega.dev/blog/spring-boot-4-is-here
https://javascript.plainenglish.io/the-future-is-now-how-spring-boot-4-0-and-framework-7-redefine-resilience-and-performance-d22d88a0fdbe


## Docs do Springboot 4
- https://docs.spring.io/spring-boot/index.html
- https://www.youtube.com/watch?v=ENpq2J5yQ8Y

