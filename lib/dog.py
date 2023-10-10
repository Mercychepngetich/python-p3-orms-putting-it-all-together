import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    all_dogs = []

    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS dogs(
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed Text
        )
        """
        CURSOR.execute(sql)


    @classmethod
    def drop_table(cls):
        sql = """
        DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)

    def save(self):
        sql = """INSERT INTO dogs(name, breed)
        VALUES(?, ?)
        """

        CURSOR. execute(sql, (self.name, self.breed))
        CONN.commit()

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = """SELECT * FROM dogs
        """
        all = CURSOR.execute(sql).fetchall()
        cls.all_dogs = [cls.new_from_db(row) for row in all]
        return cls.all_dogs

    @classmethod
    def find_by_name(cls, name):
        sql = """
        SELECT * FROM dogs
        WHERE name = ?
        LIMIT 1
        """
        
        dog = CURSOR.execute(sql,(name,)).fetchone()
        return cls.new_from_db(dog)

    @classmethod
    def find_by_id(cls, dog_id):
        sql = """
        SELECT * FROM dogs
        WHERE id = ?
        LIMIT 1
        """
        dog = CURSOR.execute(sql,(dog_id,)).fetchone()
        return cls.new_from_db(dog)

    @classmethod 
    def find_or_create_by(cls, name, breed):
        sql = """SELECT * FROM dogs
        WHERE name = ? AND breed = ?
        """
        existing_dogs = CURSOR.execute(sql, (name, breed,)).fetchall()

        if len(existing_dogs) > 0:
            return cls.new_from_db(existing_dogs[0])
        else:
            new_dog = cls.create(name, breed)
            return new_dog


    def update(self):
        if self.id is not None:
            old_name = self.name  # Save the old name
            sql = """UPDATE dogs
            SET name = ?
            WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.id))
            CONN.commit()
            # Update the instance's name
            for idx, dog in enumerate(self.all_dogs):
                if dog.id == self.id:
                    self.all_dogs[idx].name = self.name

            return old_name, self.name