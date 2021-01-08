from tools import *

#show list of available tables
print(show_tables())

#app loop
do = True
while do:

  #ask for instructions
  response = ask('What do you want to get from database?', answers=['?']).lower()

  #exit
  if response == 'exit': break

  #print user manual
  elif response == '?': print(read_user_manual)

  #show list of available tables
  elif response == 'show tables': print(show_tables())

  #run instructions
  else: 

    try:
      offers = run(response)

    #if instructions were incorect print message
    except:
      print('Wrong input. Make sure you write instruction according to user manual. (type \'?\' to get user manual)')
      continue

    #if instructions were correct print results
    else:
      print('Selected offers:')
      for i in offers:
        print(i[:-1])

      #ask about saving offers to file
      response = ask('Do you want to save offers to txt file?', answers=['yes', 'no', '?'], closed=True).lower()
      if response in ['exit', 'no']: break
      elif response == '?': print(read_user_manual)
      elif response == 'yes': 
        saving = True
        while saving:
          response = ask('Enter file name: (no special characters, no extension)').lower()

          #exit
          if response == 'exit': break

          #save to file
          else:
            try:
              save_txt(response, offers)
            except:
              print('Make sure file name is correct. (type \'?\' to get user manual)')
            else:
              saving = False

  #ask about continuing 
  response = ask('Do you want to continue?', answers=['yes', 'no', '?'], closed=True).lower()

  #exit
  if response in ['exit', 'no']: break

  #user manual
  elif response == '?': print(read_user_manual)

  #continue
  elif response == 'yes': pass
      