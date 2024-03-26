WITH PREVIEW AS (
	SELECT
		department_id
		,job_id
		,EXTRACT(QUARTER FROM datetime) AS quarter
	    ,COUNT(id) AS q_hr
		
	FROM 
		hired_employees HE
	WHERE
		EXTRACT(YEAR FROM datetime) = 2021
	GROUP BY 
		1,2,3
)
	
SELECT 
	D.department
	,J.job
	,SUM(CASE WHEN PW.quarter=1 THEN PW.q_hr ELSE 0 END) AS Q1
	,SUM(CASE WHEN PW.quarter=2 THEN PW.q_hr ELSE 0 END) AS Q2
	,SUM(CASE WHEN PW.quarter=3 THEN PW.q_hr ELSE 0 END) AS Q3
	,SUM(CASE WHEN PW.quarter=4 THEN PW.q_hr ELSE 0 END) AS Q4

FROM 
	PREVIEW PW
LEFT JOIN 
	jobs J
ON
	PW.job_id = J.id
LEFT JOIN 
	departments D
ON 
	PW.department_id = D.id
	
GROUP BY 
	D.department
	,J.job
ORDER BY
	D.department ASC
	,J.job ASC

