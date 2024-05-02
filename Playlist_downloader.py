#The Jimi Hendrix Experience - "Voodoo Child" (live) video
#https://youtu.be/qFfnlYbFEiE?si=XRGMojQVJ1CFlsAu
#Ramones - "Ramones" playlist
#https://youtube.com/playlist?list=PLBnJv6rImVe-LcbIsBXzIp6BpV6hqZnoO&si=jNymhDVGkVd3QHNn

#duplicates don't save after first one is saved

from pytube import YouTube, Playlist
from platform import system
from os import chdir, mkdir, path, environ
from math import ceil
from datetime import date
from time import localtime, strftime
from socket import create_connection


def is_internet_available():
    try:
        create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def sign_police(string):
    charlist = [a for a in string]
    i = 0
    while i < len(charlist):
        if charlist[i] in ["<", ">", ":", "\\", "/", "|", "?", "*"]:
            charlist.pop(i)
        else:
            i += 1
    
    policedstring = "".join(charlist)

    if string != policedstring:
        print(f"{string} - invalid title. Save name will not contain illegal signs")
    return policedstring

def zeros_at_beginning(index, playlist_len):
    """
    index - int
    playlist_len - int

    if playlist_len < 10:
        return "0"
    digits_of_biggest_number = len(str(playlist_len))
    digits_of_index = len(str(index))
    gg = digits_of_biggest_number - digits_of_index
    return gg * "0"
    """
    return (playlist_len < 10) * "0" + (playlist_len >= 10) *(len(str(playlist_len)) - len(str(index))) * "0"       #I'm genuinely sorry

def spaces(integer):
    integer = str(integer)
    result = ''
    while len(integer) > 3:
        result = integer[-3:] + " " + result
        integer = integer[:-3]

    result = integer + " " + result 
    return result

def GetDesktopPathAndSlashsys():
    if system() == "Darwin":
        return [environ["HOME"] + "/Desktop", r"/"]
    elif system() == "Windows":
        return [environ["USERPROFILE"] + r"\\Desktop", r"\\"]
    else:
        raise Exception("This is not Windows or MACos, sorry")

def ReadActionType():
    inputRAT = ""
    while inputRAT not in ["s", "p", "e"]:
        inputRAT = input("What do You want to download? (s - single video, p - playlist, e - extracted playlist data)\n>>").lower()
    return inputRAT

def ReadSaveExtension():
    inputRSE = ""
    while inputRSE not in ["a", "v"]:
        inputRSE = input("What format do You want to save as? (a - audio, v - video)\n>>").lower()

    if inputRSE == "a":
        return ".mp3"
    else:  #elif inputRSE == "v":
        return ".mp4"

def ReadNumbered(min_el_index):
    inputNUM = " "
    while True:
        if min_el_index != 0:
            inputNUM = input("Do You want elements to be numbered? (Enter - starting on 1, integer - starting on integer, n - no, f - starting from element's number in playlist, r - reverse)\n>>").lower()
            if inputNUM == "f":
                return min_el_index + 1
        else:
            inputNUM = input("Do You want elements to be numbered? (Enter - starting on 1, integer - starting on integer, n - no, r - reverse)\n>>").lower()
        if inputNUM == "" or inputNUM == "y":
            return 1
        if inputNUM == "r":
            return f"r1"
        if inputNUM == "n":
            return -1
        if inputNUM.isdigit():
            return int(inputNUM)

def ReadNumOfTracks(playlist_len):
    num = input("How to download the elements? (Enter - all, integer number - number of elements from start, f - starting from element...)\n>>").lower()
    if num == '':
        return [0, playlist_len]
    
    elif num == 'f':
        start = input("Starting from element:\n>>")
        if not start.isdigit():
            print("Starting from the beginning.")
            start = 0
        elif int(start) > playlist_len or int(start) < 1:
            print("Starting from the beginning.")
            start = 0
        else:
            start = int(start) - 1

        end = input("Ending on element:\n>>")  
        if not end.isdigit():
            print("Ending at the end.")
            end = playlist_len
        elif int(end) < start or int(end) > playlist_len:
            print("Ending at the end.")
            end = playlist_len
        else:
            end = int(end)

        return (start, end)

        
    elif num.isdigit() and int(num) <= playlist_len:
        return [0, int(num)]
    
    elif num.isdigit() and int(num) > playlist_len:
        print("Number inputted by You is too big! Downloading all the tracks.\n")
        return [0, playlist_len]
    
    else:
        print("Downloading whole playlist.\n")
        return [0, playlist_len]
    
def ReadExtractWriteOrder():
    order = ""
    while order not in ["a", "d"]:
        order = input("In what order do You want to write elements to file? (a - ascending, d - descending)\n>>").lower()
    return "asc"*(order=="a") + "desc"*(order=="d")

def NameYourFile(lenofcutlist, policedtitle, ext):
    if lenofcutlist[0].isdigit():
        lens = int(lenofcutlist[0])
    else:
        lens = len(lenofcutlist[0])

    if lenofcutlist[1].isdigit():
        lene = int(lenofcutlist[1])
    else:
        lene = len(lenofcutlist[1])

    try:
        if lens != 0 and lene != 0:
            return f"{policedtitle[lens:-lene]}{ext}"
        elif lens != 0:
            return f"{policedtitle[lens:]}{ext}"
        elif lene != 0:
            return f"{policedtitle[:-lene]}{ext}"
        elif lens == 0 and lene == 0:
            return f"{policedtitle}{ext}"
    except:
        print("Something is not a-okay! Couldn't change the name, You have to do it yourself, sorry")
        return f"We_have_a_problem_Chief{ext}"

def ReadCutLens():
    inputSC = " "
    listreturn = ["", ""]
    while inputSC not in ["", "s", "b", "e"]:
        inputSC = input("Do You want to cut names of all elements? (Enter - no, s - at the start, e - at the end, b - both)\n>>").lower()

    if inputSC == "s":
        listreturn[0] = str(input("Input the string or length You want to cut at the start:\n>>"))
    elif inputSC == "e":
        listreturn[1] = str(input("Input the string or length You want to cut at the ending:\n>>"))
    elif inputSC == "b":
        listreturn[0] = str(input("Input the string or length You want to cut at the start:\n>>"))
        listreturn[1] = str(input("Input the string or length You want to cut at the ending:\n>>"))

    return listreturn

def SaveSingle(extension, savepath, slashsys):
    try:
        if not is_internet_available():
            print("Internet connection failed.\n\n")
            return
        vid = YouTube(str(input("Enter the URL of the video You want to download: \n>> "))) 
    except:
        print("URL incorrect\n")
        return

    try:
        if extension == ".mp3":
            get_file = vid.streams.get_audio_only()
        elif extension == ".mp4":
            get_file = vid.streams.filter(res = str(vid.streams.get_highest_resolution()).split()[3][5:-1]).first()
    except:
        if not is_internet_available():
            print("Internet connection failed.\n\n")
            return
        print("A problem has occurred. That video might be age restricted or something has gone wrong.")

    titlevar = sign_police(vid.title)
    finalfilename = titlevar + extension
    i = 1
    while path.exists(savepath + slashsys + finalfilename):
        finalfilename = finalfilename[:-len(extension)] + "_d"*i + extension
        i += 1

    try:
        get_file.download(output_path=savepath, filename=finalfilename) 
        print("\n" + finalfilename + " has been successfully downloaded")
    except:
        pass
    #print("Something is not a-okay! Couldn't change the name, You have to do it yourself, sorry")

def SavePlaylist(extension, savepath, slashsys):
    try:
        if not is_internet_available():
            print("Internet connection failed.\n\n")
            return
        playlist = Playlist(str(input("Enter the URL of the playlist You want to download: \n>>")))
        playlist_list = [YouTube(el) for el in playlist.video_urls]
    except:
        print("URL incorrect\n")
        return

    playlist_len = len(playlist_list)
    first_and_last_index = ReadNumOfTracks(playlist_len)
    numbered = ReadNumbered(first_and_last_index[0])

    if isinstance(numbered, str) and numbered[0] == "r":
        first_and_last_index[0] = playlist_len - first_and_last_index[0] - 1
        first_and_last_index[1] = playlist_len - first_and_last_index[1] - 1
        numbered = int(numbered[1:])

    cutlen = ReadCutLens()

    if not is_internet_available():
        print("Internet connection failed.\n\n")
        return
    
    titlevar = sign_police(playlist.title)
    while path.exists(savepath + slashsys + titlevar):
        titlevar += "_d"
    mkdir(titlevar)
    chdir(titlevar)

    print("Downloading...")
    for index in range(first_and_last_index[0], first_and_last_index[1], 1-2*(first_and_last_index[0]>first_and_last_index[1])):
        vid = playlist_list[index]
        if not is_internet_available():
            print("Internet connection failed.\n\n")
            return
        titlevar = sign_police(vid.title)
        fileindex = (zeros_at_beginning(numbered, playlist_len) + f"{numbered}. ") * (numbered >= 0)
        numbered += 1
        finalfilename = fileindex + NameYourFile(cutlen, titlevar, extension)

        try:
            if extension == ".mp3":
                get_file = vid.streams.get_audio_only()
            elif extension == ".mp4":
                get_file = vid.streams.filter(res = str(vid.streams.get_highest_resolution()).split()[3][5:-1]).first()

            get_file.download(filename=finalfilename)            
            print(finalfilename)

        except:
            if not is_internet_available():
                print("Internet connection failed.\n\n")
                return
            print(f"{titlevar} is probably age restricted or something has gone wrong. Here's a link: {playlist_list[index]}")



    titlevar = sign_police(playlist.title)
    print("\n" + titlevar + " has been successfully downloaded")

def ExtractPlaylistData(savepath, slashsys):
    try:
        link = str(input("Enter the URL of the playlist You want to extract data from: \n>>"))
        if not is_internet_available():
            print("Internet connection failed.\n\n")
            return
        playlist = Playlist(link)
        playlist_list = [YouTube(el) for el in playlist.video_urls]
    except:
        print("URL incorrect\n")
        return
    
    titlevar = sign_police(playlist.title) + "_data"

    playlist_len = len(playlist_list)
    halfway = ceil(playlist_len/2)
    exception_count = 0
    write_order = ReadExtractWriteOrder()
    if write_order == "asc":
        start_index = 0
        end_index = playlist_len
    else:
        start_index = playlist_len - 1
        end_index = 0

    calendarium = str(date.today())
    current_time = strftime("%H:%M:%S", localtime())
    
    if not path.exists(savepath + slashsys + titlevar):
        mkdir(titlevar)
    chdir(titlevar)

    if not is_internet_available():
        print("Internet connection failed.\n\n")
        return

    with open(f"{titlevar}_extract_{calendarium[:4]}{calendarium[5:7]}{calendarium[8:10]}{current_time[:2]}{current_time[3:5]}{current_time[6:8]}{write_order}.txt", "w") as f:
        f.write(f"Playlist name: \t\t\t{playlist.title}\n")
        f.write(f"Playlist's url:\t\t\t{link}\n")
        f.write(f"Playlist's owner: \t\t{playlist.owner}\n")
        f.write(f"Owner's URL: \t\t\t{playlist.owner_url}\n")
        #f.write(f"Playlist last updated on: \t{playlist.last_updated}\n")
        f.write(f"Time of this data extract: \t{calendarium}, {current_time} \n")
        try:
            f.write(f"Playlist views so far: \t\t{spaces(playlist.views)}\n")
        except:
            f.write(f"Playlist views so far: \t\t*Option disabled, sorry*\n")
        f.write(f"Current playlist length: \t{playlist_len}\n\n\n\n\n")

        print("Downloading...")
        for index in range(start_index, end_index, 1-2*(end_index==0)):
            if index == halfway:
                print("We're halfway there!")
            #element = YouTube(playlist_list[index])
            element = playlist_list[index]
            if not is_internet_available():
                print("Internet connection failed.\n\n")
                return
            try:
                f.write(f"{playlist_len - index}. {element.title}\n")
                f.write(f"Views: {spaces(element.views)}\n")
                f.write(f"{playlist_list[index]}\n\n")
            except:
                if not is_internet_available():
                    print("Internet connection failed.\n\n")
                    return
                exception_count += 1
                f.write(f"{playlist_len - index}. An error has occurred when trying to download data of a video with URL: {playlist_list[index]}\n\n")

        if exception_count == 0:
            f.write("\n\n\n\nNo errors have occurred during extraction")
        else:
            f.write(f"Number of errors during extraction: {exception_count}")
            
    if not is_internet_available():
        print("Internet connection failed.\n\n")
        return
    print("\n" + playlist.title + " data has been successfully extracted to Your desktop!")
    if exception_count == 0:
        print("No errors have occurred during extraction")
    else:
        print(f"Number of errors during extraction: {exception_count}")


slashsys = GetDesktopPathAndSlashsys()[1]

while True:
    savepath = GetDesktopPathAndSlashsys()[0]
    chdir(savepath)
    action_type = ReadActionType()

    if action_type == "e":
        ExtractPlaylistData(savepath, slashsys)

    else:
        extension = ReadSaveExtension()
        if action_type == "s":
            SaveSingle(extension, savepath, slashsys)
        elif action_type == "p":
            SavePlaylist(extension, savepath, slashsys)


    again = " "
    while again not in ["", "y", "e"]:
        again = input("\nWhat now? (Enter - run program again, e - end program)\n>>")
    if again == "e":
        print()
        break
