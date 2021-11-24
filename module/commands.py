# ['list', 'get', 'set', 'cat', 'rm', 'clear', 'exit','write','diff','restore','rename']
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from . import mtconf, dict_diff
from . import command_apis as api
import sys, os.path
diff_str = dict_diff.diff_str
diff_get = dict_diff.diff

#@api.debug
@api.no_param
@api.require_api_arg("conf")
def list(conf,param):
    print("-- List of entries start --")
    ran = False
    for x in conf:
        print((", " if ran else "") + x, end="")
        ran = True
    print()
    print("-- List of entries end, totally " + str(len(conf)) + " entries --")

#@api.debug
@api.require_param
@api.require_api_arg("conf")
def get(conf,param):
    if param[1] in conf:
        print(conf[param[1]])
    else:
        print("Entry \"{}\" does not exists.".format(param[1]))

#@api.debug
@api.require_param
@api.require_api_arg("conf")
def set(conf,param):
    if param[1].__contains__(" "):
        print("Entry key cannot contain spaces!")
    else:
        if param[1] in conf:
            print("Current value of \"{}\": {}".format(param[1],str(conf[param[1]])))
        else:
            print("Creating new entry \"{}\"".format(param[1]))
        user_input = prompt('Enter the value: ',
            history = FileHistory('value_history.txt'),
            auto_suggest = AutoSuggestFromHistory(),
            )
        conf[param[1]] = user_input

#@api.debug
@api.no_param
@api.require_api_arg("conf")
def cat(conf,param):
    print(mtconf.render(conf))

#@api.debug
@api.require_param
@api.require_api_arg("conf")
def rm(conf,param):
    if param[1] in conf:
        print("You are going to delele the entry \"{}\".".format(param[1]))
        print("Do you really want to continue?")
        if input("(Yes/No) ").lower() == "yes":
            conf.pop(param[1])
        else:
            print("Cancled.")
    else:
        print("Entry does not exists!")

#@api.debug
@api.no_param
@api.require_api_arg("conf")
def clear(conf,param):
    print("You are going to delele all contents of the mt.conf.")
    print("This is IRREVERSABLE. Do you want to continue?")
    if input("(Yes/No) ").lower() == "yes":
        conf.clear()
    else:
        print("Cancled.")

#@api.debug
@api.no_param
@api.require_api_arg("orig_conf")
@api.require_api_arg("file")
@api.require_api_arg("conf")
def exit(file,param,orig_conf,conf):
    adds,dels = diff_get(orig_conf,conf)
    if len(adds) + len(dels) != 0:
        print("You have unsaved changes. Do you still want to continue?")
        diff_str(orig_conf,conf)
        if input("(Yes/No) ").lower() != "yes":
            print("Cancled.")
            return
    file.close()
    print("Bye")
    sys.exit()

#@api.debug
@api.require_api_arg("orig_conf")
@api.require_api_arg("file")
@api.require_api_arg("conf")
def write(conf,file,param,orig_conf):
    if not(len(param) == 2) or (param[1].lower() != "nobackup"):
        print("Creating backup file...")
        file_dir,file_name = os.path.split(file.name)
        back_dir = os.path.join(file_dir,"~" + file_name)
        backup_file = open(back_dir,"w")
        backup_file.write(mtconf.render(orig_conf))
        backup_file.close()
        print("Backup file at {}".format(back_dir))
    print("Writing data into file...")
    file.write(mtconf.render(conf))
    api.set_api_arg("orig_conf",conf.copy())
    print("Done")

#@api.debug
@api.no_param
@api.require_api_arg("orig_conf")
@api.require_api_arg("conf")
def diff(param,orig_conf,conf):
    adds,dels = diff_get(orig_conf,conf)
    if len(adds) + len(dels) != 0:
        diff_str(orig_conf,conf)
    else:
        print("No changes.")

#@api.debug
@api.require_param
@api.require_api_arg("conf")
def rename(conf,param):
    if param[1] not in conf:
        print("Rename failed: source not exists!")
    else:
        user_input = prompt('Enter the new name: ',
            history = FileHistory('name_history.txt'),
            auto_suggest = AutoSuggestFromHistory(),
            )
        if user_input.__contains__(" "):
            print("Entry key cannot contain spaces!")
        elif user_input in conf:
            print("Rename failed: target already exists!")
        else:
            print("Renaming...")
            conf[user_input] = conf[param[1]]
            conf.pop(param[1])
            print("Rename done.")
