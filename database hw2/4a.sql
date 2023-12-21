with cc as(
select country_code,continent_code,rdate,StringencyIndex_Average_ForDisplay as sindex
from s_index 
join country_continent on s_index.country_code=country_continent.two_letter_country_code
where rdate=20221201 or rdate=20220401 or rdate=20210401 or rdate=20200401
),
gmax as(
select continent_code,rdate,max(sindex) as sindex
from cc
group by (continent_code,rdate)
),
gmin as(
select continent_code,rdate,min(sindex) as sindex
from cc
group by (continent_code,rdate)
),
gmaxc as(
select cc.country_code,cc.continent_code,cc.rdate,cc.sindex
from cc
join gmax 
on cc.continent_code=gmax.continent_code and cc.rdate=gmax.rdate and gmax.sindex=cc.sindex
),
gminc as(
select cc.country_code,cc.continent_code,cc.rdate,cc.sindex
from cc
join gmin 
on cc.continent_code=gmin.continent_code and cc.rdate=gmin.rdate and gmin.sindex=cc.sindex
)
(select continent_name,country_name,rdate as date,sindex as stringency_index
from gmaxc
join country on gmaxc.country_code=country.two_letter_country_code
join continent on gmaxc.continent_code=continent.continent_code
)
union
(select continent_name,country_name,rdate as date,sindex as stringency_index
from gminc
join country on gminc.country_code=country.two_letter_country_code
join continent on gminc.continent_code=continent.continent_code
)
order by date,continent_name