


def user_handles(input_string)->list:

    import re    

    pattern = r'@\S+'

    user_handle=re.findall(pattern=pattern,string=input_string)
    return user_handle



import csv



mes = []



def replace_content(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        
        b = 0  # Initialize counter variable
        
        for row in reader:
            tweet= f"""  {row['emotion_in_tweet_is_directed_at']} """ 
            emotion =f"""'Tweet Text:', {row['tweet_text']}""" 
            sysrole="You Are A Brand Sentiment analysis chatbot that analyses tweets and provides an analysis on the sentiment from the tweet"

            mes.append(f'{{"messages": [{{"role": "system", "content": "{sysrole}"}}, {{"role": "user", "content": "{tweet}"}}, {{"role": "assistant", "content": "{emotion}"}}]}}')

            b += 1  # Increment counter variable
            if b >= 200:
                break

# Example JSON object


# CSV file format: tweet_text, emotion_in_tweet_is_directed_at, is_there_an_emotion_directed_at_a_brand_or_product
csv_file = 'Dataset - Train.csv'


replace_content(csv_file)



with open("input.jsonl", "w",encoding='utf-8', errors='ignore') as file:
    # Iterate over the elements of the list
    for item in mes:
        # Write each element to the file
        file.write(item + "\n")  # Add a newline after each item