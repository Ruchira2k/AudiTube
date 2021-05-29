from __future__ import unicode_literals

import datetime
import youtube_dl as y_dl
import urllib.request
import re as re
import os
import glob
import subprocess
from tabulate import tabulate as tbl


print('\n                       ▲▼')
print('---------------  A u d i T u b e  ---------------\n')
while True:
    searchQuery = input("Enter Search Query : ")

    print('\nRetrieving Data...\n')
    formattedQuery = searchQuery.replace(" ", "+")

    searchLink = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + formattedQuery)
    video_ids = re.findall(r"watch\?v=(\S{11})", searchLink.read().decode())

    prevId = ""
    counter = 1
    uniqueVideoIds = []
    for i in range(0, len(video_ids)):
        if video_ids[i] != prevId:
            # print(video_ids[i])
            uniqueVideoIds.append(video_ids[i])
            prevId = video_ids[i]
            counter += 1
        if counter == 11:
            break

    videoLinks = []
    for i in uniqueVideoIds:
        link = "https://www.youtube.com/watch?v=" + i
        videoLinks.append(link)

    ydl_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'no_check_certificate': True,
        'restrictfilenames': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    displayList = []

    with y_dl.YoutubeDL(ydl_options) as ydl:
        for i in range(0, len(videoLinks)):
            info = []
            dictMeta = ydl.extract_info(videoLinks[i], download=False)
            title = dictMeta['title']
            duration = dictMeta['duration']
            formattedDuration = str(datetime.timedelta(seconds=duration))
            displayIndex = i+1
            info.extend((displayIndex, title, formattedDuration))
            displayList.append(info)
            # print(displayIndex,"-",title,"-",type(formattedDuration))

        print('\n-- Data Retrieval Complete --\n\n')
        print(tbl(displayList, headers=['OPTION', 'TITLE', 'DURATION (HH:MM:SS)'], tablefmt='github'))
        print()

        while True:
            choice = input("\nSelect a download option (1 - 10), or press 'q' to exit : ")
            if choice == 'q':
                break
            try:
                if 1 <= int(choice) <= 10:
                    print('\nDownloading & Converting Track...\n')
                    index = int(choice) - 1
                    ydl.download([videoLinks[index]])
                    print('\n-- Download & Conversion Complete --\n')
                    while True:
                        playChoice = input('Do you want to play the downloaded track ? (y/n): ').lower()
                        if playChoice != 'y' and playChoice != 'n':
                            print('Invalid input. Please try again...')
                        else:
                            break
                    if playChoice == 'y':
                        cwd = os.getcwd()
                        files = os.listdir(cwd)
                        files2 = glob.glob(cwd + '/*.mp3')
                        latest_file = max(files2, key=os.path.getctime)

                        if os.path.exists(latest_file):
                            subprocess.call(["open", latest_file])
                        break
                    elif playChoice == 'n':
                        break
                else:
                    print("Invalid input. Please try again...")
            except ValueError:
                print("Invalid input. Please try again...")

    while True:
        loopCondition = input("\nWant to continue downloading? (y/n): ")
        if loopCondition != 'y' and loopCondition != 'n':
            print('Invalid input. Please try again...')
        else:
            break

    if loopCondition == 'n':
        print('\n\n---------------    ▲▼    ---------------')
        break
    else:
        print('\n\n---------------    ▲▼    ---------------\n')

