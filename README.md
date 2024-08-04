## Using Machine Learning to Predict the Winner of the Women's Marathon at the Paris 2024 Olympics 🥇🏃‍♀️

See my [blog post](https://jamiezim4.github.io/using-machine-learning-to-predict-paris-olympics) on my personal website to read more!

I'm a big fan and spectator of professional endurance sports, Women's distance running in particular, and I run quite a bit myself, so I decided to combine my programming skills and running fanaticism together to stretch my machine-learning chops. __I wrote this project to predict the winner of the Women's Marathon at the 2024 Paris Olympics.__
I trained a model on data from competitor's past performances: what races they ran, in which countries and when, and most importantly what time they ran. It also includes their birth date and their nationality.

I got training data from [World Athletics](https://worldathletics.org/competitions/olympic-games/paris24/athletes?competitionGroup=olympic-games&urlSlug=paris24&disciplineCode=MAR&sexCode=W). I didn't scrape their website HTML, but by inspecting the page I was able to find out that they have a GraphQL API that drives their data retrieval. (They don't know that I've done this, but it's a public site and I'm not DDOS-ing them or making money off them)

I used a __regression model__ (not classification) because I want to predict continuous values - each competitor's race time. Then I made a prediction on each athlete in the new venue on the new date, got their race time, and sorted by time to see who will medal in this event.

### Step 1: Get all the competitors running in this year's race
```python3 retrieve-marathon-competitors.py```

This creates a file `runners.json`, which lists all the competitors running the Women's Olympic Marathon. This includes their name, birth date, and what country they represent (nationality).

### Step 2: Reformat
```python3 parse-competitors.py```

I wrote this script just to reformat the json from the previous step into a csv. This creates `competitors.csv`.

### Step 3: Get each competitor's past performances
```python3 retrieve-competitor-results.py```

This takes in the file from the previous step and then creates `individual-performances.csv`. Each row is an individual race performance. I got information like the venue, the date of the race, what country it took place in, and the athlete's race time from a World Athletics GraphQL query. It also includes the competitor's name, iaaf ID, nationality, and their birthdate from the previous step (so this data gets repeated because most runners have run a half-dozen or more marathons in their professional careers).

### Step 4: Train the model, and predict the future
```python3 train-model.py```

This script does a couple things. This trains a Polynomial regression model on the data from the previous step. I didn't find it important to train the model on features like the athlete's name so I dropped that column among a couple others. 
It then predicts each competitor's Paris performance and prints the results in order by race time.

```
Polynomial Model Accuracy score is:  0.3874858240673147
---------- Athlete Predicted Results ----------
             SCHLUMPF, Fabienne (SUI): 02:52:46
                ELMORE, Malindi (CAN): 02:56:36
           MCCORMACK, Fionnuala (IRL): 03:30:02
...
```
And there you have it! According to my model, Fabienne Schlumpf of Switzerland will win in Paris with a time of 2:52!

#### Obviously I didn't achieve much success - 38% accuracy is beyond poor performance.

I think most of this is to blame on my illiteracy of machine learning. I've only ever trained a classification model before, I have no idea how to engineer my features properly, and I've never been professionally trained or educated on AI topics before. What I do know about ML constitutes about a 5th-grade level of understanding from that one single application from my first ever job to which I contributed only a little bit.

But I also think that this is a testament to how fickle, unpredictable, and exciting endurance sports are. There's a reason teams and athletes compete and we breathlessly watch: we don't know the outcome! And if someone is a favorite to win, a total shoe-in, head-and-shoulders above the rest of the competition, it's still important that they go prove it. Winning a marathon is not just raw physical strength - most of it is tied up in the execution: how prepared you are, your mental state and resiliency, and about a million other variables all of which have to align with the stars but which can create the perfect conditions for dazzling underdog performances that totally upset the competition and can't really be described by Machine Learning. So I for one am hoping to see something special from Team Switzerland!

### Opportunities for Improvement
- My model is trained as if the marathon were a time trial. It's not! Times basically don't matter in pro-racing and it's all about the strategy, tactics, and psychological warfare you can exact on your opponents to get the top spot. I'd love to figure out how to model on head-to-head matchups as I'm sure many of these athletes have raced each other.
- Incorporate more data. I'd really like to get weather data for each race, as temperature and humidity can be big factors for performance. Then on the day of the Olympic Marathon, I could see what the weather is like in Paris, and make predictions with that new information. Additionally, getting race course information like net elevation gain or number of bends in the course would be super interesting as well.
- General programming improvements. My code is pretty bush-league (as I wanted to finish this before the race occurs on August 11), I haven't programmed in python in a while, and all of my knowledge on how to use pandas, scikit-learn, and numpy are from first-page searches on Stack Overflow. Gaining some actual expertise would do me good!