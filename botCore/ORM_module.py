import sqlite3

class DataBase:

    cursos=None
    con=None

    def connect(self):
        self.conn = sqlite3.connect('/home/alexey/PycharmProjects/TelegramBot/db.sqlite3')
        self.cursor = self.conn.cursor()

    def getUser(self,id):
        request='SELECT id ,name,reputation ' \
            'FROM users ' \
            'WHERE id=%d' % id

        self.cursor.execute(request)
        return self.cursor.fetchall()[0]

    def setUser(self,id,name,reputation):
        request='INSERT INTO users (id , name , reputation) ' \
            'VALUES (%d , "%s" , %d)' % (id,name,reputation)
        self.cursor.execute(request)
        self.conn.commit()

    def getUserQuestions(self,id):
        request='SELECT id,question,reputation ' \
            'FROM questions ' \
            'WHERE user_id=%d' % id
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def updateUserQuestion(self,user_id,question_id,text):
        request='SELECT id ' \
                'FROM questions ' \
                'WHERE user_id=%d AND id=%d' % (user_id,question_id)
        self.cursor.execute(request)
        result=self.cursor.fetchall()

        if len(result)>0:
            request = 'UPDATE questions ' \
                    'SET question="%s" ' \
                    'WHERE user_id=%d AND id=%d' % (text,user_id,question_id)
            self.cursor.execute(request)
            self.conn.commit()
            return True
        else:
            return False

    def setQuestion(self,user_id,question):
        request='SELECT id ' \
                'FROM questions ' \
                'ORDER BY id DESC ' \
                'LIMIT 1'
        self.cursor.execute(request)
        result=self.cursor.fetchall()[0][0]

        request='INSERT INTO questions (user_id,question,reputation,id) ' \
                'VALUES (%d,"%s",%d,%d)' % (user_id,question,0,result+1)
        self.cursor.execute(request)
        self.conn.commit()
        return result+1


    def updateQuestionReputation(self,reputation,question_id,user_id):
        request = 'SELECT id ' \
                  'FROM questions ' \
                  'WHERE user_id=%d AND id=%d' % (user_id, question_id)
        self.cursor.execute(request)
        result = self.cursor.fetchall()

        if len(result) > 0:
            request = 'UPDATE questions ' \
                      'SET reputation=%d ' \
                      'WHERE id=%d' % (reputation, question_id)
            self.cursor.execute(request)
            self.conn.commit()

            request = 'UPDATE users ' \
                      'SET reputation=reputation-%d ' \
                      'WHERE id=%d' % (reputation, user_id)
            self.cursor.execute(request)
            self.conn.commit()

            return True
        else:
            return False


    def close(self):
        self.conn.close()