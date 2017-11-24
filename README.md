# AINltkAndSonification
Using jython music to sonify images and text data. 
Using NLTK to read understand e-books scrapped online. 
Counting and plotting frequency distribution of interactions between people in the books. 
Dynamically creating a website using genetic algorithm using entities(Person, location, timelines, etc.) from the book.

I.	Program Execution

1.	Sonify temperature data – 
a.	Execute file SHANTANU_temperatureMusic.py in the JEM editor
b.	Execute file temperaturePlot.py to get the line plot, output is as below:
<img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/temperaturePlot.png" />
 
Have plotted data only of first four years,  but we can see the pattern (mountains-valleys) in the plot, same is evident in the music as well, high pitched notes followed by low pitched followed again by high pitched notes. 
2.	Sonify grayscale image –
a.	Execute file SHANTANU_grayScaleSonify.py in the JEM editor


3.	Getting Flesch score of ebooks, execute readabilityTestAgent.py and just follow the CLI
Below is the output for Flesch Book Readability score:
<img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/flschScoreCLI.png" />  
Selecting appropriate options for category, sub category and book

Result will be as follows:
<img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/FLSCHCLI.png" />
 
Evaluate at least 2 books for  the plotting functionality to work.
Press ‘p’ for plot to appear, result will be as follows:
<img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/flschScorePlot.png" />

Press 0 anytime to go back to the previous menu.

For Natural Language Entity Relationship extraction from one of the books, select option 2.
<img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/NLPOptionCLI.png" />

Select 1 to view heatmap between person verb person, as below:
<img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/person2personIntrHeatmap.png" />

Select 2 to view scatterplot between people and locations, as below:
 <img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/person2locationScatterPlot.png" />


Select 3 to search and location download images as below:
 <img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/sonifySearchLoc.png" />

Now, in the jythonMusic folder open SHANTANU_searchsonify.py. This will play the sound from the corresponding location sentence and display an image as follows:
 
Output image shown as below:
 <img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/SentenceSonify.png" />


Website created using genetic algorithm:
Follow the command line interface to select the appropriate options, you will have to select the webpages you liked in each generation. 
 

Below are 2 samples of webpages created:
 <img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/website.jpg" />
 
  <img src = "https://github.com/shantanuspark/AINltkAndSonification/blob/master/output_images/website.jpg" />

