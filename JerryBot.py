# -*- coding: utf8 -*-
from fbchat import Client
from fbchat.models import *
from credentials import USERNAME, PASSWORD
from modules.modules import modules
from modules.tag import tag
from configuration import prefixes
import sys
import multiprocessing
import modules.permissions as p


class JerryBot(Client):
    test = True
    modules = {}

    def __init__(self, email, password, test=True, debug=True,
                 user_agent=None):
        Client.__init__(self, email, password)
        self.test = test
        self.modules = modules

    def isCommand(self, command):
        for key, val in modules.items():
            if key == command:
                return val
        return False


    def get_permission(self, author_id, thread_id, thread_type, metadata, permission):
        print("in permissions")

        # build permissions
        temp = {
            p.MESSAGE_TIME: metadata["metadata"]["timestamp"],
            p.MESSAGE_AUTHOR: author_id,
            p.MESSAGE_MESSAGEID: metadata["mid"],
            p.USER_NAME: self.fetchUserInfo(author_id)[author_id].name,
            p.MESSAGE_THREADID: thread_id,
            p.FN_ADDUSER: lambda x, y: self.addUsersToGroup(x, thread_id=y),
            p.FN_REMOVEUSER: lambda x, y: self.removeUserFromGroup(x, thread_id=y),
            p.FN_CHANGE_NICKNAME: lambda x, y, z: self.changeNickname(x, y, thread_id=z),
            p.FN_GET_UID: lambda x: self.searchForUsers(x, limit=1)[0].uid,
            p.FN_GET_NAME: lambda x: self.fetchUserInfo(x)[x].name,
            p.FN_SEND_MESSAGE: lambda x, y: self.send(Message(text=x), thread_id=y,thread_type=thread_type),
            p.THREAD_NICKNAMES: lambda x: self.fetchGroupInfo(x)[x].nicknames,
            p.THREAD_PARTICIPANTS: lambda x: self.fetchGroupInfo(x)[x].particpants,
            p.FN_SEND_IMAGE: lambda x,y: self.sendLocalImage(x, message=Message(), thread_id=y, thread_type=thread_type),
            p.SELF_UID: self.uid
        }
        return temp.get(permission, None)

    def parse_message(self, author_id, message_object, thread_id,
                      thread_type, kwargs):
        # If the message starts w/ one of the specified prefixes
        message = message_object.text
        try:
            if message[0] in prefixes:
                # split the message into parts
                args = message[1:].strip().lower().split(" ")
                # first part is the command
                command = args[0]
                # rest is the arguments
                arguments = args[1:]
                # if there is a command for the argument
                command_module = self.isCommand(command)
                if command_module is not False:
                    # get the function and permissions list
                    module, permissions = command_module
                    perm_dict = {}
                    print("index of perms is: ", permissions)
                    # build the perms
                    for perm in permissions:
                        try:
                            perm_res = self.get_permission(author_id,
                                                           thread_id,
                                                           thread_type,
                                                           kwargs,
                                                           perm)
                            print("Perm is %s" % (perm_res))
                            perm_dict[perm] = (perm_res)
                        except Exception as e:
                            print("error %s" % (e))
                    print(perm_dict)
                    # pass the function the arguments and
                    # permissions dictionary
                    result = module(arguments, perm_dict)
                    return (True, result)
            elif message[0] == '@':
                # Tagging module
                result = tag(message[1:])
                return (True, result)
        except Exception as e:
            print(e)
            with open('error.log', 'w') as log:
                log.write("OOPS, THERE WAS AN ERROR:\n {}".format(str(e)))
            return (False, "Failing gracefully..")

        return (False, "")

    def send_message(self, author_id, message_object, thread_id, thread_type,
                     kwargs):
        # if str(author_id) != str(self.uid):
        isValid, result = self.parse_message(author_id, message_object,
                                             thread_id, thread_type, kwargs)
        if isValid:
            self.send(Message(text=result), thread_id=thread_id,
                      thread_type=thread_type)
        # reply to people

    def onMessage(self, author_id, message_object, thread_id, thread_type,
                  **kwargs):
        try:
            self.markAsDelivered(author_id,
                                 message_object.uid)  # mark delivered
            self.markAsRead(author_id)  # mark read

            if self.test:
                print("==METADATA==")
                print("%s said: %s" %
                      (self.fetchUserInfo(author_id), message_object.text))
                # print(mid)
                # print(author_name)
                print(kwargs)
                print("====")

            p = multiprocessing.Process(target=self.send_message,
                                        args=(author_id,
                                              message_object,
                                              thread_id,
                                              thread_type,
                                              kwargs))
            p.start()

            # reply to groups
        except Exception as e:
            print(e)


def main():

    # create bot
    bot = JerryBot(USERNAME, PASSWORD)

    # keep going
    while 1:
        try:
            bot.listen()
        # quit
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)
        else:
            # print diagnostic info
            print(sys.exc_info()[0])


if __name__ == "__main__":
    main()
