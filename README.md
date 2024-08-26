# trueRandomNumbers
An actually random number generator: [pratyushv1.pythonanywhere.com](https://pratyushv1.pythonanywhere.com/)

## Some Backstory...
I recently read about how CloudFlare(An international security company) needed a solution for getting random input for their traffic generators. This lead me down a rabbit-hole of random number generators, particularly in computing, as I figured out it is impossible to truly generate random numbers just by algorithms. I learned, that in modern times, there are external factors(such as radiation in the air) to assist in calculating random numbers! I wanted to replicate this for those of us who don't have radiation sensors lying around, bringing us to this project.

## The Project
I want to make a python-flask web app, that takes in random inputs from the user(from various factors), allowing for the perfect local, random number generator!

## How to Use
This repo is mainly for documenting progress and storing raw code, meaning you can still run the project locally, and by yourself. However, since everyone may not be able to run the code, I decided to turn this webapp into a website(using pythonanywhere.com). This will allow me to share the project more effectively with you guys(but please feel free to run the source code yourself)!. **LINK: [pratyushv1.pythonanywhere.com](https://pratyushv1.pythonanywhere.com/)**

## Interesting Stuff, that you probably don't need to know
At the beginning of this project, I really wanted to make the random number individual to the user, so I started out with the idea of using the microphone and camera of the user to calculate ambient background effects, that would allow for a truly random number. However, I slowly started realizing that this project wouldn't be accessible if I did this, as there was always one dependency that cannot be transferred through operating systems. This lead me to start using APIs as they are a more simple(and arguably more random) way of getting numbers to input as my seed.

Now I am currently utilizing 5 APIs(that all contribute to the randomness):
  - Random.org: It just provided a random number everytime it is called
  - OpenWeather: 

-AI was used for the ideas, nothing else!!!(just for citation)


