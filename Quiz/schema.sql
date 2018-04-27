drop table if exists student;
create table student (
  id integer primary key autoincrement,
  first text not null,
  last text not null
);

drop table if exists quiz;
create table quiz (
  id integer primary key autoincrement,
  subject text not null,
  questionNum integer not null,
  quizDate date not null
);

drop table if exists student_quiz;
create table student_quiz(
  student_id integer not null,
  quiz_id integer not null,
  score integer not null
);


INSERT INTO student VALUES(1, 'John', 'Smith');
INSERT INTO quiz VALUES(1, 'Python Basics', 5, 'Feb. 5, 2015');
INSERT INTO student_quiz VALUES(1, 1, 85 );