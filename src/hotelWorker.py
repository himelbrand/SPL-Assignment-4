
import sqlite3
import time
dbcon = sqlite3.connect('cronhoteldb.db')  # connect to DB
dbcon.text_factory = bytes
cursor = dbcon.cursor()


def dohoteltask(taskname,parameter):
    ans = time.time()  # get time of task
    if taskname == 'wakeup':
        cursor.execute("""
          SELECT FirstName , LastName , RoomNumber FROM Residents
          WHERE RoomNumber = ?
          """,[parameter])
        print ('{} {} in room {} received a wakeup call at '.format(*cursor.fetchone())+str(ans))
    elif taskname == 'breakfast':
        cursor.execute("""
          SELECT FirstName , LastName , RoomNumber FROM Residents
          WHERE RoomNumber = ?
        """, [parameter])

        print ('{} {} in room {} has been served breakfast at '.format(*cursor.fetchone()) + str(ans))
    elif taskname == 'clean':
        cursor.execute(
                  "SELECT RoomNumber FROM Rooms "
                  "WHERE RoomNumber NOT IN (SELECT RoomNumber FROM Residents)")
        rooms_cleaned = cursor.fetchall()
        rooms_cleaned.sort(key=lambda tup: tup[0])
        print 'Rooms '+', '.join([str(room[0]) for room in rooms_cleaned])+' were cleaned at '+str(ans)
    return ans
