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

from global_def import VALID_CHORD_CHAR, VALID_CHORD_MODIFIER, LINE_STATE

from tools import get_lines, write_lines, check_if_this_chord_line, chord_or_lyric_first
from tools import create_chord_list, create_ST_lyrics_line_from_list
from tools import get_next_line_index, preproces_each_line, postproces_each_line


def get_st_chord_statemachine(processed_lines, chord_first):
    
    st_lyric_list = []

    next_index = 0

    for index, info in enumerate(processed_lines):

        skip_line = False

        if index != next_index:
            continue

        current_state = info[1] 
        exit_counter = 0


        while current_state != LINE_STATE['EXIT']:
            exit_counter += 1
            if exit_counter == 100:
                print("Inifite loop detector")
                break

            lyric_info = None 
            next_index = None    
            chord_info = None
            if current_state == LINE_STATE['CHORD']:
                if chord_first == True:
                    chord_line = info[2]
                    lyric_info, next_index = get_next_line_index(index + 1, processed_lines, LINE_STATE['LYRIC'])
                    
                    if lyric_info != None or next_index != None:
                        lyric_line = lyric_info[2]
                        mylist = create_chord_list(chord_line)
                        st_chord = create_ST_lyrics_line_from_list(mylist,lyric_line)
                        current_state = LINE_STATE['EXIT']
                        new_info, next_index = get_next_line_index(next_index + 1, processed_lines, LINE_STATE['ANY'])
                            
                    else:
                        print("Index = ", index, "  CHORD:Somethinh went Wrong while fethching next line")
                else:
                    current_state = LINE_STATE['SKIPLINE']
                    new_info, next_index = get_next_line_index(index + 1, processed_lines, LINE_STATE['ANY'])    
                
            elif current_state == LINE_STATE['LYRIC']:
                lyric_line = info[2]
                if chord_first == False:
                    lyric_line = info[2]
                    chord_info, next_index = get_next_line_index(index + 1, processed_lines, LINE_STATE['CHORD'])
                    if chord_info != None or next_index != None:
                        chord_line = chord_info[2]
                        mylist = create_chord_list(chord_line)
                        st_chord = create_ST_lyrics_line_from_list(mylist,lyric_line)
                        current_state = LINE_STATE['EXIT']
                        new_info, next_index = get_next_line_index(next_index + 1, processed_lines, LINE_STATE['ANY'])
                    else:
                        print("Index = ", index, "  LYRIC:Somethinh went Wrong while fethching next line")
                else:
                    current_state = LINE_STATE['SKIPLINE']
                    new_info, next_index = get_next_line_index(index + 1, processed_lines, LINE_STATE['ANY'])
                    

            elif current_state == LINE_STATE['BLANK']:
                st_chord = '\n'
                new_info, next_index = get_next_line_index(index + 1, processed_lines, LINE_STATE['ANY'])
                if new_info == None or next_index == None:
                     print("Index = ", index, "  BLANK:Somethinh went Wrong while fethching next line")
                
                current_state = LINE_STATE['EXIT']
    
            elif current_state == LINE_STATE['COMMENT']:
                st_chord = info[2]
                new_info, next_index = get_next_line_index(index + 1, processed_lines, LINE_STATE['ANY'])
                if new_info == None or next_index == None:
                     print("Index = ", index, "  COMMENT: Somethinh went Wrong while fethching next line")
                
                current_state = LINE_STATE['EXIT']
            elif current_state == LINE_STATE['SKIPLINE']:
                current_state = LINE_STATE['EXIT']
                new_info, next_index = get_next_line_index(index + 1, processed_lines, LINE_STATE['ANY'])
                skip_line = True    

            elif current_state == LINE_STATE['EXIT']:
                break
        
        if new_info == None and next_index == None:
            # We have reached the end of file and no more line to process
            print("Done prcessig the entire file")

        if not skip_line:
            st_lyric_list.append(st_chord)
    
    print("Exiting State Machine")
    return st_lyric_list

def test_get_next_line_index():
    
    input_file = 'input.txt'
    output_file = 'output.txt' 
    
    lines = get_lines(input_file)
    processed_lines = preproces_each_line(lines)

    for index, info in enumerate(processed_lines):
        new_info, next_index = get_next_line_index(index+1, processed_lines, LINE_STATE['ANY'])
        print("Index = ", next_index, "\n", new_info)

    
def main(input_file, output_file):
    
    lines = get_lines(input_file)

    #Make sure we got data toprocess
    if lines == None:
        print("Input Error")
        return
    
    processed_lines = preproces_each_line(lines)
    chord_first = chord_or_lyric_first(processed_lines)
    st_chord = get_st_chord_statemachine(processed_lines, chord_first)
    #print(st_chord)
    st_chord = postproces_each_line(st_chord)

    write_lines(st_chord, output_file)

#input_file = 'input.txt'
#output_file = 'output.txt' 
#main(input_file, output_file)
