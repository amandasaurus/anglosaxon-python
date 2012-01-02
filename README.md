Anglosaxon is a command line tool to parse XML files using SAX. It is designed to do simple transformations of XML files into other textual formats in a streaming format.

# Example Usage

    cat changesets.osm | anglosaxon.py -s changeset -o "changeset id=" -v id --nl

# Documention

``anglosaxon`` reads an xml file from stdin and writes things to stdout.

Arguments are of the form ``-s TAGNAME INSTRUCTIONS`` or ``-e TAGNAME INSTRUCTIONS``. ``-s TAGNAME`` means 'output this text when you see the open tag for TAGNAME'. ``INSTRUCTIONS`` is one or more of ``-v ATTRIBUTENAME``, ``-o RAWSTRING``, ``-V ATTRIBUTENAME DEFAULT`` or ``--nl``.

 * ``-o RAWSTRING``: Output RAWSTRING
 * ``-v ATTRIBUTENAME``: output the attribute ATTRIBUTENAME. An error is thrown if it doesn't exist. Short for 'value'.
 * ``-V ATTRIBUTENAME DEFAULT``: output the attribute ATTRIBUTENAME (like ``-v``), but if the attribute isn't there, output DEFAULTVALUE
 * ``--nl``: output a new line (``\n``), short for ``-o "\n"``.

TAGNAME can be a raw tag, like ``foo``, or it can include relative tag names, like ``bar/foo`` (to match any foo tag that's a child of a bar tag), or ``/osm/node`` (to match any node tag that's a child of an osm tag, which is a child of the root).

Likewise ``-e TAGNAME`` outputs text when it sees the end tag

