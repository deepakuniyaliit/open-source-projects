import os
import sqlparse
import sys
import csv

tablename_colname_dict = {}
possible_aggr_funcs = ["max", "min", "cou", "ave", "sum"]
all_col_names_list = []

def apply_groupby(groupby_aggr_col_index, groupby_proj_col_index, aggrs, groupby_col):
    groupby_dict = {}
    unique_proj = []
    final_output = []
    ans = []

    for i in range(len(all_data)):
        if all_data[i][groupby_col] not in unique_proj:
            val = all_data[i][groupby_col]
            unique_proj.append(all_data[i][groupby_col])
            if groupby_proj_col_index==-1:
                ans = []
            else:
                ans = [val]
            for j in range(len(groupby_aggr_col_index)):
                index = groupby_aggr_col_index[j]
                dummy = []
                
                for k in range(len(all_data)):
                    if  all_data[k][groupby_col]==val:
                        dummy.append(all_data[k][index])
                
                aggr_func = aggrs[j]
                if aggr_func=="max":
                    ans.append(max(dummy))
                elif aggr_func=="min":
                    ans.append(min(dummy))
                elif aggr_func=="count":
                    ans.append(len(dummy))
                elif aggr_func=="average":
                    ans.append(round(sum(dummy)/len(dummy),2))
                elif aggr_func=="sum":
                    ans.append(sum(dummy))
            final_output.append(ans)
    return final_output
                

def validateGroupby(projected_cols, aggr_cols, aggrs):
    if len(aggr_cols) != len(aggrs) or (len(projected_cols)>1):
        return False
    return True


def get_col_index(condition):
    left = -1
    right = -1
    for i in range(2):
        j=0
        for col_names in all_col_names_list:
            if col_names.endswith('.'+condition[i]):
                if i==0:
                    left = j 
                    break  
                elif i==1:
                    right = j
                    break
            j+=1
    return left, right


def split_operators(cond):
    op = ""
    for i in range(len(cond)):
        if cond[i] == '<' and cond[i+1] == '=':
            op = "<="
            break
        elif cond[i] == '<' and cond[i+1] != '=':
            op = "<"
            break
        elif cond[i] == '>' and cond[i+1] == '=':
            op = ">="
            break
        elif cond[i] == '>' and cond[i+1] != '=':
            op = ">"
            break
        elif cond[i] == '=' and (cond[i+1] != '=' or cond[i+1] != '<'
                            or cond[i+1] != '>' or cond[i+1] != '!'):
            op = "="
            break
    # print ("cond : ", cond , " op : ", op)
    splitted_op = cond.split(op)
    splitted_op = list(map(str.strip, splitted_op))
    # print("splt before dding op : ", splitted_op)
    if op=="=":
        splitted_op.append("==")
    else:
        splitted_op.append(op)

    return list(map(str.strip,splitted_op))


def apply_where(condition):
    c = condition.split(" ")
    c = list(map(str.strip, c))
    conn = []   # and/or
    for cond in c:
        if cond.lower().strip()=='and' or cond.lower().strip()=='or':
            conn.append(cond.lower().strip())

    # print ("connector : ", conn)
    and_str = "and"
    or_str = "or"
    cond = []
    # print ("condition : ", condition)
    if condition.find("and")!=-1:
        # print ("index : ", condition.index(and_str))
        cond.append(condition[:condition.index(and_str)].strip())
        cond.append(condition[condition.index("and")+len("and"):])
    elif condition.find("or")!=-1:
        cond.append(condition[:condition.index("or")])
        cond.append(condition[condition.index("or")+len("or"):])
    else:
        # print ("no connector used \n")
        cond.append(condition)
        # sys.exit()
    
    # print ("cond : ", cond)
    i=0
    splitted_cond = []
    for con in cond:
        splitted_cond = split_operators(con)
        # print ("splitted cond : :", splitted_cond)
        left_split, right_split = get_col_index(splitted_cond)
        # print ("left and rihgt : ", left_split, right_split)

        if left_split!=-1 and right_split!=-1:
            splitted_cond[0] = splitted_cond[0].replace(splitted_cond[0],"all_data[i][" + str(left_split) +"]")
            splitted_cond[1] = splitted_cond[1].replace(splitted_cond[1],"all_data[i][" + str(right_split) +"]")
        elif left_split!=-1:
            splitted_cond[0] = splitted_cond[0].replace(splitted_cond[0],"all_data[i][" + str(left_split) +"]")
        elif right_split!=-1:
            splitted_cond[1] = splitted_cond[1].replace(splitted_cond[1],"all_data[i][" + str(right_split) +"]")
        else:
            print ("syntax error : where cols not found \n")
            sys.exit()
        split = splitted_cond[0], splitted_cond[1]
        cond[i] = splitted_cond[2].join(split)
        i+=1
        # print ("con i : ", con)
    
    # print ("cond : ", cond)
    final_cond = cond[0]
    if len(conn)!=0:
        final_cond+=(" " + conn[0] + " " + cond[1])
    # print ("final cond L ", final_cond)

    eval_output = []
    for i in range(len(all_data)):
        # print ("in /loop : ", all_data[i])
        if eval(final_cond):
            eval_output.append(all_data[i])
    
    return eval_output


def get_sorted_output(output, sorting_order, orderby_col_index):
    # print ("in func sorting order : :", sorting_order)
    if sorting_order.lower() == "asc":
        output = sorted(output, key=lambda x: (x[orderby_col_index]))
    else:
        output = sorted(output, key=lambda x: (x[orderby_col_index]), reverse=True)

    return output


def checkSortingOrder(col):
    col = col.strip()
    # print ("col  sortnig order : ", col)
    col = col.split()
    orderby_col = ""
    sorting_order = ""
    orderby_col = col[0]
    # print ("col1 : ", col[1].lower())
    if len(col) == 1:
        sorting_order = "asc"
    else:
        if col[1].lower() == 'desc':
            sorting_order = "desc"
        elif col[1].lower() == 'asc':
            sorting_order = "asc"
        else:
            print ("syntax error in order by :\n")
            sys.exit()
    return sorting_order, orderby_col


def apply_aggr_func(req_cols, aggr):
    ans = ""
    # print ("req cols : ", req_cols)
    for i in range(len(req_cols)):
        dummy = []
        if req_cols[i]=="*" :
            if aggr[i]!="count" :
                print ("syntax error :'*' can only be used with count" )
                sys.exit()
            else:
                count = len(all_data)
                ans += str(count) + "\t"
                continue
        for j in range(len(all_data)):
            dummy.append(all_data[j][req_cols[i]])
        if aggr[i].lower() == "min":
            try:
                min_val = min(dummy)
            except ValueError:
                print("value error : min value not found")
                sys.exit()
            ans += str(min_val) + "\t"

        elif aggr[i].lower() == "max":
            try:
                max_val = max(dummy)
            except ValueError:
                print("value error : max value not found")
                sys.exit()
            ans += str(max_val) + "\t"

        elif aggr[i].lower() == "count":
            try:
                count = len(dummy)
            except ValueError:
                print("value error : counting not possible on this \n")
                sys.exit()
            ans += str(count) + "\t"

        elif aggr[i].lower() == "average":
            try:
                avg = round(sum(dummy)/len(dummy), 2)
            except ValueError:
                print("value error : avg value not found")
                sys.exit()
            ans += str(avg) + "\t"

        elif aggr[i].lower() == "sum":
            try:
                sum_val = sum(dummy)
            except ValueError:
                print("value error : sum not possible")
                sys.exit()
            ans += str(sum_val) + "\t"
        else:
            print("function not recognized\n")
            sys.exit()
    return ans


def remove_duplicate(data):
    data = data.split('\n')
    output = []
    for row in data:
        if row not in output:
            output.append(row)
    return '\n'.join(output)


def remove_quotes(line):
    for i in range(len(line)):
        if (line[i][0] == "\'" or line[i][0] == '\"') and (line[i][0] == line[i][-1]):
            line[i] = line[i][1:-1]

    return line


def read_csv(filename, is_distinct_present):
    filename = filename+".csv"
    # print("filename : ", filename)
    table_data = []
    try:
        csvfile = csv.reader(open(filename), delimiter=',')
    except Exception:
        print("error in csv file reading, check if file exists\n")
        sys.exit()

    for row in csvfile:
        row = remove_quotes(row)
        row = list(map(int, row))

        # if is_distinct_present == False or (is_distinct_present and row not in table_data):
        table_data.append(row)

    return table_data


def getJoinedData(table_names_list, is_distinct_present):
    table_data = read_csv(table_names_list[0], is_distinct_present)
    if len(table_names_list) == 1:
        return table_data
    else:
        for tablename in table_names_list[1:]:
            table2 = read_csv(tablename, is_distinct_present)
            dummy = []
            for i in table_data:
                for j in table2:
                    dummy.append(i+j)
            table_data = dummy
        return table_data


def seperate_aggr_groupby(query_cols_with_aggr, groupby_col):
    aggr = []
    projected_cols = []
    aggr_cols = []
    for col in query_cols_with_aggr:
        col = col.strip()
        if col.lower()[:3] in possible_aggr_funcs:
            aggr.append(col.split("(")[0])
            col_to_be_added = col.split("(")[1][:-1]
            # print ("in sepe aggr lop : ", col_to_be_added)
            col_found=False
            if col_to_be_added=="*" :
                if col.split("(")[0]!="count":
                    print ("syntax error : * can only be used with count")
                    sys.exit()
                for col in all_col_names_list:
                    if col.endswith(groupby_col):
                        aggr_cols.append(col)
                        col_found=True
                        break
            else:
                for col_names in all_col_names_list:
                    if col_names.endswith("."+col_to_be_added):
                        aggr_cols.append(col_names)
                        col_found=True
                        break
            # query_cols.append(col.split("(")[1][:-1])
        else:
            col_found=False
            if col=="*":
                print ("syntax error : * not used in groupby without aggr func")
                sys.exit()
            for col_names in all_col_names_list:
                if col_names.endswith("."+col):
                    projected_cols.append(col_names)
                    col_found=True
                    break
        if col_found==False:
            print ("column not found")
            sys.exit()
            # query_cols.append(col)
    return projected_cols, aggr_cols, aggr


def seperate_aggr(query_cols_with_aggr):
    aggr_present = False
    normal_col = False
    aggr = []
    query_cols = []
    for col in query_cols_with_aggr:
        col = col.strip()
        if col.lower()[:3] in possible_aggr_funcs:
            aggr.append(col.split("(")[0])
            col_to_be_added = col.split("(")[1][:-1]
            # print ("in sepe aggr lop : ", col_to_be_added)
            col_found=False
            if col_to_be_added=="*":
                query_cols.append("*")
                col_found=True
            else:
                for col_names in all_col_names_list:
                    if col_names.endswith("."+col_to_be_added):
                        query_cols.append(col_names)
                        col_found=True
                        break
                # query_cols.append(col.split("(")[1][:-1])
            aggr_present = True
        else:
            col_found=False
            if col=="*":
                query_cols.append("*")
                col_found=True
            else:
                for col_names in all_col_names_list:
                    if col_names.endswith("."+col):
                        query_cols.append(col_names)
                        col_found=True
                        break
                # query_cols.append(col)
            normal_col = True
        if col_found==False:
            print ("column not found")
            sys.exit()
        if normal_col and aggr_present:
            print("normal columns and aggr function with column are present simultaneuosly")
            sys.exit()
    return query_cols, aggr


def readQuery(query):
    query = query[:-1]
    # print("query : ", query)
    parsed_query = sqlparse.parse(query)[0].tokens

    is_select = sqlparse.sql.Statement(parsed_query).get_type()

    all_idenetifiers = sqlparse.sql.IdentifierList(
        parsed_query).get_identifiers()
    all_idenetifiers = list(map(str, all_idenetifiers))
    all_idenetifiers = [item.lower() for item in all_idenetifiers]
    # print("all_identifiers : ", all_idenetifiers)
    is_distinct_present = False
    is_where_present = False
    from_flag = False
    condition = ""
    table_names = ""
    table_names_list = []
    is_groupby_present = False
    is_orderby_present = False
    groupby_flag = False
    groupby_col = ""
    orderby_flag = False
    orderby_col = ""

    for identifier in all_idenetifiers:
        if identifier.lower() == 'distinct':
            is_distinct_present = True
        elif identifier.lower() == 'from':
            from_flag = True
        elif identifier.lower()[0:5] == 'where':
            is_where_present = True
            condition = identifier[6:].strip()
        elif from_flag:
            table_names = identifier
            table_names_list = table_names.split(",")
            table_names_list = list(map(str.strip, table_names_list))
            from_flag = False
        elif identifier.lower() == 'group by':
            groupby_flag = True
            is_groupby_present = True
        elif groupby_flag:
            groupby_col = identifier
            groupby_flag = False
        elif identifier.lower() == 'order by':
            orderby_flag = True
            is_orderby_present = True
        elif orderby_flag:
            orderby_col = identifier
            # print ("order by foud : ", orderby_col)
            orderby_flag = False

    if is_distinct_present:
        query_cols_with_aggr = all_idenetifiers[2]
    else:
        query_cols_with_aggr = all_idenetifiers[1]

    if is_orderby_present:
        sorting_order, orderby_col = checkSortingOrder(orderby_col)
        # print ("sorting_order, orderby_col : ",sorting_order, orderby_col)

    # print("query col with aggr : ", query_cols_with_aggr)

    for table_name in table_names_list:
        col_list = tablename_colname_dict[table_name]
        for col in col_list:
            all_col_names_list.append(table_name+'.'+col)
    # print("all col : ", all_col_names_list)

    query_cols_with_aggr = query_cols_with_aggr.split(",")
    
    query_cols = []
    aggrs = []
    projected_cols = []
    aggr_cols = []

    if is_groupby_present:
        projected_cols, aggr_cols, aggrs = seperate_aggr_groupby(query_cols_with_aggr, groupby_col)
        # print (" projected_cols, aggr_cols, aggrs",  projected_cols, aggr_cols, aggrs)
        is_groupby_valid = validateGroupby(projected_cols, aggr_cols, aggrs)
        if is_groupby_valid==False:
            print("groupby wrongly used : more than 1 projected col used")
            sys.exit()
        if len(projected_cols)!=0 and projected_cols[0][-1]!=groupby_col:
            print("projected col is not same as groupby col ")
            sys.exit()

        groupby_proj_col_index=-1
        # for col_names in all_col_names_list:
        if len(projected_cols) != 0:
            if projected_cols[0] in all_col_names_list:
                groupby_proj_col_index = all_col_names_list.index(projected_cols[0])
        
        # print ("group by proj column index ", groupby_proj_col_index)
        
        groupby_aggr_col_index=[]
        for aggr_col in aggr_cols:
            if aggr_col in all_col_names_list :
                groupby_aggr_col_index.append(all_col_names_list.index(aggr_col))
                
        groupby_col_index = -1
        for col in all_col_names_list:
            if col.endswith(groupby_col):
                groupby_col_index = all_col_names_list.index(col)
                break 

    else:
        query_cols, aggrs = seperate_aggr(query_cols_with_aggr)

    # print("query cols : ", query_cols)
    # print("aggrs : ", aggrs)
    # print("table name lst : ", table_names_list)

    if is_select.lower() != 'select':
        print("INVALID QUERY : No SELECT statement\n")
        sys.exit()

    global all_data
    all_data = getJoinedData(table_names_list, is_distinct_present)
    headers = ""

    for c in query_cols:
        headers = headers + c +','

    if is_where_present:
        all_data = apply_where(condition)
        print ("where op : ", len(all_data))    

    if is_groupby_present:
        # print ("all data beofre griup yb : :,", len(all_data))
        all_data = apply_groupby(groupby_aggr_col_index, groupby_proj_col_index, aggrs, groupby_col_index)
        # print("final output after group by : ",len(all_data))
        headers = "<"
        for col in projected_cols:
            headers +=col+','
        for i in range(len(aggr_cols)):
            headers += aggrs[i] +"(" + aggr_cols[i] + "),"
        headers = headers[:-1]
        headers += ">\n"
        if is_orderby_present:
            orderby_col_index = 0
            all_data = get_sorted_output(all_data, sorting_order, orderby_col_index)
        output = ""
        for i in range(len(all_data)):
            for j in range(len(all_data[i])):
                output += str(all_data[i][j])+"\t"
            output += "\n"
        # print("output before distcnt : ", output)
        if is_distinct_present:
            output = remove_duplicate(output)
        print(headers+output)
        return 

    req_cols_index = []
    if len(query_cols) == 1 and query_cols[0] == '*' and len(aggrs)==0:
            headers = ""
            for col in all_col_names_list:
                headers = headers + col + ','
            for i in range(0, len(all_col_names_list)):
                req_cols_index.append(i)
    else:
        for col in query_cols:
            if col=="*":
                req_cols_index.append("*")
                continue
            # print("col in trial : ", col)
            try:
                req_cols_index.append(all_col_names_list.index(col))
            except Exception:
                print("required col not found \n")
                sys.exit()

    # if is_groupby_present==False and len(aggrs)!=len(req_cols_index):
    #     print("Syntax error : normal col and aggr col used together")
    #     sys.exit()

    # print("req cols index : ", req_cols_index)
    if len(aggrs) == 0:
        if is_orderby_present:
            for col_names in all_col_names_list:
                if col_names.endswith('.'+orderby_col):
                    orderby_col_index = all_col_names_list.index(col_names)
                    break
            all_data = get_sorted_output(all_data, sorting_order, orderby_col_index)
        output = ""
        for i in range(len(all_data)):
            for j in req_cols_index:
                output += str(all_data[i][j])+"\t"

            output += "\n"
        if is_distinct_present:
            output = remove_duplicate(output)
    else:
        headers = ""
        for i in range(len(query_cols)):
            headers += aggrs[i] +"(" + query_cols[i] + "),"
        output = apply_aggr_func(req_cols_index, aggrs)

    headers = "<" + headers[:-1] +">\n"
    print(headers+output)


def read_metadata(filename):
    flag = 0
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() == '<begin_table>':
                columnnames = list()
                flag = 1
            elif flag == 1:
                tablename = line.strip().lower()
                flag = 0
            elif line.strip() == '<end_table>':
                tablename_colname_dict[tablename] = columnnames
            else:
                columnnames.append(line.strip().lower())


def main():
    metadata_filename = "metadata.txt"
    read_metadata(metadata_filename)
    sqlQuery = sys.argv[1]

    if sqlQuery[-1] != ';':
        print("semicolon missing \n")
        sys.exit()
    try:
        readQuery(sqlQuery)
    except Exception:
        print ("Syntax error")
        sys.exit()

main()
