from tools import *

do = True
while do == True:
  print(main_user_manual)

  #ask for search entries
  what = ask('What motorcycle do you want to find?')
  if what == 'exit': break
  cc_min = ask('Enter minimal CC:', rv_type=int)
  if cc_min == 'exit': break
  cc_max = ask('Enter maximal CC:', rv_type=int)
  if cc_max == 'exit': break
  num = ask('How many offers do you want to get?', rv_type=int)
  if num == 'exit': break
  
  #search for offers
  offs = search(what, cc_min, cc_max, num)

  #ask for saving offers
  response = ask('Do you want to save offers (links included)?', answers=['yes', 'no'], closed=True)

  #execute according to given answer
  if response == 'exit': break
  elif response == 'yes':
    print(show_tables())
    response = ask('Enter table name:', rv_type=str)
    if response == 'exit': break
    save(offers=offs, table_name=response)

  #end/continue
  response = ask('Do you want to find another motorcycle?', answers=['yes', 'no'], closed=True)
  if response in ['exit', 'no']: break
  elif response == 'yes': pass