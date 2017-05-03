

```sql lite
-- 1
select Country,
		count(Country)
from Customers
group by Country
order by count(Country) desc
limit 10;

-- 2 a
select a.ProductID,
       b.ProductName,
       sum(a.UnitPrice*a.Quantity *(1-a.Discount)) as sales
from OrderDetails as a,
     Products as b on a.ProductID = b.ProductID
group by a.ProductID
order by sales desc
limit 10;

-- 2 b, use view
drop view if exists top10;

create view top10 as
select a.ProductID,
       b.ProductName,
       c.CompanyName,
       sum(a.UnitPrice*a.Quantity *(1-a.Discount)) as sales
from OrderDetails as a,
     Products as b,
     Suppliers as c on a.ProductID = b.ProductID
and b.SupplierID = c.SupplierID
group by a.ProductID
order by sales desc
limit 10;

select a.SupplierID,
       b.CompanyName,
       sum(b.sales)
from Suppliers as a,
     top10 as b on a.CompanyName = b.companyName
group by b.companyName
order by sum(b.sales) desc;

-- 2 c, use suquery and join
select a.SupplierID,
       b.CompanyName,
       sum(subq.sales)
from
  (select ProductID,
          sum(UnitPrice*Quantity *(1-Discount)) as sales
   from OrderDetails
   group by ProductID
   order by sales desc
   limit 10) as subq
join Products as a
join Suppliers as b on subq.ProductID = a.ProductID
and a.SupplierID = b.SupplierID
group by b.companyName
order by sum(subq.sales) desc;


-- 3
select a.EmployeeID,
       a.LastName,
       sum(c.UnitPrice*c.Quantity *(1-c.Discount)) as sales
from Employees as a,
     Orders as b,
     OrderDetails as c on a.EmployeeID = b.EmployeeID
and b.OrderId = c.OrderID
group by a.EmployeeID
order by sales desc
limit 10;

-- 4
drop view if exists seasons;

create view seasons as
select a.ProductID,
       ((strftime('%Y',b.OrderDate)-2014)*4 + (strftime('%m',b.OrderDate)+2)/3) as quarter,
       (a.UnitPrice*a.Quantity *(1-a.Discount)) as sales
from OrderDetails as a,
     Orders as b on a.OrderID = b.OrderId ;

select a.ProductID,
       a.ProductName,
       b.quarter,
       sum(b.sales)
from top10 as a,
     seasons as b on a.ProductID = b.ProductID
group by a.ProductID,
         b.quarter
order by a.ProductID,
         b.quarter;
```

