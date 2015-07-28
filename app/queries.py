# ===========================================================================
# +++Database Queries File+++|
# ___________________________|
#
# Sean Frischmann 
# Scorecard -- Score Keeping App
# ===========================================================================

def getCourseList(data):
	courses = data['database'].execute(
			"SELECT * FROM courseList")
	courseList = [dict(courseName=row[0], numberOfHoles=row[1], 
		par=row[2]) for row in courses.fetchall()]
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
	course = data['database'].execute(
			"SELECT * FROM courseList WHERE "
			+"courseName = ?",[data['courseName']])
	courseInfo = [dict(courseName=row[0], numberOfHoles=row[1], 
		par=row[2]) for row in course.fetchall()]
	par = courseInfo[0]['par'].split(' ')
	parDict = dict()
	j = 0
	while j < len(par):
		par[j] = int(par[j])
		parDict[j+1] = par[j]
		j += 1
	courseInfo[0]['par'] = parDict
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
