CREATE TABLE IF NOT EXISTS product_xpaths (
    id SERIAL PRIMARY KEY,
    price_on_sale TEXT,
    price_without_sale TEXT,
    price TEXT,
    availability TEXT,
    title TEXT,
    available_text TEXT
);

CREATE TABLE IF NOT EXISTS navigation_xpaths (
    id SERIAL PRIMARY KEY,
    search_field TEXT,
    submit_button TEXT,
    search_result_products_xpath_templates TEXT,
    search_result_link_attribute TEXT
);

CREATE TABLE IF NOT EXISTS websites (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255) NOT NULL UNIQUE,
    price_format VARCHAR(50) NOT NULL,
    product_xpaths_id INTEGER NOT NULL,
    navigation_xpaths_id INTEGER NOT NULL,
    FOREIGN KEY (product_xpaths_id) REFERENCES product_xpaths(id) ON DELETE CASCADE,
    FOREIGN KEY (navigation_xpaths_id) REFERENCES navigation_xpaths(id) ON DELETE CASCADE
);