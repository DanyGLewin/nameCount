class NicknameSets(object):
    def __init__(self, filename="names.csv"):
        name_file = open(filename, "r")
        self.nicknames = {}
        self.all_names = set()
        self.load_names(name_file)
        name_file.close()

    def load_names(self, name_file):
        """
        load all names and nicknames from the csv
        """
        for line in name_file.readlines():
            line_list = line.split(",")
            self.nicknames[line_list[0]] = set()
            for name in line_list:
                if "\n" in name:  # to remove the '\n' from the end of the last name in each line
                    name = name[:-1]
                self.nicknames[line_list[0]].add(name)
                self.all_names.add(name)

    def keys(self):
        """
        :return: all the names which are keys in the nickname dictionary
        """
        return self.nicknames.keys()

    def __getitem__(self, input_name):
        input_name = input_name.lower()
        if input_name not in self.all_names:
            return None
        else:
            return self.nicknames[input_name]

    def same(self, first_name, second_name):
        """
        :param first_name: first name to be compared
        :param second_name: second name to be compared
        :return: True if the names are identical, one is a nickname of the other, or one is a suspected typo
                (a typo is counted as likely if it's the same length as the intended name and has no more than
                 length/3 mistakes)
        """
        if first_name == second_name:
            return True
        if first_name in self.keys():
            if second_name in self[first_name]:
                return True
        if second_name in self.keys():
            if first_name in self[second_name]:
                return True
        if len(first_name) == 1 or len(second_name) == 1:
            if first_name[0] == second_name[0]:
                return True
        if len(first_name) == len(second_name):
            if self.hamming(first_name, second_name) <= len(first_name) / 3:
                return True
        return False

    def same_person(self, first_names, second_names):
        """
        :param first_names: list of names of the first person
        :param second_names: list of names of the first person
        :return: True if first_names and second_names are the same person, otherwise False
        """

        # simple case, if the strings are identical, must be the same person
        if first_names == second_names:
            return True

        # if they're of different lengths, make the first one be the shorter
        if len(first_names) > len(second_names):
            first_names, second_names = second_names, first_names

        if self.same(first_names[0], second_names[0]):
            first_middle_names = first_names[1:]
            second_middle_names = second_names[1:]
            names_to_check = len(first_middle_names)
            for first_middle in first_middle_names:
                for second_middle in second_middle_names:
                    if self.same(first_middle, second_middle) or self.same(second_middle, first_middle):
                        names_to_check -= 1
                        break

            if names_to_check == 0:
                return True
        return False

    def hamming(self, a, b):
        """
        :return: hamming distance between strings a and b
        """
        if len(a) != len(b):
            return -1
        return sum(a[i] != b[i] for i in range(len(a)))


def countUniqueNames(billFirstName, billLastName,
                     shipFirstName, shipLastName, billNameOnCard):
    """
    :param billFirstName: first name (counting middle names) of the billed
    :param billLastName: last name of the billed
    :param shipFirstName: first name (counting middle names) on the shipping
    :param shipLastName: last name on the shipping
    :param billNameOnCard: full name as it appears on the billed card
    :return: number of unique people involved in the transaction
    """
    # split the input to lists of first and midle names
    # and turn everything to lower case for comfort
    bill_names = billFirstName.lower().split()
    ship_names = shipFirstName.lower().split()
    card_names = billNameOnCard.lower().split()
    billLastName = billLastName.lower()
    shipLastName = shipLastName.lower()

    # initialize a nickname dictionary
    nicknames = NicknameSets()

    # the maximum number of people for a single transaction
    people = 3

    # if the surnames are different, they can't be the same person
    if nicknames.same(billLastName, shipLastName):
        if nicknames.same_person(bill_names, ship_names):
            people -= 1

    # the surname is either the first or last name on the card
    # check if billing name == name on card
    if nicknames.same(billLastName, card_names[0]):
        if nicknames.same_person(bill_names, card_names[1:]):
            people -= 1
    elif nicknames.same(billLastName, card_names[-1]):
        if nicknames.same_person(bill_names, card_names[:-1]):
            people -= 1

    # if billing name == shipping name AND billing name == name on card,
    # then shipping name == name on card
    if people > 1:
        # check if shipping name = name on card
        if nicknames.same(shipLastName, card_names[0]):
            if nicknames.same_person(ship_names, card_names[1:]):
                people -= 1
        elif nicknames.same(shipLastName, card_names[-1]):
            if nicknames.same_person(ship_names, card_names[:-1]):
                people -= 1

    return people


def test():
    print countUniqueNames("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli")
    print countUniqueNames("Deborah", "Egli", "Debbie ", "Egli", "Deborah Egli")
    print countUniqueNames("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli")
    print countUniqueNames("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah")
    print countUniqueNames("Michelle", "Egli", "Deborah", "Egli", "Deborah Egli")


def main():
    test()


#if __name__ == "__main__":
#    main()