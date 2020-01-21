# Proposal

## What will (likely) be the title of your project?

Title ideas:
"YouNoia" (a play on "eunoia")
"Colorside"

## In just a sentence or two, summarize your project. (E.g., "A website that lets you buy and sell stocks.")

A website for aesthetic stimulation to both the general wandering soul and to the artist in search of inspiration through color.
Associates user input (a word) with corresponding colors, based on semantics.

## In a paragraph or more, detail your project. What will your software do? What features will it have? How will it be executed?

Takes in user input via a form in html in the form of a word, associates that word with a set of colors (generate as the resulted of machine learning), projects those colors in a format on screen for the user to experience or use.
I would obtain a large dataset, either through manual surveys of people around me or from existing studies online (or a combination of those), with the dataset associating all kinds of English words with specific colors.
These colors would either be in RGB format or html color code format. More research will be conducted to see which representation is more applicable to my project.
Then, I would train the machine (computer) with this dataset in hopes of it being able to accurately (or reasonably) associate relevant color with any new word input. This color (or set of colors) would be projected via html and CSS on the webpage.


## If planning to combine CS50's final project with another course's final project, with which other course? And which aspect(s) of your proposed project would relate to CS50, and which aspect(s) would relate to the other course?

N/A

## In the world of software, most everything takes longer to implement than you expect. And so it's not uncommon to accomplish less in a fixed amount of time than you hope.

### In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?

Obtain large enough dataset, successfully understand how to implement and code machine learning algorithms, and successfully train the machine to associate mood/emotion related words with a single color, that single color being a basic color in the range of white, black, red, green, orange, blue, etc., then successfully projecting that color on screen.

### In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?

Associate mood/emotion words with more than just the basic colors, using some kind of degree of similarity factor, and project multiple colors on screen.

### In a sentence (or list of features), define a BEST outcome for your final project. I.e., what do you HOPE to accomplish before the final project's deadline?

Be able to output reasonable colors for more abstract or non-mood words (this goes into more abstract connotations), e.g. for multiple random words, have most of their corresponding outputs not feel super random.

## In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research? If working with one of two classmates, who will do what?

I will need to understand how machine learning works, how to utilize Keras or Tensorflow, how to code my own machine learning program so that it fits my end goal.
Then, I need to do a survey of existing research on word-color association, sentiment analysis, word-connotation, color impact, etc. and understand details about this relationship, so that I can create a comprehensive yet feasible methd for data collection, whether from the peaople around me, myself, or existing online datasets.
Then, I need to go through the process of actually creating my model, feeding it input, and receiving output. Once that is working, I need to relatively optimize my model.
Then, I need to figure out how to connect the machine learning aspect with HTML visualization.
