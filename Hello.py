import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import random
import cloudscraper


def get_solved_problems(username):

    # Making API call to get user's submissions
    response = requests.get(f"https://codeforces.com/api/user.status?handle={username}&from=1&count=1000")

    if response.status_code == 200:
        submissions = response.json()["result"]
        solved_problem = set()

        # Filtering submissions with verdict "OK"
        for submission in submissions:
            problem = submission["problem"]
            contest_id = problem["contestId"]
            problem_index = problem["index"]
            s = str(contest_id)+str(problem_index)
            solved_problem.add(s)
        return solved_problem
        
    else:
        print("Failed to fetch data. Make sure the usernames of the players are correct.")
        return None
    

def get_problems(rating):

    url = f"https://codeforces.com/problemset?tags={rating}-{rating}"
    
    scraper = cloudscraper.create_scraper()  # Bypass Cloudflare
    response = scraper.get(url)
    
    # print("Response Code:", response.status_code)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        problems = soup.find_all('td', class_="id")
        problem_list = [item.find('a').text.strip() for item in problems if item.find('a')]
        return problem_list
        
    else:
        print("Failed to fetch problems. Make sure the ratings are multiples of 100 between 800 and 3500. Status Code:", response.status_code)
        return []


def getlatestsolved(username):

    response = requests.get(f"https://codeforces.com/api/user.status?handle={username}&from=1&count=3&verdict=OK")
    if response.status_code == 200:
        submissions = response.json()["result"]
        solved_problem = set()

        # Filtering submissions with verdict "OK"
        for submission in submissions:
            if 'verdict' in submission and submission["verdict"] == "OK":
                problem = submission["problem"]
                contest_id = problem["contestId"]
                problem_index = problem["index"]
                s = str(contest_id)+str(problem_index)
                solved_problem.add(s)
        return solved_problem
    else:
        print("Failed to fetch data. Make sure the usernames of the players are correct.")
        return None


def colour_green(val): return 'background-color: green'

def colour_red(val): return 'background-color: red'

def colour_empty(val): return ''

def make_link(problem_id):
    num = problem_id[0:4]
    letter = problem_id[4:]    
    return f"https://codeforces.com/contest/{num}/problem/{letter}"


def lockout(match_id):

    st.title("Lockout")

    match_id_split = match_id.split('_')

    match_duration = match_id_split[2]

    players_str = match_id_split[3]
    problems_str = match_id_split[4]
    points_str = match_id_split[5]
    ratings_str = match_id_split[6]
    
    players = players_str.split('/')
    problems = problems_str.split('/')
    points = points_str.split('/')
    ratings = ratings_str.split('/')

    dictionary = {'Ratings' : ratings,'Points' : points}
    scoreboard = {}
    penalty = {}

    len_problems = len(problems)
    len_players = len(players)

    for player in players:

        dictionary[player] = problems
        scoreboard[player] = 0
        penalty[player] = 0
    

    df = pd.DataFrame(dictionary)
    # sf = pd.DataFrame(scoreboard)

    # df.set_index('points', inplace=True)

    links = []
    for problem in problems:
        links.append(make_link(problem))

    data_df = pd.DataFrame(
        {
            "Problem": problems,
            "apps": links,
        }
    )

    st.data_editor(
        data_df,
        column_config={
            "apps": st.column_config.LinkColumn(
                "Link",
            ),
        },
        hide_index=True,
    )

    df_t = df.transpose()

    # df_t = df.T.set_index(0)

    end_time = time.time() + int(match_duration)*60

    write_placeholder = st.empty()

    df_placeholder = st.empty()

    sf_placeholder = st.empty()

    # df_placeholder.dataframe(df)

    already_solved_set = set()

    style1 = df_t.style.applymap(colour_empty, subset=pd.IndexSlice[players[0],0])

    finished = 0

    while time.time() < end_time:

        if finished == len_problems: break

        time_remaining = int(end_time - time.time())

        hours = time_remaining // 3600
        minutes = (time_remaining % 3600) // 60
        seconds = time_remaining % 60

        write_placeholder.write(f"Time remaining: {hours}:{minutes}:{seconds}")

        for i in range(len_players):

            solved_set = getlatestsolved(players[i])

            for j in range(len_problems):

                if (problems[j] in solved_set) and (problems[j] not in already_solved_set):

                    already_solved_set.add(problems[j])

                    finished += 1

                    scoreboard[players[i]] += int(points[j])
                    penalty[players[i]] = finished

                    for ii in range(len_players):

                        if ii==i: style1 = style1.applymap(colour_green, subset=pd.IndexSlice[players[ii],j])
                        
                        else: style1 = style1.applymap(colour_red, subset=pd.IndexSlice[players[ii],j])

        df_placeholder.dataframe(style1, use_container_width=True)

        sf = pd.DataFrame.from_dict(scoreboard, orient='index')
        sf_placeholder.dataframe(sf)

        time.sleep(1)
    
    user = st.session_state['user']

    Names = {'arnavra3' : 'Arno', 'KushKushal' : 'Kush', 'arrow_s' : 'Ashu', 'asterisk11' : 'Koni', 'isolve1400s' : 'Arno', 'kushkushali' : 'Rrho', 'redcar' : 'Satwik', 'bluecar' : 'Satwik'}

    winner = user
    max = scoreboard[user]

    for player in players:
        if max < scoreboard[player]:
            max = scoreboard[player]
            winner = player
        elif max == scoreboard[player]:
            if penalty[player] < penalty[winner]:
                winner = player

    name = user
    if user in Names: name = Names[user]

    st.write(f"Winner : {winner}")
    if user==winner:
        st.write(f"Congrats, {name}!!")
    else:
        st.write(f"You lost, {name} :(")



def waiting_room(match_id):

    match_id_split = match_id.split('_')

    target_time_str = match_id_split[1]

    current_datetime = datetime.now()

    target_time = datetime.strptime(target_time_str, "%H:%M:%S").replace(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day)

    time_difference = target_time - current_datetime

    minutes = int(time_difference.total_seconds() // 60) - 330
    seconds = int(time_difference.total_seconds() % 60)

    timer_placeholder = st.empty()

    while minutes >= 0:

        current_datetime = datetime.now()

        time_difference = target_time - current_datetime

        minutes = int(time_difference.total_seconds() // 60) - 330
        seconds = int(time_difference.total_seconds() % 60)

        if minutes<0: break

        timer_placeholder.write(f"Time remaining: {minutes:02d}:{seconds:02d}")

        time.sleep(1)

    st.session_state['lockout'] = 2    

    start_btn = st.button("Start Lockout")



def generate_match_id(user,players,target_time_str,match_duration,ratings,points,mode):

    solved_set = get_solved_problems(user)
    for player in players:
        # solved_set += get_solved_problems(player)
        solved_set = solved_set.union(get_solved_problems(player))

    problems=[]
    for rating in ratings:
        templist = get_problems(rating)
        safe=10000
        while safe:
            temp = random.choice(templist)
            if temp in solved_set:
                safe-=1
                continue
            else:
                solved_set.add(temp)
                problems.append(temp)
                break

    match_id = mode + '_' + target_time_str + '_' + match_duration + '_' + user

    for player in players:
        match_id += ('/' + player)
    match_id += '_'

    l = len(problems)
    for i in range(l):
        match_id += problems[i]
        if i!=l-1: match_id += '/'
    match_id += '_'
    for i in range(l):
        match_id += points[i]
        if i!=l-1: match_id += '/'
    match_id += '_'
    for i in range(l):
        match_id += ratings[i]
        if i!=l-1: match_id += '/'           

    return match_id    


def create_click():
    st.session_state['create_btn'] = 2


def lockout_click(user,players,target_time_str,match_duration,ratings,points):

    st.session_state['lockout'] = 1  

    match_id = generate_match_id(user,players,target_time_str,match_duration,ratings,points,"lockout")

    st.session_state['match_id'] = match_id

    st.write(f"Send this match id to other players: {match_id}")  


def match_details(user):
    
    players_str = st.text_input("Enter cf ids of other players (comma separated): ")

    target_time_str = st.text_input("Enter match start time in (HH\:MM\:SS) format: ")

    match_duration = st.text_input("Enter duration of match in minutes: ")

    ratings_str = st.text_input("Enter ratings of problems (comma separated): ")

    points_str = st.text_input("Enter points of problems (comma separated): ")

    ratings = ratings_str.split(',')
    for i in range(len(ratings)):
        ratings[i] = ratings[i].replace(' ','')
    
    points = points_str.split(',')
    for i in range(len(points)):
        points[i] = points[i].replace(' ','')

    players = players_str.split(",")
    for i in range(len(players)):
        players[i] = players[i].replace(' ','')
        
    st.write("Select match mode: ")

    lockout_btn = st.button("Lockout", on_click = lockout_click, args = (user,players,target_time_str,match_duration,ratings,points))



def join_click():
    
    st.session_state['join_btn'] = 2


def join_with_id():

    match_id = st.text_input("Enter match id: ")

    if 'join_with_id' in st.session_state:

        st.session_state['match_id'] = match_id

        st.session_state['lockout'] = 1

        waiting_room(st.session_state['match_id'])
    


if 'flag' not in st.session_state:
    st.session_state['flag'] = 0
else:
    st.session_state['flag'] += 1
st.write(st.session_state['flag'])


if 'lockout' in st.session_state:

    if st.session_state['lockout']==1: waiting_room(st.session_state['match_id'])

    elif st.session_state['lockout']==2: lockout(st.session_state['match_id'])


else:

    st.title("CF Duel")

    user = st.text_input("Enter your Codeforces handle: ")

    st.session_state['user'] = user

    create_btn = st.button("Create a match", on_click = create_click)
    join_btn = st.button("Join a match", on_click = join_click)

    if 'create_btn' not in st.session_state:
        st.session_state['create_btn'] = 1

    else:
        if st.session_state['create_btn'] == 2:
            match_details(user)

    if 'join_btn' not in st.session_state:
        st.session_state['join_btn'] = 1

    else:
        if st.session_state['join_btn'] == 2:
            join_with_id()
            st.session_state['join_with_id']=1
