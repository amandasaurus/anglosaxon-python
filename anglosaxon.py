#! /usr/bin/python

import sys
import pprint
import xml.sax


class AngloSaxonException(Exception):
    pass

class AngloSaxonExceptionInvalidOptions(AngloSaxonException):
    pass


def parse_options(options):
    curr_start = None
    current_output_options = None
    start_functions = {}
    curr_end = None
    end_functions = {}
    while options:
        option = options.pop(0)
        if option in ('-s', '-e'):
            if len(options) == 0:
                raise AngloSaxonExceptionInvalidOptions, "Option "+option+" requires argument"
            if curr_start is not None:
                start_functions[curr_start] = current_output_options
            elif curr_end is not None:
                end_functions[curr_end] = current_output_options
            curr = options.pop(0)
            if '/' in curr:
                curr = tuple(curr.split("/"))

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
            if not ( (curr_start is not None) or (curr_end is not None) ):
                raise AngloSaxonExceptionInvalidOptions, "Attempting to use "+option+" before -s/-e"
            if not ( len(options) > 0 ):
                raise AngloSaxonExceptionInvalidOptions, "Option "+option+" requires an argument"
            value = options.pop(0)
            if option in ['-o', '-v']:
                current_output_options.append((option, value))
            elif option == '-V':
                if not ( len(options) > 0 ):
                    raise AngloSaxonExceptionInvalidOptions, "Option -V without a default option"
                default_value = options.pop(0)
                current_output_options.append((option, value, default_value))

                
    if curr_start is not None:
        start_functions[curr] = current_output_options
    elif curr_end is not None:
        end_functions[curr] = current_output_options

    return start_functions, end_functions

def class_for_function(start_functions, end_functions):
    class AngloSaxonContentHandler(xml.sax.ContentHandler):
        node_stack = []
        attributes_stack = []

        def output(self, name, attrs, function_dict):
            if name in function_dict:
                output = []
                for option in function_dict[name]:
                    if len(option) == 2:
                        type, value = option
                    elif len(option) == 3:
                        type, value, default_value = option

                    if type == '-v':
                        output.append(attrs[value])
                    elif type == '-V':
                        output.append(attrs.get(value, default_value))
                    elif type == '-o':
                        output.append(value)
                sys.stdout.write(''.join(output).encode("utf8"))

            for item in function_dict:
                if isinstance(item, basestring):
                    continue
                length = len(item)
                if length > len(self.node_stack):
                    continue
                possible_match = self.node_stack[-length:]
                # we can't go possible_match == item, because possible_match is
                # a list of unicode strings and item might be a tuple of
                # strings
                if all(possible_match[i] == item[i] for i in range(length)):
                    output = []
                    for option in function_dict[item]:
                        if len(option) == 2:
                            type, value = option
                        elif len(option) == 3:
                            type, value, default_value = option
                        
                        if type == '-o':
                            output.append(value)
                        elif type in ('-v', '-V'):
                            attrs_dict = None
                            parts = value.split("/")
                            if len(parts) == 1:
                                attrs_dict = attrs
                            else:
                                assert all(x == '..' for x in parts[:-1]) and parts[-1] != '..', "Malformed traverse %s" % value
                                assert len(parts) <= len(self.attributes_stack), "Can't go up %d levels when we're only %d in" % (len(parts), len(attributes_stack))
                                attrs_dict = self.attributes_stack[-len(parts)]
                                value = parts[-1]


                            if type == '-v':
                                output.append(attrs_dict[value])
                            elif type == '-V':
                                output.append(attrs_dict.get(value, default_value))
                            
                        elif type == '-o':
                            output.append(value)
                    sys.stdout.write(''.join(output).encode("utf8"))

        def startElement(self, name, attrs):
            self.node_stack.append(name)
            self.attributes_stack.append(attrs)
            assert len(self.node_stack) == len(self.node_stack)
            self.output(name, attrs, start_functions)

        def endElement(self, name):
            assert self.node_stack[-1] == name
            self.node_stack.pop()
            self.attributes_stack.pop()
            assert len(self.node_stack) == len(self.node_stack)
            self.output(name, None, end_functions)

    return AngloSaxonContentHandler

def parse(cls, input):
    xml.sax.parse(input, cls())

def main():
    start_functions, end_functions = parse_options(sys.argv[1:])
    cls = class_for_function(start_functions, end_functions)
    parse(cls, sys.stdin)

if __name__ == '__main__':
    main()
