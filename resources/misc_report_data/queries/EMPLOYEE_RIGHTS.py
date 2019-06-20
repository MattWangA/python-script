# coding: utf-8

EMPLOYEE_RIGHTS = '''
	select
		e.ID, 
		CONCAT(e.FirstName, ' ', e.Surname) as Name,
		GROUP_CONCAT(rg.Name ORDER BY rg.Name SEPARATOR ',') as Rights,
		GROUP_CONCAT(rg.ID ORDER BY rg.Name SEPARATOR ',') as RightsIds
	from 
		employees e
		left join right_user_group rug on rug.EmployeeID=e.ID
		left join right_group rg on rg.ID=rug.GroupID
	where
		e.Status IN ('ACTIVE','PENDING')
	group by e.ID
'''
