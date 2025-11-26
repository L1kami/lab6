import aiosqlite
import asyncio
import sys
import time


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_name)
        self.connection.row_factory = aiosqlite.Row

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def execute(self, query, params=()):
        async with self.connection.execute(query, params) as cursor:
            await self.connection.commit()
            return cursor.lastrowid

    async def fetch_all(self, query, params=()):
        async with self.connection.execute(query, params) as cursor:
            return await cursor.fetchall()


db = Database("cool_orm.db")


class Field:
    def __init__(self, field_type, primary_key=False):
        self.field_type = field_type
        self.primary_key = primary_key
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if self.field_type == "INTEGER" and not isinstance(value, int):
            raise TypeError(f"Field {self.name} expected int")
        if self.field_type == "TEXT" and not isinstance(value, str):
            raise TypeError(f"Field {self.name} expected str")
        instance.__dict__[self.name] = value


class IntField(Field):
    def __init__(self, primary_key=False):
        super().__init__("INTEGER", primary_key)


class StringField(Field):
    def __init__(self):
        super().__init__("TEXT")


class QuerySet:
    def __init__(self, model_cls):
        self.model_cls = model_cls
        self.filters = {}
        self.limit_val = None

    def filter(self, **kwargs):
        self.filters.update(kwargs)
        return self

    def limit(self, val):
        self.limit_val = val
        return self

    def _build_sql(self):
        table = self.model_cls._table_name
        sql = f"SELECT * FROM {table}"
        params = []

        if self.filters:
            conditions = [f"{key} = ?" for key in self.filters]
            sql += " WHERE " + " AND ".join(conditions)
            params.extend(self.filters.values())

        if self.limit_val:
            sql += f" LIMIT {self.limit_val}"

        return sql, tuple(params)

    def __await__(self):
        return self._execute().__await__()

    async def _execute(self):
        sql, params = self._build_sql()
        rows = await db.fetch_all(sql, params)
        results = []
        for row in rows:
            obj = self.model_cls()
            for key in row.keys():
                setattr(obj, key, row[key])
            results.append(obj)
        return results

    async def first(self):
        self.limit(1)
        res = await self
        return res[0] if res else None


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        if name == "Model":
            return super().__new__(mcs, name, bases, attrs)

        fields = {k: v for k, v in attrs.items() if isinstance(v, Field)}
        table_name = name.lower() + "s"

        attrs["_fields"] = fields
        attrs["_table_name"] = table_name

        return super().__new__(mcs, name, bases, attrs)


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    async def create_table(cls):
        fields_def = []
        for name, field in cls._fields.items():
            definition = f"{name} {field.field_type}"
            if field.primary_key:
                definition += " PRIMARY KEY AUTOINCREMENT"
            fields_def.append(definition)

        sql = f"CREATE TABLE IF NOT EXISTS {cls._table_name} ({', '.join(fields_def)})"
        await db.execute(sql)

    async def save(self):
        fields = self._fields
        data = {k: getattr(self, k) for k in fields if k != 'id' or getattr(self, k) is not None}

        if hasattr(self, 'id') and self.id is not None:
            set_clause = ", ".join([f"{k} = ?" for k in data])
            sql = f"UPDATE {self._table_name} SET {set_clause} WHERE id = ?"
            params = list(data.values()) + [self.id]
            await db.execute(sql, params)
        else:
            cols = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            sql = f"INSERT INTO {self._table_name} ({cols}) VALUES ({placeholders})"
            params = list(data.values())
            new_id = await db.execute(sql, params)
            self.id = new_id

    @classmethod
    @property
    def objects(cls):
        return QuerySet(cls)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith('_'))
        return f"<{self.__class__.__name__}: {attrs}>"


def display_log(message):
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    print(f"{BOLD}[ORM SYSTEM]{RESET} ", end="")
    for char in message:
        sys.stdout.write(f"{GREEN}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(0.02)
    print()


# --- DEMONSTRATION ---

class User(Model):
    id = IntField(primary_key=True)
    username = StringField()
    age = IntField()


async def main():
    await db.connect()

    display_log("Initializing Schema...")
    await User.create_table()

    display_log("Creating Users...")
    u1 = User(username="Neo", age=30)
    u2 = User(username="Morpheus", age=45)
    u3 = User(username="Trinity", age=30)

    await u1.save()
    await u2.save()
    await u3.save()

    display_log("Executing Lazy Queries...")

    display_log("-> Query: User.objects.filter(age=30)")
    users_30 = await User.objects.filter(age=30)
    print(f"   Result: {users_30}")

    display_log("-> Query: User.objects.filter(username='Morpheus').first()")
    morpheus = await User.objects.filter(username="Morpheus").first()
    print(f"   Result: {morpheus}")

    display_log("-> Updating Morpheus...")
    if morpheus:
        morpheus.age = 50
        await morpheus.save()
        print(f"   Updated: {morpheus}")

    await db.close()


if __name__ == "__main__":
    asyncio.run(main())