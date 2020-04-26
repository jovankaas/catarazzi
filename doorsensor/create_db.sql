sqlite3 cats.db
sqlite> .schema
CREATE TABLE pics(door_open int, date text, picture text, muis int, sent_email int, unique(picture, door_open) on conflict replace);
sqlite>
