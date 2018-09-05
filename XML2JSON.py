from xml.dom.minidom import parse
import xml.dom.minidom
import json


def parseXML(moduleId, startingAddress):
    filePath = './Model/smdx/smdx_'+'{:05}'.format(moduleId)+'.xml'
    xmlDoc = xml.dom.minidom.parse(filePath)
    xmlElements = xmlDoc.documentElement
    model = xmlElements.getElementsByTagName("model")[0]
    stringPoints = xmlElements.getElementsByTagName(
        "strings")[0].getElementsByTagName("point")
    if(int(model.getAttribute("id")) == moduleId):
        points = model.getElementsByTagName("point")
        schema = {}
        for point in points:
            temp = {}
            temp['address'] = startingAddress + int(str(point.getAttribute("offset")).strip())
            temp['type'] = point.getAttribute("type")
            temp['len'] = point.getAttribute("len")
            temp['mandatory'] = point.getAttribute("mandatory")
            temp['access'] = point.getAttribute("access")
            for p in stringPoints:
                if(p.getAttribute('id') == point.getAttribute("id")):
                    try:
                        temp['description'] = str(p.getElementsByTagName('description')[0].firstChild.nodeValue)
                    except:
                        temp['description'] = ""
                    try:
                        temp['label'] = str(p.getElementsByTagName('label')[0].firstChild.nodeValue)
                    except:
                        temp['label'] = ""
            schema[str(point.getAttribute("id"))] = temp
    else:
        ValueError("Module "+str(moduleId)+" not found!!!")
    
    return schema


schemaval = parseXML(7, 4003)
for k in schemaval.keys():
    print(str(schemaval.get(k)))

with open('./Model/data.json', 'w') as fp:
    json.dump(schemaval, fp)

