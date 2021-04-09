list_films_actors = '''SELECT f.FilmName, a.ActorName FROM film f 
INNER JOIN actor a  ON
f.FilmCountryID = a.ActorCountryID
ORDER BY f.FilmName, a.ActorName ASC;'''

search_actor_gender_dob = '''SELECT ActorName, monthname(ActorDOB) as DobMonth, ActorGender FROM actor
WHERE year(ACTORDOB)=%s AND ActorGender=%s;'''

list_studios = '''SELECT StudioID, StudioName FROM studio 
order by StudioID ASC;'''

insert_country = '''INSERT INTO country
(CountryID, CountryName)
VALUES(%s, %s);'''

#list_films_by_id is different to the above queries, it will get an unknown number of values within the IN so to address this 
#will use string formatting to later insert the correct amount of %s
list_films_by_id = '''SELECT FilmID, FilmName, FilmSynopsis FROM Film
WHERE FilmID IN ({s_placeholder})'''