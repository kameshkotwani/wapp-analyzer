import re
import pandas as pd

def get_time_period(df:pd.DataFrame):
  # getting the time period
  period:list = list()
  for hour in df[['day_name','hour']]['hour']:
    if hour==23:
      period.append(str(hour)+ "-"+str('00'))
    elif hour==0:  
      period.append(str('00')+ "-"+str(hour+1))
    else:
      period.append(str(hour)+ "-"+str(hour+1))
  return period

def preprocess(data):
  
  # testing am-pm pattern
  # \d{1,}\/\d{1,}\/\d{1,},\s\d{1,2}:\d{1,2}\s(am|AM|pm|PM)\s-\s
  PATTERN = re.compile('\d{1,2}/\d{1,2}/\d{2},\s\d{2}:\d{2}\s-\s')

  try:
    # storing all the messages
    messages = re.split(PATTERN,data)[1:]

    # storing all dates
    dates = re.findall(PATTERN,data)
    df = pd.DataFrame({'user_message': messages,'message_date':dates})

    # converting str date into date format
    df.message_date = pd.to_datetime(df.message_date,format='%d/%m/%y, %H:%M - ')

    # splitting users and messages
    users = list()
    messages = list() 

    for message in df.user_message:
      entry = re.split('([\w\W]+?):\s',message)
      # user name
      if entry[1:]:
        # since if there is no : in the message, entry[1:] will return None that means this was not a message from user, so else part will be executed.
        users.append(entry[1])
        messages.append(entry[2])
      else:
        users.append('group_notification')
        messages.append(entry[0])

      # appending user and messages into dataframe
    df['user'] = users
    df['messages'] = messages

    # dropping unwanted columns
    df.drop(columns=['user_message'],inplace=True)

    # extracting year, day, month from date column
    df['year'] = df.message_date.dt.year
    df['month'] = df.message_date.dt.month
    df['month_name'] = df.message_date.dt.month_name()
    df['day'] = df.message_date.dt.day
    df['hour'] = df.message_date.dt.hour
    df['minute'] = df.message_date.dt.minute
    df['date'] = df.message_date.dt.date
    df['day_name'] = df.message_date.dt.day_name()
    # df.drop(columns=['message_date'],inplace=True)
    df['period'] = get_time_period(df)
    return df
  except:
    print("some text is not processable.")

# with open('chats.txt','r',encoding='utf-8') as f:
#   data = f.read()

# print(preprocess(data).sample(5))
