-- This presents the path column and count column from log table.
-- It will facilitate the join with articles since there are no common keys.
-- After the join on path and slug, the slug will be the unique identifier.
-- See view lpwc_articles below.
create view logPathWithCount as select path, count(*) as num from log group by path;


-- This presents a join of logPathWithCount and articles on path and slug.
-- This was facilitated by the view logPathWithCount above
create view lpwc_articles as select lpc.*, a.slug, a.title, a.author as author_id from logPathWithCount as lpc join articles as a on SPLIT_PART(lpc.path,'/',3) = a.slug order by lpc.num desc;


-- This presents all the dates with error status (or NOT '200 OK') with count.
-- Along with view requestsPerDate below, this facilitates presentation of proportion error to total.
create view datesWithErrorStatus as select DATE(time) as date, count(*) as num from log where status != '200 OK' group by date order by date desc;


-- This presents the total requests by date.
-- Along with view datesWithErrorStatus above, this facilitates presentation of proportion error to total.
create view requestsPerDate as select DATE(time) as date, count(*) as num from log group by date order by date desc;


-- This presents the query to select top 3 articles.
create view top3articles as select la.slug, la.title, s.total from lpwc_articles as la join (select slug, SUM(num) as total from lpwc_articles group by slug) as s on la.slug = s.slug order by s.total desc limit 3;

-- This presents authors ordered by popularity.
create view authorsbypopularity as select authors.name, sss.total from authors join (select DISTINCT la.author_id, s.total from lpwc_articles as la join (select author_id, SUM(num) as total from lpwc_articles group by author_id) as s on la.author_id = s.author_id order by s.total desc) as sss on authors.id = sss.author_id;

-- This presents all dates that have percentage error of greater than 1 percent.
create view topdateinerror as select dwes.date, round((dwes.num * 100.0) / rpd.num, 2) as error from datesWithErrorStatus as dwes join requestsPerDate as rpd on dwes.date = rpd.date where round((dwes.num * 100.0) / rpd.num, 2) > 1;