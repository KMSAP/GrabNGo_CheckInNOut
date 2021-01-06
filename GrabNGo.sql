insert into in_and_out(in_out_id, customer_id, check_in) values(in_out_seq.nextval, 3, systimestamp);
CREATE SEQUENCE in_out_seq;
update in_and_out set check_out = systimestamp where customer_id = 2 and check_out is null;
select check_out from in_and_out where customer_id = 2 and check_out is null;
insert into carts (cart_id, customer_id, product_id,cart_stock)
     values (cart_seq.nextval, 3, 64, 1);
select 
    ROW_NUMBER() OVER (order by c.cart_id desc) as num,
    c.product_id, c.cart_stock, c.cart_in,
    p.product_name, p.product_price
from carts c
    inner join Products p
        on c.product_id = p.product_id
    where c.customer_id = 3;

select 
    ROW_NUMBER() OVER (order by c.cart_id desc) as num,
    c.product_id, c.cart_stock, c.cart_in,
    p.product_name, p.product_price
from carts c
    inner join Products p
        on c.product_id = p.product_id
    where c.customer_id = 3;
    
select ROW_NUMBER() OVER (order by c.cart_id desc) as num, 
                                   c.product_id, c.cart_in, p.product_name, p.product_price, c.cart_stock
                                   from carts c
                                   inner join Products p
                                   on c.product_id = p.product_id
                                   where c.customer_id = 2;