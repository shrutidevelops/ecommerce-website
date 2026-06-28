create database ecommerce;
use ecommerce;

create table users
(
    user_id int auto_increment primary key,
    name varchar(100),
    email varchar(100) unique,
    password varchar(255),
    role varchar(20) default 'customer'
);

 create table categories 
(
    category_id int auto_increment primary key,
    category_name varchar(100) not null,
    image varchar(255)
);

 create table products
(
    product_id int auto_increment primary key,
    category_id int,
    product_name varchar(150) not null,
    description text,
    price int,
    stock int,
    image varchar(255),
    foreign key (category_id)
    references categories(category_id)
);

create table cart
(
    cart_id int auto_increment primary key,
    user_id int,
    product_id int,
    quantity int,
    image varchar(255),

    foreign key (user_id)
    references users(user_id)
    on delete cascade,

    foreign key (product_id)
    references products(product_id)
    on delete cascade 
);

create table orders
(
    order_id int auto_increment primary key,
    user_id int,
    total_amount int,
    order_date varchar(20),
    status varchar(20),
    image varchar(255),
    payment_method varchar(50),


    foreign key (user_id)
    references users(user_id)
   on delete cascade
);

create table order_items
(
    item_id int auto_increment primary key,
    order_id int,
    product_id int,
    quantity int,
    price int,

    foreign key (order_id)
    references orders(order_id)
    on delete cascade,

    foreign key (product_id)
    references products(product_id)
    on delete cascade
);

create table wishlist
(
    wishlist_id int auto_increment primary key,
    user_id int,
    product_id int,
    image varchar(255),
   

    foreign key (user_id)
    references users(user_id)
    on delete cascade,

    foreign key (product_id)
    references products(product_id)
    on delete cascade
);

create table contact_messages
(
    message_id int auto_increment primary key,
    name varchar(100),
    email varchar(100),
    message varchar(100)
);

create table newsletter (
    id int auto_increment primary key,
    email varchar(100) unique not null,
    subscribed_on timestamp default current_timestamp
);