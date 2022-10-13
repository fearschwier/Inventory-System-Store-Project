"""This module deals with Interacting with the User, and contains the main method to run the program."""
import DataBase_Management as db
import DB_Fact_Finder as ff
import Buying_Interface as bi


class UserInteraction:
    """"
    **Contains the main method in this module**

    A class designed around communication and interacting
     with the user through varius inputs and prints

    If the terminal has a input, or prints something to the user, it likely originates from here

    Contains a infinite main loop ask_options started by the main method,
    which is the backbone for the program

    """

    def __init__(self, name: str):
        """

        The equivalent of the constructor for the User_Interaction class

        Parameters
        ----------
        name
            the name of the user


        Instances of object in User_Interaction:
        --------------------------------------------
        self.name:
            the name of the user

        self.database:
            instiates a instance of the DataBase_Management class,
            which can be used to access methods from this class

        self.database.make_dict_items()
            makes sure the items are made and present before the user can interact with them

        self.finder
            instiates a instance of the DB_Fact_Finder class,
            and passes it an instance of the database.
            This can also be used to access methods from this class


        self.buying
            institates a instance of the BuyingInterface class,
            which can also be used to access methods from this class


        """
        self.name = name
        self.database = db.DataBase_Management()
        self.database.make_dict_items()
        self.finder = ff.DB_Fact_Finder(self.database)
        self.buying = bi.BuyingInterface(self.database)

    def ask() -> str:
        """
        A method that asks the user their name, to be stored for later.

        Return:

        name
            the name given by the user

        """
        while True:
            name = input("What is your name?\n")
            if name == "":
                print("Ha! You have to enter a name!")
            else:
                print("Welcome to the Shepherdstown Bake Shop " + name)
                return name

    def ask_options(self):
        """
        A method that presents the user with various options of actions they can do,
        the backbone of the program

        A infinite loop, as referenced by the main method

        Handles points to methods based upon user input and direction

        """
        while True:
            option = input(
                '''What would you like to do? \n1. Add a Item: \n2. Delete a Item:\n3. Edit an Item: \n4. View Inventory \n5. Shop (Enter Customer Mode) \n6. End Program\n''')
            if option == '1':
                print("Welcome to the adding process " + self.name)
                self.add_item_interaction()
                break
            if option == '2':
                print("Welcome to the item deletion process " + self.name)
                self.delete_item_interaction()
                break
            if option == "3":
                self.edit_item_interaction()
                break
            if option == "4":
                print("Here is the following inventory we have " + self.name)
                self.finder.show_available()
                break
            if option == "5":
                self.buy_item_interaction()
                break
            if option == "6":
                self.end_program()
            else:
                print("You have to enter a valid option " + self.name)

    def end_program(self) -> None:
        """
        A method that asks quits the program

        """
        quit()

    def return_to_start(self) -> None:
        """
        A method that returns back to the ask_options method, to stay in the infinite loop

        """
        self.ask_options()

    def enter_data(self, message: str, typ: type):
        """
        A method that serves as an exception for most if not every input in the program.

        Parameters:
        -----------

        message:
            the message one would like to show the user, in the form of an input

        typ:
            the type one is expecting and wants from the user

        Return
        ------
        v:
            the input of the typ and message

        """
        while True:
            try:
                v = typ(input(message))
                if (isinstance(v, int) or isinstance(v, float)) and v < 0:
                    raise ValueError
            except ValueError:
                print(f"Thats not an {typ}! or you have entered a negative!")
                continue
            else:
                break
        return v

    def add_item_interaction(self) -> None:
        """
        A method that deals with the interactions and processes of adding a new item to the database

        Points towards methods that do so after user input

        """
        while True:
            print("Here is the current inventory:")
            self.finder.show_available()
            add_item_num = self.enter_data("What is the new items #?\n", int)
            self.finder.does_itemnum_exist(add_item_num)
            itemnum_found = self.finder.get_item_found()
            if itemnum_found:
                print("There is already a item with this item #!")
                continue
            else:
                add_item_price = self.enter_data("What is the new items price?\n", float)
                add_item_quant = self.enter_data("What is the new items quantity?\n", int)
                while True:
                    add_name = self.enter_data("What is the new items name?\n", str)
                    if add_name == "":
                        print("Ha! You have to enter a name!")
                        continue
                    break
            self.database.add_item(add_item_num, add_item_price, add_item_quant, add_name)
            print("Item Added! Check Inventory Again to see!")
            break

    def delete_item_interaction(self) -> None:
        """
        A method that deals with the interactions of deleting an item, based upon user input

        """
        while True:
            self.finder.show_available()
            delete_item_number = self.enter_data("Please enter the item # of the item you would like to delete\n", int)
            self.finder.does_itemnum_exist(delete_item_number)
            itemnum_found = self.finder.get_item_found()
            if itemnum_found:
                self.database.delete_item(delete_item_number)
                print("Item Deleted! Check Inventory again for a refresh!")
                break
            else:
                print("No Item with that Item Number! Try Again!")
                continue

    def edit_item_interaction(self) -> None:
        """
        A method that deals with the interactions necessary to
        edit an already existing item in the database

        Edits 1 option at a time for each specific item

        """
        while True:
            print("Here is the current inventory:")
            self.finder.show_available()
            edit_specific_item = self.enter_data("Enter the item # of the item you would like to edit\n", int)
            self.finder.does_itemnum_exist(edit_specific_item)
            itemnum_found = self.finder.get_item_found()
            if itemnum_found:
                print("Item Found!")
                options = self.enter_data(
                    '''What would characteristic would you like to change?? \n1. Price \n2. Quantity \n3. Name\n''',
                    str)
                if options == '1':
                    price = self.enter_data("What is the new price?\n", float)
                    self.database.change_price(price, edit_specific_item)
                    print("Price Changed!")
                    break
                if options == '2':
                    quantity = self.enter_data("What is the new quantity?\n", int)
                    self.database.change_quantity_specific(quantity, edit_specific_item)
                    print("Quantity Changed!")
                    break
                if options == '3':
                    while True:
                        name = self.enter_data("What is the new name?\n", str)
                        if name == '':
                            print("Ha! You have to enter a name!")
                            continue
                        self.database.change_name(name, edit_specific_item)
                        print("Name Changed!")
                        break
                    break
                else:
                    print("You must enter a valid option!")
                    continue
            else:
                print("No item with that item number! try again!")
                continue

    def get_payment_info_interaction(self) -> str:
        """
        A comical method that asks the user their name, to be stored for later.

        Will not accept if not a int, and not 16 digits in length (no spaces)

        """
        while True:
            payment_info = self.enter_data("Please enter your credit 16 digit card number before we begin, no spaces...\n", int)
            is_length_16 = len(str(payment_info))
            if is_length_16 == 16:
                print("Card Accepted!")
                break
            else:
                print("You card is not 16 digits in length! Try Again!")
                print("Hint: 1234123412341234 is a valid number.....")
                continue
        return str(payment_info)

    def buy_item_interaction(self) -> None:
        """
        A method that deals with the interactions and loops it takes to buy items,
        and present the user continually with their varying options

        based upon user input, points towards methods that perform each options

        """
        self.get_payment_info_interaction()
        while True:
            print("Welcome to the Shepherdstown Bake Shop!")
            while True:
                print("Here are the current items we have available")
                self.finder.show_available()
                item_desired = self.enter_data("Please enter the item # of the item you would like to purchase!\n", int)
                self.finder.does_itemnum_exist(item_desired)
                itemnum_found = self.finder.get_item_found()

                if itemnum_found:
                    print("Item Found!")
                    while True:
                        amount_desired = self.enter_data("Please enter the amount " + self.finder.return_name(
                        item_desired) + "s" + " you would like to buy!\n", int)
                        amount_desired_str = str(amount_desired)
                        are_available = self.finder.check_if_qnty_available(amount_desired, item_desired)
                        if are_available:
                            self.buying.buy_item(item_desired, amount_desired)
                            total_price = str((amount_desired * self.finder.return_price(item_desired)))
                            print(amount_desired_str + ' ' + self.finder.return_name(
                            item_desired) + 's' + " for $" + total_price + " has been added to the cart")
                            break
                        else:
                            print("You are requesting more than we have..")
                            continue

                    while True:
                        option = self.enter_data(
                            '''What would you like to do? \n1. Buy another Item \n2. View Cart  \n3. Check out and Finish Shopping\n''',
                            int)

                        if option == int(1):
                            print("Lets go buy another item!")
                            break

                        if option == int(2):
                            print("Here is your cart!")
                            self.buying.view_cart()
                            continue

                        if option == int(3):
                            print("Checking out your cart " + self.name + " .....")
                            print("Here is your receipt!")
                            self.buying.finish_and_purchase_cart()
                            print("Your grand total for today in dollars is:")
                            print(self.buying.get_cart_total())
                            print("Thank you for shopping, have a great day!")
                            self.buying.clear_lists()
                            self.return_to_start()

                        else:
                            print("You must enter a valid option")
                            continue
                        break
                else:
                    print("*Sigh*... you cannot buy an item that doesn't exist! Back to the store you go!")
                    continue


if __name__ == "__main__":
    name = UserInteraction.ask()
    obj = UserInteraction(name)
    while True:
        obj.ask_options()
