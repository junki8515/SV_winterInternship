# Simple patent search (function1)

#### **function1.1 search()**

The search function is a function that returns the information searched for in google patent in the form of a dataframe through the input of the maximum number of search words and keywords through the Python input function.

```python
keyword, result = search()
```

##### **Parameters**

- **keyword** : keywords that used in searching
- **result** : searched dataframe


  

#### **function1.2 search_advanced()**

The search_advanced function is a function that connects to the link to obtain assignee and inventor information, gets the html structure, adds only necessary data to the data frame, and returns it.

```python
result2 = search_advanced()
```

##### **Parameters**

- **result2** : dataframe that added inventor, assignee



#### function1.3 field_search()

The field_search function performs a function of filtering only the data corresponding to the search condition through the search of the data frame.

```python
result3 = field_search(result2)
```

##### **Parameters**

- **result3** : filtered dataframe contains input querry
- **result2** : input dataframe for search



#### function1.4 paper_citation()

The paper_citation function returns the cited information of a specific patent. To use the function, input a specific patent number of the dataframe through the Python input, then access the link and return dataframes containing citation information.

```python
citation, non_patent = paper_citation(result)
```

##### **Parameters**

- **citation** : dataframe that contains citation information
- **non_patent** : dataframe that contains non patent citation information
- **result** : input dataframe that contains patent code which want to search



# Detailed search function (function2)

#### **function2.1 search_details()**

search_details performs dynamic crawling based on the contents of the input txt and returns the necessary information in the form of a list. The format of the txt file at this time is as follows.

```python
patent_name, patent_code, inventor, assignee, country = search_details()
```

##### **Parameters**

- **patent_name** : list contains patent_name
- **patent_code** : list contains patent_code 
- **inventor** : list contains inventor 
- **assignee** : list contains assignee 
- **country** : list contains country 



#### function2.2 search_details_df()

search_details_df returns data that exists in list form in dataframe form. At this time, the input order should be the same as in the example.

```python
output = search_details_df(patent_name, patent_code, inventor, assignee, country)
```

##### **Parameters**

- **output** : generated dataframe contains input lists



#### function2.3 change_ptname()

change_ptname modifies search results that appear as ... when searching in Google. In this case, static crawling is performed, but it takes a certain amount of time because you have to access each page and get the entire title. Therefore, this should only be done if the full patent title is needed.

```python
output2 = change_ptname(output)
```

##### **Parameters**

- **output2** : df contains changed patent name(...) to whole patent name
- **output** : input dataframe which want to change (...) to whole name 





# Patently Apple Search function (function3)

#### **function3.1 applepatent()**

Patently apple has many archives. If you access the archive, copy and paste the link and give it as input to the applepatent function, a data frame is returned.

Because it uses dynamic crawling, it takes a long time. In the example, 158 patent information was extracted, and the time it took was about 17 minutes.

At this time, the extracted patent information is as follows, and if other patent information exists, the function cannot be detected and must be corrected.

- 00,000,00
- starts with ‘20190’ or ‘20200’ or ‘20180’
- href contains ‘uspto’

```python
link = 'https://www.patentlyapple.com/patently-apple/autonomous-vehicle-technology/ '

df = applepatent(link)
```

##### **Parameters**

- **df** : searched dataframe
- **link** : link for apple patent archive



#### function3.2 applepatent_keyword()

It performs the same function as the applepatent function by receiving keywords and searching the site. Therefore, for details, refer to the documentation of the applepatent() function to obtain the relevant information.

```python
df = applepatent_keyword()
```

##### **Parameters**

- **df** : searched dataframe