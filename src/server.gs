const SEND_EMAIL_WHEN_GET = false;
const FAMILY_EMAILS = String([]);
function doGet(e) {
  Logger.log("get request");
  var ret = JSON.stringify(getTodaysReminder());
    if (SEND_EMAIL_WHEN_GET) emailToFamily();
  return ContentService.createTextOutput(ret);
}
//private
function getDate() {
  const date = new Date();//month is [0..11]
  var dateString = (1+date.getMonth()) + "/"+ date.getDate();
  return dateString;
}
function splitTitle(str) {
  var divider = str.indexOf(" ");
  var time =  str.substring(0, divider);
  var reminderName = str.substring(divider+1);
  return [time, reminderName];
}
function getTodaysReminder() {
  var returnV = {};
  var rootFolder = DriveApp.getFoldersByName("ATReminders").next();
  var allRemindersFolders = rootFolder.getFolders();
  while (allRemindersFolders.hasNext()) {
    var folder = allRemindersFolders.next();
    //TODO: remove used reminders
    if (getDate() == folder.getName()) {
      var today = folder.getFolders();
      //for each reminder:
      while (today.hasNext()) {
        var thisReminder = today.next();
        var title = splitTitle(thisReminder.getName());
        var thisTime = title[0]; var thisName = title[1];
        var resources = thisReminder.getFiles();
        Logger.log(thisTime);
        Logger.log(thisName);
        var hasAudio = false; var hasImg = false;
        var reminderObj = {};
        reminderObj["text"] = thisName;
        while (resources.hasNext()) {
          var thisSrc = resources.next();
          Logger.log(thisSrc.getMimeType());
          var type = thisSrc.getMimeType().split("/")[1];
          if (!hasImg && thisSrc.getMimeType().startsWith("image") ) {
            hasImg = true;
            //jpg or png
            if (type == "png") 
              type = ".png";
            else if (type == "jpeg") 
              type = ".jpg";
            reminderObj["imageSrc"] = thisSrc.getId();
            reminderObj["imageSrcExtension"] = type;
          } else if (!hasAudio && thisSrc.getMimeType().startsWith("audio")) {
            hasAudio = true;
            //mp3 or wav
            if (type == "mpeg") 
              type = ".mp3";
            else if (type == "wav") 
              type = ".wav";
            reminderObj['audioSrc'] = thisSrc.getId();
            reminderObj["audioSrcExtension"] = type;
          }
        }
        returnV[thisTime] = reminderObj;
        Logger.log(returnV);
        return returnV;
      }
    }
  }
}
function emailToFamily() {
  //TODO: add CCs
  var folderURL = DriveApp.getFoldersByName("ATReminders").next().getUrl();
  GmailApp.sendEmail('jfgseh@gmail.com', 'Activity Reminders are up to date!', 'Here is a link to today\'s reminders:'+folderURL, {
    name: 'Activity Reminders Bot',
    noReply: true,
    cc: FAMILY_EMAILS
});
}
function emailFamily_noConnectionToUser() {
  PropertiesService.getScriptProperties().getProperty('usedToday');
  //TODO: add CCs
  var folderURL = DriveApp.getFoldersByName("ATReminders").next().getUrl();
  GmailApp.sendEmail('jfgseh@gmail.com', 'WARNING| No connection to user', 'The user does not have today\'s reminders and schedule yet. This can be due to several reasons:\
  1.The user has no Wifi \n\
  2.The device went out of batteries \n\
  Please contact the user ASAP', {
    name: 'Activity Reminders Bot',
    noReply: true,
    cc: FAMILY_EMAILS
});
}

function myFunction() {
  // Log the name of every file in the user's Drive.
  var rootFolder = DriveApp.getFoldersByName("ATReminders").next();
  var files = rootFolder.getFiles();
  rootFolder.setSharing(DriveApp.Access.ANYONE, DriveApp.Permission.VIEW);
  while (files.hasNext()) {
    var file = files.next();
    Logger.log(file.getId());
  }
}