# import json;
# reminders = {"":""};
# class Reminder:
#			#TODO: might need to convert 0:00 to 00:00
#     #I could do this all in json, but I prefer OOP 
#     @staticmethod
#     def parse(data:str):
#         global reminders;
#         data = json.loads(data);
#         for key in data.keys():
#             if (type(data[key]) == dict):
#                 data[key]['time'] = key;
#                 reminders[key] = Reminder.new(data[key]);
#     time = "0:00";
#     text = "reminder";
#     audio = None;
#     img = None;
#     def new(data:dict):
#         this = Reminder("","");
#         for (i,val) in data.items():
#             if i == 'time':
#                 this.time = val;
#             elif i == 'text':
#                 this.text = val;
#             elif i == 'audioSrc':
#                 this.audio = val;
#             elif i == 'imageSrc':
#                 this.img = val;
#         return this;
#     def __init__(this, time, text, audio=None, img = None):
#         print(2)
#         this.time = time;
#         this.text = text;
#         this.audio = audio;
#         this.img = img;
# Reminder.parse("""{"a": { "text":"b"}} """)
# for a in reminders.keys():
#     if a != "":
#         print(reminders[a].text);