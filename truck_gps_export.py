"""
SYNOPSIS

    truck_gps_export.py - Ran as a GP tool in ArcGIS Pro

DESCRIPTION

    Script to support ArcGIS Pro GP tool.
    Tool will allow the user to select a data range, a data source, and a
      data location.
    Tool will output a feature class located in a file geodatabase.
    Furture iteration of the this script will write to a SQL table.
    
REQUIREMENTS

    Python 3.5 or higher
    TODO - Enter all dependent libraries that do not come in the standard
           Python environment this script is expected to run in.  If a library
           must be installed, provide a brief indication of how it is to be 
           installed.  EX: (install via pip)  EX: (install via conda)  

AUTHOR

    Dan Sereno, NV5, 2025
    
UPDATES

    TODO - If this script was modified, indicate when it was modified, what
           modifications were performed, and by whom.
"""

import os, sys
import traceback
from typing import Dict
import base64
from arcgis.gis import GIS
import pandas as pd
import urllib
import json
from datetime import datetime
from datetime import date

# import arcpy
# below is code to try to catch arcpy import errors
try:
    import arcpy
    arcpy_imported = True

    # Don't create/export any metadata
    if arcpy.GetLogMetadata():
        arcpy.SetLogMetadata(False)

    if arcpy.GetLogHistory():
        arcpy.SetLogHistory(False)
except:
    arcpy_imported = False
    exit_status = 1

def is_valid_path(parser: str, path: str) -> str:
    """
    Check to see if a provided path is valid.  Works with argparse
    
    Parameters
    ----------
    parser (argparse.ArgumentParser)
        The argument parser object
    path (str)
        The path to evaluate whether it exists or not
        
    Returns
    ----------
    path (str)
        If the path exists, it is returned  if not, a 
        parser.error is raised.
    """      
    if not os.path.exists(path):
        parser.error("The path {0} does not exist!".format(path))
    else:
        return path
    
def getArcGISServerToken(url: str, userN: str, userPwd: str) ->str:
    try:
        values = {'username': userN,
        'password': userPwd,
        'referer' : url,
        'f': 'json'}
        data =  urllib.parse.urlencode(values)
        data = data.encode('ascii')
        URL  = url + '/tokens/generateToken'
        req = urllib.request.Request(URL,data)
        with urllib.request.urlopen(req) as response:
            jres = json.load(response)
    except Exception as e:
        arcpy.AddMessage(fr"Get GIS token failed!")
        arcpy.AddMessage(fr"{e.args}")

    return jres['token']    

# Create GIS object
def create_GIS(portal_url: str, user: str, password: str) -> GIS:
    try:
        gis = GIS(url=portal_url,
                    username=user,
                    password=password,
                    verify_cert=False)
    except Exception as e:
        arcpy.AddMessage(fr"Creation of GIS failed!")
        arcpy.AddMessage(fr"{e.args}")

    return gis

    
def main():
    """
    Main execution code
    """
    
    try:

        # if arcpy did not import, log the message and quit
        if arcpy_imported == False:
            raise ValueError("Could not import arcpy.  Check licensing or the Python executable.")

        # Define the parameters for the geoprocessing tool
        start_date = arcpy.GetParameterAsText(0)
        end_date = arcpy.GetParameterAsText(1)

        # Convert end_date to date
        date_obj = datetime.strptime(end_date, "%m/%d/%Y %I:%M:%S %p")
        source_feature_class = arcpy.GetParameterAsText(2) #"https://gisportal.gflenv.com/server/rest/services/Hosted/Truck_GPS_Pings_STBDS/FeatureServer/0"
        output_feature_class = arcpy.GetParameterAsText(3) + "_" + date_obj.strftime("%m%d%Y")
        arcpy.AddMessage(f"{output_feature_class}")
        
        # Create a feature layer from the feature service
        arcpy.env.metadata = 
        arcpy.MakeFeatureLayer_management(source_feature_class, 'target_layer')

        # Define the SQL query to select features within the date range
        sql_query = f"OccurrenceDate >= timestamp '{start_date}' AND OccurrenceDate <= timestamp '{end_date}'"

        # Select the features that match the SQL query
        arcpy.management.SelectLayerByAttribute('target_layer', 'NEW_SELECTION', sql_query)

        # Get the count of selected records
        result = arcpy.management.GetCount('target_layer')
        count = int(result.getOutput(0))
        arcpy.AddMessage(f"Number of records selected: {count}")

        # Copy the selected features to the output feature class
        arcpy.management.CopyFeatures('target_layer', output_feature_class)

        arcpy.AddMessage("Geoprocessing tool executed successfully.")
        
        # # # # End your code above here # # # #
            
    except ValueError as e:
        exc_traceback = sys.exc_info()[2]
        error_text = 'Line: {0} --- {1}'.format(exc_traceback.tb_lineno, e)
        try:
            arcpy.AddMessage(fr"{error_text}")
        except NameError:
            arcpy.AddMessage(fr"{error_text}") 
    
    except Exception:
        exc_traceback = sys.exc_info()[2]
        tbinfo = traceback.format_exc()
        error_text = 'Line: {0} --- {1}'.format(exc_traceback.tb_lineno, tbinfo)
        try:
            arcpy.AddMessage(fr"{error_text}")
        except NameError:
            arcpy.AddMessage(fr"{binfo}")
    
if __name__ == '__main__':
    main()
