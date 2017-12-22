"""
THIS SCRIPT REPEATEDLY REPLACES EACH PIXEL'S VALUE WITH
THE MEAN OF ALL VALUES WITHIN ITS IMMEDIATE NEIGHBORHOOD

To create an ArcToolbox tool with which to execute this script, do the following.
1   In  ArcMap > Catalog > Toolboxes > My Toolboxes, either select an existing toolbox
    or right-click on My Toolboxes and use New > Toolbox to create (then rename) a new one.
2   Drag (or use ArcToolbox > Add Toolbox to add) this toolbox to ArcToolbox.
3   Right-click on the toolbox in ArcToolbox, and use Add > Script to open a dialog box.
4   In this Add Script dialog box, use Label to name the tool being created, and press Next.
5   In a new dialog box, browse to the .py file to be invoked by this tool, and press Next.
6   In the next dialog box, specify the following inputs (using dropdown menus wherever possible)
    before pressing OK or Finish.
        DISPLAY NAME        DATA TYPE       PROPERTY>DIRECTION>VALUE
        Input Grid          Raster Layer    Input
        Output Grid         Raster Dataset  Output
        Iterations          Long            Input

   To later revise any of this, right-click to the tool's name and select Properties.
"""

# Import external modules
import sys, os, string, math, arcpy, traceback, numpy, time

# Allow output to overwite any existing grid of the same name
arcpy.env.overwriteOutput = True

# If Spatial Analyst license is available, check it out
if arcpy.CheckExtension("spatial") == "Available":
    arcpy.CheckOutExtension("spatial")
    try:
        # Create inputArray
        inputGridName       = arcpy.GetParameterAsText(0)
        inputArray          = arcpy.RasterToNumPyArray(inputGridName)
        inputArray          = inputArray.astype(float)          # a real-number array storing each iteration's input values
        howManyRows         = inputArray.shape[0]               # an integer indicating number of rows ininput and output grids
        howManyColumns      = inputArray.shape[1]               # an integer indicating number of columns in input and output grids

        # Initialize an intermediateArray that is similar to that inputArray but filled with zeroes
        intermediateArray   = numpy.zeros_like(inputArray)      # a real-number array storing each iteration's output values

        # Get User-specified number of iterations
        howManyIterations = int(arcpy.GetParameterAsText(2))    # an integer indicating the number of local dispersions to apply
        if howManyIterations < 0: howManyIterations = 10

        # Start timing
        timeStart           = time.clock()

        # Loop through as many iterations as requested
        for iterationNumber in range(howManyIterations):
            arcpy.AddMessage("\nIteration " + str(iterationNumber))

            # Loop through rows and columns of pixels, skipping those at the edges (recalling that range(A,B) stops just short of B)
            for thisRow in range(5,howManyRows-10):
                for thisColumn in range(5,howManyColumns-10):
                    # Loop through the immediate neighborhood of each pixel
                    totalValue = 0
                    for neighborRow in range(thisRow-5,thisRow+10):
                        for neighborColumn in range(thisColumn-5,thisColumn+10):
                            # Tally the total value within the neighborhood
                            totalValue = totalValue + inputArray[neighborRow][neighborColumn]
                    # Once neighbors have been tallied, record their mean in the intermediateArray
                    intermediateArray[thisRow][thisColumn] = totalValue / 225
            # Once neighborhood means have been computed for all pixels, use them to update inputArray
            inputArray    = numpy.copy(intermediateArray)

        # Stop timing
        timeStop        = time.clock()
        timeTaken       = timeStop - timeStart
        arcpy.AddMessage("\nElapsed time = " + str(timeTaken) + " seconds\n")

        # Create output grid from that new array
        inputGrid       = arcpy.Raster(inputGridName)
        gridExtent      = inputGrid.extent
        lowerleftPoint  = gridExtent.lowerLeft
        gridResolution  = inputGrid.meanCellWidth
        outputGrid 	    = arcpy.NumPyArrayToRaster(intermediateArray,lowerleftPoint,gridResolution)
        outputGrid.save(arcpy.GetParameterAsText(1))

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
    print "Spatial Analyst license is " + arcpy.CheckExtension("spatial")






















