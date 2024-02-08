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


# TODO:
#   1.Write Test for each function to make sure they are solid



from global_def import VALID_CHORD_CHAR, VALID_CHORD_MODIFIER, LINE_STATE

# Define a custom exception class
class CustomError(Exception):
    def __init__(self, message="A custom error occurred"):
        self.message = message
        super().__init__(self.message)

# Function that raises the custom exception
def error_function(value):
    if value < 0:
        raise CustomError("Value should be non-negative")
    




def chord_or_lyric_first(processed_lines):
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

    return chord_first


def get_lines(input_file_txt):
    input_file = input_file_txt
    lines = None
    try:
        # Read text from the input file
        with open(input_file, 'r') as file:
            lines = file.readlines()
            
    except FileNotFoundError:
        print("Error: Input file not found.")
    except Exception as e:
        print("An error occurred:", str(e))

    return lines

def write_lines(lines, output_file_txt):
    output_file = output_file_txt
    try:
        output = open(output_file, 'w')

        for line in lines:
            output.write(line)

    except FileNotFoundError:
        print("Error: Output file not found.")
    except Exception as e:
        print("While writing An error occurred:", str(e))


def check_if_this_chord_line(line):
    
    valid = False

    for char in line:
        #print("Index=", index)
        if char == ' ':
            continue

        if (char in VALID_CHORD_CHAR) or (char in VALID_CHORD_MODIFIER):
            valid = True
        elif char == "\n":
            if valid:
                valid = True
        else:    
            valid = False
            break

    return valid


def preproces_each_line(lines):
    
    #Line that starts with # will be simply copied back to the output without any change 
    
    #line_info is a list that has the following element
    # [0]: Line Number
    # [1]: Line type; C: Chord; L:Lyrics; B:Blank; H:Comment
    # [2]: Line from the input file

    # The list processedlines will contain line_info for each line item present in the input file
      
    processedlines = [[]]

    length = len(lines)

    for i in range (0, length, 1):
        #line = lines[i].strip(); If you do this the leading blank will be deleted from chord line
        line = lines[i]
        if line != '\n': #If this is not a blank line then remove the \n
            line = line.rstrip("\n") # Remove any new line character at the end of the line
        if len(line.strip()) == 0 or line == '\n':
            #Check if this is a blank line
            line_info = [i,LINE_STATE['BLANK'],'\n']
        elif line[0] == '#':
            #Check if this is a comment line
            line_info = [i,LINE_STATE['COMMENT'],line]
        elif check_if_this_chord_line(line):
            #Check if this is a chord line
            line_info = [i,LINE_STATE['CHORD'],line]
        else:
            #This must be a lyrics line
            line_info = [i,LINE_STATE['LYRIC'],line]
            
        processedlines.append(line_info)

    # Remove the first empty list item, This is doesn't hapen if it's a simple list
    processedlines = processedlines[1:]
    return processedlines    

def postproces_each_line(lines):
    # Here we got a list with each line as an 
    processed_st_chord = []
    for line in lines:
        if line != "\n":
            line = line + "\n"

        processed_st_chord.append(line)
    
    return processed_st_chord


def create_chord_list(chord_line):

    chord_list = [[]]
    chord_list_count = 0

    for index, char in enumerate(chord_line):
        #print("Index=", index)
        if (char in VALID_CHORD_CHAR) or (char in VALID_CHORD_MODIFIER):

            #If this is a chord modifier treat differntly
            if char in VALID_CHORD_MODIFIER:
                #chord modifier can only happen after a valid Capital chord character 
                info = chord_list [chord_list_count]
                str = info[1]
                str = str + char
                new_info = [info[0], str]
                chord_list [chord_list_count] = new_info    
            else:
                chord_info = [index, char]
                chord_list.append(chord_info)
                chord_list_count += 1
    
    chord_list = chord_list[1:]
    return chord_list



def create_ST_lyrics_line_from_list(chord_list, lyrics_line):
    combined_chord_lyrics = ''
    lyrics_start_index = 0

    thisChord = chord_list[0]
    lyrics_end_index = thisChord[0]
    
    if thisChord[0] > 0:
        #this chord didn't start at the beging of the line
        combined_chord_lyrics = lyrics_line[0: lyrics_end_index]
    
    length = len(chord_list)
    
    if length == 1:
        chord_val = thisChord[1]
        line_to_add = lyrics_line[lyrics_end_index:]
        combined_chord_lyrics =  combined_chord_lyrics + "[" + chord_val + "]"+ line_to_add
        print(combined_chord_lyrics)
    else:
        for i in range(length):  #(length - 1)
            thisChord = chord_list[i]
            #After the last chord add the reaming lyrins at the end of the line 
            if i == (length - 1):
                #This is the last iteration
                lyrics_len = len(lyrics_line)
                if lyrics_len > lyrics_end_index:
                    chord_val = thisChord[1]
                    line_to_add = lyrics_line[lyrics_end_index: lyrics_len]
                    combined_chord_lyrics = combined_chord_lyrics + "[" + chord_val + "]"+ line_to_add
            else:
                nextChord = chord_list[i+1] # Do you need to check if this is out of bound 
                chord_val = thisChord[1]
                lyrics_start_index = thisChord[0]
                lyrics_end_index = nextChord[0]
                line_to_add = lyrics_line[lyrics_start_index:lyrics_end_index]
                combined_chord_lyrics = combined_chord_lyrics + "[" + chord_val + "]"+ line_to_add
                
    combined_chord_lyrics.strip()

    return combined_chord_lyrics


def get_next_line_index(index_after, processed_lines, line_state):

    #TODO:Validate input parameters
    
    if line_state not in LINE_STATE.values():
        print("Invalid line State supplied")
        return

    for index, info in enumerate(processed_lines):
        if index >= index_after:
            if line_state == LINE_STATE['ANY']:
                return info, index
            elif info[1] == line_state:
                return info, index
    
    # This will only hapne if a valid next line index can't be found in the above for loop
    # Calling function must explicity check the is None for invalid return
    #print("Returning None from get_next_line_index")
    # This basically means the file doesn't have any more lines to process.
    return None, None
