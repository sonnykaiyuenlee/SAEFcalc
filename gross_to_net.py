import csv
import os
def create_conversion_table(input_file_name, output_file_name):
    """
    function that creates a .csv conversion table from a .txt file create
    from copying and pasting from the conversion table itself in .pdf form
    
    Inputs:
        input_file_name: a string of the input file (note: don't include .txt)
        output_file_name: a string of the output file user wants to create 
        (note: don't include .csv)

    """
    input_file_name = input_file_name + ".txt"
    output_file_name = output_file_name + ".csv"

    
    fields = ['"monthly gross income"', '"one"', '"two"', '"three"', '"four"', '"five"', '"six_plus"', '"duty to support"']
    try:
        with open(output_file_name, 'w', newline = '') as out_file:
            csvwriter = csv.writer(out_file)
            csvwriter.writerow(fields)

            with open(input_file_name, 'r', encoding = 'utf-8-sig') as text_file:
                #input = text_file.read()
                #input = input.split()
                
                for line in text_file:
                    line = line.split()
                    new_row = []
                    for i,val in enumerate(line):
                        if val == '-':
                            continue
                        if i > 0:
                            if line[i - 1] == '-':
                                continue
                        if len(new_row) < 8:
                            new_row.append(val)
                        if len(new_row) == 8:
                            new_row = [float(num) for num in new_row]            
                            csvwriter.writerow(new_row)
                            new_row = []
    except OSError:
        os.remove(output_file_name)
        return -1                        

def convert(conversion_table, receive_parent_gross, support_parent_gross, num_child):
    """
    function that returns the combined net income of both parents
    according to gross to net income conversion table using 
    standardized tax amounts

    Inputs:
        gross_to_net_table: string name of the gross to net conversion table
        receive_parent_gross: receiving parent's gross monthly income
        support_parent_gross: supporting parent's gross monthly income
        num_child: number of children with recipient parent for whom
        support is being determined

    Returns:
        combined monthly net income of both parents    
    """
    conversion_table = conversion_table + '.csv'
    receive_parent_gross = float(receive_parent_gross)
    support_parent_gross = float(support_parent_gross)
    support_parent_index = 7
    #check if this assumption is correct for conversion, if 6+ children
    #treat as 6 children column?
    if num_child > 6:
        num_child = 6

    receive_parent_net = 0
    support_parent_net = 0
    try:
        with open(conversion_table) as csvfile:
            conversion_reader = csv.reader(csvfile, quoting = csv.QUOTE_NONNUMERIC)
            #this will skip the header row
            next(conversion_reader, None)
            #special attention to the first row because 
            #its range of combined adjusted net income
            #is 1-24.99 rather than num + 49.99    
            row_counter = 1
            for row in conversion_reader:
                if row_counter == 1:
                    if receive_parent_gross >= 1.00 and receive_parent_gross <= 24.99:
                        receive_parent_net = row[num_child]
                    if support_parent_gross >= 1.00 and support_parent_gross <= 24.99:
                        support_parent_net = row[support_parent_index]  
                if receive_parent_gross >= row[0] and receive_parent_gross <= row[0] + 49.99:
                        receive_parent_net = row[num_child]
                if support_parent_gross >= row[0] and support_parent_gross <= row[0] + 49.99:
                        support_parent_net = row[support_parent_index]  

            if receive_parent_net == 0 or support_parent_net == 0:
                return -1
            else:                       
                return int(receive_parent_net + support_parent_net)
    except OSError:
        return -1            