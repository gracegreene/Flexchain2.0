CREATE TABLE `user`(
    `user_id` int(11) NOT NULL AUTO_INCREMENT,
    `first_name` varchar(30) NOT NULL,
    `last_name` varchar(30) NOT NULL,
    `email` varchar(40) NOT NULL,
    `company_code` varchar(5) NOT NULL,
    `role` varchar(15) NOT NULL,
    `join_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `password` varchar(20) NOT NULL,
    PRIMARY KEY(`user_id`)
) 


CREATE TABLE `config`(
    `config_id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `config_type` varchar(20) NOT NULL,
    `config_set` set('1','2','3','4') NOT NULL,
    PRIMARY KEY(`config_id`),
    CONSTRAINT `config_user_id` FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`) ON DELETE CASCADE
)



    CREATE TABLE `product`(
    `sku`char(5) NOT NULL,
    `prod_name`varchar(40) NOT NULL,
    `description`varchar(100) NOT NULL,
    `unit_cost` float(10,2) NOT NULL,
    `weight`float(10,2) NOT NULL,
    `length`float(10,2) NOT NULL,
    `width`float(10,2) NOT NULL,
    `height`float(10,2) NOT NULL,
    `case_size` int(4) NOT NULL,
    `wholesale_price` float(10,2) NOT NULL,
    `retail_price` float(10,2) NOT NULL,
    `image_path` varchar(1024) NOT NULL,
    `collection` varchar(40) NOT NULL,
    `company_code` varchar(5) NOT NULL,
    PRIMARY KEY(`sku`), UNIQUE KEY `prod_name`(`prod_name`)
    )

    CREATE TABLE `inventory`(
    `inventory_id` int(11) NOT NULL AUTO_INCREMENT,
    `sku` char(5) NOT NULL,
    `month` int(2) NOT NULL,
    `year` int(4) NOT NULL,
    `quantity` int(6) NOT NULL,
    PRIMARY KEY(`inventory_id`),
    CONSTRAINT `inventory_sku` FOREIGN KEY (`sku`)
    REFERENCES `product` (`sku`) ON DELETE CASCADE
    )


    CREATE TABLE `forecast`(
    `forecast_id` int(11) NOT NULL AUTO_INCREMENT,
    `sku` char(5) NOT NULL,
    `month1` int(6) NOT NULL,
    `month2` int(6) NOT NULL,
    `month3` int(6) NOT NULL,
    PRIMARY KEY(`forecast_id`),
    CONSTRAINT `forecast_sku` FOREIGN KEY (`sku`)
    REFERENCES `product` (`sku`) ON DELETE CASCADE
    )

    CREATE TABLE `location`(
     `location_id` int(11) NOT NULL AUTO_INCREMENT,
     `integration_id` varchar(40),
     `location_type` enum('store','warehouse','customer','other') NOT NULL,
     `name` varchar(50) NOT NULL,
     `country` varchar(30) NOT NULL,
     `state` varchar(30) NOT NULL,
     `street_address` varchar(100) NOT NULL,
     `zipcode` varchar(12) NOT NULL,
     `coordinates` varchar(50) NOT NULL,
     `notes` varchar(100) NOT NULL,
    `company_code` varchar(5) NOT NULL,
     PRIMARY KEY (`location_id`)
    )



    CREATE TABLE `transaction`(
    `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
    `type` varchar(25) NOT NULL,
    `reason` varchar(25) NOT NULL,
    `amount` float(7,2) NOT NULL,
    `location1` int(11) NOT NULL,
    `location2` int(11) NOT NULL,
    `date` DATETIME NOT NULL,
    `transaction_sku_id` int(11) NOT NULL,
    PRIMARY KEY(`transaction_id`),
    CONSTRAINT `transaction_txn_sku` FOREIGN KEY (`transaction_sku_id`)
    REFERENCES `transaction_sku` (`transaction_sku_id`) ON DELETE CASCADE,
    CONSTRAINT `transaction_location_id1` FOREIGN KEY (`location1`)
    REFERENCES `location` (`location_id`) ON DELETE CASCADE,
    CONSTRAINT `transaction_location_id2` FOREIGN KEY (`location2`)
    REFERENCES `location` (`location_id`) ON DELETE CASCADE
    )


    CREATE TABLE `transaction_sku`(
    `transaction_sku_id` int(11) NOT NULL AUTO_INCREMENT,
    `transaction_id` int(11) NOT NULL,
    `sku` char(5) NOT NULL,
    `quantity` int(7) NOT NULL,
    `amount_override` float(7,2),
    PRIMARY KEY(`transaction_sku_id`),
    CONSTRAINT `transaction_sku_txn_id` FOREIGN KEY (`transaction_id`)
    REFERENCES `transaction` (`transaction_id`) ON DELETE CASCADE,
    CONSTRAINT `transaction_sku_sku_id` FOREIGN KEY (`sku`)
    REFERENCES `product` (`sku`) ON DELETE CASCADE
    )


    CREATE TABLE `shipping_cost`(
    `costing_id` int(11) NOT NULL AUTO_INCREMENT,
    `location1` int(11) NOT NULL,
    `location2` int(11) NOT NULL,
    `fixed_cost` float(7,2) NOT NULL,
    `cost_by_weight` float(7,2) NOT NULL,
    PRIMARY KEY(`costing_id`),
    CONSTRAINT `shipping_cost_location_id1` FOREIGN KEY (`location1`)
    REFERENCES `location` (`location_id`) ON DELETE CASCADE,
    CONSTRAINT `shipping_cost_location_id2` FOREIGN KEY (`location2`)
    REFERENCES `location` (`location_id`) ON DELETE CASCADE
    )
