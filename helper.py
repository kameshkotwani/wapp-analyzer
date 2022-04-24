from collections import Counter
from urlextract import URLExtract
from pandas import DataFrame
from wordcloud import WordCloud
import re
import emoji
PATTERN = re.compile('\d+.')
extractor = URLExtract()
# function to calculate the number of words in the messages
def __word_count(messages)->int:
  words = list()
  for message in messages:
    words.extend(message.split())
  return len(words)
  

# fetching the stats from given user
def fetch_stats(selected_user:str,df:DataFrame)->tuple:
  if selected_user != "overall":
    df = df[df.user==selected_user]
    
  # getting number of messages
  num_messages =  df.shape[0]

  # getting the word count
  words = __word_count(df.messages)

  # getting the number of media shared
  media_messages = df[df['messages']=='<Media omitted>\n'].shape[0]

  length = 0
  for message in df.messages:
    length += len(extractor.find_urls(message))
  
  return num_messages,words,media_messages,length

# fetching the most busy users
def most_active_users(df):
  active_users =  DataFrame(df.user.value_counts().head()).sort_values(by='user',ascending=False)
  user_percent  = round((df.user.value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
  return active_users,user_percent


# function to create word cloud 
def word_cloud(selected_user,df):
  if selected_user != "overall":
    df = df[df.user==selected_user]
  wc = WordCloud(width = 500,height=500,min_font_size = 10,background_color='white')
  df_word_cloud = wc.generate(df.messages.str.cat(sep=' '))
  return df_word_cloud

# function to return most used words
def most_common_words(selected_user:str,df:DataFrame):
  if selected_user != "overall":
    df = df[df.user==selected_user]

  temp:DataFrame = df[df.user!='group_notification']
  temp = temp[temp.messages!='<Media omitted>\n']
  
  words:list = list()
  try:
    import string
    
    # removing stopwords
    with open('hinglish_stop_words.txt','r') as f:
      stop_words = f.readlines()
    stop_words.extend(string.punctuation+string.digits) 
    words = list()
    for message in temp.messages:
      for word in message.lower().split():
        if word not in stop_words:
          words.append(word)

    return DataFrame(Counter(words).most_common(20),columns=['message','message_count'])
  except:
    pass

def emojis_counter(selected_user:str,df:DataFrame):
  if selected_user!='overall':
    df = df[df.user==selected_user]
  emojis:list = list()
  for message in df.messages:
    emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
  return DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


def monthly_timeline(selected_user:str,df:DataFrame):
  if selected_user!='overall':
    df = df[df.user==selected_user]
  
  # creating a new df for timeline showcase
  timeline:DataFrame = df.groupby(['year','month','month_name']).count()['messages'].reset_index()
  time:list = list()

  for i in range(timeline.shape[0]):
    time.append(timeline['month_name'][i]+" - "+ str(timeline['year'][i]))
  # adding the time df
  timeline['time'] = time
  return timeline

def daily_timeline(selected_user:str,df:DataFrame):
  if selected_user!='overall':
    df = df[df.user==selected_user]
  return DataFrame(df.groupby(['date']).count()['messages'].reset_index())

def week_activity(selected_user:str,df:DataFrame):
  if selected_user!='overall':
    df = df[df.user==selected_user]
  return  df.day_name.value_counts()

def month_activity(selected_user:str,df:DataFrame):
  if selected_user!='overall':
    df = df[df.user==selected_user]
  return  df.month_name.value_counts()
 
def activity_heat_map(selected_user:str,df:DataFrame):
  if selected_user!='overall':
    df = df[df.user==selected_user]
  return df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)