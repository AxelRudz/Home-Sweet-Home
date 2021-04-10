from datetime import date

class User(object):

    @classmethod
    def all(cls, conn):
        sql = """
            SELECT * 
            FROM users
        """
        cursor = conn.cursor()
        cursor.execute(sql)

        return cursor.fetchall()


    @classmethod
    def find_by_id(cls, conn, id):
        sql = """
            SELECT *
            FROM users
            WHERE users.id = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, id)

        return cursor.fetchone()


    @classmethod
    def find_by_email(cls, conn, email):
        sql = """
            SELECT *
            FROM users
            WHERE users.email = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, email)

        return cursor.fetchone()
    

    @classmethod
    def create(cls, conn, params):
        sql = """
            INSERT INTO users(email, password, first_name, last_name, phone_number)
            VALUES(%s, %s, %s, %s, %s);
        """

        cursor = conn.cursor()
        cursor.execute(sql, (params['email'], params['password'], params['first_name'], params['last_name'], params['phone_number']))
        conn.commit()
        return True


    @classmethod
    def login(cls, conn, email, password):
        sql = """
            SELECT *
            FROM users u
            WHERE u.email = %s and u.password = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, (email, password))
        return cursor.fetchone()
    

    @classmethod
    def favorite_houses(cls, conn, id_user):
        sql = """
            SELECT *
            FROM has_favorites INNER JOIN houses
            WHERE has_favorites.id_house = houses.id AND has_favorites.id_user = %s AND houses.deleted_at IS NULL
        """
        cursor = conn.cursor()
        cursor.execute(sql, id_user)
        return cursor.fetchall()



    @classmethod
    def add_fav_house(cls, conn, id_user, id_house):
        sql = """
            INSERT INTO has_favorites(id_user, id_house)
            VALUES(%s, %s);
        """
        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        conn.commit()
        return True

    
    @classmethod
    def delete_fav_house(cls, conn, id_user, id_house):
        sql = """
            DELETE FROM has_favorites
            WHERE id_user = %s AND id_house = %s
        """
        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        conn.commit()
        return True


    @classmethod
    def has_favorite(cls, conn, id_user, id_house):
        sql = """
            SELECT *
            FROM has_favorites
            WHERE id_user = %s AND id_house = %s
        """
        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        return cursor.fetchone()


    @classmethod
    def phone(cls, conn, id_user):
        sql = """
            SELECT phone_number
            FROM users
            WHERE id = %s
        """
        cursor = conn.cursor()
        cursor.execute(sql, id_user)
        return cursor.fetchone()

    
    @classmethod
    def houses_on_sale(cls, conn, id_user):
        sql = """
            SELECT *
            FROM houses
            WHERE owner_id = %s AND deleted_at IS NULL
        """
        cursor = conn.cursor()
        cursor.execute(sql, id_user)
        return cursor.fetchall()


    @classmethod
    def buy_house(cls, conn, id_user, id_house):
        sql = """
            INSERT INTO buys(id_user, id_house) VALUES (%s, %s)
        """
        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        conn.commit()
        sql = """
            UPDATE houses
            SET deleted_at = %s
            WHERE id = %s
        """
        cursor.execute(sql, (date.today(), id_house))
        conn.commit()
        return True


    @classmethod
    def bought_house(cls, conn, id_house, id_user):
        sql = """
            SELECT *
            FROM buys
            WHERE id_user = %s AND id_house = %s
        """
        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        return cursor.fetchone()

    
    @classmethod
    def is_owner(cls, conn, id_user, id_house):
        sql = """
            SELECT id
            FROM houses
            WHERE owner_id = %s AND id = %s
        """
        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        return cursor.fetchone()