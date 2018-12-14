# Logs Analysis Project

This is an internal reporting tool that will use information from the news database to discover what kind of articles the site's readers like.

This **Python3** application uses **Postgresql** as database backend. The python code also uses **Flask** as a web framework to get the reporting tool running immediately on python's http service. It also uses **psycopg2** to connect to Postgresql backend. To facilitate development, a Linux virtual machine was provided with all necessary applications and configuration to run the python application.

## Installation

This project requires installing a Linux virtual machine. Unfortunately, installation instructions were problematic. After days of experimentation and configuration in different machines, the following instructions finally worked for me on a Mac machine.

### Environment

**Although it is just a few steps, because I am in Thailand with cellular data, the process and experimentation took about 3 days to set up**. Be forewarned that a lot of data is needed for this setup.

1. Download and install the latest Oracle VM Virtualbox application at <a href="https://www.virtualbox.org/">https://www.virtualbox.org/</a>.
2. Download and install the latest HashiCorp Vagrant application at <a href="https://www.vagrantup.com/downloads.html">https://www.vagrantup.com/downloads.html</a>.
3. Download and unpack the VM configuration at <a href="https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip">https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip</a>.
4. `cd /vagrant` into this newly unpacked directory.
5. `vagrant up` will start the Linux VM. **Please note that this step may take a few hours (in my case on cellular data in Thailand) to run initially since it is downloading a Linux Ubuntu distro with a size of nearly 5 GB, and an additional 1 GB for distro upgrades.**
6. `vagrant ssh` will log you into the Linux shell.
7. `cd /vagrant`
8. Download and unpack the <a href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">newsdata</a>.
9. `psql -d news -f newsdata.sql` will install and populate the Postgresql database.
10. Install the views below in `psql` shell.

### Views

```
create view logPathWithCount as select path, count(*) as num from log group by path;

create view lpwc_articles as select lpc.*, a.slug, a.title, a.author as author_id from logPathWithCount as lpc join articles as a on lpc.path ~ a.slug order by lpc.num desc;

create view datesWithErrorStatus as select DATE(time) as date, count(*) as num from log where status != '200 OK' group by date order by date desc;

create view requestsPerDate as select DATE(time) as date, count(*) as num from log group by date order by date desc;

create view top3articles as select DISTINCT la.slug, la.title, s.total from lpwc_articles as la join (select slug, SUM(num) as total from lpwc_articles group by slug) as s on la.slug = s.slug order by s.total desc limit 3;

create view authorsbypopularity as select authors.name, sss.total from authors join (select DISTINCT la.author_id, s.total from lpwc_articles as la join (select author_id, SUM(num) as total from lpwc_articles group by author_id) as s on la.author_id = s.author_id order by s.total desc) as sss on authors.id = sss.author_id;

create view topdateinerror as select dwes.date, round((dwes.num * 100.0) / rpd.num, 2) as error from datesWithErrorStatus as dwes join requestsPerDate as rpd on dwes.date = rpd.date where round((dwes.num * 100.0) / rpd.num, 2) > 1;
```

**After installing the views in psql, exit `psql` and place a copy of python code newsapp.py and proceed with the following in Bash shell:**

`python newsapp.py`

Since I am using Python 3, ensure that you have it with `python3 --version`. If errors occur, then python 3 may not be installed. Install Python 3 with `sudo apt-get install python3`.

## Usage

After running `python newsapp.py`, the http service should be running on the localhost. Use a browser to go to http://localhost:8000.
![image](supplement/ReportingToolScreenShot.png)

## Sample Output

The file <a href="sampleOutput.txt">sampleOutput.txt</a> is the result of extracting the requests per day with error status. It was created with the sql query code:

`select dwes.*, rpd.num as total_requests, round((dwes.num * 100.0) / rpd.num, 2) as error from datesWithErrorStatus as dwes join requestsPerDate as rpd on dwes.date = rpd.date;`

## Code Base

My python code newsapp.py is based on the **forum** code from the Python DB-API lectures.

## Resources

* <a href="http://www.postgresqltutorial.com/postgresql-administration/">PostgreSQL Administration</a>
* <a href="https://www.postgresql.org/docs/9.3/functions-string.html">PostgreSQL: Documentation: 9.3: String Functions and Operators</a>
* <a href="https://help.github.com/articles/basic-writing-and-formatting-syntax/">Markdown: basic writing and formatting syntax</a>
* <a href="https://www.postgresql.org/docs/current/functions-matching.html">PostgreSQL: Documentation: 11: 9.7. Pattern Matching</a>
* <a href="http://www.postgresqltutorial.com/managing-postgresql-views/">Managing PostgreSQL Views</a>
* <a href="https://pythonspot.com/flask-web-app-with-python/">Flask Web App with Python</a>
* <a href="http://www.postgresqltutorial.com/postgresql-subquery/">PostgreSQL Subquery</a>
* <a href="https://dba.stackexchange.com/questions/75622/postgresql-division-in-query-not-working">PostgreSQL Division In Query</a>
* <a href="https://stackoverflow.com/questions/12864467/how-to-take-sum-of-column-with-same-id-in-sql">How to take sum of column with same id in SQL? - Stack Overflow</a>
* <a href="https://wiki.postgresql.org/wiki/Psycopg2_Tutorial">Psycopg2 Tutorial - PostgreSQL wiki</a>
* <a href="https://docs.python.org/2/library/datetime.html">Basic date and time types — Python</a>
* <a href="https://www.python.org/dev/peps/pep-0008/">PEP 8 -- Style Guide for Python Code</a>
