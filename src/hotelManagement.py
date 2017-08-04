import os

import sqlite3

import sys


def main(args):

    databaseexisted = os.path.isfile('cronhoteldb.db')
    configfile = args[1]
    # check if configuration file exists
    if not os.path.isfile(configfile):
        exit()
    else:
        if not databaseexisted:  # First time creating the database. Create the tables
            dbcon = sqlite3.connect('cronhoteldb.db')
            with dbcon:
                cursor = dbcon.cursor()
            cursor.execute("CREATE TABLE TaskTimes(TaskId INTEGER PRIMARY KEY NOT NULL,"
                           "DoEvery INTEGER NOT NULL,"
                           "NumTimes INTEGER NOT NULL)")
            cursor.execute("CREATE TABLE Tasks(TaskId INTEGER NOT NULL REFERENCES TaskTimes,"
                           "TaskName TEXT NOT NULL,"
                           "Parameter INTEGER)")
            cursor.execute("CREATE TABLE Rooms(RoomNumber INTEGER PRIMARY KEY NOT NULL)")
            cursor.execute("CREATE TABLE Residents(RoomNumber INTEGER NOT NULL REFERENCES Rooms(RoomNumber),"
                           "FirstName TEXT NOT NULL,"
                           "LastName TEXT NOT NULL)")

            with open(configfile) as inputfile:
                taskid = 0
                for line in inputfile:
                    line = line.strip("\n")
                    linesplit = line.split(',')
                    if linesplit[0] == 'room':  # insert new row intro rooms table
                        cursor.execute("INSERT INTO Rooms VALUES(?)", (linesplit[1],))
                        if len(linesplit) > 2:  # insert new row into residents table
                            cursor.execute("INSERT INTO Residents VALUES(?,?,?)", (linesplit[1], linesplit[2], linesplit[3]))
                    else:  # insert new row intro Tasks table
                        if len(linesplit) == 4:
                            parameter = int(linesplit[2])
                            lastindex = 3
                        else:
                            parameter = 0
                            lastindex = 2
                        cursor.execute("INSERT INTO Tasks (TaskId,TaskName,Parameter) VALUES(?,?,?)", (taskid, linesplit[0], parameter))
                        cursor.execute("INSERT INTO TaskTimes (TaskId,DoEvery,NumTimes) VALUES(?,?,?)", (taskid, linesplit[1], linesplit[lastindex]))
                        taskid += taskid + 1
                dbcon.commit()


if __name__ == '__main__':
    main(sys.argv)
