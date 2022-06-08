import datetime
import json
import cx_Oracle

def convert_to_json(rows, cols, filename):
    new_list = []
    for row in rows:
        new_dict = {}
        for colname, val in zip(cols, row):
            # because json does not handle datetime
            if isinstance(val,datetime.datetime):
                val = str(val)
            new_dict[colname] = val
            # print(colname,val)
        new_list.append(new_dict)
        # Create a string representation of your array of songs.
    json_obj = json.dumps(new_list, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_obj)


def extract_rows_cols(table_name):
    try:
        con = cx_Oracle.connect('system/SPilu@62@localhost:1521/orcl')
    except cx_Oracle.DatabaseError as er:
        print('There is an error in the Oracle database:', er)
    else:
        try:
            cur = con.cursor()
            # fetchall() is used to fetch all records from result set
            exec_string = 'select * from ' + table_name + ' WHERE ROWNUM <100'
            cur.execute(exec_string)  # output of tuples
            rows = cur.fetchall()
            cols = [x[0] for x in cur.description]
            return rows, cols
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:', er)
        except Exception as er:
            print('Error:' + str(er))
        finally:
            if cur:
                cur.close()
    finally:
        if con:
            con.close()


def run():
    #File 1
    rows,cols=extract_rows_cols("EINVOICE.XXSTR_EINVOICE_HEADERS")#rows are list of tuples
    cols[0] = "DOCUMENT_ID"
    convert_to_json(rows, cols, "invoice.json")

    # second file
    rows, cols = extract_rows_cols("EINVOICE.XXSTR_EINVOICE_LINES")
    cols[1] = "DOCUMENT_ID"
    convert_to_json(rows, cols, "items.json")

if __name__=="__main__":
    run()