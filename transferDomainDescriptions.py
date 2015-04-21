#-------------------------------------------------------------------------------
# Name:        Transfer Field Domain Descriptions
# Purpose:     Allows you to transfer domain description from a field you have applied a coded value domain into a new field
               # You can then maybe create a coded value domain with text datatype
               # Automates the process
#
# Author:      dmuthami
# Email :      waruid@gmail.com
#
# Created:     08/04/2015(dd/mm/yyyy)
# Copyright:   (c) dmuthami 2015
# Licence:     Absolutely Free for use and distribution
#-------------------------------------------------------------------------------
import os, sys
import logging
import arcpy
import traceback
from arcpy import env
from datetime import datetime

#Set-up logging object
logger = logging.getLogger('domainDictionary')

#Function returns a dictionary
def domainDictionary(workspace,domainName):
    #create an empty dictionary
    domainDict = {}
    try:
		domains = arcpy.da.ListDomains(workspace)
		for domain in domains:
			#print('Domain name: {0}'.format(domain.name))
			if domain.name == domainName:
				coded_values = domain.codedValues
				for val, desc in coded_values.iteritems():
					print('{0} : {1}'.format(val, desc))
					domainDict[val] = desc
				break
    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n Domain Dictionary Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows
            print pymsg
            print "\n" +msgs
            logger.info("domainDictionary in Utility_Functions "+ pymsg)
            logger.info("domainDictionary in Utility_Functions "+ msgs)

    return domainDict

##Updates hispanic areas based on selection layer and supplied update value
def writeDomainDescriptionsToNewField(workspace,featureclass,domainDict,fields):
    try:

        # Start an edit session. Must provide the workspace.
        edit = arcpy.da.Editor(workspace)

        # Edit session is started without an undo/redo stack for versioned data
        #  (for second argument, use False for unversioned data)
        #Compulsory for above feature class participating in a complex data such as parcel fabric
        edit.startEditing(False, True)

        # Start an edit operation
        edit.startOperation()

        #Update cursor goes here
        with arcpy.da.UpdateCursor(featureclass, fields) as cursor:
            for row in cursor:# loops per record in the recordset and returns an array of objects
                strr = "";
                try:

                    if row[0] != None:
                        #update zone affiliation to the supplied value
                        strr =str(domainDict[int(row[0])])

                except:
                        ## Return any Python specific errors and any error returned by the geoprocessor
                        ##
                        tb = sys.exc_info()[2]
                        tbinfo = traceback.format_tb(tb)[0]
                        pymsg = "PYTHON ERRORS:\n Writing to new field the decriptions : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                                "Line {0}".format(tb.tb_lineno)
                        msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

                        ##Add custom informative message to the Python script tool
                        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
                        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

                        ##For debugging purposes only
                        ##To be commented on python script scheduling in Windows _log
                        print pymsg
                        print "\n" +msgs
                        logger.info( pymsg)
                        logger.info(msgs)
                #test if str is not null
                if len(strr) > 0 :
                    #update tuple cell
                    row[1] = strr

                    # Update the cursor with the updated row object that contains now the new record
                    cursor.updateRow(row)

        # Stop the edit operation and commit the changes
        edit.stopOperation()

        # Stop the edit session and save the changes
        #Compulsory for release of locks arising from edit session. NB. Singleton principle is observed here
        edit.stopEditing(True)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n updateIPEDSID() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            print pymsg
            print "\n" +msgs
            logger.info( pymsg)
            logger.info(msgs)

    return ""

#main function
def transferDomainDescriptions():
    try:
        #Timestamp appended t the log file#
        currentDate = datetime.now().strftime("-%d-%m-%y_%H-%M-%S") # Current time

        #Set-up some error logging code.
        logfile = r"C:\DAVID-MUTHAMI\GIS Data\Namibia ULIMS\Scripts\transferDomainDescriptions" + "\\"+ "transfer_domain_descriptions_logfile" + str(currentDate)+ ".log"

        hdlr = logging.FileHandler(logfile)#file handler
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')# formatter object
        hdlr.setFormatter(formatter)#link handler and formatter object
        logger.addHandler(hdlr)# add handler to the logger object
        logger.setLevel(logging.INFO)#Set the logging level

        #Workspace
        _workspace = r"Database Connections\gisadmin@172.24.0.47@ulims_gis.sde"
        env.workspace = _workspace

        ## Set overwrite in workspace to true
        env.overwriteOutput = True

        #Feature class used in system
        featureClass = "ulims_gis.GISADMIN.walvis_bay_Parcels"
        oldField = "wb_zoning_id"
        newField = "wb_zoning_id2" # wb_township_id2  wb_zoning_id2
        domainName = "walvis_bay_zoning" # walvis_bay_township  walvis_bay_zoning

        #Create a domain dictionary
        domainDict = domainDictionary(env.workspace,domainName)

        #Create a fields arrray
        fields = [oldField,newField]

        #Call functon to write the domain descriptions to new field
        writeDomainDescriptionsToNewField(env.workspace,featureClass,domainDict,fields)

        #On success perfomace tuning complete is written to a variable
        msg = "Transfer Domains Descriptions Succeeded"

        #Write to console
        print msg

        #Write to log file
        logger.info(msg)

    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\n ulimsPerfomanceManagement() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                "Line {0}".format(tb.tb_lineno)
        msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##Add custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows _log
        print pymsg
        logger.info(pymsg)
        print "\n" +msgs
        logger.info(msgs)

def main():
    pass

if __name__ == '__main__':
    main()

    #Run transfer domain description module
    transferDomainDescriptions()
