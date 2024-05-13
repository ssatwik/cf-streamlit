import streamlit as st
from datetime import datetime
import time

def lockout(match_id):
    st.title("Lockout")


def waiting_room(match_id):

    match_id_split = match_id.split('_')

    target_time_str = match_id_split[1]

    current_datetime = datetime.now()

    target_time = datetime.strptime(target_time_str, "%H:%M:%S").replace(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day)

    time_difference = target_time - current_datetime

    minutes = int(time_difference.total_seconds() // 60)
    seconds = int(time_difference.total_seconds() % 60)

    timer_placeholder = st.empty()

    while minutes >= 0:

        current_datetime = datetime.now()

        time_difference = target_time - current_datetime

        minutes = int(time_difference.total_seconds() // 60)
        seconds = int(time_difference.total_seconds() % 60)

        if minutes<0: break

        timer_placeholder.write(f"Time remaining: {minutes:02d}:{seconds:02d}")

        time.sleep(1)

    st.session_state['lockout'] = 2    

    start_btn = st.button("Start Lockout")






def generate_match_id(user,players,target_time_str,mode):

    match_id = mode + '_' + target_time_str + '_' + user
    for player in players:
        match_id += ('_' + player)
    return match_id    


def create_click():
    st.session_state['create_btn'] = 2


def lockout_click(user,players,target_time_str):

    st.session_state['lockout'] = 1  

    match_id = generate_match_id(user,players,target_time_str,"lockout")

    st.session_state['match_id'] = match_id

    st.write(f"Send this match id to other players: {match_id}")  


def match_details(user):
    
    players_str = st.text_input("Enter cf ids of other players (comma separated with no space): ")

    target_time_str = st.text_input("Enter match start time in (H\:M\:S) format: ")

    players = players_str.split(",")
    st.write("Select match mode: ")

    lockout_btn = st.button("Lockout", on_click = lockout_click, args = (user,players,target_time_str))



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

    st.title("cf duel")

    user = st.text_input("Enter your cf id: ")

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
