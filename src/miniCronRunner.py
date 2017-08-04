import os

import sqlite3

import sys

import time

from hotelWorker import dohoteltask


def main():
    databaseexisted = os.path.isfile('cronhoteldb.db')
    numberoftimes = 0
    if not databaseexisted:
        exit()

    dbcon = sqlite3.connect('cronhoteldb.db')  # connect to DB
    with dbcon:
        lasttimesdic = {}  # holds last time of tasks
        cursor = dbcon.cursor()
        cursor.execute("SELECT t.TaskId, t.TaskName,"
                       "t.Parameter , tt.NumTimes "
                       "FROM Tasks AS t "
                       "JOIN TaskTimes AS tt "
                       "ON t.TaskId = tt.TaskId")
        tasks = cursor.fetchall()
        for task in tasks:
            numberoftimes += task[3]
            if task[3] > 0:
                lasttimesdic[task[0]] = dohoteltask(task[1], task[2])

                # decrement number of times
                cursor.execute("UPDATE TaskTimes SET NumTimes = ? "
                               "WHERE TaskId = ?", (task[3] - 1,task[0]))
                numberoftimes -= 1
        dbcon.commit()  # commit changes
        while databaseexisted and numberoftimes > 0:

            cursor.execute("SELECT t.TaskId, t.TaskName,"
                           "t.Parameter , tt.NumTimes, tt.DoEvery "
                           "FROM Tasks AS t "
                           "JOIN TaskTimes AS tt "
                           "ON t.TaskId = tt.TaskId")
            tasks = cursor.fetchall()

            for task in tasks:
                if task[3] > 0:  # enter task only if still have times to run
                    if time.time() >= task[4] + lasttimesdic[task[0]]:
                        # update taskTimes table, decrement NumTimes
                        lasttimesdic[task[0]] = dohoteltask(task[1], task[2])
                        cursor.execute("UPDATE TaskTimes SET NumTimes = ? "
                                       "WHERE TaskId = ?", (task[3] - 1,task[0]))
                        numberoftimes -= 1
            dbcon.commit()


if __name__ == '__main__':
    main()
