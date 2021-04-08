USE moviesdb;

SELECT * FROM actor
WHERE year(ActorDOB)= 1962 AND ActorGender="Male";
SELECT ActorName, monthname(ActorDOB) as DobMonth, ActorGender FROM actor
WHERE year(ACTORDOB)=1962 AND ActorGender="Male";

SELECT MAX(length(ActorGender)) from Actor;

SHOW tables;

SELECT * FROM film;

SELECT * FROM film f 
INNER JOIN director d ON
f.FilmCountryID = d.DirectorCountryID
INNER JOIN actor a ON 
d.DirectorCountryID = a.ActorCountryID;

SELECT * FROM country c
INNER JOIN director d ON
c.CountryID = d.DirectorCountryID
INNER JOIN actor a ON 
d.DirectorCountryID = a.ActorCountryID;


SELECT distinct(f.FilmName), c.CountryName FROM film f
INNER JOIN director d ON 
f.FilmDirectorID = d.DirectorID
INNER JOIN filmcast fc ON 
f.FilmID = fc.CastFilmID
INNER JOIN actor a ON
fc.CastActorID = a.ActorID
INNER JOIN country c ON
a.ActorCountryID = c.CountryID
WHERE a.ActorCountryID = d.DirectorCountryID
AND c.CountryName != "United States"
order by c.CountryName ASC;

#Question A
SELECT distinct(f.FilmName), 
	c.CountryName 
	FROM film f
	INNER JOIN director d ON 
		f.FilmDirectorID = d.DirectorID
	INNER JOIN filmcast fc ON 
		f.FilmID = fc.CastFilmID
	INNER JOIN actor a ON
		fc.CastActorID = a.ActorID
	INNER JOIN country c ON
		a.ActorCountryID = c.CountryID
	WHERE a.ActorCountryID = d.DirectorCountryID
	AND c.CountryName != "United States"
	order by c.CountryName ASC;
    
#Question C
SELECT FilmName FROM film 
WHERE FilmID IN(
	SELECT DISTINCT CastFilmID FROM filmcast 
    WHERE CastActorID IN(
		SELECT a.ActorID FROM actor a
		INNER JOIN country c ON
		a.ActorCountryID = c.CountryID
		WHERE c.CountryName = 'United Kingdom'
	)
)
order by FilmName ASC;

SELECT * FROM actor;

SELECT COUNT(FilmName) FROM film
group by FilmName;

SELECT filmname from film;

#Question E
SELECT 
a.ActorName,
COUNT(a.ActorID) as Roles 
FROM actor a
INNER JOIN filmcast fc ON
	a.ActorID = fc.CastActorID
INNER JOIN film f ON 
	fc.CastFilmID = f.FilmID
GROUP BY (a.ActorName)
ORDER BY Roles, ActorName ASC;

#Question G
SELECT g.GenreName, Count(g.GenreName) as Count FROM film f
INNER JOIN genre g 
	ON f.FilmGenreID = g.GenreId
GROUP BY GenreName
ORDER BY g.GenreName ASC;

SELECT StudioID, StudioName FROM studio 
order by StudioID ASC;

SELECT MAX(Length(char(StudioID))) FROM studio;

SELECT MAX(Length(char(StudioID))) FROM studio;

SELECT MAX(char_length(StudioID)) FROM studio;



SELECT f.FilmName, a.ActorName FROM film f 
INNER JOIN actor a  ON
f.FilmCountryID = a.ActorCountryID
ORDER BY f.FilmName ASC;