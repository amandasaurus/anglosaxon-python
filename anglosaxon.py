#! /usr/bin/python

import sys
import pprint
import xml.sax


options = sys.argv[1:]
curr_start = None
current_output_options = None
start_functions = {}
curr_end = None
end_functions = {}

while options:
    option = options.pop(0)
    if option in ('-s', '-e'):
        assert len(option) > 0, "Option "+option+" requires argument"
        if curr_start is not None:
            start_functions[curr_start] = current_output_options
        elif curr_end is not None:
            end_functions[curr_end] = current_output_options
        curr = options.pop(0)
        current_output_options = []
        if option == '-s':
            curr_start = curr
            curr_end = None
        elif option == '-e':
            curr_start = None
            curr_end = curr
    elif option == '--nl':
        current_output_options.append(('-o', "\n"))
    elif option in ['-o', '-v', '-V']:
        assert (curr_start is not None) or (curr_end is not None), "Attempting to use -o or -v before -s/-e"
        assert len(option) > 0, "Option "+option+" requires an argument"
        value = options.pop(0)
        if option in ['-o', '-v']:
            current_output_options.append((option, value))
        elif option == '-V':
            assert len(option) > 0, "Option -V without a default option"
            default_value = options.pop(0)
            current_output_options.append((option, value, default_value))

            
if curr_start is not None:
    start_functions[curr] = current_output_options
elif curr_end is not None:
    end_functions[curr] = current_output_options

#pprint.pprint(start_functions)
#pprint.pprint(end_functions)

class AngloSaxonContentHandler(xml.sax.ContentHandler):
    def output(self, name, attrs, function_dict):
        if name in function_dict:
            output = ""
            for option in function_dict[name]:
                if len(option) == 2:
                    type, value = option
                elif len(option) == 3:
                    type, value, default_value = option

                if type == '-v':
                    output += attrs[value]
                elif type == '-V':
                    output += attrs.get(value, default_value)
                elif type == '-o':
                    output += value
            sys.stdout.write(output.encode("utf8"))

    def startElement(self, name, attrs):
        self.output(name, attrs, start_functions)

    def endElement(self, name):
        self.output(name, None, end_functions)



xml.sax.parse(sys.stdin, AngloSaxonContentHandler())
