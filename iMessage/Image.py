import sqlite3
from datetime import datetime

from .Errors import *

class Image():
    """[summary]
    """
    def __init__(self, rowid):
        """[summary]

        Args:
            rowid ([type]): [description]
        """
        conn = sqlite3.connect("/Users/User/Library/Messages/chat.db")
        c = conn.cursor()
        self.imagerow = c.execute(f"SELECT * FROM message_attachment_join WHERE message_id = {rowid}").fetchone()[1]
        self.FullImage = c.execute(f"SELECT * FROM attachment WHERE ROWID = {self.imagerow}").fetchone()

        self.Location = self.FullImage[4]
        self.Name = self.FullImage[10]
        self.Type = self.FullImage[6]
        self.CreatedDateUnix = self.FullImage[2]
        self.CreatedDate = datetime.fromtimestamp(self.CreatedDateUnix + 978307200).strftime('%Y-%m-%d %H:%M:%S')
        self.Size = self.FullImage[11]
        self.IsSticker = self.FullImage[12]

        conn.close()

    def getAll(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return (self.Location, self.Name, self.Type, self.CreatedDateUnix, self.CreatedDate, self.Size, self.IsSticker)