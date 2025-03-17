-- Find the titles of courses in the Comp. Sci. department that have 3 credits.

-- SELECT * from course limit 5;

SELECT title from course where course.dept_name = 'Comp. Sci.' and course.credits = 3;


-- Find the IDs of all students who were taught by an instructor named
-- Einstein; make sure there are no duplicates in the result

SELECT s_id from advisor where advisor.i_id = (SELECT id from instructor where name = 'Einstein');

SELECT * from teaches limit 5;

SELECT * from takes limit 5;

-- select all the sections taught by einstein
SELECT course_id, sec_id from teaches where teaches.id = (SELECT id from instructor where name = 'Einstein');

-- select all the students who have taken the sections taught by einstein 

-- Find the maximum enrollment, across all sections, in Autumn 2009



SELECT * from student where student.id = (
SELECT takes.id from takes 
    where (takes.course_id, takes.sec_id) = 
    (SELECT course_id, sec_id from teaches where teaches.id = (SELECT id from instructor where name = 'Einstein'))
)


SELECT * from student where student.id = (
SELECT takes.id from takes 
    where (takes.course_id, takes.sec_id) = 
    (SELECT course_id, sec_id from teaches where teaches.id = (SELECT id from instructor where name = 'Einstein'))
) 


-- Find the maximum enrollment, across all sections, in Autumn 2009 

SELECT * from teaches limit 10;
SELECT * from section limit 10;

SELECT course_id, sec_id from section where year = 2018 and lower(semester) = 'summer';



