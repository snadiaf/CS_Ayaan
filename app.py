import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge,Lasso
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

#Creating the title of the pahe
st.title("Welcome to the Fortune Reader of Games!")
#Showing information about the page
st.info("ML Prediction APP to Predict total Sale of Copies in Millions")

#Function to load data
def load_data():
  #Exception handling
  try:  
    df=pd.read_csv("https://raw.githubusercontent.com/snadiaf/CS_Ayaan/refs/heads/main/revised88.csv")
    return df
  except FileNotFoundError:
    print("File not found.")

#Function to Create Bar chart. It takes the dataframe as parameter
def barChart(df):
   st.info("Total Sales By Genre")
   st.bar_chart(data=df, x='genre', y='total_sales', color='genre')
   st.write("Genre 'Sports' has highest sale")

#Function to create line chart. It takes the dataframe as parameter
def lineChart(df):
   st.info("Trend of total sales for realese year")
   st.line_chart(df88,x='year',y='total_sales')
   st.write("Games realesed between year 2012-2016 had higher sale")

#Function to create top salling games tables. It takes the dataframe as parameter
def tables(df):
   #Finding the title and total sales of 15 lasgest selling games
   top_sellers = df[['title', 'total_sales']].nlargest(15, 'total_sales')
   #Sort the largest selling games in ascending order
   ts_sorted = top_sellers.sort_values(by='total_sales',ascending=False)
    
   #Create a checkbox on the page. If the user select the check box, 
   #then they can see top selling games globally
   st.info("Select to See the Top Selling Games Globally")
   ts = st.checkbox("Top Selling Games Globally")
   if ts:
      ts_sorted

   #Getting the titkes and sales of top selling games in North America and Japan-Europe-Africa-Other
   top_sellers_NA = df_sales[['title', 'na_sales']].nlargest(15, 'na_sales')
   top_sellers_Other = df_sales[['title', 'Jp-Eu-Af-Other']].nlargest(15, 'Jp-Eu-Af-Other')
    
   #Sort the data by total sales
   na_sorted = top_sellers_NA.sort_values(by='na_sales',ascending=False)
   oth_sorted =top_sellers_Other.sort_values(by='Jp-Eu-Af-Other',ascending=False)

   #Create a checkbox on the page. If the user select the check box, 
   #then they can see top selling games in North America
   st.info("Select to See the Top Selling Games in North America")
   ns= st.checkbox("Top Selling Games in North America")
   if ns:
        na_sorted

   #Create a checkbox on the page. If the user select the check box, 
   #then the can see top selling games in Japan-Europe-Africa-Other
   st.info("Select to See the Top Selling Games in Japan-Europe-Africa-Other based on Total Sales")
   os= st.checkbox("Top Selling Games in Japan-Europe-Africa-Other")
   if os:
       oth_sorted


#Creating an exoander on the webpage to show raw data
with st.expander('data'):
    df=load_data()
    st.write("Raw Data")
    df
    
    #Using for loop to gterate through all rows of the dataframe
    for i, row in df.iterrows():
       df['Jp-Eu-Af-Other']=df['jp_sales']+df['pal_sales']+df['other_sales']
       
    st. write("Sales Data in North America Vs Japan-Europe-Africa-Other")
    df_sales=df[['title','console','genre','publisher','Jp-Eu-Af-Other','na_sales']]  
    df_sales

    #Creating a dataframe using the subset of original dataframe as did some preliminery analysis on data and 
    #found some columns less informative, so removed them for creating prediction model  
    df88=df[['title','console','genre','publisher','release_date','total_sales']]
    
    #Drop any row with null value
    df88.dropna(axis=0, inplace=True)
    
    #Extracted only year from release date
    df88['year'] = pd.DatetimeIndex(df88['release_date']).year
    
    
    st.write(" Features values for records used to create machine learning model")
    st.write('**X**')
    X_raw = df88[['console','genre','publisher','year']]
    X_raw
    
    st.write("target value")
    st.write('**y**')
    y_raw = df88.total_sales
    y_raw


#Adding another expander to show visualization
with st.expander('Visualization'):
    #Bar chart to show Total sales by Genre
    barChart(df)
    
    #Line chart to show the trend of total sales for release year.
    lineChart(df88)
    
    #Tables to show the top selling games
    tables(df)
    

    #st.info("Top Selling Games")
    #st.bar_chart(data=top_sellers, x='title', y='total_sales')



#Adding sidebar to take inout from user for the record for which 'total sales' will be predicted
with st.sidebar:
    st.header('Input Features')
    genre = st.selectbox('Genre', ('Action', 'Shooter', 'Action-Adventure', 'Sports', 'Role-Playing',
       'Simulation', 'Racing', 'Music', 'Misc', 'Fighting', 'Platform',
       'Adventure', 'Strategy', 'Puzzle', 'MMO', 'Sandbox', 'Party',
       'Education', 'Board Game', 'Visual Novel'))
    
    console=st.selectbox('Console',('PS3', 'PS4', 'PS2', 'X360', 'XOne', 'PC', 'PSP', 'Wii', 'PS',
       'DS', '2600', 'GBA', 'NES', 'XB', 'PSN', 'GEN', 'PSV', 'DC', 'N64',
       'SAT', 'SNES', 'GBC', 'GC', 'NS', '3DS', 'GB', 'WiiU', 'WS', 'VC',
       'NG', 'WW', 'SCD', 'PCE', 'XBL', '3DO', 'GG', 'OSX', 'Mob', 'PCFX'))
    
    publisher=st.selectbox('Publisher',('Rockstar Games', 'Activision', 'EA Sports', 'Electronic Arts',
       'Microsoft Game Studios', 'Microsoft Studios',
       'Bethesda Softworks', 'Ubisoft', 'Sony Computer Entertainment',
       'GT Interactive', 'Sony Computer Entertainment America', 'Namco',
       'LucasArts', 'Majesco', 'Warner Bros. Interactive',
       'Universal Interactive', 'Square Enix', 'Eidos Interactive',
       'Microsoft', 'RedOctane', 'Sega', 'Capcom', 'Atari', 'VU Games',
       'Blizzard Entertainment', 'Take-Two Interactive', 'Konami',
       'Ultra Games', 'Hasbro Interactive', 'Global Star Software',
       '2K Sports', 'THQ', 'Warner Bros. Interactive Entertainment',
       '2K Games', 'Acclaim Entertainment', 'Disney Interactive Studios',
       'Konami Digital Entertainment', 'EA Sports BIG', 'Midway Games',
       'Arena Entertainment', 'Buena Vista', 'MTV Games', 'Jaleco',
       'Deep Silver', '989 Studios', 'Hello Games', 'Vivendi Games',
       'Tengen', 'Maxis', 'Sony Interactive Entertainment', 'Imagic',
       'Valve', 'Gotham Games', 'Namco Bandai', '2K Play', '505 Games',
       'Nintendo', 'Mojang', 'Unknown', 'Virgin Interactive',
       'Destination Software, Inc', 'Banpresto', 'D3 Publisher',
       'Infogrames', 'Crave Entertainment', 'Red Storm Entertainment',
       'Atlus', 'Fox Interactive', 'Williams Entertainment',
       'Hudson Soft', 'Coleco', 'Bandai', 'Codemasters', 'ASC Games',
       'Accolade', 'Namco Bandai Games', 'TDK Mediactive', 'Zoo Games',
       'Sony Online Entertainment', '3DO', 'Bandai Namco Games',
       'Conspiracy Entertainment', 'Natsume', 'Alchemist',
       'Black Label Games', 'Sierra Entertainment', 'Level 5', 'Ocean',
       'City Interactive', 'Compile', 'ASCII Entertainment', 'Square',
       'PopCap Games', 'Broderbund', 'Agetec', 'Tomy Corporation', 'KOEI',
       'Tecmo', 'Zoo Digital Publishing', 'Taxan', 'Square EA',
       'Game Factory', 'Parker Bros.', 'Titus', 'Mud Duck Productions',
       'Tecmo Koei', 'Gearbox Software', 'Crystal Dynamics', 'Pinnacle',
       'Empire Interactive', 'Focus Home Interactive', 'Interplay',
       'Scholastic Inc.', 'Mystique', 'Telltale Games', 'ChunSoft',
       'Enix', '20th Century Fox Video Games', 'Rare', 'Men-A-Vision',
       'SouthPeak Interactive', 'Mastiff', 'Nordic Games', 'Touchstone',
       'Harmonix Music Systems', 'Playmates', 'XS Games', 'LEGO Media',
       'Quest', 'Gathering of Developers', 'Tigervision', 'Xseed Games',
       'GameMill Entertainment', 'Mattel Interactive', 'Destineer',
       'Rocket Company', 'GameMill', 'Psygnosis', 'IE Institute',
       'Navarre Corp', 'CDV Software Entertainment', 'NIS America',
       'Trion Worlds', 'Aksys Games', 'Takara', 'Ignition Entertainment',
       'Rebellion Developments', 'Working Designs', 'BAM! Entertainment',
       'Enterbrain', 'Spectrum Holobyte', 'Imagineer', 'CPG Products',
       'Aruze Corp', 'Storm City Games', 'Takara Tomy', 'Answer Software',
       'Black Pearl', 'Marvelous Interactive', 'SCS Software',
       'Gun Media', 'Hudson Entertainment', 'Frontier Developments',
       'NovaLogic', 'Epoch', 'Spike Chunsoft', 'Knowledge Adventure',
       'Telegames', 'Hip Interactive', 'ESP', 'TYO', 'Taito',
       'Magical Company', 'Westwood Studios', 'Mentor Interactive',
       'Valcon Games', 'Kemco', 'Human Entertainment', 'Data Age',
       'Kalypso Media', '989 Sports', 'Jack of All Games', 'Hot-B',
       'D3Publisher', 'Media Rings', 'New', 'Jorudan', 'Elf',
       '10TACLE Studios', 'Sammy Corporation', 'Kalypso', 'Mindscape',
       'Brash Entertainment', 'Aspyr', 'DSI Games', 'UFO Interactive',
       'ITT Family Games', 'SNK Playmore', 'BPS',
       'GungHo Online Entertainment', 'Arc System Works', 'SquareSoft',
       'Magix', 'P2 Games', 'Mumbo Jumbo', 'CokeM Interactive',
       'NewKidCo', 'Kokopeli Digital Studios', 'CBS Electronics',
       'Mad Catz', 'Koch Media', 'Spike', 'Bandai Namco Entertainment',
       'Team17 Software', 'Sold Out', 'Angel Studios',
       'Simon & Schuster Interactive', 'A1 Games', 'Video System',
       'Seta Corporation', 'Nichibutsu', 'GSP', 'Red Mile Entertainment',
       'Hamster Corporation', 'Little Orbit', 'Avanquest', 'Nicalis',
       'SNK', 'Nippon Columbia', 'Wargaming.net', 'Graffiti',
       'Tripwire Interactive', 'Microprose', 'Hect', 'NEC', 'Gamecock',
       'Home Entertainment Suppliers', 'Axela', 'NEC Interchannel',
       'ArtDink', 'THQ Nordic', 'Gust', 'O-Games', 'ValuSoft',
       'Majesco Entertainment', 'Milestone S.r.l.', 'Kadokawa Shoten',
       'Koei Tecmo', 'Bold Games', 'Marvelous',
       'Irem Software Engineering', 'Detn8 Games', 'Bomb', 'Sears',
       'AQ Interactive', 'Pioneer LDC', 'Activision Value',
       'Kadokawa Games', 'On Demand', 'Maximum Games',
       'inXile Entertainment', 'Acquire', 'Culture Brain',
       'DreamCatcher Interactive', 'Strategy First', 'NCS', 'Merscom LLC',
       'Shogakukan', 'Falcom Corporation', 'ARUSH Entertainment',
       'Nippon Telenet', 'Core Design Ltd.', 'SSI',
       'Paramount Digital Entertainment', 'TDK Core', 'Victory Lap Games',
       'JoWood Productions', 'Rooster Teeth Games',
       'Asylum Entertainment', 'Marvelous Entertainment',
       'Sound Source Interactive', 'Playlogic Game Factory',
       'Trigger Apps', 'Thomas Happ Games', 'Avalon Interactive', 'PQube',
       'Big Ben Interactive', 'Vatical Entertainment', 'VR Sports',
       'Compile Heart', 'Milestone', 'Syscom', 'FCI', 'Milestone S.r.l',
       'Carbine Studios', 'Aques', 'Victor Interactive', 'System 3',
       'PlayV', 'Rising Star Games', 'Vir2L Studios',
       'Paradox Interactive', 'Idea Factory', 'Encore', 'Media Factory',
       'Dusenberry Martin Racing', 'Grey Box', 'Microids',
       'The Adventure Company', 'Insomniac Games',
       'Idea Factory International', 'Sony Music Entertainment', 'Imadio',
       'Aquaplus', 'Legacy Interactive', 'Excalibur Publishing Limited',
       'General Entertainment', 'Broccoli', 'GameTrust',
       'Nihon Falcom Corp', 'Capcom Entertainment', 'Tommo', 'Game Arts',
       'Sunsoft', 'MLB Advanced Media', 'Tru Blu Entertainment',
       'U.S. Gold', 'PM Studios', 'Got Game Entertainment', '704Games',
       'Black Bean Games', 'Slitherine Software', 'Outright Games',
       'Gremlin Interactive Ltd', 'JVC', 'MTO', 'T&E Soft', 'Type-Moon',
       'Psyonix Studios', 'Team 17', 'O3 Entertainment',
       'Devolver Digital', 'Time Warner Interactive',
       'Bigben Interactive', 'Daito', 'Merge Games', 'Metro 3D',
       'Xicat Interactive', 'Reef Entertainment', 'Gameloft',
       'Nippon Ichi Software', 'TOHO', 'Data East',
       'Gainax Network Systems', '5pb', 'GameTek', 'Benesse', 'Paon',
       'Skybound Games', 'Micro Cabin', 'DTP Entertainment',
       'Image Epoch', 'Groove Games', 'Asmik Corp', 'Ghostlight',
       'WayForward Technologies', 'Ravenscourt',
       'Asmik Ace Entertainment', 'Soedesco', 'O~3 Entertainment',
       'Phantom EFX', 'Nippon Amuse', 'Hackberry',
       'Panasonic Interactive Media', 'Evolved Games',
       'Sony Computer Entertainment Europe', 'Griffin International',
       'Hearty Robin', 'Origin Systems', 'Nighthawk Interactive',
       'responDESIGN', 'FuRyu Corporation', 'Gaijinworks',
       'Secret Stash Games', 'Badland Games', 'Studio Wildcard', 'Glams',
       'From Software', 'MLB.com', 'Aqua Plus', 'Flight-Plan', 'Telstar',
       'Egosoft', 'Happinet', 'Viva Media', 'Unfinished Pixel',
       'bitComposer Games', 'Genius Products, Inc.', 'Virtual Play Games',
       'Myelin Media', 'Edia', 'Excalibur Publishing',
       'Planet Entertainment', 'Evolution Games', 'Sunrise Interactive',
       'Games Workshop', 'Alternative Software', 'Polykid', 'Success',
       "Yuke's", 'American Technos', 'Perfect World Entertainment',
       'GungHo', 'Locus', 'Athena', 'Aria', 'Unbalance', 'Warp', 'Ecole',
       'Imax', 'Midas Interactive Entertainment', 'Marvel Entertainment',
       '1C Company', 'HAL Laboratory', 'Ready at Dawn',
       'Nihon Falcom Corporation', 'Wired Productions', 'Aerosoft',
       'iWin', 'Creative Core', 'Media Works', 'System 3 Arcade Software',
       'Pack-In-Video', 'Cave', 'Orbital Media, Inc.', 'DigiCube',
       'Yumedia', 'Asgard', 'Electro Brain', 'Alliance Digital Media',
       'Kaga Create', 'Fortyfive', 'Grand Prix Games', 'Crimson Cow',
       'Funbox Media', 'DotEmu', 'Eidos Interactive Ltd', 'Vap',
       'Pony Canyon', 'Tivola', 'Perp Games', 'AIA', 'Rising Star',
       'ASCII Media Works', 'Anuman', 'Snail Games USA', 'Coconuts Japan',
       'Klei Entertainment', 'Blast! Entertainment Ltd', 'Comfort',
       'Yeti', 'Introversion Software', 'Dovetail Games', 'Tequila Works',
       'Prototype', 'Giants Software', 'TREVA Entertainment',
       'Phantagram', 'Genki', 'RTL', 'SVG Distribution', 'Misawa', 'Pow',
       'Viacom', 'eGames', 'Sprite', 'The Learning Company',
       'Team17 Digital Ltd', 'NCSoft', 'Acttil', 'Big Fish Games',
       'Red Hook Studios', 'IGS', 'Alawar Entertainment', 'Rombax Games',
       'Ascaron Entertainment', 'SCi', 'Experience Inc.', 'TGL',
       'Zushi Games', 'Zenrin', 'CyberFront', 'Dramatic Create',
       'SouthPeak Games', 'Interchannel', 'Sonnet', 'Techland',
       'FDG Entertainment', 'Riverhillsoft', 'Rondomedia', 'id Software',
       'Masque Publishing', 'Lionhead Studios', 'Societa', 'Perpetual',
       'Summitsoft', 'Sidhe Interactive', 'Playmore', 'Frozenbyte',
       'Avanquest Software', 'Cygames', 'Phantom 8 Studio', 'Russel',
       '11 bit studios', 'Stainless Games', 'Yacht Club Games',
       'Oxygen Interactive', 'Berkeley', 'Modus Games',
       'Maximum Family Games', 'Leadman Games', 'Badland Studio', 'Rejet',
       'Quinrose', 'Tulip Games', 'Kids Station', 'Nobilis', 'Stardock',
       'CK Games', 'Paon Corporation', 'BushiRoad', 'GN Software',
       'Mastertronic', 'KID', 'Licensed 4U', 'Sweets', 'Headup Games',
       'Princess Soft', 'Fuji', 'Mamba Games', 'Her Interactive',
       'Daedalic Entertainment', '49Games', 'Kamui', 'KSS', "3 O'Clock",
       'ASK', 'Fields', 'Funcom', 'imageepoch Inc.', 'Nexon', 'Sting',
       'G.Rev', 'Tryfirst', 'Office Create', 'UIG Entertainment',
       'Giza10', 'Red Flagship', 'fonfun', 'Imageworks', '7G//AMES',
       'Monte Christo Multimedia', 'Graphsim Entertainment',
       'U&I Entertainment', 'Technos Japan Corporation', '04-Aug',
       'Mediascape', 'Starfish', 'King Records', 'Focus Multimedia',
       'Turbine Inc.', 'Obsidian Entertainment', 'Yamasa Entertainment',
       'Plenty', 'Dorart', 'Mirai Shounen', 'Gakken', 'Alvion',
       'honeybee', 'Minato Station', 'Enlight', 'Revolution Software',
       'League of Geeks', 'New World Computing', 'Meridian4', 'Entergram',
       'HuneX', 'Daedalic', 'Neko Entertainment', 'Dispatch Games',
       'System Soft Alpha', 'Views', 'Quintet', 'ReadySoft',
       'Karin Entertainment', 'Datam Polystar', 'Giga',
       'Revolution (Japan)', 'System Soft', 'Technical Associates Inc',
       'RED Entertainment', 'Rebellion', 'Visco', 'Epic Games', 'Gaga',
       'Arika', 'Villa Gorilla', 'Warashi', 'Neocore Games',
       'Essential Games', 'Piacci', 'SystemSoft Alpha',
       'Hoplite Research', 'Digiturbo', 'MAGES', 'Takuyo', 'M2',
       'Silky`s', 'Genterprise', 'Tri Synergy', 'Interchannel-Holon',
       'KING Art Games', 'Moss', 'Hiromi', 'SystemSoft',
       'Agatsuma Entertainment', 'GMX Media', 'Commseed',
       'RailSimulator.com', 'Ongakukan', 'Independent Arts Software GmbH',
       'Paradox Development', 'First Class Simulations', 'Studio Artdink',
       'Lighthouse Interactive', 'Otomate', 'Nitroplus', 'NetRevo',
       'Naxat Soft', 'Boost On', 'Foreign Media Games',
       'Media Entertainment', 'Milkstone Studios', 'Best Media',
       'Global A Entertainment', 'Interplay Productions',
       'Triangle Service', 'Qute', 'Easy Interactive', 'EuroVideo Medien',
       'Harukaze', 'iMel', 'Matatabi', 'Otomate Idea Factory',
       'Gadget Soft', 'Abel', 'Astragon', 'Assemble Entertainment',
       'Dimple Entertainment', 'Nippon Cultural Broadcasting eXtend',
       "Shin'en", 'Bergsala Lightweight', 'Now Production',
       'H2 Interactive Co., Ltd.', 'Michaelsoft', 'TopWare Interactive',
       'ArenaNet', 'Rebellion Games', 'Toby Fox', 'Rain Games',
       'Team Meat', 'El Dia', 'Wolfgame', 'King Games', 'Numantian Games',
       'Sirtech', 'TopWare', 'Adventure Soft', 'Elephant Entertainment',
       'GTE Entertainment', 'The Fullbright Company',
       'Iceberg Interactive', 'Phenomedia', 'MC2 Entertainment',
       'Blade Interactive', 'Red Orb', 'Tradewest', 'Fru Blu Games',
       'Mindstorm Studios', 'Alpha Unit', 'GamersGate', 'Virgin Play',
       'Image Space Incorporated', 'Mercury Games', 'LSP Games',
       'Nordcurrent', 'Microforum', 'SilverStar', 'Lexicon Entertainment',
       'Petit Reve', 'Behaviour Interactive', 'Chara-ani',
       'Illusion Softworks', 'Sandlot Games', 'E-Frontier',
       'Digital Jesters', 'Just Flight', 'iEntertainment Network',
       'MegaHouse', 'Recom', 'Thekla, Inc.', 'althi Inc.', 'Focus',
       'Tera Box', 'Ides', 'Land Ho', 'Summitsoft Entertainment', 'Datel',
       'HdO Adventure', 'Freeze Tag', 'Artifex Mundi sp. z o.o.',
       'Virtual Playground', 'Enjoy Gaming ltd.', 'Rovio Mobile',
       'Futurlab 1', 'Game Factory Interactive', 'FireFly Studios',
       '1C Maddox Games', 'HD Interactive', 'Whiptail Interactive',
       'DTMC', 'EON Digital Entertainment', 'Spellbound', 'DMM Games',
       'Noviy Disk', 'Joindots', 'United Developers', 'Stack',
       'Digital Works Entertainment'))
    
    year=st.slider('Year', 1977, 2024, 2008)

    #Creatinga dictionary using user input  
    data = {'console': console,
            'genre': genre,
            'publisher': publisher,
            'year': year
            }
    #Creating data frame from the created dictionary
    input_df = pd.DataFrame(data, index=[0])

    #Concating the inout with X
    input_game = pd.concat([input_df, X_raw], axis=0)
    
    # showing the inout features
    with st.expander('Input features'):
       st.write('**Input Game**')
       input_df
   
    #Creating a list with Object type feature/column names
    encode = ['console', 'genre', 'publisher']

    #Getting the dummies for the object type data
    df_games = pd.get_dummies(input_game, prefix=encode)
    
    
    # Removing the input record from the data as model will be trained on past data only
    X=df_games[1:]
    input_row=df_games[:1]
    y=y_raw
    
    #I used the following code block to use the GridSearch method to find the best alpha. I am commenting it here 
    # as it takes a lot of time to run 
    # I am using alpha=1.04 that I got from this method
    
    ##################################
    #cv = RepeatedKFold(n_splits=5, n_repeats=2, random_state=1)
    # define grid
    #grid = dict()
    #grid['alpha'] = np.logspace(-1,1,num = 50)
    #define search
    #search = GridSearchCV(model, grid, scoring= 'r2', cv=cv, n_jobs=-1)
    #perform the search
    #results = search.fit(X, y)
    #########################################

    #Creating linear regression model
    model = Ridge(alpha=1.04)
    
    #Training the model 
    model.fit(X, y)

    #Predicting the target value for the input record
    prediction = model.predict(input_row)

    #Showing the result
    with st.expander('Result'):
       st.write(prediction)
       




    


    




    



   






