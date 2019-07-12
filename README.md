# CC ANALYTICS

After thinking about how this mini project could be done effectively, I have created a class called SumpleCSV that has simple functionalities to process CSV files, its functionalities are inspired from SQL language.
construction method has three arguments: csv_file, delimiter and skip_header

## METHODS


### read method: 

Has two arguments that deal with the needed performances 
columns_to_include : sometimes we don't need to load and process all fields of a CSV file and "columns_to_include" argument helps on getting what we only need from the CSV file 
read_style: this argument could be 'line_by_line' or 'entire_file'
this  'line_by_line'  value helps to solve the issue of "out of memory error" in case the file is too big to be loaded into the memory (RAM) or just because loading the whole file doesn't help improving performances.
the 'entire_file' value, load the entire file into the memory and that could be helpful in case the content of the file will be used several times to achieve certain functionalities.

### indexing method

the indexing function plays a performance role in which it transforms a CSV file into a dictionary  with "column_to_index" as indexes and "column_to_index" as a list of content

### distinct_values method

it does the exact function as distinct() in sql, it returns a list of only distinct (different) values of the desired "column_to_distinct" argument


### csv_spliting_style method
since we are not allowed to import any library, I wrote a simple function that split a CSV record. it takes into consideration the used delimiter and ignores it inside double quotes.

### save_list_to_csv_file
a simple method that saves a list into a CSV file.

### group_counting method
this function group and count needed CSV records (columns_to_group_by argument) that meet the selection requirement (where arguement) 
it's the equivalent of the sql query as bellow
```
select "columns_to_group_by " count(*) 
from "csv_file" 
where 
group by " columns_to_group_by "
```

### Validate method

This function is used to validate CSV fields by just providing rules on what each field should be. 
the method returns an empty list in case all fields are correct or a list about founded errors  
An example of validation rules could be as follow:

```
validation_rules =  [
                        {'row_index':0, 'condition':'is_numeric'}, # product_id must be nemeric
                        {'row_index':1, 'condition':'length_greater_than', 'compare_to':1}, #product_name must be at least one char length
                        {'row_index':2, 'condition':'is_numeric'}, # aisle_id must be numeric
                        {'row_index':3, 'condition':'is_numeric'}, # department_id must be numeric
                    ]
```


## Used algorithm

### Step 1
load products ids with their departments ids  and index it by the product_id 
products_indexed_by_id  = simple_csv.indexing(columns_to_include=[0,3], column_to_index=0)
the data structure is a dictionary because this information is requested for each order product. 

### Step 2
read orders, group them by product_id and count them 
    orders_by_products_id   = simple_csv.group_counting(columns_to_group_by=[1])
	
### Step 3
read orders that meet the requirement to be as first order, group them by product_id and count them.
    first_orders_by_product_id   = simple_csv.group_counting(columns_to_group_by=[1,3], where={'column_index':1, 'column_value':0})

### Step 4
PROCESS DEPARTMENT STATS
```
for each orders_by_products_id
	get the department_id from the products_indexed_by_id dictionary
	process number of orders by department
	process number of first orders
```

### Step 5
sorting the result by department_id and saving it to a csv file
