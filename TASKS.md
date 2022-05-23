# Development Tasks
These tasks will be in support of developing our system 

## Logging
### Development
Logging is an *integral* part of the development process. The tools developed for this task will be used across all 
modules. 
An easy way to think of logging is as a *replacement for print statements*. 
Each time a log event occurs, the time, date, module, and message are recorded to a *non-volatile* file.
This allows us as developers to look back at the log files and view any issues our program runs into when we are not 
actively monitoring it. 

#### Requirements

| RID | Name | Description |
| --- | ---- | ----------- |
| 00 | Available from any module | the ability to write events to the/a log file should be available from any module |
| 01 | Organized | whether the logs save to a single file or multiple, the origin module, time and date need to be clear |
| 02 | single instantiation | The logging module should be instantiated once at the beginning of the module creating logs |
| 03 | simple to use | The complexity of use should be no more than a print statement |
| 04 | capture tracebacks | stretch goal -- tracebacks may be created during try/except blocks, look into the details that may be collected to aid the debugging process |

#### Resources

- [Stack Overflow - Logging across modules](https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules)
- [Python Docs - Logging](https://docs.python.org/3/library/logging.html)
- [Python Docs - Logging Config](https://docs.python.org/3/library/logging.config.html)


## Maps
### Web

Much of the data we will be collecting will need to be displayed on maps. We need to decide what graphs will be useful
(or look useful) and attempt to build them. For now, we may use fake data to verify the functionality of the maps.

The preferred method for creating these maps is to use Plotly. The reason is the integration with dash is fairly 
seamless. Additionally, Plotly has several of the maps built in. 

This task is complex and has many parts. Please dig in and see what we can do with the maps available in the resources 
link. 

#### Requirements

| RID | Name | Description |
| --- | ---- | ----------- |
| 00 | Examples of useful maps | gradient maps, map of nodes as points, etc |
| 01 | Simple to create | each type of map should be created using a function in the maps module taking the required data as arguments |
| 03 | stretch goal - increased interactivity | look into clickable points for nodes or other data that may be displayed when hovering over an area or point |
| 04 | stretch goal - animated maps | animate the changes over time - like a weather map [see ecample - second map](https://plotly.com/python/bubble-maps/) |
| 05 | stretch goal - one click change map view | [see second map for example - polotical candidate analysis](https://plotly.com/python/mapbox-county-choropleth/)


#### Resources

- [Plotly Documentation](https://plotly.com/python/maps/)
- [Map Module](source/map.py)


## Graphs
### Web 

Graphs are another way we may display the data to users. Plotly has an extensive library of graphs. 

The objective of this investigation is two parts.

- Look through the available graphs and determine which graphs may be good for displaying the data we collect
- Create a function to create each type of graph and demonstrate the result with example data

#### Resources
- [Plotly Overview](https://plotly.com/python/)


## Database
### Backend

This task is mainly creating queries for specific cases within the database. 

An example would be to get the temperature values for all nodes in an area between a start and end date. 

We are using a document based database called TinyDB. The specific queries will be developed over the course of the 
project as required. 

#### Resources
- [TinyDB Documentation](https://tinydb.readthedocs.io/en/latest/)

