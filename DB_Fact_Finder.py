"""This Module serves as a fast fact finder for the Inventory System"""


class DB_Fact_Finder(object):
    """"
    A class used to get fast facts and information from the database,
    to either be used logically, or to print to the user

    """

    def __init__(self, management):
        """

        The equivalent of the constructor for the DB_Fact_Finder class

        Parameters
        ----------
        management
            an instance of the database, given to the class by the User_Interaction class


        Instances of object in DB_Fact_Finder class:
        --------------------------------------------
        self.management:
            an instance of the database, given to the class by the User_Interaction class

            allows methods to be called from the DataBase_Management module

        self.item_found:
            creates a instance to be used whether an
            item is found already within the database or not

            automatically set to None, not equal to anything til needed and used

        """
        self.management = management
        self.item_found = None

    def does_itemnum_exist(self, item_num: int) -> None:
        """
        A method that checks if a item exists within the database, based upon item #

        sets self.item_found as true or false depending on whether the item is found or not

        Parameters
        ----------

        item_num
            the item# of the item being check if in self.result

        """

        self.item_found = False
        for item in self.management.result:
            if item['Item #'] == item_num:
                self.item_found = True
                break

    def show_available(self) -> None:
        """
        A method that shows the available inventory to the user,
        iterating through each dictionary in self.result

        """
        sorted_list = sorted(self.management.result, key=lambda d: d["Item #"])
        for item in sorted_list:
            print(item)

    def get_item_found(self) -> list:
        """
        A method that serves as a getter for if the item was found

        Returns
        -------
            returns a true or false value that is set by does_itemnum_exist()

        """
        return self.item_found

    def return_item_num(self, item_num: int) -> str:
        """
        A method that serves to return the item number of a specific item

        Does so by finding the specific dictionary in the
        list with the desired value of the Item # key

        Parameter:
        ----------

        item_num
            the specific item number desired

        Returns:
        --------

        the specific items item #, in the form of a string

        """
        item_desired = next(item for item in self.management.result if item['Item #'] == item_num)
        return str(item_desired["Item # "])

    def return_price(self, item_num: int) -> float:
        """
        A method that serves to return the price of a specific item

        Does so by finding the specific dictionary
        in the list with the
        desired value of the Item # key

        Parameter:
        ----------

        item_num
            the specific item number desired

        Returns:
        --------

        the specific items price, in the form of a float

        """

        item_desired = next(item for item in self.management.result if item['Item #'] == item_num)
        return float(item_desired["Price "])

    def return_name(self, item_num: int) -> str:
        """
        A method that serves to return the name of a specific item

        Does so by finding the specific dictionary in the
        list with the desired value of the Item # key

        Parameter:
        ----------

        item_num
            the specific item number desired

        Returns:
        --------

        the specific items name, in the form of a string

        """
        item_desired = next(item for item in self.management.result if item['Item #'] == item_num)
        return str(item_desired["Name"])

    def return_qnty(self, item_num: int) -> int:
        """
        A method that serves to return the quantity of a specific item

        Does so by finding the specific dictionary in the list
        with the desired value of the Item # key

        Parameter:
        ----------

        item_num
            the specific item number desired

        Returns:
        --------

        the specific items quantity, in the form of a int

        """

        item_desired = next(item for item in self.management.result if item['Item #'] == item_num)
        return int(item_desired["Quantity"])

    def check_if_qnty_available(self, amount_desired: int, item_number: int) -> bool:
        """
        Checks for the system if the amount requested to buy
        from a customer is actually available

        @param amount_desired:
            - the amount a customer wishes to buy

        @param item_number:
            - the item number one wishes to buy from

        @return:
            - A boolean value, True if requesting to buy less than
            what the system has, false if more.
        """
        amount_available = self.return_qnty(item_number)
        if amount_available < amount_desired:
            return False
        else:
            return True
