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
    digits_of_index = len(str(index+1))
    gg = digits_of_biggest_number - digits_of_index
    return gg * "0"
    """
    return (playlist_len < 10) * "0" + (playlist_len >= 10) *(len(str(playlist_len)) - len(str(index+1))) * "0"       #I'm genuinely sorry

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
        inputRAT = input("Input s for a single download, p for playlist download or e for playlist data extract\n>>").lower()
    return inputRAT

def ReadSaveExtension():
    inputRSE = ""
    while inputRSE not in ["a", "v"]:
        inputRSE = input("Input a to download as audio or v to download as a video\n>>").lower()

    if inputRSE == "a":
        return ".mp3"
    else:  #elif inputRSE == "v":
        return ".mp4"

def ReadNumbered():
    inputNUM = " "
    while True:
        inputNUM = input("Do You want elements to be numbered? (Enter - yes, r - reverse, n - no)\n>>").lower()
        if inputNUM == "" or inputNUM == "y":
            return "normal"
        if inputNUM == "r":
            return "reverse"
        if inputNUM == "n":
            return "no"

def ReadNumOfTracks(playlist_len):
    num = input("Input the number of tracks (if all press Enter): \n>> ")
    if num == '':
        return playlist_len
    elif int(num) > playlist_len:
        print("Number inputted by You is too big! Will download all the tracks.")
        return playlist_len
    else:
        return int(num)
    
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
        inputSC = input("Press Enter to not cut anything, input s to cut out at the start, e to cut at the end or b to cut both\n>>").lower()

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
        vid = YouTube(str(input("Enter the URL of the video You want to download: \n>> "))) 
    except:
        return

    try:
        if extension == ".mp3":
            get_file = vid.streams.get_audio_only()
        elif extension == ".mp4":
            get_file = vid.streams.filter(res = str(vid.streams.get_highest_resolution()).split()[3][5:-1]).first()
    except:
        print("A problem has occurred. That video might be age restricted.")

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
        playlist = Playlist(str(input("Enter the URL of the album You want to download: \n>>")))
    except:
        return
    
    titlevar = sign_police(playlist.title)

    i = 1
    while path.exists(savepath + slashsys + titlevar):
        titlevar += "_d"*i
        i += 1

    mkdir(titlevar)
    chdir(titlevar)
    playlist_list = playlist.video_urls
    number_of_tracks = ReadNumOfTracks(len(playlist_list))
    playlist_list = playlist_list[:number_of_tracks]

    playlist_len = len(playlist_list)
    numbered = ReadNumbered()
    if numbered == "reverse":
        playlist_list.reverse()
    cutlen = ReadCutLens()

    for index in range(0, number_of_tracks):
        vid = YouTube(playlist_list[index])
        titlevar = sign_police(vid.title)
        fileindex = (zeros_at_beginning(index, playlist_len) + f"{index+1}. ") * (numbered != "no")
        finalfilename = fileindex + NameYourFile(cutlen, titlevar, extension)

        try:
            if extension == ".mp3":
                get_file = vid.streams.get_audio_only()
            elif extension == ".mp4":
                get_file = vid.streams.filter(res = str(vid.streams.get_highest_resolution()).split()[3][5:-1]).first()

            get_file.download(filename=finalfilename)            
            print(finalfilename)

        except:
            print(f"{titlevar} is probably age restricted. Here's a link: {playlist_list[index]}")



    titlevar = sign_police(playlist.title)
    print("\n" + titlevar + " has been successfully downloaded")

def ExtractPlaylistData(savepath, slashsys):
    try:
        link = str(input("Enter the URL of the playlist You want to extract data from: \n>>"))
        playlist = Playlist(link)
    except:
        return
    
    titlevar = sign_police(playlist.title) + "_data"
    if not path.exists(savepath + slashsys + titlevar):
        mkdir(titlevar)

    chdir(titlevar)
    playlist_list = playlist.video_urls
    number_of_tracks = len(playlist_list)
    calendarium = str(date.today())
    current_time = strftime("%H:%M:%S", localtime())

    with open(f"{titlevar}_extract_{calendarium[:4]}{calendarium[5:7]}{calendarium[8:10]}{current_time[:2]}{current_time[3:5]}{current_time[6:8]}.txt", "w") as f:
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
        f.write(f"Current playlist length: \t{number_of_tracks}\n\n\n\n\n")

        halfway = ceil(number_of_tracks/2)
        exception_count = 0

        for index in range(number_of_tracks):
            if index == halfway:
                print("We're halfway there!")
            element = YouTube(playlist_list[index])
            try:
                f.write(f"{number_of_tracks - index}. {element.title}\n")
                f.write(f"Views: {spaces(element.views)}\n")
                f.write(f"{playlist_list[index]}\n\n")
            except:
                exception_count += 1
                f.write(f"{index}. An error has occurred when trying to download data of a video with URL: {playlist_list[index]}\n\n")

        if exception_count == 0:
            f.write("\n\n\n\nNo errors have occurred during extraction")
        else:
            f.write(f"Number of errors during extraction: {exception_count}")

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
        again = input("\nPress Enter to download another time or input e to end the program\n>>")
    if again == "e":
        print()
        break
