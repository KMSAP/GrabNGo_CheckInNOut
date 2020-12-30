import os
import cx_Oracle
import pandas as pd

class DB_Connection():

    def __init__(self):
        os.putenv('NLS_LANG', '.UTF8')
        # 연결에 필요한 기본 정보 (유저, 비밀번호, 데이터베이스 서버 주소)
        self.connection = cx_Oracle.connect("유저", "비밀번호", "데이터베이스 서버 주소")
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    def select_user(self, customer_id):
        self.cursor.execute("select login_session, customer_name from CUSTOMERS where customer_id = :id",
                       {"id": customer_id})
        print('cursor: ',type(self.cursor))
        print('connection: ', type(self.connection))
        cnt = self.cursor.fetchone()
        print('cnt: ', type(cnt))
        return cnt

    def update_login_session_T(self, customer_id):
        # 고객이 로그아웃 후 login_session을 리셋해 줌.
        self.cursor.execute("update customers set login_session = 'True' where customer_id = :id", {"id": customer_id})

    def update_login_session_F(self, customer_id):
        # 고객이 로그아웃 후 login_session을 리셋해 줌.
        self.cursor.execute("update customers set login_session = 'False' where customer_id = :id", {"id": customer_id})

    def select_cart_product(self, customer_id):
        self.cursor.execute("""select ROW_NUMBER() OVER (order by c.cart_id desc) as num, c.product_id, c.cart_in, p.product_name, p.product_price, c.cart_stock
                                   from carts c
                                   inner join Products p
                                   on c.product_id = p.product_id
                                   where c.customer_id = :id""", {"id": customer_id})
        df = pd.DataFrame(self.cursor.fetchall())
        return df

    def insert_order(self, customer_id, total_price):
        self.cursor.execute("""insert into orders(order_id, customer_id, total_price)
                                                values(order_seq.nextval,:id,:total_price)"""
                       , {"id": customer_id, "total_price": total_price})

    def insert_order_detail(self, df):
        for index, row in df.iterrows():  # cart_id, product_id, cart_in, product_name, product_price, cart_stock
            print(row[0], row[1], row[2], row[3], row[4], row[5])
            self.cursor.execute("""insert into order_details (order_detail_id, order_id, product_id, cart_in, ordered_price, cart_stock)
                                values(order_details_seq.nextval, order_seq.currval, :product_id, :cart_in, :ordered_price, :cart_stock)"""
                           , {"product_id": row[1], "cart_in": row[2], "ordered_price": row[4], "cart_stock": row[5]})

    def delete_cart(self, customer_id):
        self.cursor.execute("""delete carts where customer_id = :id"""
                       , {"id": customer_id})
