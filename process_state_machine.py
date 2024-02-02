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
from tools import get_next_line_index, preproces_each_line


def get_st_chord_statemachine(processed_lines, chord_first):
    
    st_lyric_list = []

    next_index = 0

    for index, info in enumerate(processed_lines):

        if index != next_index:
            continue

        current_state = info[1] 

        while current_state != LINE_STATE['EXIT']:
            
            if current_state == LINE_STATE['CHORD']:
                chord_line = info[2]
                if chord_first == True:
                    lyric_info, next_index = get_next_line_index(index+1, processed_lines, LINE_STATE['LYRIC'])
                    lyric_line = lyric_info[2]

                    mylist = create_chord_list(chord_line)
                    st_chord = create_ST_lyrics_line_from_list(mylist,lyric_line)    
                current_state = LINE_STATE['EXIT']
                
            elif current_state == LINE_STATE['LYRIC']:
                lyric_line = info[2]
                if chord_first == False:
                    chord_info, next_index = get_next_line_index(index+1, processed_lines, LINE_STATE['CHORD'])
                    chord_line = lyric_info[2]
                    mylist = create_chord_list(chord_line)
                    st_chord = create_ST_lyrics_line_from_list(mylist,lyric_line)
                
                current_state = LINE_STATE['EXIT']
                
            elif current_state == LINE_STATE['BLANK']:
                st_chord = '\n'
                current_state = LINE_STATE['EXIT']
                new_info, next_index = get_next_line_index(index+1, processed_lines, LINE_STATE['ANY'])
    
            elif current_state == LINE_STATE['COMMENT']:
                st_chord = info[2]
                current_state = LINE_STATE['EXIT']
                new_info, next_index = get_next_line_index(index+1, processed_lines, LINE_STATE['ANY'])

            elif current_state == LINE_STATE['EXIT']:
                break
        
        st_lyric_list.append(st_chord)

    return st_lyric_list


def test():
    input_file = 'input.txt'
    output_file = 'output.txt' 
    
    lines = get_lines(input_file)
    
    processed_lines = preproces_each_line(lines)
    chord_first = chord_or_lyric_first(processed_lines)
    st_chord = get_st_chord_statemachine(processed_lines, chord_first)
    #print(st_chord)
    write_lines(st_chord, output_file)




test()