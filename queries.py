# ===========================================================================
# +++Database Queries File+++|
# ___________________________|
#
# Sean Frischmann 
# Scorecard -- Score Keeping App
# ===========================================================================

def getNumberOfHoles(data):
	numberOfHoles = data['database'].execute(
			"SELECT numberOfHoles FROM courseList "
			+"WHERE courseName = ?",[data['courseName']])
	numberOfHoles = [row[0] for row in numberOfHoles.fetchall()]
	numberOfHoles = numberOfHoles[0]
	return int(numberOfHoles)

def getCourseList(data):
	courses = data['database'].execute(
			"SELECT * FROM courseList")
	courseList = [dict(courseName=row[1], numberOfHoles=row[2], 
		par=row[3]) for row in courses.fetchall()]
	i = 0
	while i < len(courseList):
		par = courseList[i]['par'].split(' ')
		j = 0
		while j < len(par):
			par[j] = int(par[j])
			j += 1
		averagePar = int(sum(par)/len(par))
		courseList[i]['par'] = averagePar
		i += 1
	return courseList

def getCourseInfo(data):
	courses = data['database'].execute(
			"SELECT * FROM courseList "
			+"WHERE courseName = ?",[data['courseName']])
	courseInfo = [dict(numberOfHoles=row[2], 
		par=row[3]) for row in courses.fetchall()]
	courseInfo = courseInfo[0]
	par = courseInfo['par'].split(' ')
	courseInfo['par'] = par
	i = 0
	holes = []
	while i < int(courseInfo['numberOfHoles']):
		holes.append(i+1)
		i += 1
	courseInfo['holes'] = holes
	return courseInfo

def gameExists(data):
	ret = data['database'].execute(
			"SELECT CASE WHEN EXISTS ( "
			+"SELECT * FROM gameList) " 
			+"THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END")
	ret = [row[0] for row in ret.fetchall()]
	return bool(ret[0])

def getCourseGames(data):
	if(gameExists(data)):
		course = data['database'].execute(
				"SELECT G.Timestamp, C.par, G.score FROM gameList AS G "
				+"JOIN courseList AS C ON G.courseId=C.courseId "
				+"WHERE C.courseName = ?",[data['courseName']])
		courseInfo = [dict(Timestamp=row[0], par=row[1], 
			score=row[2]) for row in course.fetchall()]
		i = 0
		while i < len(courseInfo):
			#***Finding total par***#
			par = courseInfo[i]['par'].split(' ')
			j = 0
			while j < len(par):
				par[j] = int(par[j])
				j += 1
			finalPar = int(sum(par))
			courseInfo[i]['par'] = finalPar
			
			#***Finding total score***#
			score = courseInfo[i]['score'].split(' ')
			j = 0
			while j < len(score):
				score[j] = int(score[j])
				j += 1
			finalScore = int(sum(score))
			courseInfo[i]['score'] = finalScore
			courseInfo[i]['gameCount'] = i+1
			i += 1
	else:
		courseInfo = [dict(Timestamp='N/A', par='N/A', score='N/A', gameCount='N/A')]
	return courseInfo

def courseExists(data):
	ret = data['database'].execute(
			"SELECT CASE WHEN EXISTS ( "
			+"SELECT * FROM courseList) " 
			+"THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END")
	ret = [row[0] for row in ret.fetchall()]
	return bool(ret[0])

def courseCheck(data):
	courseExists = data['database'].execute(
			"SELECT CASE WHEN EXISTS ( "
			+"SELECT courseName FROM courseList " 
			+"WHERE courseName = ?) "
			+"THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"
			, [data['courseName']])
	courseExists = [row[0] for row in courseExists.fetchall()]
	return bool(courseExists[0])

def postCourse(data):
	message = 'Course already exists'
	if not courseCheck(data):
		try:
			data['database'].execute("INSERT INTO courseList "
					+"(courseName, numberOfHoles, par) "
					+"VALUES (?,?,?)", [data['courseName'], data['numberOfHoles'], data['par']])
			data['database'].commit()
			message = 'Course successfully added'
		except:
			message = 'There was a system error, course not added'
	return message

def removeCourse(data):
	data['database'].execute("DELETE FROM courseList "
			+"WHERE courseName = ?", [data['courseName']])
	data['database'].commit()
	return 'Course was successfully removed'

def postGame(data):
	courseId = data['database'].execute("SELECT courseId FROM courseList "
			+"WHERE courseName = ?",[data['courseName']])
	courseId = [row[0] for row in courseId.fetchall()]
	courseId = int(courseId[0])
	data['database'].execute("INSERT INTO gameList "
			+"(courseId, score, Timestamp) "
			+"VALUES (?,?,?)", [courseId, data['score'], data['date']])
	data['database'].commit()
	message = 'Game successfully added'
	return message

def removeGame(data):
	data['database'].execute("DELETE FROM gameList "
			+"WHERE gameId = ?", [data['gameId']])
	data['database'].commit()
	return 'Game was successfully removed'
