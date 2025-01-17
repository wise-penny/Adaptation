import pymysql
from datetime import datetime
from geopy.distance import distance

# Config imports and constants
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_db_connection():
    return pymysql.connect(host=DB_HOST,
                           user=DB_USER,
                           password=DB_PASSWORD,
                           db=DB_NAME,
                           cursorclass=pymysql.cursors.DictCursor)

# MARK: fetch_hourly_deals
def fetch_hourly_deals():
    deals = {}
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT STORE_NAME, SLOGAN, DESCRIPTION, IMG, URL, ZIP 
                    FROM ADVS 
                    WHERE START <= NOW() AND END >= NOW()
                """)
                ads = cursor.fetchall()

                for ad in ads:
                    store_name = ad['STORE_NAME']
                    if store_name not in deals:
                        deals[store_name] = []
                    deals[store_name].append({
                        'slogan': ad['SLOGAN'],
                        'description': ad['DESCRIPTION'],
                        'image': ad['IMG'],
                        'url': ad['URL'],
                        'zip': ad['ZIP']
                    })
    except Exception as e:
        print(f"Error fetching deals: {e}")
    return deals

# MARK: update_ad_views
def update_ad_views(store_name):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ADVS 
                    SET SEEN = SEEN + 1 
                    WHERE STORE_NAME = %s AND START <= NOW() AND END >= NOW()
                """, (store_name,))
                connection.commit()
    except Exception as e:
        print(f"Error updating ad views: {e}")

# MARK: fetch_deals_by_category
def fetch_deals_by_category(category_id, user_location):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT a.*, f.central_latitude, f.central_longitude, f.distribution_radius
        FROM ADVS a
        JOIN FRANCHISE f ON a.store_id = f.store_id
        WHERE f.category_id = %s AND a.start <= NOW() AND a.end >= NOW()
    """, (category_id,))
    all_deals = c.fetchall()
    conn.close()

    nearby_deals = [deal for deal in all_deals if is_in_range(user_location, (deal['central_latitude'], deal['central_longitude']), deal['distribution_radius'])]
    return nearby_deals

# MARK: is_in_range
def is_in_range(user_location, store_location, radius):
    return distance(user_location, store_location).miles <= radius

# MARK: get_hot_deals
def get_hot_deals(user_id, user_location):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT a.*, f.latitude, f.longitude, f.distribution_radius
        FROM ADVS a
        JOIN FRANCHISE f ON a.store_id = f.store_id
        JOIN HOTLISTS h ON h.item LIKE CONCAT('%', a.description, '%')
        WHERE h.user_id = %s AND a.start <= NOW() AND a.end >= NOW()
    """, (user_id,))
    hot_deals = c.fetchall()
    conn.close()

    nearby_hot_deals = [deal for deal in hot_deals if is_in_range(user_location, (deal['latitude'], deal['longitude']), deal['distribution_radius'])]
    return nearby_hot_deals

# MARK: update_deal_views
def update_deal_views(deal_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE ADVS SET seen = seen + 1 WHERE id = %s", (deal_id,))
    conn.commit()
    conn.close()

# MARK: get_trending_deals
def get_trending_deals(user_location):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT a.*, f.latitude, f.longitude, f.distribution_radius
        FROM ADVS a
        JOIN FRANCHISE f ON a.store_id = f.store_id
        ORDER BY a.seen DESC
        LIMIT 10
    """)
    trending_deals = c.fetchall()
    conn.close()

    nearby_trending_deals = [deal for deal in trending_deals if is_in_range(user_location, (deal['latitude'], deal['longitude']), deal['distribution_radius'])]
    return nearby_trending_deals