# importing packages 
#C:\Users\Tomek\Desktop
#Palm - "Composite" video
#https://youtu.be/yCLrXEvfsGk?si=9AuyfwbHON1Nnx7m
#Ramones - "Ramones" playlist
#https://youtube.com/playlist?list=PLBnJv6rImVe-LcbIsBXzIp6BpV6hqZnoO&si=jNymhDVGkVd3QHNn
#Trening o 17 channel ID
#UCxfsPSY-xHBDhNhKk9N10kA
#Orgrim
#UCvhsxkLSlV2L0P1YkdXk-sg


from pytube import YouTube, Playlist
from keyboard import read_key
from sys import exit
import os 

branch_link = ""
branch_format = ""
savepath = ""

if os.environ["OS"][0:7] == "Windows":
    savepath = os.environ["USERPROFILE"] + r"\\Desktop"
else:
    print("Works only for Windows, sorry!!")
    exit()

os.chdir(savepath)

print("Press s for a single download or p for playlist download")
while branch_link not in ["s", "p"]:
    branch_link = read_key()
    if branch_link in ["s", "p"]:
        print(branch_link)
        break

print("Press a to download as audio or v to download as a video")
while branch_format not in ["a", "v"]:
    branch_format = read_key()
    if branch_format in ["a", "v"]:
        print(branch_format)
        break

if branch_link == "s":
    vid = YouTube(str(input("Enter the URL of the video You want to download: \n>> "))) 
    
    if branch_format == "a":
        get_file = vid.streams.get_audio_only()
    elif branch_format == "v":
        get_file = vid.streams.filter(res = str(vid.streams.get_highest_resolution()).split()[3][5:-1]).first()
    
    out_file = get_file.download(output_path = savepath) 
 
    print(vid.title + " has been successfully downloaded")

if branch_link == "p":
    playlist_obj = Playlist(str(input("Enter the URL of the album You want to download: \n>> "))) 

    if not os.path.exists(savepath + r"\\" + playlist_obj.title):
        os.mkdir(playlist_obj.title)

    os.chdir(playlist_obj.title)
    playlist_list = playlist_obj.videos
    number_of_tracks = input("Input the number of tracks (if all press Enter): \n>> ")

    if number_of_tracks == '':
        number_of_tracks = len(playlist_list)
    elif int(number_of_tracks) > len(playlist_list):
        print("Too big number!")
        number_of_tracks = len(playlist_list)
    else:
        number_of_tracks = int(number_of_tracks)

    for index in range(number_of_tracks):
        print(f"{index+1}. {playlist_list[index].title}")
        if branch_format == "a":
            get_file = playlist_list[index].streams.get_audio_only()
        elif branch_format == "v":
            get_file = playlist_list[index].streams.filter(res = str(playlist_list[index].streams.get_highest_resolution()).split()[3][5:-1]).first()
        out_file = get_file.download(output_path=os.getcwd()) 
        try:
            os.rename(out_file, f"{index+1}. {playlist_list[index].title}.mp3")
        except:
            print("Something is not a-okay! Couldn't change the name, You have to do it yourself, sorry")

    print(playlist_obj.title + " has been successfully downloaded")

