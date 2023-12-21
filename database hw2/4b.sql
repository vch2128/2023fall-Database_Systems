with ccsindex as(
select country_code,continent_code,rdate,StringencyIndex_Average_ForDisplay as sindex
from s_index 
join country_continent on s_index.country_code=country_continent.two_letter_country_code
where rdate=20221201 or rdate=20220401 or rdate=20210401 or rdate=20200401
),
earlier as(
select country_code,rdate,confirmed_cases as cases
from oindicators 
where rdate=20221124 or rdate=20220325 or rdate=20210325 or rdate=20200325
),
now as(
select country_code,rdate,confirmed_cases as cases
from oindicators 
where rdate=20221201 or rdate=20220401 or rdate=20210401 or rdate=20200401
),
dif as(
select now.country_code,now.rdate,earlier.cases as ecases,now.cases as ncases
from earlier
join now on earlier.country_code=now.country_code
where (earlier.rdate=20221124 and now.rdate=20221201) 
	or (earlier.rdate=20220325 and now.rdate=20220401) 
	or (earlier.rdate=20210325 and now.rdate=20210401) 
	or (earlier.rdate=20200325 and now.rdate=20200401)
),
diff as (
select country_code,rdate,(cast(ncases as float(2))-cast(ecases as float(2)))/7 as casesgrowth
from dif
),
oversindex as (
select diff.country_code,continent_code,diff.rdate,case 
										when casesgrowth!=0 then sindex/casesgrowth
										when casesgrowth=0 then sindex/0.1
										end as osindex
from ccsindex
join diff 
on diff.country_code=ccsindex.country_code and diff.rdate=ccsindex.rdate
),
omax as (
select continent_code,rdate,max(osindex) as osindex
from oversindex
group by (continent_code,rdate)
),
omin as (
select continent_code,rdate,min(osindex) as osindex
from oversindex
group by (continent_code,rdate)
),
omm as(
(select omax.continent_code,country_code,omax.rdate,omax.osindex
from omax
join oversindex
on omax.continent_code=oversindex.continent_code 
	and omax.rdate=oversindex.rdate
	and omax.osindex=oversindex.osindex)
union
(select omin.continent_code,country_code,omin.rdate,omin.osindex
from omin
join oversindex
on omin.continent_code=oversindex.continent_code 
	and omin.rdate=oversindex.rdate
	and omin.osindex=oversindex.osindex)
)
select continent_name,country_name,rdate as date,osindex as over_stringency_index
from omm
join country on omm.country_code=country.two_letter_country_code
join continent on omm.continent_code=continent.continent_code
order by date,continent_name;