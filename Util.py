import struct, csv, sys
import constants as myc

# TODO: throw exception if format not found


def isWhiteSpaceorNone(s):
    if( not s or str(s).isspace()):
        return True
    else:
        return False


def convertFromBytes(data, format):
    """This function converts an array of bytes into the data format provided
    Supported data types: short, int, int16, int32, int64, float, float32, float64, double, string """
    # conversionTable={"int":'i', "integer":'i', "short":'h', "unsignedInt":'I', "unsignedshort":'H',"sunssf":'i',"unit16":'i', "float":'f',"double":'d', "int16":'h',"int32":'i', "int64":'d',
    # "float16":'f', "float32":'f', "float64":'d', "string":'s'}
    

    # if(format == "str" or format == "string"):
    #  print(">"+str(len(data))+str(conversionTable.get(format))+"Data:"+str(len(data)))

    # print(">"+str(conversionTable.get(format))+" Data:"+str(len(data)))
    if(myc.conversionTable.get(format) != None):
        if(myc.conversionTable.get(format) == "s"):
            return data.decode()
        else:
            try:
                return struct.unpack(">"+str(myc.conversionTable.get(format)), data)[0]
            except:
                ValueError("Unpack error for format:"+format+"  Data:"+str(data))
    else:
        raise ValueError("No mapping found for data type:"+format)


def writeHTML(data, header=None):
    """This function writes the dictionary elements to a csv file. This accepts list of dictionaries 
    Right now the values written is hard coded. Will be generlized later"""

    # create headder
    if(header is None):
        header = list(data[0].keys())
    html = '''<!DOCTYPE html>
<html>

<head>
    <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
        }

        td,
        th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #dddddd;
        }
    </style>
    <script>
        function sortTable(n) {
            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            table = document.getElementById("SummaryTable");
            switching = true;
            dir = "asc";
            while (switching) {
                switching = false;
                rows = table.getElementsByTagName("TR");
                for (i = 1; i < (rows.length - 1); i++) {
                    shouldSwitch = false;
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    if (dir == "asc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "desc") {
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
                if (shouldSwitch) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;
                } else {
                    if (switchcount == 0 && dir == "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
        }
    </script>
</head>
<body><table id="SummaryTable" width="100%" >'''
    counter = 0
    for key in header:
        html += "<th onclick=\"sortTable("+str(counter)+")\">"+str(key)+"</th>"
        counter += 1
    html += "</tr>"
    for row in data:
        html += "<tr>"
        for col in header:
            html += "<td>"+str(row.get(col))+"</td>"
        html += "</tr>"
    html += "</table>"

    # claculating summary
    passCounter = FailCounter = 0
    for row in data:
        if(row.get("Result") == "Pass"):
            passCounter += 1
        elif(row.get("Result") == "Fail"):
            FailCounter += 1

    html += "<h3>Summary</h3></br><table width=\"50%\"><tr><td>Total number of test cases</td><td>" + \
        str(len(data))+"</td></tr>"
    html += "<tr><td>Total number of passed test cases</td><td>" + \
        str(passCounter)+"</td></tr>"
    html += "<tr><td>Total number of failed test cases</td><td>" + \
        str(FailCounter)+"</td></tr>"
    html += "<tr><td>Pass %</td><td>"+str((passCounter/len(data))*100)+"</td></tr>"
    html += "</table></body></html>"
    with open("./Model/result.html", 'w') as f:
        f.write(html)
