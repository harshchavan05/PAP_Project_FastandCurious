import random
import mysql.connector

class WasteManagementSystem:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="waste_management"
        )
        self.cursor = self.db_connection.cursor()
        self.create_subscriptions_table()
        self.create_payment_methods_table()
        self.accepted_waste_types = ["recyclables", "non-recyclables", "hazardous waste"]

    def create_subscriptions_table(self):
        # Check if 'subscriptions' table exists, create if not
        create_table_query = """
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INT PRIMARY KEY,
            resident_id INT,
            frequency VARCHAR(255)
        );
        """
        self.cursor.execute(create_table_query)
        self.db_connection.commit()

    def create_payment_methods_table(self):
        # Check if 'payment_methods' table exists, create if not
        create_table_query = """
        CREATE TABLE IF NOT EXISTS payment_methods (
            resident_id INT,
            payment_method VARCHAR(255),
            PRIMARY KEY (resident_id, payment_method)
        );
        """
        self.cursor.execute(create_table_query)
        self.db_connection.commit()

    def place_order(self):
        print("Stimulus: Resident requests waste collection services.")

        # Display numbered waste type options
        print("Waste Type Options:")
        for i, waste_type in enumerate(self.accepted_waste_types, start=1):
            print(f"{i}. {waste_type}")

        # Get user input for waste type
        waste_type_choice = int(input("Enter the number corresponding to the waste type: "))

        # Validate user input
        if 1 <= waste_type_choice <= len(self.accepted_waste_types):
            waste_type = self.accepted_waste_types[waste_type_choice - 1]

            quantity = input("Enter quantity or size of waste: ")
            collection_time = input("Enter preferred collection time: ")
            order_id = random.randint(1000, 9999)
            
            # Save order to database
            query = "INSERT INTO orders (order_id, resident_id, waste_type, quantity, collection_time, status) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (order_id, 123, waste_type, quantity, collection_time, "Pending")
            self.cursor.execute(query, values)
            self.db_connection.commit()

            print(f"Response: Order placed successfully. Order ID: {order_id}")
        else:
            print("Invalid waste type choice. Please enter a valid option.")

    def modify_order(self):
        print("Stimulus: Resident requests to modify a waste collection order.")
        order_id = int(input("Enter the order ID you want to modify: "))

        # Check if the order exists and is pending
        query = "SELECT * FROM orders WHERE order_id = %s AND status = 'Pending' AND resident_id = %s"
        values = (order_id, 123)
        self.cursor.execute(query, values)
        order = self.cursor.fetchone()

        if order:
            # Display numbered waste type options
            print("Waste Type Options:")
            for i, waste_type in enumerate(self.accepted_waste_types, start=1):
                print(f"{i}. {waste_type}")

            # Get user input for new waste type
            new_waste_type_choice = int(input("Enter the number corresponding to the new waste type: "))

            # Validate user input
            if 1 <= new_waste_type_choice <= len(self.accepted_waste_types):
                new_waste_type = self.accepted_waste_types[new_waste_type_choice - 1]
                new_quantity = input("Enter new quantity: ")
                new_collection_time = input("Enter new preferred collection time: ")

                # Update the order in the database
                update_query = "UPDATE orders SET waste_type = %s, quantity = %s, collection_time = %s WHERE order_id = %s"
                update_values = (new_waste_type, new_quantity, new_collection_time, order_id)
                self.cursor.execute(update_query, update_values)
                self.db_connection.commit()

                print("Response: Order modified successfully.")
            else:
                print("Invalid waste type choice. Order modification not allowed.")
        else:
            print("Response: Order modification not allowed.")

    def cancel_order(self):
        print("Stimulus: Resident requests to cancel a waste collection order.")

        # Fetch current orders
        self.view_orders()

        # Get user input for order ID to cancel
        order_id = int(input("Enter the order ID you want to cancel: "))

        # Check if the order exists and is pending
        query = "SELECT * FROM orders WHERE order_id = %s AND status = 'Pending' AND resident_id = %s"
        values = (order_id, 123)
        self.cursor.execute(query, values)
        order = self.cursor.fetchone()

        if order:
            # Update the order status to "Cancelled" in the database
            update_query = "UPDATE orders SET status = 'Cancelled' WHERE order_id = %s"
            update_values = (order_id,)
            self.cursor.execute(update_query, update_values)
            self.db_connection.commit()

            print("Response: Order cancelled successfully.")
        else:
            print("Response: Order cancellation not allowed.")

    def create_subscription(self):
        print("Stimulus: Resident creates a waste collection subscription.")

        # Display numbered frequency options
        print("Frequency Options:")
        frequency_options = ["weekly", "bi-weekly"]
        for i, frequency in enumerate(frequency_options, start=1):
            print(f"{i}. {frequency}")

        # Get user input for frequency
        frequency_choice = int(input("Enter the number corresponding to the preferred frequency: "))

        # Validate user input
        if 1 <= frequency_choice <= len(frequency_options):
            frequency = frequency_options[frequency_choice - 1]

            # Display payment method options
            print("Payment Method Options:")
            payment_method_options = ["online payments", "mobile wallets"]
            for i, payment_method in enumerate(payment_method_options, start=1):
                print(f"{i}. {payment_method}")

            # Get user input for payment method
            payment_method_choice = int(input("Enter the number corresponding to the preferred payment method: "))

            # Validate user input
            if 1 <= payment_method_choice <= len(payment_method_options):
                payment_method = payment_method_options[payment_method_choice - 1]

                # Check if the payment method already exists for the resident
                check_query = "SELECT * FROM payment_methods WHERE resident_id = %s AND payment_method = %s"
                check_values = (123, payment_method)
                self.cursor.execute(check_query, check_values)
                existing_payment_method = self.cursor.fetchone()

                if existing_payment_method:
                    print("Response: Payment method already registered for this resident.")
                else:
                    # Insert the subscription information into the database
                    subscription_id = random.randint(10000, 99999)
                    query = "INSERT INTO subscriptions (subscription_id, resident_id, frequency) VALUES (%s, %s, %s)"
                    values = (subscription_id, 123, frequency)
                    self.cursor.execute(query, values)
                    self.db_connection.commit()

                    # Insert the payment method information into the database
                    insert_query = "INSERT INTO payment_methods (resident_id, payment_method) VALUES (%s, %s)"
                    insert_values = (123, payment_method)
                    self.cursor.execute(insert_query, insert_values)
                    self.db_connection.commit()

                    print("Response: Subscription created successfully.")
                    print("Response: Payment method registered successfully.")
            else:
                print("Invalid payment method choice. Please enter a valid option.")
        else:
            print("Invalid frequency choice. Please enter a valid option.")

    def view_subscriptions(self):
        # Fetch subscriptions from the database based on resident_id
        query = "SELECT * FROM subscriptions WHERE resident_id = %s"
        values = (123,)
        self.cursor.execute(query, values)
        subscriptions = self.cursor.fetchall()

        print("Response: Active Subscriptions:")
        for i, sub in enumerate(subscriptions, start=1):
            print(f"{i}. Subscription ID: {sub[0]}, Frequency: {sub[2]}")

        # Fetch payment methods from the database based on resident_id
        query = "SELECT payment_method FROM payment_methods WHERE resident_id = %s"
        values = (123,)
        self.cursor.execute(query, values)
        payment_methods = self.cursor.fetchall()

        print("Registered Payment Methods:")
        for i, pm in enumerate(payment_methods, start=1):
            print(f"{i}. {pm[0]}")

    def modify_subscription(self):
        print("Stimulus: Resident requests to modify a waste collection subscription.")

        # Fetch current subscriptions
        self.view_subscriptions()

        # Get user input for subscription ID to modify
        subscription_id = int(input("Enter the subscription ID you want to modify: "))

        # Check if the subscription exists
        query = "SELECT * FROM subscriptions WHERE subscription_id = %s AND resident_id = %s"
        values = (subscription_id, 123)
        self.cursor.execute(query, values)
        subscription = self.cursor.fetchone()

        if subscription:
            # Display frequency options
            print("Frequency Options:")
            frequency_options = ["weekly", "bi-weekly"]
            for i, frequency in enumerate(frequency_options, start=1):
                print(f"{i}. {frequency}")

            # Get user input for new frequency
            new_frequency_choice = int(input("Enter the number corresponding to the new frequency: "))

            # Validate user input
            if 1 <= new_frequency_choice <= len(frequency_options):
                new_frequency = frequency_options[new_frequency_choice - 1]

                # Update the subscription in the database
                update_query = "UPDATE subscriptions SET frequency = %s WHERE subscription_id = %s"
                update_values = (new_frequency, subscription_id)
                self.cursor.execute(update_query, update_values)
                self.db_connection.commit()

                print("Response: Subscription modified successfully.")
            else:
                print("Invalid frequency choice. Subscription modification not allowed.")
        else:
            print("Response: Subscription not found or not allowed for modification.")


    def cancel_subscription(self):
        print("Stimulus: Resident requests to cancel a waste collection subscription.")

        # Fetch current subscriptions
        self.view_subscriptions()

        # Get user input for subscription ID to cancel
        subscription_id = int(input("Enter the subscription ID you want to cancel: "))

        # Check if the subscription exists
        query = "SELECT * FROM subscriptions WHERE subscription_id = %s AND resident_id = %s"
        values = (subscription_id, 123)
        self.cursor.execute(query, values)
        subscription = self.cursor.fetchone()

        if subscription:
            # Remove the subscription from the database
            delete_query = "DELETE FROM subscriptions WHERE subscription_id = %s"
            delete_values = (subscription_id,)
            self.cursor.execute(delete_query, delete_values)
            self.db_connection.commit()

            print("Response: Subscription cancelled successfully.")
        else:
            print("Response: Subscription cancellation not allowed.")

    def register_payment_method(self):
        print("Stimulus: Resident registers for waste payment options.")

        # Display payment method options
        print("Payment Method Options:")
        payment_method_options = ["online payments", "mobile wallets"]
        for i, payment_method in enumerate(payment_method_options, start=1):
            print(f"{i}. {payment_method}")

        # Get user input for payment method
        payment_method_choice = int(input("Enter the number corresponding to the payment method: "))

        # Validate user input
        if 1 <= payment_method_choice <= len(payment_method_options):
            payment_method = payment_method_options[payment_method_choice - 1]

            # Check if the payment method already exists for the resident
            check_query = "SELECT * FROM payment_methods WHERE resident_id = %s AND payment_method = %s"
            check_values = (123, payment_method)
            self.cursor.execute(check_query, check_values)
            existing_payment_method = self.cursor.fetchone()

            if existing_payment_method:
                print("Response: Payment method already registered for this resident.")
            else:
                # Insert the payment method information into the database
                insert_query = "INSERT INTO payment_methods (resident_id, payment_method) VALUES (%s, %s)"
                insert_values = (123, payment_method)
                self.cursor.execute(insert_query, insert_values)
                self.db_connection.commit()
                print("Response: Payment method registered successfully.")
        else:
            print("Invalid payment method choice. Please enter a valid option.")

    def view_payment_methods(self):
        # Fetch payment methods from the database based on resident_id
        query = "SELECT payment_method FROM payment_methods WHERE resident_id = %s"
        values = (123,)
        self.cursor.execute(query, values)
        payment_methods = self.cursor.fetchall()

        print("Response: Registered Payment Methods:")
        for pm in payment_methods:
            print(pm[0])

    def request_special_collection(self):
        print("Stimulus: Resident requests special waste collection services.")

        # Display special waste type options
        print("Special Waste Type Options:")
        special_waste_options = ["large items", "hazardous waste"]
        for i, waste_type in enumerate(special_waste_options, start=1):
            print(f"{i}. {waste_type}")

        # Get user input for special waste type
        waste_type_choice = int(input("Enter the number corresponding to the type of special waste: "))

        # Validate user input
        if 1 <= waste_type_choice <= len(special_waste_options):
            waste_type = special_waste_options[waste_type_choice - 1]
            quantity = input("Enter the quantity of special waste: ")
            request_id = random.randint(100000, 999999)
            request = {"request_id": request_id, "resident_id": 123, "waste_type": waste_type, "quantity": quantity, "status": "Pending"}
            self.special_requests.append(request)
            print(f"Response: Special waste collection request submitted. Request ID: {request_id}")
        else:
            print("Invalid special waste type choice. Please enter a valid option.")

    def approve_special_collection(self):
        request_id = int(input("Enter the request ID you want to approve: "))
        request = next((r for r in self.special_requests if r["request_id"] == request_id and r["status"] == "Pending"), None)
        if request:
            # Logic for approval
            request["status"] = "Approved"
            print(f"Response: Special waste collection request {request_id} approved.")
        else:
            print(f"Response: Special waste collection request {request_id} not found or already processed.")

    def confirm_special_collection(self):
        request_id = int(input("Enter the request ID you want to confirm: "))
        request = next((r for r in self.special_requests if r["request_id"] == request_id and r["status"] == "Approved"), None)
        if request:
            # Logic for confirmation
            date = input("Enter the scheduled date: ")
            time = input("Enter the scheduled time: ")
            print(f"Response: Special waste collection for request {request_id} scheduled on {date} at {time}.")
        else:
            print(f"Response: Special waste collection request {request_id} not approved or already confirmed.")

    def delete_from_waste_menu(self):
        print("Stimulus: Authorities delete certain waste types from the menu.")

        # Display waste type options
        print("Waste Type Options:")
        for i, waste_type in enumerate(self.accepted_waste_types, start=1):
            print(f"{i}. {waste_type}")

        # Get user input for waste type to delete
        waste_type_choice = int(input("Enter the number corresponding to the waste type to be deleted: "))

        # Validate user input
        if 1 <= waste_type_choice <= len(self.accepted_waste_types):
            waste_type_to_delete = self.accepted_waste_types[waste_type_choice - 1]
            self.accepted_waste_types.remove(waste_type_to_delete)
            print(f"Response: {waste_type_to_delete} removed from the waste menu.")
        else:
            print("Invalid waste type choice. Please enter a valid option.")

    def provide_education(self):
        print("Response: The system provides educational content on waste segregation and proper disposal practices.")

    def provide_feedback(self):
        print("Stimulus: Resident provides feedback on the waste collection service.")
        feedback_text = input("Enter your feedback: ")

        # Insert feedback into the 'feedback' table
        insert_query = "INSERT INTO feedback (resident_id, feedback_text) VALUES (%s, %s)"
        insert_values = (123, feedback_text)
        self.cursor.execute(insert_query, insert_values)
        self.db_connection.commit()

        print("Response: Thank you for your feedback. It has been recorded.")

    def view_feedback(self):
        # Fetch feedback from the 'feedback' table based on resident_id
        query = "SELECT feedback_text FROM feedback WHERE resident_id = %s"
        values = (123,)
        self.cursor.execute(query, values)
        feedback_entries = self.cursor.fetchall()

        print("Response: Resident Feedback:")
        for entry in feedback_entries:
            print(entry[0])

    def __del__(self):
        self.cursor.close()
        self.db_connection.close()


# Example Usage
waste_system = WasteManagementSystem()

while True:
    print("\nWaste Management System Menu:")
    print("1. Place Order")
    print("2. Modify Order")
    print("3. Cancel Order")
    print("4. Create Subscription")
    print("5. View Subscriptions (including Payment Methods)")
    print("6. Modify Subscription")
    print("7. Cancel Subscription")
    print("8. Request Special Collection")
    print("9. Approve Special Collection")
    print("10. Confirm Special Collection")
    print("11. Delete from Waste Menu")
    print("12. Provide Education")
    print("13. Provide Feedback")
    print("14. View Feedback")
    print("15. Exit")

    choice = int(input("Enter the number corresponding to your choice: "))

    if choice == 1:
        waste_system.place_order()
    elif choice == 2:
        waste_system.modify_order()
    elif choice == 3:
        waste_system.cancel_order()
    elif choice == 4:
        waste_system.create_subscription()
    elif choice == 5:
        waste_system.view_subscriptions()
    elif choice == 6:
        waste_system.modify_subscription()
    elif choice == 7:
        waste_system.cancel_subscription()
    elif choice == 8:
        waste_system.request_special_collection()
    elif choice == 9:
        waste_system.approve_special_collection()
    elif choice == 10:
        waste_system.confirm_special_collection()
    elif choice == 11:
        waste_system.delete_from_waste_menu()
    elif choice == 12:
        waste_system.provide_education()
    elif choice == 13:
        waste_system.provide_feedback()
    elif choice == 14:
        waste_system.view_feedback()
    elif choice == 15:
        print("Exiting Waste Management System. Goodbye!")
        del waste_system  # Explicitly delete the object to trigger __del__ method
        break
    else:
        print("Invalid choice. Please enter a valid option.")




