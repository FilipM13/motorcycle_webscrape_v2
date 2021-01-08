def ask(question, rv_type=False, answers=[], closed=False):
  '''
  Function asking question. Makes input request, validates input and returns specific type value.

  Parameters:

  question: string

  rv_type - type of return value you want to get (int, str, float, etc.)

  answer: list - possible answers for closed type question (requires closed=True)

  closed: bolean - True if question is closed (requires answers), False if question is open

  Return:

  specific type input value 
  '''
  #adds exit to list of answers
  if 'exit' not in answers:
    answers.append('exit')
  ad = '/'.join([str(a) for a in answers])

  #starts validation loop
  valid = False
  while not valid:
    is_ans = False
    is_type = False

    #take input
    response = input(question + f' ({ad}) ').lower()

    #if the answer is empty string ask again
    if not response:
      print('Answer is obligatory.')
      continue
    
    #if response is 'exit' return it -> main.py closes script
    if response == 'exit':
      return response

    #checks if response is in answers or if it is an open question
    if (response in answers) or (closed == False):
      is_ans = True
    else:
      print('Invalid answer.')
    
    #checks if response can be transformed into specific data type
    if (rv_type != False):
      try:
        response = rv_type(response)
        is_type = True
      except:
        is_type = False
        print('Invalid answer.')
    else:
      is_type = True
      
    #if all conditions are satisfied response is returned and loop is closed
    if is_type and is_ans:
      valid = True
      return response

def save(offers: list, table_name: str):
  '''
  Function saves offer list to MySQL database. Autotically deletes offers older than 180 days.

  Parameters:

  offers: list - list of offers to be saved in file

  file_name: str - name of file 
  '''
  #import mysql 
  import mysql.connector

  #login to to mysql
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
  )

  #create cursor
  mycursor = mydb.cursor()

  #creates database if there is none
  mycursor.execute('''
    CREATE DATABASE IF NOT EXISTS motorcycles;
  ''', [])

  #relog (close old connection and open new one with specified database)
  mycursor.close()
  mydb.close()
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="motorcycles"
  )
  mycursor = mydb.cursor()

  #creates table for a certain motorcycles
  mycursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name}(
      offer_date DATE DEFAULT (CURDATE()),
      title VARCHAR(255) NOT NULL,
      price DECIMAL(12, 2) NOT NULL,
      url_link VARCHAR(255)
    );
  ''')

  #modifies offers (list of lists -> list of tuple)
  offers = [tuple(o) for o in offers]

  #inserts offers to table
  mycursor.executemany(f'''
    INSERT INTO {table_name} 
      (title, price, url_link)
    VALUES
      (%s, %s, %s)
  ''', offers)
  mydb.commit()

  #delete offers older than 180 days
  mycursor.execute(f'''
    DELETE FROM {table_name} 
      WHERE DATEDIFF(offer_date, CURDATE()) > 180;
  ''', [])
  mydb.commit()

  #close cursor and connection
  mycursor.close()
  mydb.close()

def search(item_name: str, min_cc: int, max_cc: int, max_num=10):
  '''
  Function makes request http request, downloads page as html text file and extracts data from it.

  Parameters:

  item_name: str - entry to be searched on webside

  min_cc: int - minimal cc of motorcycle 

  max_cc: int - maximal cc of motorcycle

  max_num: int - maximal number of offers to get

  Return:

  list of offers
  '''
  #check input types
  if not isinstance(item_name, str): raise Exception('Wrong type of input')
  if not isinstance(min_cc, int): raise Exception('Wrong type of input')
  if not isinstance(max_cc, int): raise Exception('Wrong type of input')
  if not isinstance(max_num, int): raise Exception('Wrong type of input')

  from bs4 import BeautifulSoup as bs
  import requests as rq

  offers = []
  #save html code of page as text
  html = rq.get(f'https://www.olx.pl/motoryzacja/motocykle-skutery/q-{item_name}/?search%5Bfilter_float_enginesize%3Afrom%5D={min_cc}&search%5Bfilter_float_enginesize%3Ato%5D={max_cc}&search%5Bfilter_enum_condition%5D%5B0%5D=notdamaged').text
  
  #create beautiful soup obejct with lxml formating
  soup = bs(html, 'lxml')
  
  #extract all offer divs -> list
  offer_tags = soup.find_all('div', class_='offer-wrapper') 
  
  #check numbers of offer
  if len(offer_tags) <= max_num:
    max_num == len(offer_tags) - 1
  
  #print header for cmd interface
  print(f'--->\t{item_name}\t<---') #print header for cmd interface
  
  #extract desired data from div
  for i in offer_tags[0:max_num+1]:
    try:
      target = i.find('h3', class_="lheight22 margintop5")  #title and link are stored in this location
      link = target.find('a')['href'].replace('\n', '') #take link
      name = target.find('a').text.replace('\n', '')  #take title
      price = i.find('p', class_='price').text.replace('\n', '')  #take price as string with currency
      price = ''.join(list(filter(lambda x: (x.isnumeric() or x=='.'), price))) #convert price to decimal without currency
      offers.append([name, price, link])  #add extracted data to offers
      print(f'{name} - {price}')  #print results to cmd interface
    except: #if there is no offer with these parameters (name, min_cc, max_cc) program would throw an error, this way it will pass instead
      pass
  
  #return offers as list
  return offers

def show_tables():
  '''
  Function fetching and returning list of tables in motorcycle database.
  '''
  import mysql.connector
  #login
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="motorcycles"
  )
  mycursor = mydb.cursor()

  #take table names
  mycursor.execute('''
    SHOW TABLES;
  ''', [])
  tables = mycursor.fetchall()
  tables = [i[0] for i in tables]
  tables.insert(0, 'Tables:')
  tables ='\n'.join(tables)
  return tables

def run(coded):
  '''
  Function decoding string to extract specific options for selecting data from database.

  Parameters:

  coded: str - string alike one in user manual

  Return:

  list of offers
  '''
  import mysql.connector
  tn = ''
  fil = ''
  asc_desc = ''
  lim = ''

  #decode instructions
  parts = coded.split('.')
  for p in parts:
    if 'get offers from' in p:
      tn = p.replace('get offers from ','')
    if 'order offers by' in p:
      order = p.replace('order offers by ','')
      order = order.split(',')
      fil = order[0]
      if len(order) == 2:
        asc_desc = order[1]
      if 'ascending' in asc_desc: asc_desc = 'ASC'
      if 'descending' in asc_desc: asc_desc = 'DESC'
    if 'take top ' in p:
      lim = p.replace('take top ','').replace('offers','')

  #generate query
  query = f'''
  SELECT DATE_FORMAT(offer_date, '%Y/%c/%d'), title, CONVERT(price, FLOAT), url_link 
  FROM {tn}
  '''
  if fil != '': 
    query += f'ORDER BY {fil}'
    if asc_desc != '':
      query += f' {asc_desc}'
  if lim != '': query += f'\nLIMIT {lim}'
  query += ';'

  #login
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="motorcycles"
  )
  mycursor = mydb.cursor()

  #run query
  mycursor.execute(query,[])
  return mycursor.fetchall()

def save_txt(file_name, offers):
  '''
  Function saving list of offers to txt file.

  Parameters:

  file_name: str 

  offers: list
  '''
  #check if file_name is correct
  if any( not c.isalnum() for c in file_name) or '.txt' in file_name: raise Exception('Wrong file_name.')

  #change offers from list of tuples to list of strings
  of = []
  for i in offers:
    of.append(f'{i[0]} - {i[1]} - {i[2]} PLN - {i[3]} \n')
  offers = of

  #save offers
  file_name += '.txt'
  file = open(file_name, 'w')
  file.writelines(offers)
  
read_user_manual = '''
----- USER MANUAL -----
Taking data from database: 
When asked 'What do you want to get from database?' you can specify what offers and in what order do you want to get.
Scheme:
Get offer from <table name>. Order offers by <date / price>, <ascending / descending>. Take top <integer> offers.
First sentence is obligatory, the other 2 may be omitted.

Showing tables:
To get available table names write 'show tables' when asked 'What do you want to get from database?.

Saving:
If you answered 'yes' to 'Do you want to save offers to txt file?' you will be asked for file name.
DO NOT INCLUDE special characters, spaces or file extension (.txt) in file name.
Offers will be saved in this format:
  ofer_date - title - price PLN - url_link
File with offers will be created in current directory of executable file.
'''