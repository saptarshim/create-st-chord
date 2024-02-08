import argparse
import sys
#from process_state_machine import main
import process_state_machine as sm

def main():
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
    
    sm.main(input_file, output_file)

if __name__ == "__main__":
    # Entry point of the script
    #import pdb; 
    #pdb.set_trace()  # Set breakpoint
    main()