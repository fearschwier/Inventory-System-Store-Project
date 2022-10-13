"""This module deals with management the inventory database"""
import csv


class DataBase_Management(object):
    """
    A class designed to create the inventory,
    as well as manage it and changes any specifications of it,
    whether that be item #, price, quantity, or the
    name of the item
    """

    def __init__(self):
        """

        The equivalent of the constructor for the DataBase_Management class

        Instances of object in DataBase_Management:
        --------------------------------------------
        self.result
            a list which is used to store the inventory, in a list of dictionaries.
            Represents the inventory in the program

        """
        self.result = []

    def make_dict_items(self):
        """
        A method designed to pull the rows, columns, and headers from a csv document, and add them to self.
        Result to be able to be messed with
        in the form of a list of dictionaries

        """
        with open("Items2.csv") as fp:
            reader = csv.reader(fp)
            labels = next(reader, None)
            self.result = []
            for row in reader:
                if row:
                    row[0] = int(row[0])
                    row[1] = float(row[1])
                    row[2] = int(row[2])
                    pairs = zip(labels, row)
                    self.result.append(dict(pairs))
            fp.close()

    def get_list_dicts(self) -> list:
        """
        A method designed to be a getter to return the list of dictionaries stored by self.result

        Returns
        --------

        self.result
            the list of dictionaries which represents the inventory
        """
        return self.result

    def change_price(self, price: int, item_num: int) -> None:
        """
        A method designed to change the price of a specific item in self.result

        Parameters:
        -----------
        price
            the desired price to change the item to

        item_num
            the desired item number one would like to change

        """

        new = next(item for item in self.result if item['Item #'] == item_num)
        new["Price "] = float(price)
        self.update_csv()

    def change_name(self, name: str, item_num: int):
        """
        A method designed to change the name of a specific item in self.result

        Parameters:
        -----------
        name
            the desired name to change the item to

        item_num
            the desired item number one would like to change

        """
        new = next(item for item in self.result if item['Item #'] == item_num)
        new["Name"] = str(name)
        self.update_csv()

    def change_quantity_specific(self, quantity: int, item_num: int) -> None:
        """
        A method designed to change the quantity of a specific item in self.result

        Parameters:
        -----------
        name
            the desired quantity to change the item to

        item_num
            the desired item number one would like to change

        """
        new = next(item for item in self.result if item['Item #'] == item_num)
        new["Quantity"] = int(quantity)
        self.update_csv()

    def change_quantity_buying(self, amount_buying: int, item_num: int) -> None:

        """
        A method designed to change the quantity of a specific item in self.result, when *BUYING*

        Parameters:
        -----------
        amount_buying
            the desired quantity one would like to buy

        item_num
            the desired item number one would like to buy

        """
        new = next(item for item in self.result if item['Item #'] == item_num)
        updated_quantity = new["Quantity"] - amount_buying
        new["Quantity"] = updated_quantity
        self.update_csv()

    def add_item(self, item_num, price, quant, name) :
        """
        A method designed to add an item to the inventory, represented by self.result

        Parameters:
        -----------
        item_num
            the desired item number of the new item

        price
            the desired price of the new item

        quant
            the desired quantity of the new item

        name
            the desired name of the new item

        """
        new_row = [int(item_num), float(price), int(quant), str(name)]
        with open("Items2.csv", "a+") as fp:
            reader = csv.reader(fp)
            fp.seek(0)
            labels = next(reader, None)
            fp.close()
            new_record = dict(zip(labels, new_row))
            self.result.append(new_record)
            self.update_csv()

    def delete_item(self, item_num: int) -> None:
        """
        a method designed to delete an item from the inventory, represented by self.result

        Parameters:
        -----------

        item_num
            the specific item number of the item one would like to delete

        """
        self.result[:] = [d for d in self.result if d.get("Item #") != int(item_num)]
        self.update_csv()

    def update_csv(self) -> None:
        """
        A method designed to update the csv document of any changes made to the inventory represented by self.result

        """
        sorted_list = sorted(self.result, key=lambda d: d["Item #"])
        keys = sorted_list[0].keys()
        with open("Items2.csv", 'w', newline='') as fp:
            dict_writer = csv.DictWriter(fp, keys)
            dict_writer.writeheader()
            dict_writer.writerows(sorted_list)
            fp.close()
