SELECT 
    id,
    use,
    time,
    ingredient_id,
    recipe_id,
    SUM(quantity),
    COUNT(*)
FROM app_api_recipeingredients
GROUP BY ingredient_id
HAVING COUNT(*) > 0