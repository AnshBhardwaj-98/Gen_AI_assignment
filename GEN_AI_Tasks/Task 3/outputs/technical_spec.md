# Low-Level Technical Specification

## Business Requirement
Build a food delivery application where users can browse restaurants,
place orders, make payments, and track delivery in real time.

## System Modules
- User Management
- Restaurant Catalog
- Order Management
- Payment Processing
- Delivery Management
- Notification Service

## Database Schema
- Here's a simple database schema design based on your modules and rules:
- users(user_id, first_name, last_name, email, password_hash, phone_number, user_type, created_at, updated_at)
- restaurants(restaurant_id, owner_user_id, name, description, address_street, address_city, address_state, address_zip, phone_number, email, website, logo_url, rating, created_at, updated_at)
- menu_items(menu_item_id, restaurant_id, name, description, price, category, image_url, is_available, created_at, updated_at)
- orders(order_id, customer_user_id, restaurant_id, delivery_address_street, delivery_address_city, delivery_address_state, delivery_address_zip, total_amount, order_status, special_instructions, order_date, created_at, updated_at)
- order_items(order_item_id, order_id, menu_item_id, quantity, price_at_order, special_requests)
- payments(payment_id, order_id, amount, payment_method, transaction_status, transaction_date, payment_gateway_id, gateway_transaction_id, created_at, updated_at)
- deliveries(delivery_id, order_id, driver_user_id, delivery_status, pickup_time, estimated_delivery_time, actual_delivery_time, tracking_code, driver_notes, created_at, updated_at)
- notifications(notification_id, recipient_user_id, message, notification_type, is_read, created_at)

## API Endpoints
- Here are the REST API endpoints for your modules:
- **User Management**
- *   `POST /users`
- *   `POST /auth/login`
- *   `GET /users/me`
- *   `GET /users/{id}`
- *   `PUT /users/me`
- *   `PUT /users/{id}/password`
- *   `DELETE /users/me`
- *   `GET /users`
- *   `PUT /users/{id}/role`
- *   `POST /auth/forgot-password`
- *   `POST /auth/reset-password`
- **Restaurant Catalog**
- *   `GET /restaurants`
- *   `GET /restaurants/{id}`
- *   `POST /restaurants`
- *   `PUT /restaurants/{id}`
- *   `DELETE /restaurants/{id}`
- *   `GET /restaurants/{id}/menu`
- *   `POST /restaurants/{id}/menu/items`
- *   `PUT /restaurants/{restaurantId}/menu/items/{itemId}`
- *   `DELETE /restaurants/{restaurantId}/menu/items/{itemId}`
- *   `GET /restaurants/{id}/reviews`
- *   `POST /restaurants/{id}/reviews`
- **Order Management**
- *   `POST /orders`
- *   `GET /orders/{id}`
- *   `GET /users/me/orders`
- *   `GET /orders`
- *   `PUT /orders/{id}/status`
- *   `DELETE /orders/{id}`
- *   `POST /orders/{orderId}/items`
- *   `DELETE /orders/{orderId}/items/{itemId}`
- **Payment Processing**
- *   `POST /payments`
- *   `GET /payments/{id}`
- *   `GET /orders/{orderId}/payment`
- *   `POST /payments/{id}/capture`
- *   `POST /payments/{id}/refund`
- *   `GET /users/me/payment-methods`
- *   `POST /users/me/payment-methods`
- *   `DELETE /users/me/payment-methods/{id}`
- **Delivery Management**
- *   `GET /deliveries/{id}`
- *   `GET /orders/{orderId}/delivery`
- *   `PUT /deliveries/{id}/status`
- *   `POST /deliveries/{id}/assign-driver`
- *   `GET /drivers`
- *   `GET /drivers/{id}`
- *   `POST /drivers`
- *   `PUT /drivers/{id}`
- *   `GET /drivers/{id}/deliveries`
- *   `GET /deliveries/pending`
- *   `GET /deliveries/{id}/location`
- **Notification Service**
- *   `POST /notifications/send`
- *   `GET /users/me/notifications`
- *   `PUT /users/me/notifications/{id}/read`
- *   `DELETE /users/me/notifications/{id}`
- *   `GET /users/me/notification-settings`
- *   `PUT /users/me/notification-settings`

## Pseudocode
```
Here's high-level pseudocode for the food delivery application:

```
START APPLICATION

    // --- User Authentication Flow ---
    DISPLAY "Welcome to Food Delivery App"
    GET UserChoice (options: "Login", "Sign Up")

    IF UserChoice IS "Sign Up" THEN
        CALL Function_SignUpUser()
        IF SignUp WAS SUCCESSFUL THEN
            DISPLAY "Please log in with your new account."
            CALL Function_LoginUser()
        ELSE
            DISPLAY "Sign up failed. Please try again."
            EXIT APPLICATION
        END IF
    ELSE IF UserChoice IS "Login" THEN
        CALL Function_LoginUser()
    ELSE
        DISPLAY "Invalid choice. Exiting."
        EXIT APPLICATION
    END IF

    // --- Main Application Flow (after successful login) ---
    IF User IS LoggedIn THEN
        SET CurrentUserLocation = GET User's GPS Location
        
        LOOP WHILE User IS LoggedIn
            DISPLAY Main Dashboard (showing nearby restaurants, search bar, order history link)
            GET UserAction (options: "Browse Restaurants", "View My Orders", "Account Settings", "Logout")

            IF UserAction IS "Browse Restaurants" THEN
                CALL Function_BrowseRestaurants(CurrentUserLocation)
            ELSE IF UserAction IS "View My Orders" THEN
                CALL Function_ViewOrderHistory(CurrentUser.ID)
            ELSE IF UserAction IS "Account Settings" THEN
                CALL Function_ManageAccount(CurrentUser.ID)
            ELSE IF UserAction IS "Logout" THEN
                SET User IS LoggedOut
                DISPLAY "You have been logged out."
                BREAK LOOP // Exit the main application loop
            ELSE
                DISPLAY "Invalid action. Please select a valid option."
            END IF
        END LOOP
    ELSE
        DISPLAY "Authentication failed. Exiting application."
    END IF

END APPLICATION


// --- Core Functions ---

FUNCTION Function_SignUpUser()
    DISPLAY "Sign Up Form"
    GET UserInput (Name, Email, Password, Phone)
    IF Validate_Input(UserInput) THEN
        SAVE NewUser_To_Database(UserInput)
        RETURN TRUE
    ELSE
        DISPLAY "Invalid input. Please check your details."
        RETURN FALSE
    END IF
END FUNCTION

FUNCTION Function_LoginUser()
    DISPLAY "Login Form"
    GET UserInput (Email, Password)
    IF Authenticate_User(UserInput.Email, UserInput.Password) THEN
        SET CurrentUser = GET User_Data_From_Database(UserInput.Email)
        DISPLAY "Login successful."
        RETURN TRUE
    ELSE
        DISPLAY "Login failed. Incorrect email or password."
        RETURN FALSE
    END IF
END FUNCTION

FUNCTION Function_BrowseRestaurants(location)
    SET CurrentCart = EMPTY_CART
    LOOP
        DISPLAY List of Restaurants (sorted by proximity to 'location', ratings, cuisine)
        GET UserAction (options: "Select Restaurant", "Search", "Filter", "Back to Main Menu")

        IF UserAction IS "Select Restaurant" THEN
            SET SelectedRestaurantID = GET RestaurantID_From_User_Selection
            CALL Function_ViewRestaurantMenu(SelectedRestaurantID, CurrentCart) // Pass cart to persist items
        ELSE IF UserAction IS "Search" THEN
            GET SearchQuery
            DISPLAY Filtered_Restaurants_By_Search(SearchQuery)
        ELSE IF UserAction IS "Filter" THEN
            GET FilterCriteria (e.g., "Cuisine", "Price Range", "Rating")
            DISPLAY Filtered_Restaurants_By_Criteria(FilterCriteria)
        ELSE IF UserAction IS "Back to Main Menu" THEN
            BREAK LOOP // Exit restaurant browsing
        ELSE
            DISPLAY "Invalid action."
        END IF
    END LOOP
END FUNCTION

FUNCTION Function_ViewRestaurantMenu(restaurantID, cart)
    DISPLAY Restaurant Details (Name, Address, Rating)
    DISPLAY Menu Categories
    LOOP
        DISPLAY Menu Items for restaurantID (Name, Description, Price)
        GET UserAction (options: "Add Item to Cart", "View Cart", "Checkout", "Back to Restaurants")

        IF UserAction IS "Add Item to Cart" THEN
            SET SelectedItemID = GET ItemID_From_User_Selection
            SET Quantity = GET Quantity_From_User
            ADD SelectedItemID WITH Quantity TO cart
            DISPLAY "Item added to cart."
        ELSE IF UserAction IS "View Cart" THEN
            CALL Function_ViewCart(cart)
        ELSE IF UserAction IS "Checkout" THEN
            IF cart IS NOT EMPTY THEN
                CALL Function_Checkout(cart, restaurantID)
                IF Checkout WAS SUCCESSFUL THEN
                    CLEAR cart // Cart is now processed
                    BREAK LOOP // Exit menu and potentially back to main dashboard
                END IF
            ELSE
                DISPLAY "Your cart is empty. Please add items before checking out."
            END IF
        ELSE IF UserAction IS "Back to Restaurants" THEN
            BREAK LOOP // Return to browse restaurants list
        ELSE
            DISPLAY "Invalid action."
        END IF
    END LOOP
END FUNCTION

FUNCTION Function_ViewCart(cart)
    DISPLAY Current Items in Cart (Item Name, Quantity, Price, Subtotal for each)
    DISPLAY Total_Cart_Amount
    GET UserAction (options: "Update Quantity", "Remove Item", "Proceed to Checkout", "Back to Menu")

    IF UserAction IS "Update Quantity" THEN
        SET ItemID = GET ItemID_To_Update
        SET NewQuantity = GET New_Quantity
        UPDATE Quantity OF ItemID IN cart TO NewQuantity
        DISPLAY "Cart updated."
    ELSE IF UserAction IS "Remove Item" THEN
        SET ItemID = GET ItemID_To_Remove
        REMOVE ItemID FROM cart
        DISPLAY "Item removed."
    ELSE IF UserAction IS "Proceed to Checkout" THEN
        // This will typically happen from the menu itself, but allows direct checkout from cart view.
        // The calling function (Function_ViewRestaurantMenu) would handle the actual checkout call.
        DISPLAY "Returning to menu to complete checkout."
    ELSE IF UserAction IS "Back to Menu" THEN
        // Do nothing, just return
    END IF
END FUNCTION

FUNCTION Function_Checkout(cart, restaurantID)
    DISPLAY Order Summary (Items, Subtotal, Delivery Fee, Taxes, Total Amount)
    GET UserDeliveryAddress (from saved addresses or new input)
    GET UserPaymentMethod (options: "Credit Card", "Digital Wallet", "Cash on Delivery")

    IF UserDeliveryAddress IS VALID AND UserPaymentMethod IS SELECTED THEN
        IF UserPaymentMethod IS NOT "Cash on Delivery" THEN
            CALL Function_ProcessPayment(TotalAmount, UserPaymentMethod, CurrentUser.ID)
            IF Payment IS Successful THEN
                CALL Function_PlaceOrder(cart, restaurantID, UserDeliveryAddress, PaymentDetails, CurrentUser.ID)
                RETURN TRUE // Checkout successful
            ELSE
                DISPLAY "Payment failed. Please try a different method or try again."
                RETURN FALSE
            END IF
        ELSE // Cash on Delivery
            CALL Function_PlaceOrder(cart, restaurantID, UserDeliveryAddress, "Cash On Delivery", CurrentUser.ID)
            RETURN TRUE // Checkout successful
        END IF
    ELSE
        DISPLAY "Please provide a valid delivery address and select a payment method."
        RETURN FALSE
    END IF
END FUNCTION

FUNCTION Function_ProcessPayment(amount, method, userID)
    DISPLAY Payment Gateway Interface for 'method'
    GET PaymentDetails_From_User (e.g., Card Number, Expiry, CVV)
    SEND Payment_Request_To_PaymentGateway(amount, method, PaymentDetails_From_User, userID)
    GET PaymentGateway_Response
    IF PaymentGateway_Response IS "Success" THEN
        DISPLAY "Payment successful."
        RETURN TRUE
    ELSE
        DISPLAY "Payment failed: " + PaymentGateway_Response.ErrorMessage
        RETURN FALSE
    END IF
END FUNCTION

FUNCTION Function_PlaceOrder(cart, restaurantID, address, paymentDetails, userID)
    SET NewOrderID = GENERATE_UNIQUE_ORDER_ID()
    SAVE OrderDetails_To_Database(NewOrderID, userID, restaurantID, cart, address, paymentDetails, "Pending")
    SEND Notification_To_Restaurant_For_NewOrder(NewOrderID)
    DISPLAY "Order placed successfully! Tracking your delivery..."
    CALL Function_TrackDelivery(NewOrderID) // Immediately start tracking
    RETURN NewOrderID
END FUNCTION

FUNCTION Function_TrackDelivery(orderID)
    LOOP WHILE TRUE
        GET CurrentOrderStatus_From_Database(orderID)
        DISPLAY "Order Status: " + CurrentOrderStatus_From_Database
        
        IF CurrentOrderStatus_From_Database IS "Restaurant Preparing" THEN
            DISPLAY "Restaurant is preparing your meal."
        ELSE IF CurrentOrderStatus_From_Database IS "Driver Assigned" THEN
            GET DriverLocation_From_Database(orderID)
            DISPLAY Map showing DriverLocation and your DeliveryAddress
            DISPLAY "Driver " + GET DriverName_From_Database(orderID) + " is on the way."
            DISPLAY "Estimated Delivery: " + GET EstimatedDeliveryTime_From_Database(orderID)
        ELSE IF CurrentOrderStatus_From_Database IS "Delivered" THEN
            DISPLAY "Your order has been delivered! Enjoy your food."
            PROMPT User_For_Rating_And_Review(orderID) // Optional
            BREAK LOOP // Exit tracking
        ELSE IF CurrentOrderStatus_From_Database IS "Cancelled" THEN
            DISPLAY "Your order has been cancelled."
            BREAK LOOP // Exit tracking
        END IF
        
        WAIT 30 SECONDS // Update status every 30 seconds
    END LOOP
END FUNCTION

FUNCTION Function_ViewOrderHistory(userID)
    DISPLAY List_Of_PastOrders_From_Database(userID) (showing summary: restaurant, total, status)
    GET UserAction (options: "View Order Details", "Back to Main Menu")

    IF UserAction IS "View Order Details" THEN
        SET SelectedOrderID = GET OrderID_From_User_Selection
        DISPLAY Detailed_Information_For_Order(SelectedOrderID)
        // Could also allow re-ordering or contacting support
    ELSE IF UserAction IS "Back to Main Menu" THEN
        // Do nothing, just return
    END IF
END FUNCTION

FUNCTION Function_ManageAccount(userID)
    DISPLAY Account Settings Options (e.g., "Edit Profile", "Change Password", "Manage Payment Methods", "Manage Addresses")
    GET UserAction

    IF UserAction IS "Edit Profile" THEN
        DISPLAY UserProfile_Form(userID)
        GET NewProfileData
        SAVE NewProfileData_To_Database(userID)
        DISPLAY "Profile updated."
    ELSE IF UserAction IS "Change Password" THEN
        DISPLAY ChangePassword_Form
        GET OldPassword, NewPassword
        IF Authenticate_OldPassword(userID, OldPassword) THEN
            UPDATE UserPassword_In_Database(userID, NewPassword)
            DISPLAY "Password updated."
        ELSE
            DISPLAY "Incorrect old password."
        END IF
    // ... other account management options
    END IF
END FUNCTION
```
```