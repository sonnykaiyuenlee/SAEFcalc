import csv
import os

def create_schedule_table(input_file_name, output_file_name):
    """
    function that creates a .csv schedule table from a .txt file created
    from copying and pasting from the schedule itself in .pdf form

    Inputs:
        input_file_name: a string of the input file (note: don't include .txt)
        output_file_name: a string of the output file user wants to create 
        (note: don't include .csv)

    Returns:
        Nothing    
    """
    input_file_name = input_file_name + ".txt"
    output_file_name = output_file_name + ".csv"

    
    fields = ['"combined adjusted net income"', '"one"', '"two"', '"three"', '"four"', '"five"', '"six_plus"']
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
                        if len(new_row) < 7:
                            new_row.append(val)
                        if len(new_row) == 7:
                            new_row = [float(num) for num in new_row]            
                            csvwriter.writerow(new_row)
                            new_row = []
    except OSError:
        os.remove(output_file_name)
        return -1                        

def schedule_finder(schedule_table, comb_adj_income, num_child):
    """
    function to return the corresponding schedule according to 
    combined adjusted net income and number of children

    Inputs:
        schedule_table: string name of the schedule table
        comb_adj_income: combined monthly adjusted net income
        num_child: number of children

    Returns:
        schedule amount    
    """
    schedule_table = schedule_table + '.csv'
    schedule_amount = 0

    comb_adj_income = float(comb_adj_income)
    if num_child > 6:
        num_child = 6
    try:    
        with open(schedule_table) as csvfile:
            sched_reader = csv.reader(csvfile, quoting = csv.QUOTE_NONNUMERIC)
            #this will skip the header row
            header = next(sched_reader)
            #special attention to the first row because 
            #its range of combined adjusted net income
            #is 0-824.99 rather than num + 49.99
            row_counter = 1
            for row in sched_reader:
                #row[0] = float(row[0])
                if row_counter == 1:
                    if comb_adj_income >= 0.00 and comb_adj_income <= 824.99:
                        row_counter += 1
                        schedule_amount = int(row[num_child])
                        return schedule_amount
                if comb_adj_income >= row[0] and comb_adj_income <= row[0] + 49.99:
                    schedule_amount = int(row[num_child])
                    return schedule_amount
                row_counter += 1    

            if schedule_amount == 0:
                return -1
    except OSError:
        return -1            
