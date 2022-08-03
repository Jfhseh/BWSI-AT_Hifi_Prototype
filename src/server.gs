/**
 * send a email to the user's family members
 * **when** the user starts using the device.
*/
const SEND_EMAIL_WHEN_GET = false;
/**
 * Note: the family emails are hidden
 */
const FAMILY_EMAILS = String(["jfgseh@gmail.com"]);
/**
 * lastGetRequest:string
 * lastStartCharge:string
 */
const environment_vars = PropertiesService.getScriptProperties();
/**email settings for sending email */
const Email_config = {
    name: 'Activity Reminders Bot',
    noReply: true,
    cc: FAMILY_EMAILS
};
/**
 * This function will run **when** the server receives a get request
 * @returns {JSON} a json file that stores the schedule and file ids for the reminders
 */
function doGet(e) {
  Logger.log("get request");
  let type = e.parameter["type"];
  Logger.log(type);
  if (type == undefined || type == "getSchedule") {
    environment_vars.setProperty("lastGetSchedule", getDate);
    var ret = JSON.stringify(getTodaysReminder());
    if (SEND_EMAIL_WHEN_GET) emailToFamily();
    return ContentService.createTextOutput(ret);
  } 
}
/**Send email to user's family memebers
 * there are 4 kind of emails:
 * -  low battery email
 * - completeTask email
 * - missed Task email
 * - start charging email(TODO)
 */
function doPost(e) {
  Logger.log("post request");  
  let args = e.parameter;
  let type = args["type"];
  Logger.log(type);
  //must return for each if
  if (type == "lowBattery") {
    email( 'WARNING| Low Battery reminder', 'The activity reminder device currently has'+args["battery"]+'% battery');
    return ContentService.createTextOutput("battery email sent");
  } else if (type == "completeTask") {
    let taskName = args["taskName"];
    let scheduleTime = args["scheduleTime"];
    let atTime = new Date().toLocaleTimeString();
    email("✅The user have completed a task!", "the user have completed the task:  " +taskName
    +"\n scheduled at: " +scheduleTime +"completed at time: "+ atTime+"!");
    return ContentService.createTextOutput("completeTask email sent");
  } else if (type == "startCharging") {
    environment_vars.setProperty("lastStartCharge", getDate());
    email("The user just start charging the device!", "");
    return ContentService.createTextOutput("startCharging email sent");
  } else if (type == "missTask") {
    let taskName = args["taskName"];
    let scheduleTime = args["scheduleTime"];
    let atTime = new Date().toLocaleTimeString();
    email("❌The user missed a task!", "the user have missed the task:  " +taskName
    +"\n scheduled at: " +scheduleTime +"!");
    return ContentService.createTextOutput("missTask email sent");
  }
  return ContentService.createTextOutput(JSON.stringify(e));
}
/**
 * get the current date stored in the format MM/DD 
 * @returns the current date stored in the format MM/DD,
 * where MM is in the range of [1,12] instead of [0,11]
*/
function getDate() {
  const date = new Date();//month is [0..11]
  var dateString = (1+date.getMonth()) + "/"+ date.getDate();
  return dateString;
}
/**
 * Splits the name of a reminder
 * @param {string} str a folder's name
 * @returns {string[]} that provides the time and the name of the reminder
 */
function splitTitle(str) {
  var divider = str.indexOf(" ");
  var time =  str.substring(0, divider);
  var reminderName = str.substring(divider+1);
  return [time, reminderName];
}
/**
 * gets today's schedule and reminders from google drive
 * @returns {JSON} a json file that stores the schedule and file ids for the reminders
*/
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
/** 
 * send a email to the user's family
 *  @note this feature can be turned on using the constant **SEND_EMAIL_WHEN_GET**
*/
function emailToFamily() {
  var folderURL = DriveApp.getFoldersByName("ATReminders").next().getUrl();
  GmailApp.sendEmail('jfgseh@gmail.com', 'Activity Reminders are up to date!', 'Here is a link to today\'s reminders:'+folderURL, Email_config);
}
/** */
function email(title, msg) {
  GmailApp.sendEmail('jfgseh@gmail.com', title, msg,  Email_config);
}
//TODO: time trigger
/**
 * Contact the user's family when the user has not use the device before a certain time
 * @note this function can be automatically called by Appscript trigger
*/
function handle_emailFamily_noConnectionToUser() {
  if (environment_vars.getProperty("lastGetRquest") == getDate()) {
    return;//is connected
  }
  PropertiesService.getScriptProperties().getProperty('usedToday');
  //TODO: add CCs
  var folderURL = DriveApp.getFoldersByName("ATReminders").next().getUrl();
  GmailApp.sendEmail('jfgseh@gmail.com', 'WARNING| No connection to user', 'The user does not have today\'s reminders and schedule yet. This can be due to several reasons:\
  1.The user has no Wifi \n\
  2.The device went out of batteries \n\
  Please contact the user ASAP',  Email_config );
}
//TODO: time trigger
function handle_forgetChargingBattery() {
  if (environment_vars.getProperty("lastStartCharge") == getDate()) return; //is charging
  email("The user forgot to charge the device!", "");
}
/**
 * @deprecated for testing only
 */
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
