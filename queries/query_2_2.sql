SELECT 
	D.id
	,D.department
	,COUNT(HE.id) AS hired

FROM 
	hired_employees HE
LEFT JOIN 
	departments D
ON 
	HE.department_id = D.id	
GROUP BY 
	1,2
HAVING
	COUNT(HE.id) > (SELECT 1.0*COUNT(id)/(SELECT COUNT(id) FROM departments) AS avg_2021 FROM hired_employees WHERE EXTRACT(YEAR FROM datetime) = 2021)

ORDER BY 
	hired DESC

