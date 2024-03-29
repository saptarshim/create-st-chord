# MIT License

# Copyright (c) 2024 Saptarshi Mondal (saptarshi.mondal@gmail.com)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import argparse
import sys
#from process_state_machine import main
import process_state_machine as sm
import line as l


def main(old):
    if len(sys.argv) < 2:
        # Default value if no argument is provided
        input_file = 'input.txt'
        output_file = 'output.txt'
    elif len(sys.argv) < 3:
        #Only input is gven 
        output_file = 'output.txt'
    else:
        # Create argument parser
        parser = argparse.ArgumentParser(description='Convert Chord file to Stage Traxx format')


        # Add positional argument
        parser.add_argument('arg1', type=str, help='input file in txt format, default will be input.txt')
        parser.add_argument('arg2', type=int, help='output file name, default will be output.txt')
        #parser.get_default()
        args = parser.parse_args()
        input_file = args.arg1
        output_file = args.arg2
    
    if old:
        sm.main(input_file, output_file)
    else:
        l.STChordApp(input_file, output_file)


if __name__ == "__main__":
    # Entry point of the script
    #import pdb; 
    #pdb.set_trace()  # Set breakpoint
    main(False)
    
    