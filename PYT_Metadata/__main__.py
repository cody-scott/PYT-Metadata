import sys
import optparse

from .generate_pyt_meta import meta_toolbox



def parse_options(args=None, values=None):
    """
    Define and parse `optparse` options for command-line usage.
    """
    usage = """%prog [options] [TOOLBOX_PATH]"""
    desc = "Generate ArcGIS Metadata from markdown'd toolbox code. "

    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option("-y", "--yes", dest="yes", default=None, action='store_true',
                      help="Implicit confirmation to run")

    (options, args) = parser.parse_args(args, values)

    if len(args) == 0:
        raise Exception("Input toolbox needed")
    else:
        input_file = args[0]


    opts = {
        'input': input_file,
        'implicit_run': options.yes,
    }

    return opts

def run():
    try:
        import arcpy
    except ImportError:
        raise Exception("ArcPy is required to run this tool")
        
    options = parse_options()
    if options['implicit_run'] is None:
        print("\n".join([
            "",
            "Your toolbox is imported using the imp module.",
            "To avoid running unknown code, you should verify the toolbox contents prior to running this tool",
            "",
        ]))
        print("To confirm, re-run using the -y option.")
        print(f"python -m PYT_Metadata {options['input']} -y")
        sys.exit(1)

    # Run
    meta_toolbox(options['input'])
    
if __name__ == '__main__':
    run()