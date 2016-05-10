import oauth2 as oauth
import urllib2 as urllib
from bs4 import BeautifulSoup
import pylab as P
import json
import time
import sched
import datetime
from ast import literal_eval as make_tuple
import threading
import os
import pickle
import unicodedata
import numpy as np
import Tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.font_manager import FontProperties


access_token_key = "602211113-GkgphSYMEaJaBCwHEdttp4jjoaBzJkOYnlZAAAMv"
access_token_secret = "ssicR93TZkcYwzvVqNSfpwu5amaQnJej7kEPLcpt5tWyN"
consumer_key = "A3yGrn8juJV101tYiUnDg"
consumer_secret = "9VCyJMoQR7N8q75cc2ueTYDYfzjG33u3jLMeBHxVyNo"
_debug = 0
oauth_token = oauth.Token(key = access_token_key, secret = access_token_secret)
oauth_consumer = oauth.Consumer(key = consumer_key, secret = consumer_secret)
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
http_method = "GET"
http_handler = urllib.HTTPHandler(debuglevel = _debug)
https_handler = urllib.HTTPSHandler(debuglevel = _debug)

tweets_list = []
response_all = []
start_draw = False
root = tk.Tk()
var = tk.StringVar(root)
var_start_h = tk.StringVar(root)
var_start_m = tk.StringVar(root)
var_end_h = tk.StringVar(root)
var_end_m = tk.StringVar(root)


def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token = oauth_token,
                                             http_method = http_method,
                                             http_url = url, 
                                             parameters = parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)
  
  print "open"
  try:
    response = opener.open(url, encoded_post_data)
    print "opened"
  except Exception as e:
    print "Exception when opening"
    print e
  
  print "Response"
  #print response
  return response


def parseTweet(tweet):
  source = None
  #country = None

  if 'source' in tweet:
    if tweet['source'] is not None:
      link = BeautifulSoup(tweet['source'])
      text = link.find('a')
      if text is not None:
         # Get the text from the link
         #source = text.contents[0]
         source = unicodedata.normalize('NFKD', text.contents[0]).encode('ascii','ignore')

  #if 'place' in tweet:
    #if tweet['place'] is not None:
      #country = tweet['place']['country']
      #country = unicodedata.normalize('NFKD', tweet['place']['country']).encode('ascii','ignore')
      
  #if 'user' in tweet:
    #print "user"
    #if tweet['user']['location'] is not None:
      #print "location"
      #country = tweet['user']['location']

  return source
  
    
def writeToFile(data_file_path, file_data):
  with open(data_file_path, 'ab+') as data_file:
    data_file.write(str(file_data) + '\n')
    
    
def writeFile(data_file_path, file_data):
  with open(data_file_path, 'ab+') as data_file:
    for data in file_data:
      data_file.write(str(data) + '\n')
      

def readFile(data_file_path, file_data):
  try:
    if os.stat(data_file_path).st_size == 0: 
      return False
    with open(data_file_path, 'r') as data_file:
      for line in data_file:
        #file_data.append(make_tuple(line))
        file_data.append(line)
  except IOError:
    return False
  except OSError:
    return False

  return True
  
  
def show_piechart_now(time_interval):
  
  chart_data = []
  readFile(generate_file_path(time_interval), chart_data)
  
  android = 0
  iOS = 0
  blackberry = 0
  other = 0
  
  for j in range(len(chart_data)):
    str_check = str(chart_data[j])
    if "Android" in str_check:
      android += 1
    elif "iOS" in str_check or "iPhone" in str_check or "iPad" in str_check:
      iOS += 1
    elif "BlackBerry" in str_check:
      blackberry += 1
    else:
      other += 1
  
  
  labels = 'Android Devices', 'iOS Devices', 'BlackBerry Devices', 'Desktop'
  fracs = [android, iOS, blackberry, other]
  title = 'Twitter Device Sources % for interval ' + str(time_interval)
  explode=(0.02, 0.02, 0.02, 0.02)
  
  the_grid = GridSpec(1, 1)
  
  plt.subplot(the_grid[0, 0], aspect=1)
  plt.pie(fracs, labels = labels, autopct = '%1.1f%%', colors = ('b', 'r', 'y', 'g'), shadow = True)
  plt.title(title, bbox = {'facecolor':'0.8', 'pad':5})
  
  plt.show()
  
  
def show_piechart():
  
  #plt.close()
  
  chart_data = []
  
  parsed_time = []
  parsed_time.append(int(str(var.get()[0]) + str(var.get()[1])))
  parsed_time.append(int(str(var.get()[3]) + str(var.get()[4])))
  parsed_time.append(int(str(var.get()[8]) + str(var.get()[9])))
  parsed_time.append(int(str(var.get()[11]) + str(var.get()[12])))
  
  time_interval = make_tuple(str(parsed_time))
  print generate_file_path(time_interval)
  readFile(generate_file_path(time_interval), chart_data)
  #print chart_data
  
  android = 0
  iOS = 0
  blackberry = 0
  other = 0
  
  for j in range(len(chart_data)):
    str_check = str(chart_data[j])
    if "Android" in str_check:
      android += 1
    elif "iOS" in str_check or "iPhone" in str_check or "iPad" in str_check:
      iOS += 1
    elif "BlackBerry" in str_check:
      blackberry += 1
    else:
      other += 1
  
  labels = 'Android Devices', 'iOS Devices', 'BlackBerry Devices', 'Desktop'
  fracs = [android, iOS, blackberry, other]
  title = 'Twitter Device Sources % for interval ' + str(time_interval)
  explode=(0.02, 0.02, 0.02, 0.02)
  
  the_grid = GridSpec(1, 1)
  
  plt.subplot(the_grid[0, 0], aspect=1)
  plt.pie(fracs, labels = labels, autopct = '%1.1f%%', colors = ('b', 'r', 'y', 'g'), shadow = True)
  plt.title(title, bbox = {'facecolor':'0.8', 'pad':5})
  
  plt.show()
  
  
def show_charts_totals():

  scheduled_time = []

  readFile("time_schedule.in", scheduled_time)
  
  chart_data = [[] for x in range(len(scheduled_time))]
  labels_bar = []
  for i in range(len(scheduled_time)):
    readFile(generate_file_path(make_tuple(str(scheduled_time[i]))), chart_data[i])
    labels_bar.append(scheduled_time[i])
    
  android = 0
  iOS = 0
  blackberry = 0
  other = 0
  
  android_temp = 0
  iOS_temp = 0
  blackberry_temp = 0
  other_temp = 0
  
  totals_android = []
  totals_iOS = []
  totals_blackberry = []
  totals_other = []
    
  for sublist in chart_data:
    android_temp = 0
    iOS_temp = 0
    blackberry_temp = 0
    other_temp = 0
    for j in range(len(sublist)):
      str_check = str(sublist[j])
      #print str_check
      if "Android" in str_check:
        android += 1
        android_temp += 1
      elif "iOS" in str_check or "iPhone" in str_check or "iPad" in str_check:
        iOS += 1
        iOS_temp += 1
      elif "BlackBerry" in str_check:
        blackberry += 1
        blackberry_temp += 1
      else:
        other += 1
        other_temp += 1
    totals_android.append(android_temp)
    totals_iOS.append(iOS_temp)
    totals_blackberry.append(blackberry_temp)
    totals_other.append(other_temp)

  plt.figure(figsize=(14, 7), dpi=100)

  #pie chart
  labels = 'Android Devices', 'iOS Devices', 'BlackBerry Devices', 'Desktop'
  fracs = [android, iOS, blackberry, other]
  title = 'Twitter Device Sources % Totals'
  explode=(0.02, 0.02, 0.02, 0.02)
  
  the_grid = GridSpec(1, 2)
  
  plt.subplot(the_grid[0, 0], aspect=1)
  plt.pie(fracs, labels = labels, autopct = '%1.1f%%', colors = ('b', 'r', 'y', 'g'), shadow = True)
  plt.title(title, bbox = {'facecolor':'0.8', 'pad':5})
  
  # multiple bar chart
  plt.subplot(the_grid[0, 1], aspect=0.2)
  n_intervals = len(scheduled_time)
  
  index = np.arange(0, 30 * n_intervals, 30)
  bar_width = 4
  opacity = 0.7

  plt.bar(index + bar_width, totals_android, width=bar_width, alpha = opacity, color = 'b', label = 'Android')
  plt.bar(index + bar_width * 2, totals_iOS, width=bar_width, alpha = opacity, color = 'r', label = 'iOS')
  plt.bar(index + bar_width * 3, totals_blackberry, width=bar_width, alpha = opacity, color = 'y', label = 'BlackBerry')
  plt.bar(index + bar_width * 4, totals_other, width=bar_width, alpha = opacity, color = 'g', label = 'Desktop')
  plt.xlabel('Intervals')
  plt.ylabel('Number of Tweets')
  plt.xticks(index + bar_width * 3, labels_bar, fontsize=9)  
  plt.ylim(ymax = max(max(totals_android), max(totals_iOS), max(totals_blackberry), max(totals_other)) + 5)
  plt.xlim(xmax=150)
  plt.legend(bbox_to_anchor=(1.3, 1))
  plt.title('Twitter Device Sources Number Totals / Interval', bbox = {'facecolor':'0.8', 'pad':5})
    
  plt.show()
  

def get_twitter_data(tweets_list, time_interval):

  url = "https://stream.twitter.com/1.1/statuses/sample.json"
  response_all.append(twitterreq(url, "GET", []))
  print "Response from twitter"

  for line in response_all.pop():
    if end_interval_reached(time_interval[2], time_interval[3]):
      print "gata"
      break

    tweet = json.loads(line)
    tweet_parsed = parseTweet(tweet)
    if (tweet_parsed is not None): # and tweet_parsed[1] is not None
      #tweet_pickled = pickle.dumps(tweet_parsed)
      #print pickle.loads(tweet_pickled)
      #tweets_list.append(pickle.loads(tweet_pickled))
      tweets_list.append(tweet_parsed)


def generate_file_path(time_interval): 
  return "twitterData_" + ''.join(str(t) + "_" for t in time_interval) + "date.out"
  
  
def calculate_time(h, m):
  now = datetime.datetime.now()
  delta_h = h - now.hour
  delta_m = m - now.minute
  run_from = now + datetime.timedelta(minutes = delta_h*60 + delta_m)
  return (run_from - now).total_seconds()


def start_stream_intervals():
  scheduled_time = []
  time_interval = []
  
  if not readFile("time_schedule_int.in", scheduled_time):
    print "Error in data_scheduler while reading the file." 
    return
  
  for i in range(len(scheduled_time)):
    time_interval = make_tuple(scheduled_time[i])
    #writeToFile("time_schedule.in", time_interval)
    if start_interval_reached(time_interval[0], time_interval[1]):
      writeToFile("time_schedule.in", time_interval)
      time = calculate_time(int(time_interval[0]), int(time_interval[1]))
      print time
      threading.Timer(time, get_continuously_data, [time_interval]).start()

  
def start_stream():
  stop_event = threading.Event()
  
  var_start_h.get()
  var_start_m.get()
  var_end_h.get()
  var_end_m.get()
  
  time_interval = (int(var_start_h.get()), int(var_start_m.get()), int(var_end_h.get()), int(var_end_m.get()))
  
  writeToFile("time_schedule.in", time_interval)
  
  if not check_times(time_interval):
    print time_interval
    print "Error in data_scheduler, wrong format in the file."
    return
  
  if start_interval_reached(time_interval[0], time_interval[1]):
    time = calculate_time(time_interval[0], time_interval[1])
    print time
    threading.Timer(time, get_continuously_data, [make_tuple(str(time_interval))]).start()
    
  while not stop_event.is_set():
    if (end_interval_reached1(time_interval[2], time_interval[3], 3)):
      show_piechart_now(time_interval)
      stop_event.set()

  #time = calculate_time(time_interval[2], time_interval[3])
  #print time
  #threading.Timer(time, show_piechart_now, [time_interval]).start()

def get_continuously_data(time_interval):
  stop_event = threading.Event()
  tweets_list = []

  #get_twitter_data(tweets_list, time_interval)
  threading.Thread(target=get_twitter_data, args=(tweets_list, time_interval),).start()
    
  print "received"
  while not stop_event.is_set():
    if end_interval_reached(time_interval[2], time_interval[3]):
      stop_event.set()
      #tweet_data = pickle.dumps(tweets_list)
      #writeFile(generate_file_path(time_interval), pickle.loads(tweet_data))
      writeFile(generate_file_path(time_interval), tweets_list)


def check_times(time):
    # Check if the hours are correct
  if time[0] < 0 or time[0] > 23 or time[2] < 0 or time[2] > 23:
    return False
  if time[0] > time[2]:
    return False
    # Check if the minutes are correct
  if time[1] < 0 or time[1] > 59 or time[3] < 0 or time[3] > 59:
    return False
  return True 


def start_interval_reached(h, m):
  now = datetime.datetime.now()
  if now.hour <= h and now.minute <= m:
    return True
  else:
    return False 
    

def end_interval_reached(h, m):
  now = datetime.datetime.now() 
  if now.hour == h and now.minute == m:
    return True
  else:
    return False 
    
    
def end_interval_reached1(h, m, s):
  now = datetime.datetime.now() 
  if now.hour == h and now.minute == m and now.second == s:
    return True
  else:
    return False 

  
def start_app():
  #root = tk.Tk()
  root.geometry("400x350+300+300")
  root.title("Tweets Statistics")
  
  # button for totals
  button = tk.Button(root, text="Show totals from previously saved data", command=show_charts_totals)
  button.pack(side='left', padx=20, pady=10)
  button.place(x=10, y=50)
  
  scheduled_time = []
  readFile("time_schedule.in", scheduled_time)
  
  #var = tk.StringVar(root)
  
  # optionmenu for intervals
  choices = []
  for i in range(len(scheduled_time)):
    choices.append(str(scheduled_time[i][1]) +  str(scheduled_time[i][2]) + ":" + str(scheduled_time[i][5]) + str(scheduled_time[i][6]) + " - " + str(scheduled_time[i][9]) + str(scheduled_time[i][10]) + ":" + str(scheduled_time[i][13]) + str(scheduled_time[i][14]))
    
  var.set(choices[0])
  
  option = tk.OptionMenu(root, var, *choices)
  option.pack(side='left', padx=10, pady=10)
  option.place(x=200, y=110)
  # button for optionmenu
  button = tk.Button(root, text="Show data from interval", command=show_piechart)
  button.pack(side='left', padx=0, pady=0)
  button.place(x=10, y=110)
  
  # text boxes: start_hour, start_minute, end_hour, end_minute
  #var_start_h = tk.StringVar(root)
  start_hour = tk.Entry(root, width=8, textvariable=var_start_h)
  start_hour.pack()
  start_hour.place(x = 10, y = 180)
  var_start_h.set("start hour")
  
  text = tk.Text(root)
  text.insert(tk.INSERT, ":")
  text.pack()
  text.place(x = 85, y = 180)
  
  #var_start_m = tk.StringVar(root)
  start_minute = tk.Entry(root, width=8, textvariable=var_start_m)
  start_minute.pack()
  start_minute.place(x = 100, y = 180)
  var_start_m.set("start min")
  
  #var_end_h = tk.StringVar(root)
  end_hour = tk.Entry(root, width=8, textvariable=var_end_h)
  end_hour.pack()
  end_hour.place(x = 10, y = 210)
  var_end_h.set("end hour")
  
  text = tk.Text(root)
  text.insert(tk.INSERT, ":")
  text.pack()
  text.place(x = 85, y = 210)
  
  #var_end_m = tk.StringVar(root)
  end_minute = tk.Entry(root, width=8, textvariable=var_end_m)
  end_minute.pack()
  end_minute.place(x = 100, y = 210)
  var_end_m.set("end min")

  # button to start streaming
  button = tk.Button(root, text="Start stream", command=start_stream)
  button.pack(side='left', padx=20, pady=10)
  button.place(x=35, y=240)
  
  # button to read intervals from file
  button = tk.Button(root, text="Start stream with intervals from file", command=start_stream_intervals)
  button.pack(side='left', padx=20, pady=10)
  button.place(x=10, y=290)
  
  root.mainloop()
  
  
if __name__ == '__main__':
  start_app()