The website is designed to be minimalist, with considerations
made with regards to background color not detracting from the functions of the site.

LINKS:
Google Form: https://goo.gl/forms/Rc7LrM4EG0iEvkCk1
YouTube video: https://youtu.be/Pu63pSYtd34

STEPS OF PROJECT:
1) Initial Brainstorm
        I wanted to do something with color. I live my life in color. Everwhere I go, the first instinctive thing I do in take in the visuals of my surroundings and see the color.
        Sometimes, the current day will have a color to me. "Aesthetics" and "aesthetically pleasing" are at the top of my most used vocabulary. I wondered why do colors affect me so much?
        I'm reading a book right now wirtten by a designer on how aesthetics can greatly impact our psychology and happiness.
        The abstract and concrete associations that people make between feelings, emotions, even simple words with colors is fascinating.
        Specifically, I realized that if I could figure out these associations, it would be beneficial to data visualization, like product design, or art, or any endeavor to create something with a visual component that elicits an emotional response from other people.
2) Research
        I researched existing studies on emotion or word-color association.
        I found this study particularly helpful in determining what basic emotions and colors to include in my survey:
        "Emotions Evoked by Common Words and Phrases: Using Mechanical Turk to Create an Emotion Lexicon" by Saif M. Mohammad and Peter D. Turney at Institute for Information Technology, National Research Council Canada
3) Planning
        I ran through my head multiple different ways I could implement this project, e.g. should I make my own survey in IDE or use Google Forms, how should I analyze the data, what kind of output do I want to put on the website, etc.
        This part of my process took much longer than expected, especially narrowing it down to a detailed step by step plan that accomplished my original goal. See details of each step in "Implementation" below.
4) Implementation
    a) Data collection
        Designing Survey
            I spent A LOT of time doing this step because I had to take all these things into consideration:
                Issue: Do I make my own survey on my website, or do I make a Google form?
                    Solution: I went with Google form, because I wanted to send my survey to mailing lists of people for maximum response, and if I wrote it in IDE I wouldn't be able to share it like that.
                Issue: What do I ask for in the form?
                    Solution: Stick to basics because this is an initial prototype and it needs to work on a small scale before going too complex.
                            Use the 8 common human emotions from Robert Plutchik's theory of emotion, plus the emotion of "calm" as a neutral emotion.
                            Use the basic colors, and only one shade of each:
                            Issue: Different shades of a color can be associated with different emotions
                                Solution: I admit, the scope of this project does not effectively account for a wider range of colors in the data collection. Further development could include a web-hosted custom form with color selectors from a gradient rather than a short list.
                Issue: How do I make this form so that more people are likely to answer it?
                    Solution: Keep it short. Ask simple questions and make it easy to navigate/answer each question. Therefore, don't ask for text responses - only a dropdown menu where they can select because it's fast.
                            Don't make the questions long.
                            Offer gift card incentive! (And follow up)
                Issue/Solution: Make sure to account for colorblindness of respondent!
        Sending Survey
            Harvard mailing lists! Group chats I'm in! Friends, family, people I don't know. This part went better than I expected. I got 127 responses in a short amount of time! Even from lots of people I don't know personally but were willing ot help me on my project.
            The resposes were automatically recorded in a Google Sheet; each column is an emotion, each row is for a single person's response for color for each emotion
        Analyzing data with Google Sheets Functions
            Function I used to total, for each emotion, the amount of responses for each color: =IF(D$128, COUNTIF(D$2:D$127, CONCATENATE("=",$C129)) + 0.5 * E129, COUNTIF(D$2:D$127, CONCATENATE("=",$C129)))
            Function I used to find most associated emotion per color=INDEX(D$1:U$1, 1, MATCH(MAX(D129:U129), D129:U129, 0))
        Transfering to SQL database
            Each color-emotion pair was manually entered into a SQL database.
            I chose a database, not a Python dictionary, because for future developments I'd like to include the survey on my website and dynamically update the data to analyze.
    b) Creating website
        Finding colorpicker
            After much search and experimentation, I found and chose the Spectrum colorpicker because it's a mim=nimalist look that provides all ranges of colors. See script for the Spectrum website
        Implementing colorpicker in a form
            I spent hours on w3schools and IDE trying to learn and edit JavaScript to implement the colorpicker to show up correctly and work in a form (because it appeared correctly outside the form).
        Performing distance and the percentage calculations
            After converting all colors both in the database and the input to the correct orm of integer valued RGB triples, I decided that I would calculate distance Euclidean style to mathematically determine the amount of association between colors.
        Outputting calculations
            I wanted a simple, clear, minimalist look, So I kept the white background and only showed the top 3 associated emotions for each word, rather than all emotions in descending order.
            I figured out how to sort emotions by distance from input while keeping their respective associations with the right color, calculated proportions and then scaled percents.
        Creating homepage, About page, Survey page, and Contact page