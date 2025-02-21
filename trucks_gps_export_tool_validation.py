class ToolValidator:
  # Class to add custom behavior and properties to the tool and tool parameters.

    def __init__(self):
        # set self.params for use in other function
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        # Customize parameter properties. 
        # This gets called when the tool is opened.
        return

    def updateParameters(self):

        # Modify parameter values and properties.
        # This gets called each time a parameter is modified, before 
        # standard validation.
        
        return
        
    def updateMessages(self):
        from datetime import datetime, timedelta
                
        # Customize messages for the parameters.
        # This gets called after standard validation.
        if self.params[0]:

            # Convert the start and end date strings to a datetime object
            start_date = datetime.strptime(self.params[0].valueAsText, "%m/%d/%Y %I:%M:%S %p")

            # Get the current date
            current_date = datetime.now()
        
            # Calculate the date 7 days ago from the current date
            seven_days_ago = current_date - timedelta(days=7)
        
            # Check if the start date is older than 7 days
            if start_date < seven_days_ago:
                self.params[0].setErrorMessage("Start Date cannot be older than 7 days.")
                
            # Check if the start date is in the future
            if start_date > current_date:
                self.params[0].setErrorMessage("Start Date cannot be in the future.")
                
            # Check if the end date is before start date
            if self.params[1].altered:
                end_date = datetime.strptime(self.params[1].valueAsText, "%m/%d/%Y %I:%M:%S %p")
                if end_date < start_date:
                    self.params[1].setErrorMessage("End Date cannot be before Start Date.")
        return

    # def isLicensed(self):
    #     # set tool isLicensed.
    # return True

    # def postExecute(self):
    #     # This method takes place after outputs are processed and
    #     # added to the display.
    # return