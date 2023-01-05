import string
from sortedcontainers import SortedList
from sortedcollections import ValueSortedDict

ALL_INTERESTS = ["sport", "cinema", "art", "health", "technology", "DIY", "cooking", "travel"]

allUsersById = {}
currentLastId = 0 # Will be incremented as new user ids are taken

#Initialize the allUsersDict dictionary, with keys from A to Z, and filled with empty SortedLists, all set-up to sort by the 'fullName' key. 
allUsersDict = {}
for letter in string.ascii_uppercase:
  allUsersDict[letter] = SortedList(key=lambda u: u['fullName'])

# Check if a string contains any numbers. Used to avoid throwing exceptions when using int(string)
def hasNumbers(inputString):
  return any(char.isdigit() for char in inputString)

def idToIdAndName(id):
  name = allUsersById[id]["fullName"]
  return f"{id}.{name}"

def userListToIdAndNameList(userList):
  return [idToIdAndName(user["id"]) for user in userList]

def idListToUserList(idList):
  return [allUsersById[id] for id in idList] 


def idListToIdAndNameList(idList):
  return [idToIdAndName(id) for id in idList]

def printUser(user):
  print("----USER INFORMATION----")
  print(f"ID          : {user['id']}")
  print(f"Name        : {user['fullName']}")
  print(f"Age         : {user['age']}")
  print(f"Study Year  : {user['studyYear']}")
  print(f"Study Field : {user['studyField']}")
  print(f"Residence   : {user['residence']}")
  print(f"Interests   : {' '.join([ALL_INTERESTS[i] for i in user['interests']])}")
  print(f"Followers   : {' '.join(idListToIdAndNameList(user['followers']))}")
  print(f"Following   : {' '.join(idListToIdAndNameList(user['following']))}")

def printAllUsersByName():
  print("----ALL USERS ORDERED BY NAME----")
  for letter, userList in allUsersDict.items():
    idsAndNames = ', '.join(userListToIdAndNameList(userList))

    print(f"{letter}) {idsAndNames}")

def printAllUsersById():
  print("----ALL USERS ORDERED BY ID----")
  for userString in userListToIdAndNameList(allUsersById.values()):
    print(userString)

def printUserFollowers(id):
  user = allUsersById[id]
  followers = user["followers"]
  print(f"{user['fullName']} is followed by {len(followers)} user{'s' if len(followers) != 1 else ''}:")

  for idName in idListToIdAndNameList(followers):
    print(f"  {idName}")
  
def test():
  pass

def generateNewId():
  global currentLastId
  currentLastId += 1
  return currentLastId-1

def addUserToIdCorrespondance(user, id):
  global allUsersById
  allUsersById[id] = user

def addUserToAllUsers(user):
  firstLetter = user['fullName'][0]
  allUsersDict[firstLetter].add(user)


def addNewUser(fullName = "Test User", age = 18, studyYear = 2021, studyField = "Testing", residence = "My Computer", interests = set([1, 3, 6])):

  id = generateNewId()
  user = {
    "id"        : id,
    "fullName"  : fullName,
    "age"       : age,
    "studyYear" : studyYear,
    "studyField": studyField,
    "residence" : residence,
    "interests" : interests,
    "following" : set(),
    "followers" : set()
  }

  addUserToAllUsers(user)
  addUserToIdCorrespondance(user, id)

def removeUserFromAllUsersDict(user):
  firstLetter = user['fullName'][0]
  allUsersDict[firstLetter].remove(user)

def removeUserFromFollowersAndFollowing(removeId):
  removedUser = allUsersById[removeId]
  # We need to copy the set of followers / following, because removeFollow will modify that set. 
  for followingId in removedUser["following"].copy():
    removeFollow(removeId, followingId)

  for followerId in removedUser["followers"].copy():
    removeFollow(followerId, removeId)

def removeUser(id):
  removeUserFromAllUsersDict(allUsersById[id])
  removeUserFromFollowersAndFollowing(id)
  allUsersById.pop(id)

def inputNewUser():
  print("----CREATE A NEW USER PROFILE----")
  fullName   =     input("Full Name   : ").title()
  age        = int(input("Age         : "))
  studyYear  = int(input("Study Year  : "))
  studyField =     input("Study Field : ")
  residence  =     input("Residence   : ")

  print("  Possible interests: ")
  for i, interest in enumerate(ALL_INTERESTS):
    print(f"    {i+1}. {interest} ")

  interestsString = input("List of interests(by index): ")

  interestsSet = set()
  for i in interestsString.split(" "):
    if(hasNumbers(i)):
      # The interests are stored in an array with the index starting from 0, whereas the user inputs them with an index starting a 1.
      interestsSet.add(int(i)-1)
  
  return addNewUser(fullName, age, studyYear, studyField, residence, interestsSet)

# If the newValue is an empty string, return the old value, else return the new value
def sameIfEmptyString(oldValue, newValue):
  if newValue == "": return oldValue
  return newValue

def inputUpdateUser(userId):
  user = allUsersById[userId]

  oldFullName     = user["fullName"]
  oldAge          = user["age"]
  oldStudyYear    = user["studyYear"]
  oldStudyField   = user["studyField"]
  oldResidence    = user["residence"]
  oldInterestsSet = user["interests"]

  print("----UPDATE USER PROFILE----")
  newFullName        = input(f"Full Name ({oldFullName}): ").title()
  newAgeString       = input(f"Age ({oldAge}): ")
  newStudyYear       = input(f"Study Year ({oldStudyYear}): ")
  newStudyField      = input(f"Study Field ({oldStudyField}): ")
  newResidence       = input(f"Residence ({oldResidence}): ")

  print("  Possible interests: ")
  for i, interest in enumerate(ALL_INTERESTS):
    print(f"    {i+1}. {interest} ")

  interestsString = input(f"Interests ({' '.join([str(i+1) for i in oldInterestsSet])}): ")

  newInterestsSet = set()
  for i in interestsString.split(" "):
    if(hasNumbers(i)):
      # The interests are stored in an array with the index starting from 0, whereas the user inputs them with an index starting a 1.
      newInterestsSet.add(int(i)-1)

  if newFullName != "":
    # If the first letter of user's name changes, we need to update it in the allUsersDict. We first remove the user from the dictionary before changing the name, then later we will re-add it with the new name.
    
    if newFullName[0] != oldFullName[0]:
      isFirstLetterDifferent = True
      removeUserFromAllUsersDict(user)
    else:
      isFirstLetterDifferent = False

  user["fullName"]   =     sameIfEmptyString(oldFullName, newFullName)
  user["age"]        = int(sameIfEmptyString(str(oldAge), newAgeString))
  user["studyYear"]  = int(sameIfEmptyString(str(oldStudyYear), newStudyYear))
  user["studyField"] =     sameIfEmptyString(oldStudyField, newStudyField)
  user["residence"]  =     sameIfEmptyString(oldResidence, newResidence)
  
  if len(newInterestsSet) != 0:
    user["interests"] = newInterestsSet

  if isFirstLetterDifferent:
    addUserToAllUsers(user)

# Returns False if the user if there is already a follow/followed relationship, True if not.
def addFollow(followerId, followingId):
  follower = allUsersById[followerId]
  following = allUsersById[followingId]

  if followingId in follower['following']:
    return False

  follower['following'].add(followingId)
  following['followers'].add(followerId)
  return True

def removeFollow(followerId, followingId):
  follower = allUsersById[followerId]
  following = allUsersById[followingId]

  if followingId not in follower['following']:
    return False

  follower['following'].remove(followingId)
  following['followers'].remove(followerId)

def searchUsers(name = None, studyYear = None, studyField = None, interests = None):
  matches = []
  for id, user in allUsersById.items():
    if name != None and name.lower() not in user["fullName"].lower():
      continue
    if studyYear != None and studyYear != user["studyYear"]:
      continue
    if studyField != None and studyField != user["studyField"]:
      continue
    if interests != None and not set(interests).issubset(user["interests"]):
      continue
    
    matches.append(id)

  return matches

# This function should be symetrical
def getRecommendationScore(userId1, userId2):
  user1 = allUsersById[userId1]
  user2 = allUsersById[userId2]


  follows_score = 1 + len(user1["following"].intersection(user2["following"]))

  interests_score = 1+ len(user1["interests"].intersection(user2["interests"]))

  return interests_score * follows_score

  

def getRecommendations(userId, n=5):
  # recommendations = ValueSortedDict(lambda score: -score)
  recommendations = ValueSortedDict()
  
  for id in allUsersById.keys():
    if id == userId: continue # Don't want to add self
    recommendations[id] = getRecommendationScore(userId, id)
    if len(recommendations) > n:
      recommendations.popitem[0] # Remove the first one
  
  return list(recommendations.keys())[::-1]

def main():
  addNewUser()
  addNewUser(fullName = "Alex")
  addNewUser(fullName = "Dylan", interests = [2, 5, 3])
  addNewUser(fullName = "Bob", interests = [])
  addNewUser(fullName = "Bobby", interests = [])
  addNewUser(fullName = "Rick Asley", interests = [])
  # printAllUsersByName()
  # printAllUsersById()
  
  addFollow(0, 2)
  addFollow(1, 2)

  # for id in searchUsers():
  #   printUser(allUsersById[id])
  #   print()

  print(getRecommendations(0))


if __name__ == "__main__":
  # execute only if run as a script
  main()

