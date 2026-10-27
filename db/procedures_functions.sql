CREATE OR REPLACE FUNCTION calc_total_pg(
    price NUMERIC,
    quantity INTEGER
)
RETURNS NUMERIC AS $$
BEGIN
    IF price IS NULL OR quantity IS NULL OR quantity <= 0 THEN
        RETURN 0;
    END IF;

    RETURN price * quantity;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE create_order_pg(
    p_user_id INTEGER,
    p_stock_item_id INTEGER,
    p_qty INTEGER
)
AS $$
DECLARE
    v_stock INTEGER;
    v_price NUMERIC;
    v_order_id INTEGER;
BEGIN
    IF p_qty IS NULL OR p_qty <= 0 THEN
        RAISE EXCEPTION 'Некорректное количество';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM users WHERE user_id = p_user_id
    ) THEN
        RAISE EXCEPTION 'Пользователь не найден';
    END IF;

    SELECT si.quantity, p.price
    INTO v_stock, v_price
    FROM stock_items si
    JOIN products p ON p.product_id = si.product_id
    WHERE si.stock_item_id = p_stock_item_id
    FOR UPDATE OF si;

    IF NOT FOUND OR v_stock < p_qty THEN
        RAISE EXCEPTION 'Недостаточно товара на складе';
    END IF;

    INSERT INTO orders (order_date, user_id)
    VALUES (CURRENT_DATE, p_user_id)
    RETURNING order_id INTO v_order_id;

    INSERT INTO order_items (
        order_id, stock_item_id, quantity, unit_price
    )
    VALUES (
        v_order_id, p_stock_item_id, p_qty, v_price
    );

    UPDATE stock_items
    SET quantity = quantity - p_qty
    WHERE stock_item_id = p_stock_item_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE update_stock_pg(
    p_stock_item_id INTEGER,
    p_qty INTEGER
)
AS $$
DECLARE
    v_stock INTEGER;
BEGIN
    IF p_qty IS NULL OR p_qty <= 0 THEN
        RAISE EXCEPTION 'Некорректное количество';
    END IF;

    SELECT quantity
    INTO v_stock
    FROM stock_items
    WHERE stock_item_id = p_stock_item_id
    FOR UPDATE;

    IF NOT FOUND OR v_stock < p_qty THEN
        RAISE EXCEPTION 'Недостаточно товара';
    END IF;

    UPDATE stock_items
    SET quantity = quantity - p_qty
    WHERE stock_item_id = p_stock_item_id;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Недостаточно товара на складе!';
END;
$$ LANGUAGE plpgsql;
