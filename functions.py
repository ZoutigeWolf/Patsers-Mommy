from replit import db

defaultColor = 0xDC696B
embedAuthor = {
  "name": "Sumi",
  "icon_url": "https://cdn.discordapp.com/attachments/814146826214965271/834453090207137872/de7cg0p-e2dcc2c3-b548-4c51-808e-b44efc8ca690_2.png"
}

async def updateListDB(key, value):
  key = str(key)
  if key in db.keys():
    values = db[key]
    values.append(value)
    db[key] = values
    print(f"Updated database as list | key: {key} | value: {value}")

  else:
    db[key] = value
    print(f"Created database as list | key: {key} | value: {value}")

async def updateDictDB(key, name, value):
  key = str(key)
  if key in db.keys():
    values = db[key]
    values[name] = value
    db[key] = values
    print(f"Updated database as dict | key: {key} | name: {name} | value: {value}")

  else:
    db[key] = {name: value}
    print(f"Created database as dict | key: {key} | name: {name} | value: {value}")