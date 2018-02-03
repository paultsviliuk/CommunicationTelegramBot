import sqlite3
import MySQLdb


class DataBase:

    user='admin'
    host='localhost'
    passw='1qaz2wsx3edc4rfv'
    charset = 'cp1251'
    db='bot'
    cursos=None
    con=None

    def connect(self):
        #self.conn = sqlite3.connect('/home/alexey/PycharmProjects/TelegramBot/db.sqlite3')
        self.conn = MySQLdb.connect(host=self.host,user=self.user,password=self.passw,db=self.db,charset=self.charset)
        self.cursor = self.conn.cursor()

    def getUser(self,id):
        request='SELECT id ,name,reputation ' \
            'FROM users ' \
            'WHERE id=%d' % id

        self.cursor.execute(request)
        user=self.cursor.fetchall()
        if len(user)!=0:
            return user[0]
        else:
            return None

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

    def getAllQuestions(self, id):
        request='SELECT id,question,reputation ' \
                'FROM questions ' \
                'WHERE id != %d ' % id
        self.cursor.execute(request)
        return self.cursor.fetchall()

    def getQuestionsByWord(self,id, question):
        request='SELECT id,question,reputation ' \
                'FROM questions ' \
                'WHERE question LIKE ? AND id!=? '
        data = ('%{}%'.format(question), str(id))
        self.cursor.execute(request, data)
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

    def setRespondent(self,user_id, question_id):
            request='SELECT id ' \
                    'FROM respondents ' \
                    'ORDER BY id DESC ' \
                    'LIMIT 1'
            self.cursor.execute(request)
            result = self.cursor.fetchall()
            if len(result) > 0:
                result = result[0][0]
            else:
                result = 0

            request='INSERT INTO respondents (user_id, question_id, id) ' \
                    'VALUES (%d, %d, %d)' % (user_id, question_id, result+1)
            self.cursor.execute(request)
            self.conn.commit()
            return result + 1

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

    def getRespondetnsList(self,user_id):
        request='SELECT questions.question, users.name,questions.reputation, respondents.id ' \
                'FROM respondents LEFT JOIN users ON respondents.user_id=users.id ' \
                'LEFT JOIN questions ON questions.id=respondents.question_id ' \
                'WHERE questions.user_id=%d' %(user_id)
        self.cursor.execute(request)
        result=self.cursor.fetchall()
        return result


    def close(self):
        self.conn.close()


