# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 01:23:34 2019

@author: AZZ
"""
import sys
from datetime import datetime
startTime = datetime.now()


class SimpleValidator:
    def __init__(self):
        self.rules       = []
        
    def  validate(self, rule):    
        three_arguments = ['equal', 'greater_than', 'less_than', 'length_greater_than']
        #two_arguments   = ['is_numeri', 'is_email', 'is_string']
        
        if rule['condition'] in three_arguments:
            compare_to  = rule['compare_to']
            
        variable    = rule['variable']
        condition   = rule['condition']
        
        if(condition == 'is_numeric'):
            return str(variable).isnumeric()
        if(condition == 'length_greater_than'):
            return len(variable) > compare_to
        if(condition == 'equal'):
            return variable == compare_to
        if(condition == 'number_of_elements'):
            #print('wrong number of elements')
            return variable == len(compare_to)
        # TO EXTEND BY MORE VALIDATIONS
        
    def  add_rule(self, rule):
        self.rules.append(rule)

    def  clear_rules(self):
        self.rules.clear()
        
    def example_of_another_validation_function(self):
        return True
   


''' 
simple_validator = SimpleValidator()
simple_validator.add_rule({'variable':'A', 'condition':'equal',         'compare_to':'V' })
simple_validator.add_rule({'variable':'B', 'condition':'is_numeric' })
simple_validator.add_rule({'variable':'B', 'condition':'is_numeric' })
print(simple_validator.validate())
#'''

class SimpleCSV:
    def __init__(self, csv_file, delimiter=',', skip_header='yes'):
        #print("This is the constructor method.")
        self.csv_file       = csv_file
        self.delimiter      = delimiter
        self.skip_header    = skip_header
          
        
    def read(self, columns_to_include, read_style='line_by_line'):
            #fp = open(self.csv_file, "r")
            fp = open(self.csv_file, errors='ignore')
            if(self.skip_header == 'yes'):
                line = fp.readline().rstrip('\r\n')
            
            if(read_style == 'line_by_line'):
                for line in fp:
                    #[print(line.rstrip('\r\n').split(delimiter)[i]) for i in columns_to_include]
                    line = line.rstrip('\r\n')
                    row = self.csv_spliting_style(line, self.delimiter)
                    yield [row[i] for i in columns_to_include]
                fp.close()
            else:
                ret = []
                for line in fp:
                    line = line.rstrip('\r\n')
                    row = self.csv_spliting_style(line, self.delimiter)
                    ret.append([row[i] for i in columns_to_include])
                fp.close()
                return ret


    def validate(self, rules):
        #{'row_index':1, 'condition':'equal',         'value':'V' }
        simple_validator    = SimpleValidator()
        columns_to_validate = [rule['row_index'] for rule in rules]
        line_number         = 0;
        errors              = []
        
        #reading the file line by line
        for row in self.read(columns_to_validate, 'line_by_line'):
            line_number += 1
            # adding rules for each line of the csv, each line is validated separately
            for rule in rules:
                #prepare rules
                prepared_rule               = dict()
                prepared_rule['variable']   = row[rule['row_index']]
                prepared_rule['condition']  = rule['condition']
                if 'compare_to' in rule.keys(): 
                    prepared_rule['compare_to'] = rule['compare_to']
                #print(prepared_rule)
                #break
                if(not simple_validator.validate( prepared_rule )):
                    errors.append('validation error at line '+ str(line_number)+',  for '+str(prepared_rule['variable'])+' with rule '+str(rule['condition']))
        return errors
        
    
    def group_counting(self, columns_to_group_by, where=None, read_style='line_by_line'):
        dic = dict()
        for row in self.read(columns_to_group_by, read_style):
            values = [row[i] for i in range(len(columns_to_group_by))]
            index  = '_'.join([str(i) for i in values])
            
            if where != None and str(row[where['column_index']]) != str(where['column_value']):
                continue
            
            if index in dic:
                dic[index] += 1
            else:
                dic[index] = 1
            
        return dic

    
    def indexing(self,columns_to_include, column_to_index, read_style='line_by_line'):
        '''
        index a csv file by a specific column for a fast access,
        :param list columns_to_include: columns to include 
        :param int column_to_index: index of the column to index in columns_to_include 
        :param str read_style: reading style, can be 'line_by_line' to read the csv file line by line,
        or anything else to read thw whole file 
        '''
        dic = dict()
        for row in self.read(columns_to_include, read_style):
            dic[row[column_to_index]] = row
        return dic
       
        
    def distinct_values(self, column_to_distinct, read_style='line_by_line'):
        dic = dict()
        for rows in self.read([column_to_distinct], read_style):
            dic[rows[0]] = ''
        return [int(key) for key in dic.keys()]
        
    
    def csv_spliting_style(self, string, delimiter): 
        result_list = []
        index = 0
        start = 0
        while(index < len(string)):
            if(string[index] == '"'):
                index += 1
                while(index < len(string)) and (string[index] != '"'):
                    index += 1
            if index < len(string) and string[index] == delimiter:
                result_list.append(string[start:index])
                start = index + 1
            index += 1
        result_list.append(string[start:index + 1])
        return result_list

    def save_list_to_csv_file(self, list_to_save, delimiter=','):
        f = open(self.csv_file, "w")
        for row in list_to_save:
            str_to_write = ''
            for field in row:
                str_to_write += str(field)+delimiter
            str_to_write = str_to_write[:-1]
            str_to_write += "\n"
            f.write(str_to_write)
        f.close()
    
    









def main():
    print('start time => ',datetime.now())
    '''
    input_order_products_csv 	= '../input/order_products__train.csv' #sys.argv[1]
    input_products_csv 			= '../input/products_.csv' #sys.argv[2]
    output_report_csv 			= '../output/report.csv' #sys.argv[3]
    '''
    #'''   
    input_order_products_csv 	= sys.argv[1]
    input_products_csv 			= sys.argv[2]
    output_report_csv 			= sys.argv[3]
    #''' 

    
    
    simple_csv = SimpleCSV(csv_file=input_products_csv)
    '''
    #validate the "input_products_csv.csv" file
    validation_rules =  [
							{'row_index':0, 'condition':'is_numeric'},                          # product_id must be nemeric
							{'row_index':1, 'condition':'length_greater_than', 'compare_to':1}, #product_name must be at least one char length
							{'row_index':2, 'condition':'is_numeric'},                          # aisle_id must be numeric
							{'row_index':3, 'condition':'is_numeric'},                          # department_id must be numeric
						]
    validation_errors_products = simple_csv.validate(validation_rules)
    #'''

    # load products ids with their departements ids  and index it by the product_id
    products_indexed_by_id  = simple_csv.indexing(columns_to_include=[0,3], column_to_index=0)
    print('products_indexed_by_id => ',datetime.now())

    simple_csv = SimpleCSV(csv_file=input_order_products_csv)

    '''
    #validate the "order_products__prior.csv" file
    validation_rules =  [
							{'row_index':0, 'condition':'is_numeric'}, # order_id must be nemeric
							{'row_index':1, 'condition':'is_numeric'}, #product_id must be at least one char length
							{'row_index':2, 'condition':'is_numeric'}, # add_to_cart_order must be numeric
							{'row_index':3, 'condition':'is_numeric'}, # reordered must be numeric
						]
    validation_errors_orders = simple_csv.validate(validation_rules)
    #'''

    # load orders and group them by product_id (1 is the index of product_id in the csv file)
    orders_by_products_id   = simple_csv.group_counting(columns_to_group_by=[1])
    print('orders_by_products_id => ',datetime.now())


    # load orders and group them by product_id (1 is the index of product_id in the csv file)
    first_orders_by_product_id   = simple_csv.group_counting(columns_to_group_by=[1,3], where={'column_index':1, 'column_value':0})
    print('first_orders_by_product_id => ',datetime.now())

    # distinct 
    #simple_csv      = SimpleCSV(csv_file='products.csv')
    #department_ids  = simple_csv.distinct_values(column_to_distinct=3)

    #--------------------------------#
    #   PROCESS DEPARTMENT STATS  
    #-------------------------------#
    departments_stats = dict()
    for product_id, orders_count in orders_by_products_id.items():
        department_id = products_indexed_by_id[str(product_id)][1] # the index 1 is for department_id
    		
        #process number of orders by department
        if department_id in departments_stats: 
            departments_stats[department_id][1] += orders_count
        else:
            departments_stats[department_id]     = [0, 0, 0, 0]
            departments_stats[department_id][0]  = department_id
            departments_stats[department_id][1]  = orders_count		
    
        #process number of first orders
        if str(product_id)+'_0' in first_orders_by_product_id:
            departments_stats[department_id][2] += 1 # the index 2 is for number of first orders
    
        #process percentage
    for department_id in departments_stats.keys():
        percentage = departments_stats[department_id][2] / departments_stats[department_id][1]
        departments_stats[department_id][3] = format(percentage, '.2f') # str(round(percentage,2)) 
    		
        #PROCESS sorting by department_id
    keys = sorted([int(key) for key in departments_stats.keys()])
    list_departments_stats = [['department_id', 'number_of_orders', 'number_of_first_orders', 'percentage']]
    for key in keys:
        list_departments_stats.append([departments_stats[str(key)][0], departments_stats[str(key)][1], departments_stats[str(key)][2], departments_stats[str(key)][3]])
    
    #saving it to a csv file 
    output = SimpleCSV(csv_file=output_report_csv)
    output.save_list_to_csv_file(list_departments_stats)

    print('departments_stats => ',datetime.now())
    print('Total execution time', datetime.now() - startTime)

if __name__== "__main__":
    main() 

