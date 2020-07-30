from datetime import datetime
import sqlite3

from .Errors import *
from .Image import Image



class Message():
    """[summary]
    """
    def __init__(self, row):
        """[summary]

        Args:
            row ([type]): [description]

        Returns:
            [type]: [description]
        """
        conn = sqlite3.connect("/Users/User/Library/Messages/chat.db")
        c = conn.cursor()
        try:
            self.FullMessage = c.execute(f"SELECT * FROM message WHERE ROWID = {row}").fetchone()
            self.Handle = c.execute("SELECT * FROM handle ORDER BY ROWID;").fetchall()[self.FullMessage[5]-1]
        except:
            return None

        #Messages Table
        self.Id = self.FullMessage[0]
        self.Text = self.FullMessage[2]
        self.TimestampUnix = self.FullMessage[15]
        self.Timestamp = datetime.fromtimestamp((self.TimestampUnix / 1000000000)+978307200).strftime('%Y-%m-%d %H:%M:%S.%f')
        self.Room = self.FullMessage[35]
        self.HasAttachment = self.FullMessage[34]

        if self.HasAttachment == 1:
            self.Attachment = Image(self.Id)
        else:
            self.Attachment = None

        #Handle Table
        self.PhoneNumber = self.Handle[1]
        self.Country = self.Handle[2]
        self.iMessage = self.Handle[3]

        conn.close()

    def getAll(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        if self.HasAttachment == 1:
            return (self.Id, self.Text, self.TimestampUnix, self.Timestamp, self.Room, self.HasAttachment, self.PhoneNumber,
                   self.Country, self.iMessage) + self.Attachment.getAll()
        else:
            return (self.Id, self.Text, self.TimestampUnix, self.Timestamp, self.Room, self.HasAttachment, self.PhoneNumber,
                   self.Country, self.iMessage) + (None,None,None,None,None,None,None)

    def storeData(self):
        """[summary]
        """
        MessageLog = sqlite3.connect("./ChatLog.db")

        sqlcommand = '''INSERT INTO MessageLog(Id,Text,TimestampUnix,Timestamp,Room, HasAttachment, PhoneNumber, Country, iMessage,
        AttachmentLocation, AttachmentName, AttachmentType, AttachmentCreatedDateUnix, AttachmentCreatedDate,
        AttachmentSize, AttachmentIsSticker)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        #print(f"Message.getAll: {Message.getAll()}")
        cursor = MessageLog.cursor()
        cursor.execute(sqlcommand, self.getAll())
        MessageLog.commit()
        cursor.close()
        return

    def getCtx(self):
        return NotImplimentedError


class MessageSent(Exception):
    pass