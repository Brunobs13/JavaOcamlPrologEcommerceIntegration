### Languages and Computation - Computer Engineering Bachelor's Project

**Author:** Bruno Ricardo de Sá Ferreira  

This project consists of codes divided into 7 Java files and one OCaml file. 

## Compilation and Execution

To compile the OCaml file, use the following command: 

ocamlc -o main str.cma main.ml ./main

To compile and execute the Java code, use the following commands:

javac Main.java java Main


Make sure all documents are in the same directory.

## Project Description

The project was developed in stages, starting with the main function provided by the professor, which served as a base for the implementation of the required functionalities. During the process, adjustments were made in the way of reading the data from the database to ensure compatibility, without compromising the program's logic.

### Calculation Functions (OCaml)

1. `calculate_total_price`: Calculates the total price of the items in the cart without discounts.
2. `calculate_category_discounts`: Calculates the category discounts for the items in the cart.
3. `calculate_loyalty_discount`: Calculates the loyalty discount based on the customer's years of loyalty.
4. `calculate_shipping_cost`: Gets the shipping cost based on the delivery district.
5. `calculate_final_price`: Calculates the final price of the cart after applying all discounts and adding the shipping cost.

### Display Functions

1. `display_cart`: Displays the cart items with their respective categories, quantities, and prices.

### Main Function

Coordinates the execution of the program, performs the reading of the `store.pl` file and the parsing of the information.
Displays the category discounts, available items, loyalty discounts, and shipping costs. Calculates the total price of the cart, category discounts, loyalty discount, shipping cost, and final price of the cart.
Displays the results of the calculations and the cart items.

## Detailed Report of the OperacoesCarrinho Class (Java)

1. Introduction:
   - Responsible for coordinating operations related to the shopping cart, such as price calculations, discounts, and shipping costs, and using subprocesses to execute OCaml code, keeping the program simple and avoiding repetition of logic, this is considered the most important and challenging function of the project.
2. OCaml Execution Methods:
   - Has a private method `executarOCaml` to execute OCaml commands and return the output as a list of strings. This method uses subprocesses to compile and execute the OCaml code.
   - Each calculation method calls `executarOCaml` with the appropriate parameters and interprets the output to obtain the desired results.
3. Price and Discount Calculations:
   - The function responsible for passing the calculation logic implemented in Ocaml. This is not responsible for complex calculations but rather for making the "transition" from one code to another.
4. Final Price Calculation:
   - `calcularPrecoFinal` combines the results of the previous calculations to determine the final price of the cart. It receives the values of the total price, category discount, loyalty discount, and shipping cost as parameters.
5. Shopping Cart Display:
   - `exibirCarrinho` displays the shopping cart using the corresponding OCaml code. Returns a string containing the formatted cart items.
6. Result Processing:
   - Each method that calls the OCaml code interprets the output to extract the desired results. For example, discount values are extracted from lines that start with the relevant information.
   - The output is processed line by line, allowing the results to be retrieved efficiently and accurately.

## Main.Java() Method

1. We create a new instance of the Store class to represent the store.
2. We create a new customer with some fictitious information, such as ID, city, district, and years of loyalty.
3. We add fictitious items to the customer's cart, using the Item class.
4. We add the customer to the store.
5. Calculations and Display:
   - We calculate the total price of the cart, the category discount, the loyalty discount, and the shipping cost using methods from the OperacoesCarrinho class.
   - Based on these calculations, we determine the final price of the cart.
   - We display the shopping cart, the loyalty discount, the shipping cost, the category discount, the total price without discounts, and the final price of the cart on the standard output.
6. Logical Decisions:
   - We use objects from the Cliente, Item, Store classes and methods from the OperacoesCarrinho class to modularize and organize the code.
   - We chose to use fictitious values for customers and items, making it easier to demonstrate the operation of the program.
   - We decided to calculate the final price of the cart considering category discounts, loyalty discount, and shipping cost, providing a more realistic simulation of the purchase process.
   - We use the OperacoesCarrinho class to capture complex calculations, keeping the main code more readable and organized.

After running the tests, we observed that the program produced consistent and accurate results.
1. Category Discounts:
   - The discounts for each category were correctly calculated and displayed, with values of 10%, 20%, 30%, 15%, and 25% for the categories "potions", "wands", "enchanted_books", "crystals", and "amulets" respectively.
2. Loyalty Discount:
   - The loyalty discounts were accurately applied, ranging from 5% to 25% based on the customer's years of loyalty.
3. Shipping Cost:
   - The shipping cost for each district was correctly calculated, with values of 5.00, 7.00, and 10.00 for the districts "Aveiro", "Lisboa", and "Porto", respectively.
4. Total Price without Discounts:
   - The total price of the cart without discounts was correctly calculated as 110.00.
5. Final Price of the Cart:
   - The final price of the cart, after applying all discounts and shipping cost, was calculated as 75.00.
6. Items in the Shopping Cart:
   - The items in the shopping cart were correctly displayed, with detailed information about each item, including category, quantity, and price.
These tests were performed with five different products, allowing to verify the accuracy of the calculations and the logic implemented in the program. In summary, the program was designed with the simplest possible logic, aiming to facilitate the understanding and maintenance of the code. However, when dealing with complex calculations and integration with OCaml code, subprocesses became an essential piece to successfully complete the project. These played a crucial role in the communication between the Java code and the OCaml code. They allowed the results generated by the OCaml code to be passed back to the Java code, enabling efficient integration of both parts of the system.
