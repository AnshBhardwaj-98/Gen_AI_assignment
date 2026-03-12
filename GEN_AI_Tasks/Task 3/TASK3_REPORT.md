# Task 3: Technical Specification Generator - Detailed Report

## Overview

Task 3 generates comprehensive technical specifications for software systems using AI. It analyzes business requirements and auto-generates system modules, database schemas, API endpoints, and pseudocode, compiling everything into a professional markdown specification document.

## Workflow Steps

### Step 1: Analyze Business Requirement

**File**: `code/analyzer.py` → `analyze_requirement(requirement)`

- **Input**: Business requirement text describing system to build
- **Tool**: Google Gemini 2.5-flash

- **Process**:
  1. Receive business requirement (e.g., "Build a food delivery application...")
  2. Parse requirement text to identify:
     - Core features needed
     - User types and workflows
     - Key business processes
     - Technical constraints
  3. Generate structured analysis of requirements
  4. Return analysis summary

**Output**: Analyzed requirement text with key points extracted

**Default Requirement**:

```
Build a food delivery application where users can browse restaurants,
place orders, make payments, and track delivery in real time.
```

- **Fallback**: If Gemini fails, returns original requirement text as-is

---

### Step 2: Generate System Modules

**File**: `code/module_generator.py` → `generate_modules(requirement)`

- **Model**: Google Gemini 2.5-flash
- **Prompt**: Instructs model to design software modules based on requirements:
  - Identify 5-8 core system modules
  - Define module responsibilities
  - Module should be loosely coupled and highly cohesive
  - Include module interactions

- **Process**:
  1. Send analyzed requirement to Gemini
  2. Request list of modules needed for the system
  3. Parse response to extract module list
  4. Return structured module list

**Output**: List of 5-8 system modules

**Example Modules** (for food delivery):

- User Management & Authentication
- Restaurant & Menu Management
- Order Management & Processing
- Payment Gateway Integration
- Delivery Tracking & Logistics
- Rating & Review System
- Admin Dashboard
- Notification Service

- **Fallback**: If API fails, uses hardcoded food delivery modules:
  ```
  - User Management & Authentication
  - Restaurant & Menu Management
  - Order Management & Processing
  - Payment Gateway Integration
  - Delivery Tracking & Logistics
  - Rating & Review System
  - Admin Dashboard
  - Notification Service
  ```

---

### Step 3: Generate Database Schema

**File**: `code/schema_generator.py` → `generate_schema(modules)`

- **Model**: Google Gemini 2.5-flash
- **Prompt**: Instructs model to design database tables based on modules:
  - Define 6-10 core database tables
  - Include primary keys and relationships
  - Specify important field data types
  - Define foreign key relationships

- **Process**:
  1. Send module list to Gemini
  2. Request database schema design for the modules
  3. Parse response to extract table definitions
  4. Return structured schema list

**Output**: List of database table definitions

**Example Schema**:

```
- Users (id, name, email, phone, address, role)
- Restaurants (id, name, cuisine, latitude, longitude, rating)
- Menus (id, restaurant_id, item_name, price, category)
- Orders (id, user_id, restaurant_id, total_amount, status, timestamp)
- Deliveries (id, order_id, driver_id, status, location, eta)
- Payments (id, order_id, amount, method, status, timestamp)
- Reviews (id, order_id, rating, comment, timestamp)
- Drivers (id, name, phone, vehicle_info, status, current_location)
```

- **Fallback**: If API fails, uses hardcoded schema for food delivery system

---

### Step 4: Generate API Endpoints

**File**: `code/api_generator.py` → `generate_apis(modules)`

- **Model**: Google Gemini 2.5-flash
- **Prompt**: Instructs model to design RESTful API endpoints:
  - Design 8-12 core API endpoints
  - Include HTTP methods (GET, POST, PUT, DELETE)
  - Define request/response formats
  - Include authentication requirements

- **Process**:
  1. Send module list to Gemini
  2. Request API endpoint design
  3. Parse response to extract endpoint list
  4. Return structured API list with methods and paths

**Output**: List of RESTful API endpoints

**Example APIs**:

```
- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- GET /api/restaurants - Browse restaurants
- GET /api/restaurants/{id}/menu - Get restaurant menu
- POST /api/orders - Create new order
- GET /api/orders/{id} - Get order status
- PUT /api/orders/{id}/cancel - Cancel order
- GET /api/deliveries/{id} - Track delivery
- POST /api/reviews/{order_id} - Submit review
- POST /api/payments - Process payment
- GET /api/user/profile - Get user profile
- PUT /api/user/profile - Update user profile
```

- **Fallback**: If API fails, uses hardcoded REST API set for food delivery

---

### Step 5: Generate Pseudocode

**File**: `code/pseudocode_gen.py` → `generate_pseudocode(requirement)`

- **Model**: Google Gemini 2.5-flash
- **Prompt**: Instructs model to write pseudocode for core workflows:
  - Design order placement workflow
  - Include data validation
  - Define error handling
  - Include payment processing
  - Define delivery tracking logic

- **Process**:
  1. Send requirement to Gemini
  2. Request pseudocode for main workflows
  3. Parse response (pseudocode block)
  4. Return pseudocode as string

**Output**: Multi-step pseudocode for system workflows

**Example Pseudocode**:

```
FUNCTION placeOrder(userId, restaurantId, items):
  VALIDATE user exists and is authenticated
  VALIDATE restaurant is open
  FOR EACH item IN items:
    CHECK inventory availability
    CALCULATE item total
  CALCULATE order total
  CREATE order record
  INITIATE payment processing
  IF payment successful:
    UPDATE inventory
    NOTIFY restaurant
    NOTIFY delivery system
    CREATE delivery task
    RETURN order confirmation
  ELSE:
    ROLLBACK order
    NOTIFY user
    RETURN error

FUNCTION trackDelivery(orderId):
  FETCH delivery record
  GET driver location
  GET estimated arrival
  UPDATE order status
  NOTIFY user
  RETURN tracking info
```

- **Fallback**: If API fails, returns hardcoded pseudocode for food delivery system

---

### Step 6: Compile Technical Specification

**File**: `code/main.py` → `save_output(requirement, modules, schema, apis, pseudocode)`

- **Format**: Markdown (.md)
- **Structure**:

  ```markdown
  # Low-Level Technical Specification

  ## Business Requirement

  [Analyzed requirement]

  ## System Modules

  - Module 1
  - Module 2
    ...

  ## Database Schema

  - Table 1
  - Table 2
    ...

  ## API Endpoints

  - POST /api/endpoint1
  - GET /api/endpoint2
    ...

  ## Pseudocode
  ```

  [Multi-step pseudocode]

  ```

  ```

- **Process**:
  1. Create output directory if not exists
  2. Determine next available filename: `technical_spec_1.md`, `technical_spec_2.md`, etc.
  3. Write comprehensive specification file with all sections
  4. Return full path to generated file

**Output**: `technical_spec_{N}.md` (N = auto-incrementing number)

---

### Step 7: Output Management

**Directory Structure**:

```
Task 3/
├── code/
│   ├── main.py (entry point & orchestrator)
│   ├── analyzer.py (requirement analysis)
│   ├── module_generator.py (system modules)
│   ├── schema_generator.py (database design)
│   ├── api_generator.py (API endpoints)
│   ├── pseudocode_gen.py (workflow pseudocode)
│   └── requirements.txt
└── outputs/
    ├── technical_spec_1.md
    ├── technical_spec_2.md
    └── ...
```

**Numbering System**:

- Each run checks for existing files: `technical_spec_1.md`, `technical_spec_2.md`, etc.
- Automatically picks the next available number
- Prevents overwriting previous outputs

**Path Resolution**:

- Uses absolute path computed from script location: `os.path.abspath(__file__)`
- Works correctly regardless of current working directory
- Output always goes to `Task 3/outputs/` folder

---

## Key Technologies

| Component            | Technology              | Purpose                              |
| -------------------- | ----------------------- | ------------------------------------ |
| Requirement Analysis | Google Gemini 2.5-flash | Parse and understand requirements    |
| Module Design        | Google Gemini 2.5-flash | Generate system architecture         |
| Schema Design        | Google Gemini 2.5-flash | Design database structure            |
| API Design           | Google Gemini 2.5-flash | Define RESTful endpoints             |
| Pseudocode           | Google Gemini 2.5-flash | Write workflow logic                 |
| File Format          | Markdown (.md)          | Professional specification output    |
| File Management      | Python `os` module      | Organize outputs with absolute paths |

---

## Configuration

- **Python Version**: 3.13
- **API Key**: Set via `$env:GEMINI_API_KEY` environment variable
- **Model**: Google Gemini 2.5-flash
- **Output Path**: Computed from script location using `os.path.abspath(__file__)`

---

## Error Handling & Fallbacks

1. **Requirement Analysis Failure**:
   - Returns original requirement text as-is
   - Allows downstream processing to continue

2. **Module Generation Failure**:
   - Uses hardcoded 8-module architecture for food delivery system
   - Ensures consistent output structure

3. **Schema Generation Failure**:
   - Uses hardcoded 8-table schema design
   - Tables designed to support module requirements

4. **API Endpoint Generation Failure**:
   - Uses hardcoded 12-endpoint REST API
   - Endpoints designed to support all modules

5. **Pseudocode Generation Failure**:
   - Uses hardcoded pseudocode for main workflows
   - Includes order placement and delivery tracking

6. **File Write Failure**:
   - Automatically creates output directory if missing
   - Raises exception if file write still fails

---

## API Quota Handling

- **Gemini Free Tier**: 20 requests per day limit
- **Requests per Run**: 5 (analyzer, modules, schema, apis, pseudocode)
- **Fallback Strategy**: All Gemini calls wrapped in try-except
- **Behavior**: If quota exceeded, fallback functions generate valid content
- **Result**: Task still completes successfully, may use fallback data

---

## Performance Notes

- **Total Execution Time**: ~10-30 seconds
- **Internet Required**: Yes (Gemini API)
- **Disk Space**: ~5-15 KB per markdown file
- **Memory Usage**: ~100 MB (minimal)

---

## Data Flow Diagram

```
Business Requirement Text
        ↓
[analyzer] → Analyzed Requirement
        ↓
    Modules ← [module_generator]
    Schema ← [schema_generator]
    APIs ← [api_generator]
    Pseudocode ← [pseudocode_gen]
        ↓
[save_output]
        ↓
technical_spec_{N}.md
```

---

## Example Run Output

```
Analyzing business requirement...
✅ Requirement analyzed

Generating system modules...
✅ 8 modules generated:
  - User Management & Authentication
  - Restaurant & Menu Management
  - Order Management & Processing
  - Payment Gateway Integration
  - Delivery Tracking & Logistics
  - Rating & Review System
  - Admin Dashboard
  - Notification Service

Generating database schema...
✅ 8 database tables designed:
  - Users
  - Restaurants
  - Menus
  - Orders
  - Deliveries
  - Payments
  - Reviews
  - Drivers

Generating API endpoints...
✅ 12 REST API endpoints designed

Generating pseudocode...
✅ Workflow pseudocode generated

Saving technical specification...
✅ Technical specification generated: C:\...\GEN_AI_Tasks\Task 3\outputs\technical_spec_1.md
```

---

## Specification Document Structure

Each generated `technical_spec_{N}.md` file contains:

1. **Business Requirement Section**:
   - Original or analyzed system requirement
   - Key features and objectives

2. **System Modules Section**:
   - List of 5-8 core system modules
   - Module descriptions
   - Responsibilities and boundaries

3. **Database Schema Section**:
   - 6-10 database table definitions
   - Table structures with fields
   - Primary and foreign key relationships

4. **API Endpoints Section**:
   - 8-12 RESTful endpoints
   - HTTP methods and paths
   - Request/response formats
   - Authentication requirements

5. **Pseudocode Section**:
   - Multi-step workflow logic
   - Core business process implementations
   - Error handling and edge cases
   - Data validation

---

## Use Cases

This task is useful for:

- **Rapid Prototyping**: Quickly design systems before development
- **Design Review**: Get AI-generated specifications for feedback
- **Documentation**: Auto-generate technical specs for new projects
- **Architecture Planning**: Understand module and database design
- **Learning**: Study professional API and database design patterns
