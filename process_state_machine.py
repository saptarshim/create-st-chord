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

import global_def





def get_st_chord_statemachine(processed_lines):
    
    st_lyric_list = []

    chord_first = chord_or_lyric_first(processed_lines)
    
    next_index = 0

    for index, info in enumerate(processed_lines):

        if index != next_index:
            continue

        current_state = LINE_STATE['INIT'] 

        while current_state != LINE_STATE['EXIT']:
            
            if current_state == LINE_STATE['INIT']:
                if info[1] == LINE_STATE['BLANK']:
                    current_state = LINE_STATE['BLANK']
                elif info[1] == LINE_STATE['COMMENT']:
                    current_state = LINE_STATE['COMMENT']
                elif info[1] == LINE_STATE['CHORD']:
                    current_state = LINE_STATE['CHORD']
                elif info[1] == LINE_STATE['LYRIC']:
                    current_state = LINE_STATE['LYRIC']
                else: 
                    current_state = LINE_STATE['EXIT']
                
            elif current_state == LINE_STATE['CHORD']:
                chord_line = info[2]
                if chord_first == True:
                    lyric_info, next_index = get_next_line(index+1, processed_lines, LINE_STATE['LYRIC'])
                    lyric_line = lyric_info[2]

                    mylist = create_chord_list(chord_line)
                    st_chord = create_ST_lyrics_line_from_list(mylist,lyric_line)    
                current_state = LINE_STATE['EXIT']
                
            elif current_state == LINE_STATE['LYRIC']:
                lyric_line = info[2]
                if chord_first == False:
                    chord_info, next_index = get_next_line(index+1, processed_lines, LINE_STATE['CHORD'])
                    chord_line = lyric_info[2]
                    mylist = create_chord_list(chord_line)
                    st_chord = create_ST_lyrics_line_from_list(mylist,lyric_line)
                
                current_state = LINE_STATE['EXIT']
                
            elif current_state == LINE_STATE['BLANK']:
                st_chord = '\n'
                next_index = index + 1
                current_state = LINE_STATE['EXIT']
                
            elif current_state == LINE_STATE['COMMENT']:
                st_chord = info[2]
                next_index = index + 1
                current_state = LINE_STATE['EXIT']
            elif current_state == LINE_STATE['EXIT']:
                break
        
        st_lyric_list.append(st_chord)

    return st_lyric_list
