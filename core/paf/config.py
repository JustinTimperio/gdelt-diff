#! /usr/bin/env python3
import sys
from .file import read_file


############
# Read Unix-Like Configs
######

def read_config(path, mandatory, optional):
    '''
    Reads *nix like config files into a dict. Expects a path and two lists.
    Unless all mandatory values are found the function will force exit.
    Duplicate values in the source config is not allowed.
    '''
    mand = set()
    opt = set()
    extra = set()

    def convert_value(val):
        # Convert Ints
        try:
            x = int(val[1])
            return (val[0], x)
        except ValueError:
            pass

        # Convert Bool
        if val[1].lower() == 'true':
            return (val[0], True)

        elif val[1].lower() == 'false':
            return (val[0], False)

        # Return If Can't Convert
        return val

    # Process Raw Config File
    for line in read_file(path, typ='list'):
        # Pass On Blank Lines and Comments
        if not line or not line.strip() or line.startswith('#'):
            pass

        else:
            tupl = (line.split('=', 1)[0].strip(), line.split('=', 1)[1].strip())

            # Find Mandatory Options
            if tupl[0] in mandatory:
                if tupl not in mand:
                    mand.add(convert_value(tupl))
                else:
                    sys.exit('Error: Config File `' + path + '` Has Duplicate Entries For `' + tupl[0] + '`!')

            # Find Optional Options
            elif tupl[0] in optional:
                if tupl not in opt:
                    opt.add(convert_value(tupl))
                else:
                    sys.exit('Error: Config File `' + path + '` Has Duplicate Entries For `' + tupl[0] + '`!')

            # Find Extra Options
            else:
                extra.add(tupl)

    # Create and Return Config Dict
    if len(mand) == len(mandatory):
        return dict(set((mand | opt)))

    else:
        missing = len(mandatory) - len(mand)
        sys.exit('Error: Config File `' + path + '` Is Missing ' + str(missing) + ' Mandatory Values!')
