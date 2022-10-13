"""This module handles a what it takes to buy an object"""
import DB_Fact_Finder as ff


class BuyingInterface():
    """"
    A class used to serve as the buying calculations and interface,
    performing all of the work it takes to buy an item

    """

    def __init__(self, management):
        """

        The equivalent of the constructor for the Buying_Interface class

        Parameters
        ----------
        name: management
            an instance of the database, given to the class by the User_Interaction class


        Instances of object in Buying_Interface:
        --------------------------------------------
        self.management:
            an instance of the database, given to the class by the User_Interaction class

            allows methods to be called from the DataBase_Management module and class

        self.finder
            creates an instance of the DB_Fact_Finder class and module,
            which is passed an instance of the DataBase_Management class

            allows methods to be called from the DB_Fact_Finder module and class

        self.item_cart
            creates a list to store the dictionaries of the items the user decides to purchase

        self.specific_item_total
            creates a list to store the total prices of the user based upon item

            For example, if a user buys 3 hotdogs for 3.00$, 9 will be inputted into the list.

        """
        self.management = management
        self.finder = ff.DB_Fact_Finder(management)
        self.item_cart = []
        self.specific_item_total = []

    def buy_item(self, item_num: int, amount: int) -> None:
        """
        A method designed to buy an item from the database, handling everything that should do.

        Searches for the item, finds it, changes the quantity of said item,
        and adds the specifications of the purchase to the two lists

        Parameter:

        item_num
            the specific item number of the item one wishes to purchase

        amount
            the amount of that item one would like to purchase

        """
        item_desired = next(item for item in self.management.result if item['Item #'] == item_num)
        self.management.change_quantity_buying(amount, item_num)
        copy_of_dict = item_desired.copy()
        copy_of_dict["Quantity"] = amount
        self.item_cart.append(copy_of_dict)
        self.specific_item_total.append(self.finder.return_price(item_num) * amount)

    def finish_and_purchase_cart(self) -> None:
        """
        A method designed to finish the purchase, and act as a receipt almost

        Combines the two lists of the class into a list of dictionaries,
        with Total for each item being added, and prints each dictionary to the user
        in a receipt esque way.

        """

        output = [{**dct, 'Total': total} for dct, total in zip(self.item_cart, self.specific_item_total)]
        for item in output:
            print(item)

    def get_cart_total(self) -> float:
        """
        A method designed to get the of every item in the cart,
        based upon quantity and price of each item

        iterates through the specific_item_total list,
        and adds each element (which is a price),
        to get the total purchase amount

        Returns:
        --------

        total
            the total purchase amount

        """
        total = 0
        for price in range(0, len(self.specific_item_total)):
            total = total + self.specific_item_total[price]
        return total

    def clear_lists(self) -> None:
        """
        A method desgined to clear the self.item_cart list and the self.specific_item_total list

        A problem arose that if a user did a checkout,
        and then went back to the main loop (ask_options in User_Interaction)
        and tried to purchase more items, the last cart would still show.

        Clears these lists, so this doesn't happen.

        """

        self.item_cart.clear()
        self.specific_item_total.clear()

    def view_cart(self) -> None:
        """
        A method designed to iterate through the list of dictionaries
        in self.item_cart and print each dictionary on a line.

        """

        for item in self.item_cart:
            print(item)
