-- SELECT 
--     id,
--     use,
--     time,
--     ingredient_id,
--     recipe_id,
--     SUM(quantity),
--     COUNT(*)
-- FROM app_api_recipeingredients
-- GROUP BY ingredient_id
-- HAVING COUNT(*) > 0


-- SELECT 
--     r.*,

-- FROM app_api_recipes r
-- JOIN app_api_recipeingredients ri
--     ON r.id = ri.recipe_id
-- GROUP BY r.ingredient_id

-- SELECT
--     r.*,
--     ri.ingredient_id,
--     i.name,
--     -- ri.quantity
--     SUM(ri.quantity) as recipe_quantity
-- FROM app_api_recipes r
-- JOIN app_api_recipeingredients ri
--     ON r.id = ri.recipe_id
-- JOIN app_api_ingredients i 
--     ON i.id = ri.ingredient_id
-- WHERE r.id = 1
-- GROUP BY ri.ingredient_id
-- SELECT
--     ui.ingredient_id,
--     i.name,
--     ui.quantity user_quantity
-- FROM auth_user u 
-- JOIN app_api_useringredients ui
--     ON u.id = ui.user_id
-- JOIN app_api_ingredients i 
--     ON i.id = ui.ingredient_id
-- WHERE u.id = 1

SELECT *
FROM (
    SELECT
        r.*,
        ri.ingredient_id,
        i.name recipe_ingredient_name,
        -- ri.quantity
        SUM(ri.quantity) as recipe_quantity
    FROM app_api_recipes r
    JOIN app_api_recipeingredients ri
        ON r.id = ri.recipe_id
    JOIN app_api_ingredients i 
        ON i.id = ri.ingredient_id
    -- WHERE r.id = 2
    GROUP BY ri.ingredient_id
) as r
LEFT JOIN (
    SELECT
        ui.ingredient_id,
        i.name user_ingredient_name,
        ui.quantity user_quantity
    FROM auth_user u 
    JOIN app_api_useringredients ui
        ON u.id = ui.user_id
    JOIN app_api_ingredients i 
        ON i.id = ui.ingredient_id
    WHERE u.id = 1
) as u 
ON r.ingredient_id = u.ingredient_id