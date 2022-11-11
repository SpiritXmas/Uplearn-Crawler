import requests
from json import loads
from re import sub

Endpoints = {
  "validateQuestion":"https://app.uplearn.co.uk/validateQuizNew.php",
  "validateQuiz":"https://app.uplearn.co.uk/validateSectionQuiz.php"
}

OK = requests.codes.ok
SESSION = requests.Session()

AUTH_TOKEN = ""
PHP_SES_ID = "" # bruh idk, its accepting my static one and the one I grab normally doesn't work
USER_ID = ""

email = input("Enter email: ")
password = input("Enter password: ")

json_data={'operationName':'AuthenticateUserByEmail','variables':{'email':email,'password':password},'query':'mutation AuthenticateUserByEmail($email: String!, $password: String!) {\n  authenticationResult: authenticateUserByEmail(\n    email: $email\n    password: $password\n  ) {\n    token\n    user {\n      id\n      name\n      email\n      phoneNumber\n      signedUpAt\n      gender\n      roles\n      parentId\n      studentId\n      lastLoggedInIp\n      utmSource\n      utmMedium\n      utmCampaign\n      intercomHash\n      isMerckUser\n      emailVerified\n      emailBounced\n      multipleSignUps\n      accountSetupCompleted\n      introductionSource\n      postcode\n      notificationPreferences {\n        allowAllEmails\n        allowCourseNotifications\n        allowReminderEmails\n        __typename\n      }\n      schoolYear\n      subjectRequests {\n        id\n        board {\n          id\n          __typename\n        }\n        subject {\n          id\n          __typename\n        }\n        qualification {\n          id\n          __typename\n        }\n        __typename\n      }\n      school {\n        id\n        name\n        __typename\n      }\n      managedSchool {\n        id\n        name\n        __typename\n      }\n      enrolments {\n        id\n        score\n        moduleId\n        isTrial\n        xp\n        enrolmentPlan\n        renewedAt\n        createdAt\n        __typename\n      }\n      childEnrolments {\n        id\n        __typename\n      }\n      schoolEnrolments {\n        id\n        optInStatus\n        school {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      purchases {\n        id\n        isTrial\n        trialType\n        __typename\n      }\n      onboardingSession {\n        id\n        currentStep\n        studentGoal\n        questionsInStageOne\n        courseId\n        selectedCourse {\n          id\n          title\n          uniqueCode\n          __typename\n        }\n        chooseCourseStepOptions {\n          id\n          displayName\n          course {\n            id\n            title\n            uniqueCode\n            __typename\n          }\n          __typename\n        }\n        chooseSubsectionStepOptions {\n          id\n          displayName\n          subsection {\n            id\n            name\n            __typename\n          }\n          __typename\n        }\n        subsectionId\n        selectedSubsection {\n          id\n          name\n          uniqueCode\n          subsectionQuizAvailable\n          __typename\n        }\n        endedAt\n        __typename\n      }\n      experimentMemberships {\n        id\n        experiment {\n          id\n          uniqueCode\n          isActive\n          __typename\n        }\n        status\n        startedAt\n        __typename\n      }\n      experimentGroups {\n        id\n        experiment {\n          id\n          name\n          description\n          uniqueCode\n          expiryDate\n          isActive\n          __typename\n        }\n        activities(filter: {order: 1}) {\n          id\n          order\n          activity {\n            id\n            uniqueCode\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}'}

with SESSION as http:
  data = http.post('https://web.uplearn.co.uk/api/', json=json_data)
  if data.status_code == OK:
    parsed = None

    try:
      parsed = loads(data.text)
    except:
      quit("Error with parsing login data.")

    if parsed["data"]["authenticationResult"] == None:
      quit("Incorrect password or email!")

    AUTH_TOKEN = parsed["data"]["authenticationResult"]["token"]
    USER_ID = parsed["data"]["authenticationResult"]["user"]["id"]
  else:
    quit("Error with POST request to login.")

  data = http.get('https://app.uplearn.co.uk/validateSectionQuiz.php')
  if data.status_code == OK:
    PHP_SES_ID = data.headers["Set-Cookie"].split(";")[0]
  else:
    quit("Error with GET request to grab php session id.")


print("")


def Post(url, data):
  data = sub("user=?(.*?)&m", "user=" + USER_ID + "&m", data)
  request = requests.post(url, data, headers={"cookie":"PHPSESSID=1e4545b76368c6210487d66d12724fb5; auth-token=" + AUTH_TOKEN, "content-type": "application/x-www-form-urlencoded; charset=UTF-8"})
  
  if request.status_code == OK:
    return request

  return False

AnswerPaths = {
  "FoundationsI":{
    "Number":["optionsCheckboxes[0][]=option1&optionsCheckboxes[0][]=option2&optionsCheckboxes[0][]=option3&optionsCheckboxes[0][]=option4&quizType[0][]=multimultiplechoice&quizValidate[0][]=148&quizID=148&user=1&module=30&format=s&currentLesson=463&timeOnCur=0&confidenceValue=3", "optionsRadios[0][]=option1&quizType[0][]=multiplechoice&quizValidate[0][]=149&quizID=149&user=1&module=30&format=s&currentLesson=463&timeOnCur=0&confidenceValue=3", "ended=1&user=1&module=30&section=463"],

    "SymbolsAndMeaning":["optionsCheckboxes[0][]=option2&optionsCheckboxes[0][]=option4&quizType[0][]=multimultiplechoice&quizValidate[0][]=150&quizID=150&user=1&module=30&format=s&currentLesson=464&timeOnCur=0&confidenceValue=3", "optionsCheckboxes[0][]=option2&quizType[0][]=multimultiplechoice&quizValidate[0][]=151&quizID=151&user=1&module=30&format=s&currentLesson=464&timeOnCur=0&confidenceValue=3", "optionsRadios[0][]=option3&quizType[0][]=multiplechoice&quizValidate[0][]=152&optionsRadios[1][]=option1&quizType[1][]=multiplechoice&quizValidate[1][]=152&quizID=152&user=1&module=30&format=s&currentLesson=464&timeOnCur=0&confidenceValue=3", "optionsCheckboxes[0][]=option1&optionsCheckboxes[0][]=option2&optionsCheckboxes[0][]=option3&optionsCheckboxes[0][]=option4&quizType[0][]=multimultiplechoice&quizValidate[0][]=153&quizID=153&user=1&module=30&format=s&currentLesson=464&timeOnCur=0&confidenceValue=3", "optionsCheckboxes[0][]=option2&optionsCheckboxes[0][]=option4&quizType[0][]=multimultiplechoice&quizValidate[0][]=154&quizID=154&user=1&module=30&format=s&currentLesson=464&timeOnCur=0&confidenceValue=3", "optionsCheckboxes[0][]=option1&optionsCheckboxes[0][]=option2&optionsCheckboxes[0][]=option3&optionsCheckboxes[0][]=option5&optionsCheckboxes[0][]=option7&optionsCheckboxes[0][]=option8&quizType[0][]=multimultiplechoice&quizValidate[0][]=155&quizID=155&user=1&module=30&format=s&currentLesson=464&timeOnCur=0&confidenceValue=3", "optionsDropdown[0][]=%E2%89%A1&quizType[0][]=dropdown&quizValidate[0][]=156&optionsDropdown[1][]=%E2%89%A1&quizType[1][]=dropdown&quizValidate[1][]=156&optionsDropdown[2][]=%3D&quizType[2][]=dropdown&quizValidate[2][]=156&optionsDropdown[3][]=%E2%89%A1&quizType[3][]=dropdown&quizValidate[3][]=156&optionsCheckboxes[4][]=option1&optionsCheckboxes[4][]=option3&quizType[4][]=multimultiplechoice&quizValidate[4][]=156&quizID=156&user=1&module=30&format=s&currentLesson=464&timeOnCur=0&confidenceValue=3", "optionsCheckboxes[0][]=option1&quizType[0][]=multimultiplechoice&quizValidate[0][]=157&quizID=157&user=1&module=30&format=s&currentLesson=464&timeOnCur=0&confidenceValue=3", "ended=1&user=1&module=30&section=464"],

    "Arithmetic":[]
                 }
}

Parent, Child = AnswerPaths[input("Enter a category: ")], ""
if Parent:
  Child = Parent[input("Enter a quiz: ")]

  if not Child:
    quit()
else:
  quit()

Length = len(Child)-1
for index, value in enumerate(Child):
  if index != Length:
    Post(Endpoints["validateQuestion"], value)
    continue

  Post(Endpoints["validateQuiz"], value)