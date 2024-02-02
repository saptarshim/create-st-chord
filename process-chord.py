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
from tools import get_next_line, preproces_each_line



def check_if_this_chord_line(line):
    
    valid = False

    for index, char in enumerate(line):
        #print("Index=", index)
        if char == ' ':
            continue

        if char in VALID_CHORD_CHAR:
            valid = True
        else:
            valid = False
            break

    return valid

# def create_chord_lyrics_list(processed_lines):
    
#     #Do we still need this function
#     chord_and_lyric_list = [[]]

#     length = len(lines)

#     for i in range (0, length-1, 2):
#         each_line = processed_lines[i]
#         if not check_if_this_chord_line(chord_line):
#             print("This is not a chord line")
#             continue

#         #lyrics line
        
#         lyric_line = lines[i+1].strip()
#         info = [chord_line, lyric_line]
#         chord_and_lyric_list.append(info)
        
#     chord_and_lyric_list = chord_and_lyric_list[1:]
#     return chord_and_lyric_list







def get_st_chord(processed_lines):
    st_lyric_list = []
 
    # By default we will assume the input file has chord followed by lyrincs line
    chord_detected = False
    lyrics_detected = False
    chord_first = True

    # Find out the structure of the input, Does it start with Chord or Lyrics 

    for info in processed_lines:
        if info[1] == LINE_STATE['BLANK'] or info[1] == LINE_STATE['COMMENT']:
            #this is a blank or comment line so simply add it to the output
            continue
        elif info[1] == LINE_STATE['CHORD']:
            if lyrics_detected == False:
                chord_first = True
            else:
                chord_first = False
            break         
        elif info[1] == LINE_STATE['LYRIC']:
            if chord_detected == False:
                chord_first = False
            else:
                chord_first = True
        break


    processs_line_length = len(processed_lines)
    already_processed_line = False

    for index, info in enumerate(processed_lines):
        nop_line = False
        if info[1] == LINE_STATE['BLANK'] or info[1] == LINE_STATE['COMMENT']:
            if already_processed_line:
                already_processed_line = False
                continue
            #this is a blank or comment line so simply add it to the output if this is not already procssed
            st_chord = info[2]
            nop_line = True
        elif info[1] == LINE_STATE['CHORD']:
            if chord_first:
                chord_line = info[2]
                #This shpould not happen but just in case
                if index + 1 < processs_line_length:
                    next_info = processed_lines[index + 1]
                    if next_info[1] == LINE_STATE['LYRIC']:
                        lyric_line = next_info[2]
                    elif next_info[1] == LINE_STATE['BLANK'] or info[1] == LINE_STATE['COMMENT']:
                        if index + 2 < processs_line_length:
                            next_info = processed_lines[index + 2]
                            if next_info[1] == LINE_STATE['LYRIC']:
                                lyric_line = next_info[2]
                                already_processed_line = True
                            else:
                                print("Lyrics must appeear within the two lines after the chord")
                    else:
                        #Lyrics must appeear within the two lines after the chord if not abort
                        print("Lyrics must appeear within the two lines after the chord")
                else:
                    print("Lyrics Missing")
            else:
                continue                                    
        elif info[1] == LINE_STATE['LYRIC']:
            if not chord_first:
                lyric_line = info[2]
                #This shpould not happen but just in case
                if index + 1 < processs_line_length:
                    next_info = processed_lines[index + 1]
                    if next_info[1] == LINE_STATE['CHORD']:
                        chord_line = next_info[2]
                    elif next_info[1] == LINE_STATE['BLANK'] or info[1] == LINE_STATE['COMMENT']:
                        if index + 2 < processs_line_length:
                            next_info = processed_lines[index + 2]
                            if next_info[1] == LINE_STATE['CHORD']:
                                chord_line = next_info[2]
                                already_processed_line = True
                            else:
                                print("Chord must appeear within the two lines after the Lyrics")
                    else:
                        #Lyrics must appeear within the two lines after the chord if not abort
                        print("Chord must appeear within the two lines after the chord")
                else:
                        print("We have a blank line after lyrics line bad")
            else:
                continue
        else:
            print("This is bad, should not happen")
                
        if not nop_line:
            mylist = create_chord_list(chord_line)
            st_chord = create_ST_lyrics_line_from_list(mylist,lyric_line)
        
        st_lyric_list.append(st_chord)

    return st_lyric_list




# def test_all():
#     lines = get_lines()
    
#     processed_lines = preproces_each_line(lines)
#     #st_chord = get_st_chord(processed_lines)
#     st_chord = get_st_chord_statemachine(processed_lines)
#     print(st_chord)
#     write_lines(st_chord)
    
def test_line_char():
    
    lines = get_lines()
    
    line1 = lines[0].strip()
    line2 = lines[1].strip()

    #print("Line 2= ", line1, "\nLine 2 =", line2)
    if check_if_this_chord_line(line1):
        print("Line-1 is Chord Line")
    else:
        print("Line-1 is Lyrics Line")    

    if check_if_this_chord_line(line2):
        print("Line-2 is Chord Line")
    else:
        print("Line-2 is Lyrics Line")    



def test_line_processing():
    preproces_each_line(get_lines())

#test_line_processing()
#test_line_char()
#test_all()

