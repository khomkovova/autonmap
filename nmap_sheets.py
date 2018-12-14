from __future__ import print_function

import argparse

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os

from pprint import pprint

import xmltodict, json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '174-bmk-7tOieS4oJQN40BPpj1rlPHar7GmUh3BVOTs0'
SAMPLE_RANGE_NAME = "Ports & Services"
NMAP_RANGE_NAME = "Nmap"
parser = argparse.ArgumentParser(description="Write your command, file and thread. Example nmapParser.py -xml N -d test/ -sid spreadsheetid")
parser.add_argument("-xml", dest="xml", help="X if parse XML and False,  if upload N file")
parser.add_argument("-d", dest="directory", help="Set directory to folder with xml nmap reports")
parser.add_argument("-sid", dest="spreadsheetid", help="Spreadsheet ID")
args = parser.parse_args()

DIR = str(args.directory)
SAMPLE_SPREADSHEET_ID = str(args.spreadsheetid)
XML = str(args.xml)



class PortInfo:
    port = 0
    protocol = ""
    state = ""
    version = ""


class IpInfo:
    pinfo = []
    listInfo = []
    ip = ""

    def getReport(self, report):
        self.listInfo = []
        try:
            self.ip = report["nmaprun"]["host"]["address"]["@addr"]
        except:
            return
        try:
            ports = report["nmaprun"]["host"]["ports"]["port"]
        except:
            return
        for portIn in ports:
            pinf = PortInfo()
            try:
                pinf.port = portIn["@portid"]
            except:
                pinf.port = ""
            try:
                pinf.protocol = portIn["@protocol"]
            except:
                pinf.protocol = ""
            try:
                pinf.state = portIn["state"]["@state"]
            except:
                pinf.state = ""
            i = 0
            try:
                product = portIn["service"]["@product"]
            except:
                i+=1
                product = ""

            try:
                version = portIn["service"]["@version"]
            except:
                i += 1
                version = ""

            try:
                extrainf = portIn["service"]["@extrainfo"]
            except:
                i += 1
                extrainf = ""

            pinf.version =  product + version  + extrainf

            if pinf.port+ pinf.protocol+ pinf.state+ pinf.version == "":
                print("LOL")
                return
            else:
                if pinf.version == "":
                    pinf.version = " "
                self.listInfo.append([" ", " ", pinf.port, pinf.protocol, pinf.state, pinf.version])
                # print(self.listInfo)
                self.pinfo.append(pinf)

def updateNmapSpreadsheets(values):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    body = {
        'values': values
    }
    print(values)
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption="RAW", range=NMAP_RANGE_NAME, body=body).execute()
    print(' cells updated.', result.get('values', []))

def updateSpreadsheets(values):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    body = {
        'values': values
    }
    print(values)
    result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, valueInputOption="RAW", range=SAMPLE_RANGE_NAME, body=body).execute()
    print(' cells updated.', result.get('values', []))

def getSpreadsheetsValues():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        return None
    return values

def getNmapSpreadsheetsValues():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=NMAP_RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        return None
    return values

def convertXMLtoJson(xml):
    try:
        o = xmltodict.parse(xml)
        jsonReport = json.loads(json.dumps(o))
        return jsonReport
    except:
        return None

def addInfoToValues(ipinf, values):
    if type(values) == type(None):
        values = []
        values.append(["", "IP", "Port", "Protocol", "Status", "Service"])
    t = False
    try:
        for i in range(0, len(values)-1):
            if values[i][1] == ipinf.ip:
                for row in ipinf.listInfo:
                    values.insert(i+1, row)
                t = True
    except:
        print("Value range")


    if t == False:
        values.append([" ", ipinf.ip," "," "," "," "])
        l = len(values)
        for row in ipinf.listInfo:
            values.insert(l, row)
        values.append([" "," "," "," "," "," "])
    return values

def createSheetsPort():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()

    spreadsheet1 = {'requests': [
        {"addSheet": {
            'properties': {
                "sheetId": 1,
                "title": SAMPLE_RANGE_NAME,
                "index": 1
            }
        }
        }
    ]
    }
    try:
        sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=spreadsheet1).execute()
    except:
        pass

def createSheetsNmap():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()

    spreadsheet2 = {'requests': [
        {"addSheet": {
            'properties': {
                "sheetId": 2,
                "title": NMAP_RANGE_NAME,
                "index": 2
            }
        }
        }
    ]
    }
    try:
        sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=spreadsheet2).execute()
    except:
        pass
def addNmapReportToSpreadsheet(nmapReport):
    values = getNmapSpreadsheetsValues()
    if type(values) == type(None):
        print("nonsadfe")
        values = []
        values.append([" ", " ", " ", "Nmap Report"])
    values.append([" "," "," ",nmapReport])
    print("v = ", values)
    updateNmapSpreadsheets(values)

def addReportToSpreadsheet(reportXML):

    ipinf = IpInfo()

    jsonXml = convertXMLtoJson(reportXML)
    if jsonXml == None:
        return
    ipinf.getReport(jsonXml)
    values = getSpreadsheetsValues()
    v = addInfoToValues(ipinf, values)
    updateSpreadsheets(v)
    ipinf = None

def mainPortReport():
    createSheetsPort()
    for root, dirs, files in os.walk(DIR):
        for filename in files:
            if not filename.__contains__(".xml"):
                continue
            f = open(DIR + filename, "r")
            r = f.read()
            addReportToSpreadsheet(r)
            f.close()

def mainNmapReport():
    createSheetsNmap()
    for root, dirs, files in os.walk(DIR):
        for filename in files:
            if not filename.__contains__(".nmap"):
                continue
            f = open(DIR + filename, "r")
            r = f.read()
            addNmapReportToSpreadsheet(r)
            f.close()

def main():
    if XML == "X":
        mainPortReport()
    if XML == "N":
        mainNmapReport()
if __name__ == '__main__':
    main()