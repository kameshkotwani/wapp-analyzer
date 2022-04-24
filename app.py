from click import FileError
import emoji
import seaborn as sns
import streamlit as st
from preprocessor import preprocess
from helper import activity_heat_map, daily_timeline, emojis_counter, fetch_stats, month_activity, monthly_timeline,most_active_users, most_common_words, week_activity,word_cloud
import matplotlib.pyplot as plt 
from pandas import DataFrame

st.set_page_config(
  page_title="WhatsApp Chat Analyzer",
  page_icon='icons8-whatsapp-64.png'
  )
st.sidebar.title("Upload here")
with st.spinner("Processing...."):
  try:
    uploaded_file = st.sidebar.file_uploader("Upload a WhatsApp txt file")
      
    if uploaded_file is not None:
        # getting the file extension
      extension = uploaded_file.name.split('.')[-1]
      if(extension !='txt'):
        raise FileError
      
      # To read file as bytes:
      bytes_data = uploaded_file.getvalue()
      data = bytes_data.decode('utf-8')
      # data will be preprocessed first using preprocess function
      data_frame = preprocess(data)

      # fetch unique users
      users:list = data_frame.user.unique().tolist()
      users.remove('group_notification')
      users.sort()
      users.insert(0,"overall")
      
      selected_user = st.sidebar.selectbox("Select user",users)
      if st.sidebar.button("Show Analysis"):
        if(selected_user=="overall"):
          st.header("Overall Group Analysis")
        else:
          st.header(f"Showing Analysis for  {selected_user}")
        col1,col2,col3,col4 = st.columns(4)
        num_messages,word_count,media_messages,length = fetch_stats(selected_user,data_frame)
      
        # showing column 1
        with col1:
          st.header("Total Messages")
          st.title(num_messages)
        
        # showing column 2
        with col2:
          st.header("Total Words")
          st.title(word_count)

        # showing column 3
        with col3:
          st.header("Media Shared")
          st.title(media_messages)
        
        # showing column 4
        with col4:
          st.header("Links Shared")
          st.title(length)

        # showing timeline
        st.title("monthly messages")
        timeline:DataFrame = monthly_timeline(selected_user,data_frame)
        fig,ax = plt.subplots()
        ax.barh(timeline['time'],timeline['messages'],color='green')
        st.pyplot(fig)

        # daily timeline
        st.title("daily message frequency")
        daily_timeline_df:DataFrame = daily_timeline(selected_user,data_frame)
        fig,ax = plt.subplots()
        ax.barh(daily_timeline_df['date'],daily_timeline_df['messages'],color="red")
        st.pyplot(fig)

        # week activity map
        st.title('activity map')
        col1,col2 = st.columns(2)

       # day wise
        with col1:
          week_activity_map:DataFrame = week_activity(selected_user,data_frame)
          st.header("day wise")
          fig,ax = plt.subplots()
          ax.bar(week_activity_map.index,week_activity_map.values,color='orange')
          st.pyplot(fig)
       
        with col2:
          st.header("month wise")
          month_activity_map:DataFrame = month_activity(selected_user,data_frame)
          fig,ax = plt.subplots()
          ax.bar(month_activity_map.index,month_activity_map.values,color='cyan')
          st.pyplot(fig)
          
        # hourly heat map
        st.header('hourly heatmap')
        hourly_heat_map:DataFrame = activity_heat_map(selected_user,data_frame)
        fig,ax = plt.subplots()
        ax = sns.heatmap(hourly_heat_map)
        st.pyplot(fig)




        # finding most active user in the group
        if selected_user == "overall":
          st.title("most active users")
          active_users,user_percent = most_active_users(data_frame)
          col5,col6 = st.columns(2)
          
          
          # bar graph at col 1
          with col5:
            # displaying the most Active Users
            st.bar_chart(active_users)
            
          # displaying percent
          with col6:
            st.dataframe(user_percent)
        
        # word cloud 
        st.header("most used words")
        df_word_cloud = word_cloud(selected_user,data_frame)
        fig,ax = plt.subplots()
        ax.imshow(df_word_cloud)
        st.pyplot(fig)

        # most common words
        st.title("most common words")
        fig,ax = plt.subplots()
        common_words:DataFrame =most_common_words(selected_user,data_frame)
       
        plt.xticks(rotation='vertical')
        ax.barh(common_words.message,common_words.message_count)
        st.pyplot(fig)

        # emoji user
        st.title("emojis analysis")
        emoji_df:DataFrame = emojis_counter(selected_user,data_frame)
        col1,col2 = st.columns(2)
        # printing df at column 1
        with col1:
          st.dataframe(emoji_df)

        with col2:
          fig,ax = plt.subplots()
          ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
          st.pyplot(fig)

      
    else:
      st.header("WhatsApp Chat Analyzer.")
      st.write("This chat analyzer takes in your unprocessed WhatsApp chats and applies in-depth analysis on it, who knows you might find something interesting.")
      st.write("Please make sure that your messages are in 24-hour format, currently 12-hour time-period is not supported, but is under works and will be added soon.")

      st.header("[My GitHub page](https://www.github.com/kameshkotwani)")

  # except FileError as fe:

  except Exception as e:
      print(e)
      st.error("oh oh, something went wrong, perhaps you are not passing an expected file-type (txt), or we are having some computational issues.\n We're very sorry.")
      pass