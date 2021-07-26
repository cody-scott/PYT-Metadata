# PYT-Metadata 

A Metadata tool for ArcGIS Toolboxes in the Item Description style.

## Description

The simple goal for this package is to attempt write everything related to your python toolbox tools in the python toolbox.  

This means your code for the non-business logic (but could also include business logic), but also your metadata, which normally is completed in ArcGIS Pro/Desktop afterwards, often as an afterthought.

Since this leverages Markdown for the descriptions, writing simple full content is simple, but also allows for a lot of flexibility.

## Install

This is tested in **ArcGIS Pro only**. It may work in ArcGIS Desktop, but I have not tested it.

This tool also requires `arcpy` to be in the python install used for the module, as its calling arcpy.Parameter() to obtain some of the metadata details.

Installing is simple:

 1. Clone default ArcGIS Pro conda environment (if you have not already)
 2. Switch to target environment
 3. Install package
 
 Install:

    pip install PYT-Metadata

If you are working in a jupyter notebook (ArcGIS Notebook) then you can install with the following command in a cell:

    !pip install PYT-Metadata

## Security

Because this tool uses the imp module to load your toolbox from source, as pyt files are not loaded by python, you need to ensure the contents of the toolbox (and any imports) satisfy your security policies. 

The TLDR is: make sure you know whats inside the toolbox code before running it.

Ultimately when you load the toolbox in arcgis desktop/pro it will run the code anyways, but as a best practice you should understand the contents. 

Since you're writing metadata for this, you'll likely be one of the authors, so should have a grasp on the contents.

## Usage

To add metadata to your tool, a dictionary of `meta_params` is required

Each tool will have its own key in the dictionary, using its name parameter, and the value should be a dictionary the dialog and python reference.

using a multi-line string for the text is recommended, but not required. Text is a markdown structure

See the ./example/working.pyt for an example.

```
meta_params = {
        'tool_name_1': {
            'dialog_reference': """

            """,
        },
        'tool_name_2': {
            'dialog_reference': """

            """,
            'python_reference': """

            """,
        },
        "tags": ['tag1'],
        'summary':"""

        """,
        'usage': """

        """
    }
```

Once you have added your metadata, call it when in your conda environment:

    python -m PYT_Metadata -y ./example/working.pyt

If you do not include the -y it will prompt you to include it and a reminder about the imp module.

## Output

The tool will overwrite existing files for the metadata. This means any changes made in ArcGIS Pro/Desktop will be overwritten.

Further, since this tool renders the HTML directly, it lets you add features not supported directly through the ArcGIS Metadata Editor, including codeblocks. If you edit the metadata in ArcGIS, these additional structures will be removed by ArcGIS.

## Whats not supported?

 * Geography Metadata
 * Table Metadata
 * ArcGIS Desktop (but may still work)

 These may be a future addition, but are not currently supported.

 ## Whats next?

 This is a work in progress so there is a lot of room for improvement.

 Please share any ideas or issues you have.
 