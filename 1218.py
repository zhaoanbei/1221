"""
1st Raster calculator:
Combine rasters into 2 raster: 96-02; 03-13
        DISPLAY NAME        DATA TYPE       PROPERTY>DIRECTION>VALUE
        96                  Raster Layer    Input
        98                  Raster Layer    Input
        99                  Raster Layer    Input
        00                  Raster Layer    Input
        02                  Raster Layer    Input
        03                  Raster Layer    Input
        05                  Raster Layer    Input
        06                  Raster Layer    Input
        08                  Raster Layer    Input
        10                  Raster Layer    Input
        13                  Raster Layer    Input
        96-02               Raster Dataset  Output
        03-13               Raster Dataset  Output
"""

# Import external modules
import sys, os, string, math, arcpy, traceback, numpy, time
from arcpy import env
from arcpy.sa import *
# Allow output to overwite any existing grid of the same name
arcpy.env.overwriteOutput = True
#Set environment settings
env.workspace = "D:\Desktop\larp\1218GIS"
# If Spatial Analyst license is available, check it out
if arcpy.CheckExtension("spatial") == "Available":
    arcpy.CheckOutExtension("spatial")
    try:
        # Raster calculator to combine input rasters into two rasters: 96-02, 03-13
        Y96 = arcpy.GetParameterAsText(0)
        Y98 = arcpy.GetParameterAsText(1)
        Y99 = arcpy.GetParameterAsText(2)
        Y00 = arcpy.GetParameterAsText(3)
        Y02 = arcpy.GetParameterAsText(4)
        Y03 = arcpy.GetParameterAsText(5)
        Y05 = arcpy.GetParameterAsText(6)
        Y06 = arcpy.GetParameterAsText(7)
        Y08 = arcpy.GetParameterAsText(8)
        Y10 = arcpy.GetParameterAsText(9)
        Y13 = arcpy.GetParameterAsText(10)

        # Raster calculator： 96-02
        Y9698 = Plus(Y96, Y98)
        Y9699 = Plus(Y9698, Y99)
        Y9600 = Plus(Y9699, Y00)
        Y9602 = Plus(Y9600, Y02)
        Y9602 = Divide(Y9602, 225)
        Y9602.save(arcpy.GetParameterAsText(11))

        # Raster calculator： 03-13
        Y0305 = Plus(Y03, Y05)
        Y0306 = Plus(Y0305, Y06)
        Y0308 = Plus(Y0306, Y08)
        Y0310 = Plus(Y0308, Y10)
        Y0313 = Plus(Y0310, Y13)
        Y0313 = Divide(Y0313, 225)
        Y0313.save(arcpy.GetParameterAsText(12))
        arcpy.CheckInExtension("spatial")

    except Exception as e:
    	# If unsuccessful, end gracefully by indicating why
    	arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    	# ... and where
    	exceptionreport = sys.exc_info()[2]
    	fullermessage   = traceback.format_tb(exceptionreport)[0]
    	arcpy.AddError("at this location: \n\n" + fullermessage + "\n")

    # Check in Spatial Analyst extension license
    arcpy.CheckInExtension("spatial")
else:
    # Report error message if Spatial Analyst license is unavailable
    arcpy.AddMessage ("Spatial Analyst license is unavailable")
