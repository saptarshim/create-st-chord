
def create_chord_list(chord_line):
    valid_chord_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', '#','b', 'm', '7','M']
    valid_chord_modifier = ['#','b', 'm', '7','M']

    chord_list = [[]]
    chord_list_count = 0

    for index, char in enumerate(chord_line):
        #print("Index=", index)
        if char in valid_chord_char:

            #If this is a chord modifier treat differntly
            if char in valid_chord_modifier:
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

    length = len(chord_list) - 1
    for i in range(length):
        thisChord = chord_list[i]
        nextChord = chord_list[i+1]
        chord_val = thisChord[1]
        lyrics_start_index = thisChord[0]
        lyrics_end_index = nextChord[0]
        line_to_add = lyrics_line[lyrics_start_index:lyrics_end_index]
        combined_chord_lyrics = combined_chord_lyrics + "[" + chord_val + "]"+ line_to_add
        #After the last chord add the reaming lyrins at the end of the line 
        if i == (length - 1):
            #This is the last iteration
            lyrics_len = len(lyrics_line)
            if lyrics_len > lyrics_end_index:
                combined_chord_lyrics = combined_chord_lyrics + lyrics_line[lyrics_end_index: lyrics_len]
    
    combined_chord_lyrics.strip()

    return combined_chord_lyrics


def check_if_this_chord_line(line):
    valid_chord_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', '#','b', 'm', '7', 'M']
    
    valid = False

    for index, char in enumerate(line):
        #print("Index=", index)
        if char == ' ':
            continue

        if char in valid_chord_char:
            valid = True
        else:
            valid = False
            break

    return valid

def create_chord_lyrics_list(processed_lines):
    
    #Do we still need this function
    chord_and_lyric_list = [[]]

    length = len(lines)

    for i in range (0, length-1, 2):
        each_line = processed_lines[i]
        if not check_if_this_chord_line(chord_line):
            print("This is not a chord line")
            continue

        #lyrics line
        
        lyric_line = lines[i+1].strip()
        info = [chord_line, lyric_line]
        chord_and_lyric_list.append(info)
        
    chord_and_lyric_list = chord_and_lyric_list[1:]
    return chord_and_lyric_list


def get_st_chord(processed_lines):
    st_lyric_list = []
 
    # By default we will assume the input file has chord followed by lyrincs line
    chord_detected = False
    lyrics_detected = False
    chord_first = True

    # Find out the structure of the input, Does it start with Chord or Lyrics 

    for info in processed_lines:
        if info[1] == 'B' or info[1] == 'H':
            #this is a blank or comment line so simply add it to the output
            continue
        elif info[1] == 'C':
            if lyrics_detected == False:
                chord_first = True
            else:
                chord_first = False
            break         
        elif info[1] == 'L':
            if chord_detected == False:
                chord_first = False
            else:
                chord_first = True
        break


    processs_line_length = len(processed_lines)

    for index, info in enumerate(processed_lines):
        nop_line = False
        if info[1] == 'B' or info[1] == 'H':
            #this is a blank or comment line so simply add it to the output
            st_chord = info[2]
            nop_line = True
        elif info[1] == 'C':
            if chord_first:
                chord_line = info[2]
                #This shpould not happen but just in case
                if index + 1 < processs_line_length:
                    next_info = processed_lines[index + 1]
                    if next_info[1] == 'L':
                        lyric_line = next_info[2]
                    else:
                        print("We have a blank line after chord line bad")
            else:
                continue                                    
        elif info[1] == 'L':
            if not chord_first:
                lyric_line = info[2]
                #This shpould not happen but just in case
                if index + 1 < processs_line_length:
                    next_info = processed_lines[index + 1]
                    if next_info[1] == 'C':
                        chord_line = next_info[2]
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

def preproces_each_line(lines):
    
    #Line that starts with # will be simply copied back to the output without any change 
    
    #line_info is a list that has the following element
    # [0]: Line Number
    # [1]: Line type; C: Chord; L:Lyrics; B:Blank; H:Comment
    # [2]: Line from the input file

    # The list processedlines will contain line_info for each line item present in the input file
      
    processedlines = [[]]

    length = len(lines)

    for i in range (0, length-1, 1):
        line = lines[i].strip()
        
        
        if len(line) == 0:
            #Check if this is a blank line
            line_info = [i,'B','\n']
        elif line[0] == '#':
            #Check if this is a comment line
            line_info = [i,'H',line]
        elif check_if_this_chord_line(line):
            #Check if this is a chord line
            line_info = [i,'C',line]
        else:
            #This must be a lyrics line
            line_info = [i,'L',line]
            
        processedlines.append(line_info)

    processedlines = processedlines[1:]
    return processedlines    


def get_lines():
    input_file = 'input.txt'
    try:
        # Read text from the input file
        with open(input_file, 'r') as file:
            lines = file.readlines()
            
    except FileNotFoundError:
        print("Error: Input file not found.")
    except Exception as e:
        print("An error occurred:", str(e))

    return lines

def write_lines(lines):
    output_file = 'output.txt'
    try:
        output = open(output_file, 'w')

        for line in lines:
            output.write(line)
            print(line)
            output.write("\n")

    except FileNotFoundError:
        print("Error: Output file not found.")
    except Exception as e:
        print("While writing An error occurred:", str(e))



def test_all():
    lines = get_lines()
    
    processed_lines = preproces_each_line(lines)

    #chord_and_lyric_list = create_chord_lyrics_list(processed_lines)
    
    st_chord = get_st_chord(processed_lines)
    write_lines(st_chord)
    
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
test_all()

