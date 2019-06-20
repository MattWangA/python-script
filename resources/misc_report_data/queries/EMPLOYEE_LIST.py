# coding: utf-8

EMPLOYEE_LIST = '''
	#Office=LIST;;
		SELECT
			'' AS ID,
			'...' AS Label
		UNION SELECT
			Distinct Location AS ID,
			Location AS Label  
		From
			employees
	§
	select
	    e.ID as "EmployeeID",
		t.Name as "Team",
		concat(e.FirstName," ",e.Surname) as "Name",
		e.EmailAddress as "Email",
		e.Location,
		e.FirstName,
		e.Surname,
		e.PhoneNumber,
		e.Location,
		date(e.StartDate) as "StartDate",
		IF(e.Title="Research Associate",e.Position,e.Title) as 'Role',
		IF(Extension > 0,
			concat(
				case e.Location
					when 'LDN' then 2
					when 'SHG' then 3
					when 'NYC' then 4
					when 'NDL' then 5
					when 'HK' then 6
				end,
				if(e.Extension<10,'0',''),
				e.Extension),
			'-'
		) as "Extension"
	from
		employees as e
		left join teams as t on t.ID = e.TeamID
	where
		e.Status IN ("ACTIVE","PENDING")
		{?Office}AND e.Location = "{Office}"{?}
	order by
		t.Name
'''