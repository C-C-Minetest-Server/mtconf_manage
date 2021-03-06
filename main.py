from module import mtconf, commands, command_apis
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter, ThreadedCompleter
from inspect import getmembers, isfunction

cmds = [o[0] for o in getmembers(commands) if isfunction(o[1]) and not o[0].startswith("_")]

CMDCompleter = ThreadedCompleter(WordCompleter(cmds, ignore_case=True))

def main():
    file_path = prompt('Enter the mt.conf path: ',
        history = FileHistory('path_history.txt'),
        auto_suggest = AutoSuggestFromHistory()
        )
    try:
        file = open(file_path,'r+',encoding='utf-8')
    except IOError:
        print("ERROR: Error while accessing file?")
    conf = mtconf.fromfile(file)
    command_apis.set_api_arg("orig_conf",conf.copy())
    command_apis.set_api_arg("conf",conf)
    command_apis.set_api_arg("file",file)
    while True:
        user_input = prompt('mtconf> ',
            history = FileHistory('history.txt'),
            auto_suggest = AutoSuggestFromHistory(),
            completer = CMDCompleter,
            )
        params = user_input.split(' ',1)
        if len(params) == 0:
            continue
        elif params[0] == "help":
            for x in cmds:
                print("{}: {}".format(x,command_apis.helps[x]))
        else:
            try:
                getattr(commands, params[0])(param=params)
            except AttributeError:
                print("Unknown command: " + params[0])



if __name__ == "__main__":
    main()
