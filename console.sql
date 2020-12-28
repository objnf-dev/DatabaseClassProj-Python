CREATE DATABASE ticket_sys;

USE ticket_sys;

CREATE TABLE `admin`(
    `id` int not null primary key auto_increment,
    `username` char(20) not null,
    `password` char(60) not null
);

CREATE TABLE `user`(
    `id` int not null key auto_increment,
    `username` char(20) not null,
    `password` char(60) not null,
    `group_id` int
);

CREATE TABLE train(
    
)