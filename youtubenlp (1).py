# -*- coding: utf-8 -*-
"""YoutubeNLP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tJ5VAc4Cq5VNXjK8g4Y4B_0EM7s6_7NO

1: Import Packages
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

df = pd.read_csv ("/content/Perseverance_Landing.csv")

df.head()

# convert time column to minutes past midnight, column label "time"
df['time'] = df['time'].apply(lambda x: sum(int(i) * 60**index for index, i in enumerate(reversed(x.split(':')))))

#create the 15 minute time bucket intervals, column label "time_buckets"

time_buckets = pd.cut(df['time'], bins=range(0, 1501,15), right=False)

#combine time buckets with comments, name "time_bucket"

df['time_bucket'] = time_buckets

#count occurences of each phrase within a 15 minute interval
phrase_counts = df.groupby('time_bucket')['comment'].apply(lambda x: Counter(x)).reset_index()

df.head()

# Group by 'time_bucket' and find top 3 comments in each group
top_comments = df.groupby('time_bucket')['comment'].value_counts().groupby(level=0).nlargest(3)

top_comments = top_comments.groupby(level=0).filter(lambda x: len(x) > 1)

from google.colab import drive
drive.mount('/content/drive')

# Iterate through top_comments and print the values
for time_bucket, comments in top_comments.groupby(level=0):
    print(f"Time Bucket: {time_bucket}")
    for comment, frequency in comments.items():
        print(f"Comment: {comment}, Frequency: {frequency}")
    print()

print(df.columns)

time_buckets = top_comments['time_bucket'].unique()
fig, axs = plt.subplots(len(time_buckets), figsize=(10, 6 * len(time_buckets)))

# Plotting each time bucket separately
for i, bucket in enumerate(time_buckets):
    data = top_comments[top_comments['time_bucket'] == bucket]
    ax = axs[i] if len(time_buckets) > 1 else axs
    ax.barh(data['comment'], data['frequency'], color='skyblue')  # Adjusted column names here
    ax.set_title(f'Top 10 Comments - {bucket}')
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Comment')  # Adjusted ylabel to 'Comment'

plt.tight_layout()
plt.show()

#list the most repeated comments
top_comments.head()

# Assuming top_comments is your DataFrame with columns 'time_bucket', 'comment', 'frequency'
# Replace 'frequency' with the actual column name containing your frequency data
top_comments = top_comments[top_comments['frequency'] > 1]  # Filter comments with frequency > 1

plt.figure(figsize=(24, 10))  # Adjust figure size

# Plotting the bar graph
top_comments.plot(kind='bar', x='comment', y='frequency', title='Top Comments with Frequency > 1', rot=45, color='skyblue')

plt.xlabel('Comment', fontsize=12)  # Label for x-axis
plt.ylabel('Frequency', fontsize=12)  # Label for y-axis

plt.xticks(fontsize=8)  # Adjust font size of x-axis tick labels
plt.yticks(fontsize=8)  # Adjust font size of y-axis tick labels

plt.grid(axis='y')  # Add grid lines along the y-axis

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# Aggregate comment frequencies
comment_frequencies = df['comment'].value_counts().reset_index()
comment_frequencies.columns = ['comment', 'frequency']

# Sort by frequency in descending order and select top ten comments
top_fifteen_comments = comment_frequencies.head(15)

# Plotting the top ten comments
plt.figure(figsize=(10, 6))
plt.bar(top_fifteen_comments['comment'], top_fifteen_comments['frequency'], color='skyblue')
plt.xlabel('Comment')
plt.ylabel('Frequency')
plt.title('Top fifteen Comments by Frequency')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()