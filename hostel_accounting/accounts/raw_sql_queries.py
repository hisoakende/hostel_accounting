all_group_purchases_query = '''
            SELECT 0 AS id, u.id AS user_id, u.username, u.email, u.first_name, u.last_name, u.is_superuser, u.is_staff, 
            u.date_joined, u.last_login, product.id AS product_id, product.name AS product_name, category.id AS category_id, 
            category.name AS category_name, product_purchase.price
            FROM accounts_user AS u
                JOIN goods_accounting_purchase AS purchase
                    ON u.id = purchase.user_id
                JOIN goods_accounting_productpurchase AS product_purchase
                    ON purchase.id = product_purchase.purchase_id
                JOIN goods_accounting_product AS product
                    ON product_purchase.product_id = product.id
                JOIN goods_accounting_productcategory AS category
                    ON product.category_id = category.id
                JOIN accounts_roommatesgroup AS roommates_group
                    ON roommates_group.id = u.roommates_group_id
            WHERE roommates_group.id = %s;'''
