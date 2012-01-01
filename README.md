Anglosaxon is a command line tool to parse XML files using SAX. It is designed to do simple transformations of XML files into other textual formats in a streaming format.

# Example Usage

    cat changesets.osm | anglosaxon.py -s changeset -o "changeset id=" -v id --nl

