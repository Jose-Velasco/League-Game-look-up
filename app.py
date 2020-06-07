import tkinter as tk
import requests
from PIL import Image, ImageTk

HEIGHT = 700
WIDTH = 800

# version of modules in virtualenv 4/24/19
'''
altgraph==0.16.1
certifi==2019.3.9
chardet==3.0.4
future==0.17.1
idna==2.8
macholib==1.11
pefile==2019.4.18
Pillow==6.0.0
PyInstaller==3.4
pywin32-ctypes==0.2.0
requests==2.21.0
urllib3==1.24.2
virtualenv==16.2.0
'''
# i used pyinstaller to make it into a exe file to run even if user does not have python installed

## APIkey will change evry 24hr
# get info from riot games's api server for leauge of legnds
# https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key=RGAPI-ffc5b624-e94b-45c4-a8a6-0cb1ec485360     to get summoner id inorder to acceses other data
# https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}?api_key=RGAPI-ffc5b624-e94b-45c4-a8a6-0cb1ec485360       use ID to get ranked info
#  Possable bug( the program might be just hiding widgets and everytime the summoner_id is called it creates a new widget on top of old one)
# bug validdate API key from user if key is not vaild or else user has to restart program and input new key since search function will always output error message
# (possable if send a http request to api using key and if it returns a json file then contine program  if it returns a error then key is not vaild and have user input key again)


# use api key and id to get ranked info
def summoner_info(Id, lol_key):
    url_info = 'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/%s?api_key=%s' %(Id, lol_key)
    #send http resond with required info
    response_info = requests.get(url_info)
    #store data responce into info variable to parse
    info = response_info.json()
    que_type = info[0]['queueType']

    # check to see were if the data needed is in json idex of 0 or one
    if len(info) == 2:
        que_type2 = info[1]['queueType']
        if que_type == 'RANKED_SOLO_5x5':
            #parseing json for data that is needed
            solo_tier = info[0]['tier']
            solo_rank = info[0]['rank']
            summonerName = info[0]['summonerName']
            solo_wins = info[0]['wins']
            solo_loss = info[0]['losses']                

            final_list = [solo_tier, solo_rank, summonerName, solo_wins, solo_loss]
        if que_type2 == 'RANKED_SOLO_5x5':
            solo_tier = info[1]['tier']
            solo_rank = info[1]['rank']
            summonerName = info[1]['summonerName']
            solo_wins = info[1]['wins']
            solo_loss = info[1]['losses']

            final_list = [solo_tier, solo_rank, summonerName, solo_wins, solo_loss]

    # if ID's json file only has one element  
    if len(info) == 1:
        if que_type == 'RANKED_SOLO_5x5':
            solo_tier = info[0]['tier']
            solo_rank = info[0]['rank']
            summonerName = info[0]['summonerName']
            solo_wins = info[0]['wins']
            solo_loss = info[0]['losses']                
 
            final_list = [solo_tier, solo_rank, summonerName, solo_wins, solo_loss]
 

    return final_list



def summoner_id(name, lol_Key):
    ## key will change every 24 hrs
    ## if summoner(ID) has not been placed in current or summoner does not exist return error message
    try:
        #to erase error messge form middle of screen
        label.config(text='')
        Repack()


        
        lol_key = lol_Key
        url_id = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s?api_key=%s' %(name, lol_key)
        response = requests.get(url_id)
        summoner = response.json()
        level = summoner['summonerLevel']
        Id = summoner['id']
    
        stats_list = summoner_info(Id, lol_key)
            
        stats_list.append(level)
        stats_text(stats_list)

        rank_name = stats_list[0]

        Open_image(rank_name)

    # if sommuner does not exist or summoner has not been placed in corrent soloQ season give error message
    except:
        # remove old stats from screen 
        name_label.place_forget()
        rank_icon.place_forget()
        winnum_label.place_forget()
        lossnum_label.place_forget()
        tier_label.place_forget()
        levelnum_label.place_forget()
        
        label['text'] = 'There was a problem retrieving soloque stats'


# use PIL(pill module) to open image and display image evrytime function is called
def Open_image(rank_name):
    size = int(lower_frame.winfo_height()*0.45)
    #images are all in img folder (img/XXXXXX.png)
    img = ImageTk.PhotoImage(Image.open('img/Emblem_'+rank_name+'.png').resize((size,size)))
    rank_icon.delete("all")
    rank_icon.create_image(0,0, anchor='nw', image=img)
    rank_icon.image = img

# used to  replace widget if errror destryoed them
def Repack():
    rank_icon.place(relx=0.59, rely=0.02, relwidth=1, relheight=0.6)
    name_label.place(relx=0.03, rely=0.02, relwidth=.57, relheight=0.14)
    winnum_label.place(relx=0.09, rely=0.26, relwidth=0.18, relheight=0.09)
    lossnum_label.place(relx=0.35, rely=0.26, relwidth=0.18, relheight=0.09)
    tier_label.place(relx=0.55, rely=0.49, relwidth=0.44, relheight=0.09)
    levelnum_label.place(relx=0.08, rely=0.63, relwidth=0.30, relheight=0.25)

# used to display stats as text in thier widgets    
def stats_text(stats_list):
    # make font dynamic based on window size
    font_size = int(lower_frame.winfo_width()*0.06)
    #name_label['text'] = stats_list[2]
    # so rank and tier number are displayed together
    tier_str = '%s %s' %(stats_list[0], stats_list[1])
 
    # create legend for each number
    win_label = tk.Label(lower_frame, text='WINS', font=('Courier', int(font_size*.65), 'bold'), fg='#42FF00', bd=0, highlightthickness=0, bg='white')
    win_label.place(relx=0.11, rely=0.18, relwidth=0.15, relheight=0.09)
    
    loss_label = tk.Label(lower_frame, text='LOSSES', font=('Courier', int(font_size*.65), 'bold'), fg='red', bd=0, highlightthickness=0, bg='white')
    loss_label.place(relx=0.35, rely=0.18, relwidth=0.18, relheight=0.09)

    level_label = tk.Label(lower_frame, text='LEVEL', font=('Courier', int(font_size*.40), 'bold'), fg='#676767', bd=0, highlightthickness=0, bg='white')
    level_label.place(relx=0.12, rely=0.49, relwidth=0.18, relheight=0.09)


    #set access each widegt and change their text and adjust thier fonts based on screen size and make them smaller by *
    name_label['text'] = stats_list[2]
    name_label['font'] = ('Courier', font_size,'bold')
    winnum_label['text'] = stats_list[3]
    winnum_label['font'] = ('Courier', int(font_size*.40), 'bold')
    lossnum_label['text'] = stats_list[4]
    lossnum_label['font'] = ('Courier', int(font_size*.40), 'bold')
    tier_label['text'] = tier_str
    tier_label['font'] = ('Courier', int(font_size*.70), 'bold')
    levelnum_label['text'] = stats_list[5]
    levelnum_label['font'] = ('Courier', int(font_size*1.50), 'bold')

# used to create a key and change its value once called in a function
class KeyAPI:
    def __init__(self, newkey = 'empty key'):
        self.apiKey = newkey
    
    def setApiKey(self, newkey):
        self.apiKey = newkey
    def showKey(self):
        return self.apiKey
        
# get entry input form user and save it as lol_key to be used to hit riot games's api
def destroy_apiFrame(apiKey):

    lol_key.setApiKey(apiKey)

    # destroy first screen
    api_frame.destroy()



# ker variable
lol_key = KeyAPI()


root =  tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()



# open image from images folder
background_image = ImageTk.PhotoImage(Image.open('img/Arcade_Art_3840x1080.jpg'))
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1 ,relheight=1)


frame = tk.Frame(root, bg='#f2d500', bd=5)
frame.place(relx=0.5, rely=0.85, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=('Courier', 20))
entry.place(relwidth=0.65, relheight=1)

# use api key enter from first screen to hit api
# get user input and look that summoner up
button = tk.Button(frame, text="Search", font=('Courier', 18), command=lambda: summoner_id(entry.get(), lol_key.showKey()))
button.place(relx=0.7, relwidth=0.3, relheight=1)

lower_frame = tk.Frame(root, bg='#00cbef', bd=7)
lower_frame.place(relx=0.5, rely=0.8, relwidth=0.80, relheight=0.75, anchor='s')

label = tk.Label(lower_frame)
label.config(bg='white')
label.place(relwidth=1, relheight=1)


rank_icon = tk.Canvas(label, bg='white', bd=0, highlightthickness=0)
rank_icon.place(relx=0.59, rely=0.02, relwidth=1, relheight=0.6)



name_label = tk.Label(lower_frame, bd=0, highlightthickness=0, bg='white')
name_label.place(relx=0.03, rely=0.02, relwidth=.57, relheight=0.14)



winnum_label = tk.Label(lower_frame, fg='#676767', bd=0, highlightthickness=0, bg='white')
winnum_label.place(relx=0.09, rely=0.26, relwidth=0.18, relheight=0.09)



lossnum_label = tk.Label(lower_frame, fg='#676767', bd=0, highlightthickness=0, bg='white')
lossnum_label.place(relx=0.35, rely=0.26, relwidth=0.18, relheight=0.09)

tier_label = tk.Label(lower_frame, fg='#3E3E3E', bd=0, highlightthickness=0, bg='white')
tier_label.place(relx=0.55, rely=0.49, relwidth=0.44, relheight=0.09)



levelnum_label = tk.Label(lower_frame, fg='#3E3E3E', bd=0, highlightthickness=0, bg='white')
levelnum_label.place(relx=0.08, rely=0.63, relwidth=0.30, relheight=0.25)


api_frame = tk.Frame(root)
api_frame.place(relwidth=1, relheight=1)

apibg_label = tk.Label(api_frame, image=background_image)
apibg_label.place(relwidth=1, relheight=1)

api_entry = tk.Entry(api_frame, font=('Courier', 19))
api_entry.place(relx=0.10, rely=0.45, relwidth=0.50, relheight=.09)

apiEnter_label = tk.Label(api_frame, text="Enter API key:",font=('Courier', 19))
apiEnter_label.place(relx=0.10, rely=0.39, relwidth=0.27, relheight=.04)

apiInfo_label = tk.Label(api_frame, text="get an API key: https://developer.riotgames.com/",font=('Courier', 11))
apiInfo_label.place(relx=0.10, rely=0.57, relwidth=0.56, relheight=.04)

# get user input(hopefully a the right key) and destroy first screen
api_button = tk.Button(api_frame, text='Enter',font=('Courier', 18), command=lambda: destroy_apiFrame(api_entry.get()))
api_button.place(relx=0.65, rely=0.46, relwidth=0.20, relheight=.07)



root.mainloop()