import glob


class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self):
        # the constructor initializes the name of the table as an empty string
        # Inintializes content as a dictionary and the number of rows as 0.
        self._name_of_table = ""
        self._content = dict()
        self._num_rows = 0

    def initialize(self, name_of_table, list_of_header, data):
        ''' name_of_table is the name of the table as in the database
        REQ:
        list_of_header is a list [0,...,n] containing all the column names
        in the same order as found in the csv file
        data is a list of all the lines coming from the file
        '''
        self._name_of_table = name_of_table
        self._content = self.create_columns(list_of_header)
        self._num_rows = self.add_values_dict(
            self._content, data, list_of_header)

    def get_headers(self):
        '''
        ()->list
        REQ:The table must have header names
        This method returns a list of the headers
        '''
        return list(self._content.keys())

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        self._content = new_dict
        self._num_rows = len(new_dict)

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}
        REQ:
        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        # get the content of a table
        return self._content

    def get_name(self):
        '''
        ()->str
        REQ:
        '''
        # get name of the table
        return self._name_of_table

    def num_rows(self, table):
        '''
        (table)->int
        REQ:table must be in the same directory
        This method gets the number of rows in a table
        '''
        # get the number of rows
        return self._num_rows

    def print_csv(self):
        '''
        () -> NoneType
        Print a representation of table in csv format.
        '''
        # no need to edit this one, but you may find it useful (you're welcome)
        dict_rep = self.get_dict()
        columns = list(dict_rep.keys())
        print(','.join(columns))
        rows = self._num_rows
        for i in range(rows):
            cur_column = []
            for column in columns:
                cur_column.append(dict_rep[column][i])
            print(','.join(cur_column))

    def create_columns(self, list_of_header):
        '''
        (IO.TextIOWrapper)-> int
        REQ: list_of_header must be non-empty
        This method returns how many column a table has.
        '''
        dict_table = dict()
        dict_table = {}
        # loop though all of the columns and create an empty list
        # for each of them
        for column in list_of_header:
            dict_table[column] = list()
        return dict_table

    def add_values_dict(self, table_dict, all_table_values, list_of_header):
        '''
        (dict, list, list) -> integer
        REQ:
        add all the data to the table. The data is a list of strings,
        each string has all the values for one row
        '''
        num_rows = 0
        # loop though every single line in the table
        # each line contains values separated with comma and ends with \n
        # the line is split and added to the table object
        for line in all_table_values:
            line_striped = line.strip()
            length = len(line)
            if len(line.strip()) > 1:
                self.add_line_to_dict(table_dict, line, list_of_header)
                num_rows += 1
        return num_rows

    def add_line_to_dict(self, table_dict, line, list_of_header):
        '''
        (dict, str, str) -> NoneType
        REQ:
        add one value at the bottom of the new table
        '''

        line_list = line.split(",")
        index = 0
        # loop through all of the element of the list
        for element in line_list:
            element = element.strip()
            # set the key as the element of the list of headers
            key = list_of_header[index]
            # add element to the dictionary
            self.insert_element_to_dict(table_dict, element, key)
            index += 1

    def insert_element_to_dict(self, table_dict, element, key):
        '''
        (dict,str,str)->NoneType
        REQ:
        This function inserts an element to the dictionary
        '''
        # set the list of the values as the keys of the dictionary
        list_of_values = table_dict[key]
        list_of_values.append(element)

    def remove(
            self,
            where_equal_left_col,
            where_equal_right_col,
            where_greater_left_col,
            where_greater_right_col,
            where_smaller_left_col,
            where_smaller_right_col):
        '''
        (list, list, list, list, list, list) - > NoneType
        REQ:
        We remove all the rows from the table that doesn’t match the ‘where’
        in the query. 2 lists are for the ‘=’, 2 are for ‘>’ and 2 are for ‘<’.
        '''
        #
        new_table_dic = self.create_columns(self.get_headers())
        new_row_count = 0
        # loop through all of the rows in table
        for row_index in range(self._num_rows):
            row_dict = self.create_dic_for_row(row_index)
            #
            if self.row_is_good(
                    row_dict,
                    where_equal_left_col,
                    where_equal_right_col,
                    where_greater_left_col,
                    where_greater_right_col,
                    where_smaller_left_col,
                    where_smaller_right_col):
                self.append_row_dic_to_new_table_dic(new_table_dic, row_dict)
                # increment row index
                new_row_count += 1
        self._content = new_table_dic
        self._num_rows = new_row_count

    def create_dic_for_row(self, row_num):
        '''
        (integer) ->dict
        REQ:
        we get all the values for a single row from the table and return
        them in a dict. The key in the dict is the name of the column
        and the value associated comes from the table.
        '''
        result = dict()
        result = {}
        # loop through all of the column in table
        for column in self._content.keys():
            # create list of value  for eah of the column in the table
            list_of_values = self._content[column]
            result[column] = list_of_values[row_num]
        return result

    def row_is_good(
            self,
            row_dict,
            where_equal_left_col,
            where_equal_right_col,
            where_greater_left_col,
            where_greater_right_col,
            where_smaller_left_col,
            where_smaller_right_col):
        '''
        (dic, list, list, list, list, list, list) -> bool
        REQ:
        We test if the row is accepted by the ‘where’ in the query

        '''
        equal_index = 0
        greater_index = 0
        smaller_index = 0
        result = True
        # loop though equal sign
        for equal_index in range(len(where_equal_left_col)):
            left_value = row_dict[where_equal_left_col[equal_index]]
            right_value = self.get_real_value(
                where_equal_right_col[equal_index], row_dict)
            result &= (left_value == right_value)
        # loop though greater sign
        for greater_index in range(len(where_greater_left_col)):
            left_value = row_dict[where_greater_left_col[greater_index]]
            right_value = self.get_real_value(
                where_greater_right_col[greater_index], row_dict)
            result &= (left_value > right_value)
        # loop though smaller sign
        for smaller_index in range(len(where_smaller_left_col)):
            left_value = row_dict[where_smaller_left_col[smaller_index]]
            right_value = self.get_real_value(
                where_smaller_right_col[smaller_index], row_dict)
            result &= (left_value < right_value)
        return result

    def get_real_value(self, right_para, row_dict):
        '''
        (str, dict)->str
        REQ: right_para must either be a string or be a list
        This method returns unquoted value or dictionary value
        '''
        result = ""
        if right_para.count("\"") > 0:
            result = right_para.strip("\"")
        else:
            result = row_dict[right_para]
        return result

    def append_row_dic_to_new_table_dic(self, new_table_dic, row_dic):
        '''
        (dic , dic) -> NoneType
        REQ:
        row_dic contains all the values for a row of data. Each key
        is the name of a column. The function will add the new row
        at the bottom of the new table
        '''
        # loop though all of the column in the table
        for column in self._content.keys():
            # add row to list of values
            value_to_insert = row_dic[column]
            list_of_values = new_table_dic[column]
            list_of_values.append(value_to_insert)

    def get_single_value(self, header, row_index):
        '''
        (str, integer) -> str
        REQ:
        access to a single value by the name of the column and the row index
        '''
        value = self._content[header][row_index]
        return value


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self):
        self._database_dict = dict()
        self._database_dict = {}

    def add_table(self, table_name, table):
        ''' (str, Table) ->NoneType
        Will just add this table to the dict.
        '''
        self._database_dict[table_name] = table

    def print_csv(self):
        '''
        ()->NoneType
        REQ: table must be in the database
        this ethod prints the database
        '''
        print(self._database_dict.keys())
        # loop through all of the table name
        for table_name in self._database_dict:
            # get the table from the databse dictionary
            table = self._database_dict[table_name]
            print(table)
            print(table_name)
            table.print_csv()

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self._database_dict = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._database_dict

    def get_table_object(self, table_name):
        '''
        (str) -> Table
        REQ: table_name must be valid
        This method gets a table based on the table name
        '''
        return self._database_dict[table_name]
Database_file
