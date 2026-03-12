# Low-Level Technical Specification

## Business Requirement
Build a food delivery application where users can browse restaurants,
place orders, make payments, and track delivery in real time.

## System Modules
- User Management
- Restaurant Management
- Order Management
- Payment Processing
- Delivery Management

## Database Schema
- Here is a simple database schema designed for the modules described:
- Users(user_id (PK), username, email, password_hash, phone_number, first_name, last_name, address, role)
- Restaurants(restaurant_id (PK), owner_user_id (FK), name, address, phone_number, cuisine_type, opening_time, closing_time, status)
- Menu_Items(menu_item_id (PK), restaurant_id (FK), name, description, price, category, is_available)
- Orders(order_id (PK), customer_user_id (FK), restaurant_id (FK), order_date, delivery_address, total_amount, order_status)
- Order_Items(order_item_id (PK), order_id (FK), menu_item_id (FK), quantity, item_price_at_order, notes)
- Payments(payment_id (PK), order_id (FK), amount, payment_date, payment_method, payment_status)
- Deliveries(delivery_id (PK), order_id (FK), driver_user_id (FK), pickup_time, delivery_time, delivery_status, delivery_fee)

## API Endpoints
- Here are REST API endpoints for the specified modules, following your rules:
- **User Management**
- POST /users
- GET /users
- GET /users/{userId}
- PUT /users/{userId}
- DELETE /users/{userId}
- POST /auth/register
- POST /auth/login
- POST /auth/password/forgot
- POST /auth/password/reset
- **Restaurant Management**
- POST /restaurants
- GET /restaurants
- GET /restaurants/{restaurantId}
- PUT /restaurants/{restaurantId}
- DELETE /restaurants/{restaurantId}
- GET /restaurants/{restaurantId}/menu
- POST /restaurants/{restaurantId}/menu/items
- PUT /restaurants/{restaurantId}/menu/items/{itemId}
- DELETE /restaurants/{restaurantId}/menu/items/{itemId}
- GET /restaurants/{restaurantId}/orders
- **Order Management**
- POST /orders
- GET /orders
- GET /orders/{orderId}
- GET /users/{userId}/orders
- PATCH /orders/{orderId}/status
- DELETE /orders/{orderId}
- **Payment Processing**
- POST /payments/process
- GET /payments/{paymentId}
- POST /payments/{paymentId}/refund
- GET /orders/{orderId}/payment
- **Delivery Management**
- GET /deliveries
- GET /deliveries/{deliveryId}
- GET /drivers/{driverId}/deliveries
- GET /orders/{orderId}/delivery
- PATCH /deliveries/{deliveryId}/assign
- PATCH /deliveries/{deliveryId}/status
- GET /deliveries/{deliveryId}/location

## Pseudocode
```
Here's high-level pseudocode for a food delivery application, focusing on the user's journey and key system interactions:

```
START APPLICATION

// Main User Loop
LOOP while Application_Is_Running
    AUTHENTICATE_USER() // Assumes login/registration happens here

    LOOP while User_Is_LoggedIn
        DISPLAY Main_Screen_Options (e.g., "Browse Restaurants", "View Cart", "Track Order", "View Past Orders", "Log Out")
        GET User_Choice

        IF User_Choice is "Browse Restaurants" THEN
            // Module: Browse Restaurants
            DISPLAY List_Of_Restaurants_With_Filters
            GET Selected_Restaurant_ID

            IF Selected_Restaurant_ID is VALID THEN
                DISPLAY Menu_For_Restaurant(Selected_Restaurant_ID)
                LOOP while User_Is_Adding_Items
                    GET Item_ID, Quantity
                    ADD Item_To_Cart(Item_ID, Quantity)
                    ASK_USER_IF_ADD_MORE_ITEMS
                    IF User_Says_No THEN
                        User_Is_Adding_Items = FALSE
                    END IF
                END LOOP
            ELSE
                DISPLAY "Invalid restaurant selected."
            END IF

        ELSE IF User_Choice is "View Cart" THEN
            // Module: Place Order & Payment
            IF Cart_Is_Empty THEN
                DISPLAY "Your cart is empty. Please add items."
            ELSE
                DISPLAY Cart_Contents, Total_Price
                GET Delivery_Address, Special_Instructions
                DISPLAY "Confirm order details (items, address, total price)."
                GET User_Confirmation

                IF User_Confirmation is "YES" THEN
                    DISPLAY "Choose payment method (Credit Card, Debit Card, Wallet)."
                    GET Payment_Method_Details

                    CALL FUNCTION Process_Payment(Total_Price, Payment_Method_Details)
                    IF Payment_Is_Successful THEN
                        CREATE New_Order_Record(User_ID, Cart_Contents, Delivery_Address, Special_Instructions, Payment_Details)
                        SET Order_Status_For_User = "Order Placed - Pending Confirmation"
                        NOTIFY Restaurant_Of_New_Order(New_Order_ID)
                        CLEAR_CART()
                        DISPLAY "Order placed successfully! Redirecting to tracking..."
                        CALL FUNCTION Track_Delivery(New_Order_ID) // Automatically go to tracking
                    ELSE
                        DISPLAY "Payment failed. Please try again or choose another method."
                    END IF
                ELSE
                    DISPLAY "Order not placed."
                END IF
            END IF

        ELSE IF User_Choice is "Track Order" THEN
            // Module: Track Delivery
            DISPLAY List_Of_Active_Orders_For_User
            GET Order_ID_To_Track

            IF Order_ID_To_Track is VALID THEN
                LOOP while Current_Order_Status(Order_ID_To_Track) is NOT "Delivered" AND Current_Order_Status(Order_ID_To_Track) is NOT "Cancelled"
                    DISPLAY Current_Order_Status(Order_ID_To_Track)
                    IF Current_Order_Status(Order_ID_To_Track) is "Out For Delivery" THEN
                        DISPLAY Driver_Location_On_Map(Order_ID_To_Track)
                        DISPLAY Estimated_Delivery_Time(Order_ID_To_Track)
                    END IF
                    WAIT 30_SECONDS // Simulate refreshing status
                END LOOP
                DISPLAY "Order " + Current_Order_Status(Order_ID_To_Track)
                IF Current_Order_Status(Order_ID_To_Track) is "Delivered" THEN
                    ASK_FOR_ORDER_REVIEW(Order_ID_To_Track)
                END IF
            ELSE
                DISPLAY "Invalid order selected for tracking."
            END IF

        ELSE IF User_Choice is "View Past Orders" THEN
            DISPLAY List_Of_Past_Orders_For_User(Including_Status_And_Details)

        ELSE IF User_Choice is "Log Out" THEN
            User_Is_LoggedIn = FALSE
            DISPLAY "You have been logged out."

        ELSE
            DISPLAY "Invalid option. Please try again."
        END IF

    END LOOP // End User_Is_LoggedIn loop
END LOOP // End Application_Is_Running loop

END APPLICATION


// --- SYSTEM BACKGROUND PROCESSES (Simplified High-Level) ---

// FUNCTION Process_Payment(Amount, Payment_Details)
//     CALL External_Payment_Gateway(Amount, Payment_Details)
//     IF Gateway_Response is "Success" THEN
//         RETURN TRUE
//     ELSE
//         RETURN FALSE
//     END IF
// END FUNCTION

// SYSTEM PROCESS: Restaurant Order Handling
// LOOP while TRUE // Runs continuously in the background
//     IF New_Order_Received_By_Restaurant(Order_ID) THEN
//         NOTIFY Restaurant_Staff_Of_New_Order(Order_ID)
//         WAIT_FOR_RESTAURANT_ACTION(Order_ID) // Staff accepts/rejects
//         GET Restaurant_Decision

//         IF Restaurant_Decision is "Accept" THEN
//             UPDATE Order_Status(Order_ID) = "Preparing"
//             NOTIFY User_Order_Accepted(Order_ID)
//             CALL FUNCTION Assign_Driver_To_Order(Order_ID)
//         ELSE IF Restaurant_Decision is "Reject" THEN
//             UPDATE Order_Status(Order_ID) = "Restaurant Rejected"
//             NOTIFY User_Order_Rejected(Order_ID)
//             INITIATE_REFUND(Order_ID)
//         END IF
//     END IF
//     // Periodically check for other restaurant-related tasks
// END LOOP

// FUNCTION Assign_Driver_To_Order(Order_ID)
//     FIND Available_Driver_Near_Restaurant(Order_ID)
//     IF Driver_Found THEN
//         NOTIFY Driver_Of_New_Delivery(Order_ID)
//         WAIT FOR Driver_Acceptance
//         IF Driver_Accepts THEN
//             UPDATE Order_Status(Order_ID) = "Driver Assigned"
//             NOTIFY User_Driver_Assigned(Order_ID, Driver_Details)
//         ELSE
//             // Retry finding another driver or mark as "No Driver Available"
//             UPDATE Order_Status(Order_ID) = "No Driver Available"
//             NOTIFY Restaurant_And_User_Of_Driver_Issue(Order_ID)
//         END IF
//     ELSE
//         UPDATE Order_Status(Order_ID) = "No Driver Available"
//         NOTIFY Restaurant_And_User_Of_Driver_Issue(Order_ID)
//     END IF
// END FUNCTION

// SYSTEM PROCESS: Driver App Updates
// LOOP while TRUE // Driver app continuously sends updates
//     IF Driver_Updates_Status(Order_ID, New_Status, Current_Location) THEN
//         UPDATE Order_Status(Order_ID) = New_Status
//         UPDATE Driver_Location_For_Order(Order_ID) = Current_Location
//         NOTIFY User_Of_Order_Status_Update(Order_ID, New_Status, Current_Location)
//     END IF
// END LOOP

```
```