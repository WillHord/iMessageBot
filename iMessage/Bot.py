from threading import Thread
import sqlite3
from time import sleep
import subprocess
from inspect import signature
from inspect import getmembers
from inspect import ismethod
from importlib import import_module

from .Message import Message, MessageSent
from .User import User
from .Image import Image
from .Errors import *


class bot():
    """[summary]

    Returns:
        [type]: [description]
    """
    DebugMode = False

    def __init__(self, prefixes):
        """[summary]
        """
        if prefixes != None and prefixes != []:
            if isinstance(prefixes, list):
                self.prefixes = prefixes
            else:
                self.prefixes = list(prefixes)
        else:
            raise InvalidPrefixes(f"Prefixes: {prefixes} are not valid")

        self.extensions = []
        self.extensionCommands = {}

        self._running = False

        self.queue = []
        self.database = "/Users/User/Library/Messages/chat.db"
        self.DefaultChat = ''


    def import_extension(self, extensionName):
        """[summary]

        Args:
            extensionName ([type]): [description]
        """
        temp = import_module(extensionName)
        temp.setup(self)
        return

    def add_extension(self, extension):
        """[summary]

        Args:
            extension ([type]): [description]
        """
        def get_methods(obj):
            """[summary]

            Args:
                obj ([type]): [description]

            Returns:
                [type]: [description]
            """
            ls = []
            for i in range(len(getmembers(obj, predicate=ismethod))):
                if getmembers(obj, predicate=ismethod)[i][0] != '__init__':
                    ls.append(getmembers(obj, predicate=ismethod)[i][0])
            return ls
        try:
            self.extensions.append(extension)
            try :
                i = max(self.extensionCommands.keys())
                i += 1
                self.extensionCommands[i] = {'Name':type(self.extensions[i]).__name__, 'Commands':get_methods(self.extensions[i])}
            except:
                self.extensionCommands[0] = {'Name':type(self.extensions[0]).__name__, 'Commands':get_methods(self.extensions[0])}
            return
        except:
            print(f"Extension {extension} could not be loaded")
            return


    def run_command(self, message):
        """[summary]

        Args:
            message ([type]): [description]

        Returns:
            [type]: [description]
        """
        if message.Text[0] in self.prefixes:
            text = message.Text[1:].split()
            command = text.pop(0)

            argdict = {}
            run = None

            for i in self.extensionCommands:
                for j in self.extensionCommands[i]['Commands']:
                    if command.lower() == j.lower():
                        run = getattr(self.extensions[i],j)
                        break

            if run == None:
                print(f"Command {command} could not be found")
                return
            else:
                if len(signature(run).parameters) != 0:
                    for i in range(len(signature(run).parameters)):
                        if list(signature(run).parameters.keys())[i] == 'ctx':
                            argdict[f'arg{i}'] = 'ctx' #getctx()
                        elif i == (len(signature(run).parameters) - 1) and len(text) > 1:
                            lastargument = ' '.join(text)
                            argdict[f'arg{i}'] = lastargument
                        elif len(text) > 0:
                            argdict[f'arg{i}'] = text.pop(0)
                        else:
                            print(f"ERROR: Not Enough Arguments for function: {command}")
                            return NotEnoughArgs

                    run(*argdict.values())
                    return

                else:
                    run()
                    return

        else:
            print(f"Passed invalid message: {message}")
            return


    def sendMessage(self, Chat, Message):
        """[summary]

        Args:
            Chat ([type]): [description]
            Message ([type]): [description]

        Returns:
            [type]: [description]
        """
        if bot.DebugMode != True:
            subprocess.run(["osascript","./iMessage/sendMessage.scpt",Chat,Message])
            return MessageSent
        else:
            print(f"Message: '{Message}' sent to Chat:{Chat}")
            return

    def getData(self):
        """[summary]
        """
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        rowId = c.execute("SELECT * FROM message ORDER BY ROWID DESC LIMIT 1;").fetchone()[0]
        #currentMessage = Message(rowId)
        #self.queue.append(currentMessage)
        conn.close()

        while self._running == True:
            conn = sqlite3.connect(self.database)
            c = conn.cursor()

            currentMessage = Message(rowId)

            if currentMessage.FullMessage != None:
                rowId += 1
                print(f"Now Processing Row: {rowId}", end="\r")
                self.queue.append(currentMessage)

            conn.close()
            sleep(0.2)

    def processData(self):
        """[summary]
        """
        while self._running == True:
            if len(self.queue) != 0:
                temp = self.queue.pop(0)
                if temp.Text != None:
                    if temp.Text[0] in self.prefixes:
                        self.run_command(temp)
                temp.storeData()
            sleep(0.5)


    def start(self):
        """[summary]
        """
        if self._running == True:
            print("The Bot is already running")
            return
        else:
            self._running = True

            self.t1 = Thread(target = self.getData)
            self.t2 = Thread(target = self.processData)

            self.t1.start()
            self.t2.start()
            return

    def stop(self):
        """[summary]
        """
        self._running = False
        self.t1.join()
        self.t2.join()
        return

    def restart(self):
        """[summary]
        """
        self.stop()
        self.start()
        return