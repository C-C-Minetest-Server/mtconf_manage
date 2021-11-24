# ['list', 'get', 'set', 'cat', 'rm', 'clear', 'exit','write']
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from . import mtconf, dict_diff
from . import command_apis as api
import sys, os.path
diff_str = dict_diff.diff_str

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
@api.require_api_arg("file")
def exit(file,param):
    print("Make sure you saved all your jobs. Do you still want to exit?")
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
    print("Done")
