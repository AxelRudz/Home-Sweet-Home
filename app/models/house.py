class House(object):

    @classmethod
    def all(cls, conn):
        sql = """
            SELECT *
            FROM houses
            WHERE deleted_at IS NULL
            ORDER BY created_at;
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    
    @classmethod
    def on_sale(cls, conn):
        sql = """
            SELECT *
            FROM houses
            WHERE on_sale = 1 AND deleted_at IS NULL
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


    @classmethod
    def last(cls, conn):
        sql = """
            SELECT * 
            FROM houses
            WHERE deleted_at IS NULL
            ORDER BY created_at DESC
            LIMIT 4;
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def last_on_sale(cls, conn):
        sql = """
            SELECT * 
            FROM houses
            WHERE on_sale = 1 AND deleted_at IS NULL
            ORDER BY created_at
            LIMIT 4;
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    
    @classmethod
    def was_sold(cls, conn, id):
        sql = """
            SELECT id
            FROM houses
            WHERE id = %s AND deleted_at IS NOT NULL
        """
        cursor = conn.cursor()
        cursor.execute(sql, id)
        if cursor.fetchone():
            return True
        return False


    @classmethod
    def find_by_id(cls, conn, id):
        sql = """
            SELECT *
            FROM houses
            WHERE id = %s;
        """
        cursor = conn.cursor()
        cursor.execute(sql, id)
        return cursor.fetchone()


    @classmethod
    def verify_like(cls, conn, id_user, id_house):
        sql = """
            SELECT id_user
            FROM liked
            WHERE id_user = %s AND id_house = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        return cursor.fetchone()

    
    @classmethod
    def verify_dislike(cls, conn, id_user, id_house):
        sql = """
            SELECT id_user
            FROM disliked
            WHERE id_user = %s AND id_house = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        return cursor.fetchone()

    
    @classmethod
    def remove_like(cls, conn, id_user, id_house):
        sql = """
            DELETE FROM liked
            WHERE id_user = %s AND id_house = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        conn.commit()

        sql = """
            UPDATE houses
            SET likes = likes - 1
            WHERE id = %s
        """
        cursor.execute(sql, id_house)
        conn.commit()
        return True


    @classmethod
    def remove_dislike(cls, conn, id_user, id_house):
        sql = """
            DELETE FROM disliked
            WHERE id_user = %s AND id_house = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        conn.commit()

        sql = """
            UPDATE houses
            SET dislikes = dislikes - 1
            WHERE id = %s
        """
        cursor.execute(sql, id_house)
        conn.commit()
        return True



    @classmethod
    def add_like(cls, conn, id_user, id_house):
        sql = """
            INSERT INTO liked (id_user, id_house)
            VALUES (%s, %s);
        """

        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        conn.commit()

        sql = """
            UPDATE houses
            SET likes = likes + 1
            WHERE id = %s
        """

        cursor.execute(sql, id_house)
        conn.commit()
        return True


    @classmethod
    def add_dislike(cls, conn, id_user, id_house):
        sql = """
            INSERT INTO disliked (id_user, id_house)
            VALUES (%s, %s);
        """

        cursor = conn.cursor()
        cursor.execute(sql, (id_user, id_house))
        conn.commit()

        sql = """
            UPDATE houses
            SET dislikes = dislikes + 1
            WHERE id = %s
        """

        cursor.execute(sql, id_house)
        conn.commit()
        return True
    

    @classmethod
    def likes(cls, conn, id_house):
        sql = """
            SELECT likes
            FROM houses
            WHERE id = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, id_house)
        return cursor.fetchone()
    
    @classmethod
    def dislikes(cls, conn, id_house):
        sql = """
            SELECT dislikes
            FROM houses
            WHERE id = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, id_house)
        return cursor.fetchone()
    

    @classmethod
    def update_stars(cls, conn, id_house, stars):
        sql = """
            UPDATE houses
            SET stars = %s
            WHERE id = %s
        """
        cursor = conn.cursor()
        cursor.execute(sql, (stars, id_house))
        conn.commit()
        return True


    @classmethod
    def add_house(cls, conn, id_user, name, adress, description, has_picture, actual_price=None, old_price=None, on_sale=0):
        sql = """
            INSERT INTO houses (owner_id, name, adress, actual_price, old_price, description, on_sale, likes, dislikes, stars, has_picture, deleted_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 0, 0, 0, %s, %s);
        """

        cursor = conn.cursor()
        cursor.execute(sql, (id_user, name, adress, actual_price, old_price, description, on_sale, has_picture, None))
        conn.commit()

        return cursor.lastrowid

    
    @classmethod
    def exist(cls, conn, id_house):
        sql = """
            SELECT id
            FROM houses
            WHERE id=%s AND deleted_at IS NULL
        """

        cursor = conn.cursor()
        cursor.execute(sql, id_house)
        return cursor.fetchone()


    @classmethod
    def purchases(cls, conn, id_user):
        sql = """
            SELECT *
            FROM buys INNER JOIN houses
            WHERE buys.id_house = houses.id AND buys.id_user = %s
        """
        cursor = conn.cursor()
        cursor.execute(sql, id_user)
        return cursor.fetchall()

    
    @classmethod
    def delete(cls, conn, id_house):

        sql = """
            DELETE FROM liked
            WHERE id_house = %s
        """

        cursor = conn.cursor()
        cursor.execute(sql, id_house)
        conn.commit()
        
        sql = """
            DELETE FROM disliked
            WHERE id_house = %s
        """

        cursor.execute(sql, id_house)
        conn.commit()

        sql = """
            DELETE FROM houses
            WHERE id = %s
        """

        cursor.execute(sql, id_house)
        conn.commit()

        return True

    
    @classmethod
    def restore_houses(cls, conn):
        instructions = []
        instructions.append("""
            UPDATE houses
            SET deleted_at=NULL, likes=0, dislikes=0, stars=0
            WHERE id IN (1,2,3,4)
        """)
        instructions.append("""
            DELETE FROM houses
            WHERE id NOT IN (1,2,3,4)
        """)
        instructions.append("DELETE FROM buys")
        instructions.append("DELETE FROM liked")
        instructions.append("DELETE FROM disliked")
        instructions.append("DELETE FROM has_favorites")
        
        cursor = conn.cursor()
        for inst in instructions:
            cursor.execute(inst)
        conn.commit()
        return True