# Senior Design Project: Vigil

The system, named Vigil, is comprised of a jetson nano device that identifies student faces
and a Firebase database that stores attendance data.

#### [attend_device.py](https://github.com/tday01/CS179-Project/blob/master/attend_device.py)

Implementation for device to identify student faces and transmit name & timestamp to database.

#### [ML_absentee_risk.ipynb](https://github.com/tday01/CS179-Project/blob/master/ML_absentee_risk.ipynb)

Program demonstrates theoretical test case of how machine learning can be used to assess and identify students
for chronic absenteeism risk.

#### [website_database](https://github.com/tday01/CS179-Project/tree/master/website_database)

Folder contains implementation for database access, website host, user authentication, and account registration. This portion of the project was completed by teammates Jonathan and Chris.

## Abstract

Vigil is an automated attendance system that uses face recognition technology to identify and log students preregistered with the system. Automating the attendance process increases classroom productivity, but most importantly, allows for robust and consistent records of student attendance. [According to the United States Department of Education (USDE)](https://www2.ed.gov/datastory/chronicabsenteeism.html), chronic absenteeism affects more than 7 million students each year that miss a month or more of school. The USDE has declared chronic absenteeism a hidden educational crisis. Vigil not only automates the process of classroom attendance, but also detects patterns in student absences & late arrivals that are associated with chronic absenteeism. The goal of Vigil is early identification of students developing a pattern implicative of future chronic absenteeism. With this data, the school’s administration may take corrective action before the student/parent behavior becomes habitual and more difficult to correct.
	
The device is comprised of a Jetson Nano and Raspberry Pi camera which facilitate face recognition along with OpenCV & dlib libraries as well as a a hosted internet database accessible with any web interface. Face images are encoded and encrypted before transmission to the device from our Firebase database during initial device set up. When a student’s face is detected by the device, their name and timestamp are transmitted in real-time to the database. An instructor or administrator can use any web interface to login and view live attendance gathering. In case of needed corrections, the instructor manually marks their students as present or absent from any web interface.

Machine learning techniques are used on attendance and timestamp data to infer which students are at risk for periods of chronic absenteeism based on past data of known chronic absentees. This information is stored in the database and viewable through a school admin account. Students may opt out of the system with parent waiver, in which case, the system will not be able to identify the student or generate corresponding logs within the database. The system is intended for grades high school and below; where chronic absenteeism is shown to be the most detrimental to positive academic and life outcomes.

