import os
import data

def get_reviews(cursor, section):
  statement = "SELECT * FROM review WHERE section = %d" % (section)
  cursor.execute(statement)
  
  count = 0
  all_reviews = cursor.fetchall()
  for i in all_reviews:
    print(str(count) + "  " + str(i["reviewID"]))
    count += 1

  selected = int(input("\n\nSelect a review using the numbers of the left: "))
  reviewID = (all_reviews[selected])["reviewID"]

  statement2 = "SELECT * FROM review WHERE reviewID = %d" % (reviewID)
  cursor.execute(statement2)

  this_review = cursor.fetchall()

  grade_received  = (this_review[0])["gradeReceived"]
  time_spent = (this_review[0])["timeSpentOnClass"]
  difficulty = (this_review[0])["courseDifficulty"]
  course_quality = (this_review[0])["courseQuality"]
  professor_quality = (this_review[0])["professorQuality"]
  comments = (this_review[0])["comments"]

  os.system('cls' if os.name == 'nt' else 'clear')
  print("Grade Received:\n" + str(grade_received) + "\n")
  print("Weekly hours spent on class: \n" + str(time_spent) + "\n")
  print("Course difficulty (0 = Very easy...10 = Very Difficult)")
  data.make_data_bar("", difficulty)
  print("\nCourse quality (0 = Poor...10 = Excellent)")
  data.make_data_bar("", course_quality)
  print("\nProfessor quality (0 = Poor...10 = Excellent)")
  data.make_data_bar("", professor_quality)
  print("\nComments:\n" + comments)

  input("\nContinue?")



def by_course_code(cursor):
  print("Enter the code or partial code of the course you wish to view...\n")
  code = input(">> ")


def by_professor(cursor):
  print("Enter the name, or partial name, of the instructor of your class...")
  print("Names should this format: First Last")
  print("You may also simply enter the first or last name of the professor and choose from the results.\n")
  prof = input(">> ")
  print("\n")
  cursor.callproc("filter_by_professor", (prof,))

  all_prof = cursor.fetchall()
  count = 0
  for i in all_prof:
    print(str(count) + "  " + i["name"] + "  -  " + i["email"])
    count += 1

  choice = int(input("\nSelect a professor (by entering the number next to their name): "))
  choice_name = (all_prof[choice])["name"]
  choice_email = (all_prof[choice])["email"]

  os.system('cls' if os.name == 'nt' else 'clear')
  print("Home > By Professor > " + choice_name + "\n\n")

  cursor.callproc("section_by_professor", (choice_email,))
  all_sections = cursor.fetchall()

  count = 0
  for i in all_sections:
    cursor.execute("SELECT courseName FROM course WHERE subjectCode = '%s' AND courseCode = %d" % (i["subjectCode"], i["courseCode"]))
    title = (cursor.fetchall()[0])["courseName"]
    print(str(count) + "  " + i["subjectCode"] + str(i["courseCode"]) + " - " + title + " - " + str(i["semester"]) + " " + str(i["year"]))
    count += 1
  
  selected_course = int(input("\n\nEnter the number of the course you would like to view: "))

  section_id = (all_sections[selected_course])["sectionID"]

  os.system('cls' if os.name == 'nt' else 'clear')

  print("Home > By Professor > " + choice_name + " > " + (all_sections[selected_course])["subjectCode"] + str((all_sections[selected_course])["courseCode"]))
  
  get_reviews(cursor, section_id)

 

