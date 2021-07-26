
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    meta_params = {
        'model_output_file': {
            'dialog_reference': """
            ### Some header to your contents

            this is the contents
            
                def code1():
                    print('some code')


                def code2():
                    print('some code')    
                            
                def code3():
                    print('some code')


            end
            """,
            'python_reference': """
            some ref

            code

                output_file = parameters[0].valueAsText
            """,
            
        },
        "tags": ['infowater', 'report', 'rpt'],
        'summary':"""
        a summary with some **bold** contents

        `a code block`


        """,

        'usage': """
        usage stuff
        
        `code block`

        **other**
        
            code block
        """
    }

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = "this is the description of the tool"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Model Output File",
            name="model_output_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input",
        )
        param0.filter.list = ["RPT"]

        param1 = arcpy.Parameter(
            displayName="Output Folder",
            name="output_folder",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
        )
        param1.filter.list = ["File System"]

        param2 = arcpy.Parameter(
            displayName="Output Excel Name",
            name="output_excel_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        # param2.filter.list = []

        param3 = arcpy.Parameter(
            displayName="Pressure Zone Sheet",
            name="zone_sheet",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input",
        )
        param3.filter.list = ['xls', 'xlsx']
        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        return