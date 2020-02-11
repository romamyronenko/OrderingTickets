CREATE TABLE IF NOT EXISTS event(
    `id` int auto_increment,
    `Name` varchar(90) NOT NULL,
    `Date` date,
    `Place` varchar(90) NOT NULL,
    `Total Available` int,
    UNIQUE(id)
);

CREATE TABLE IF NOT EXISTS ticket(
    `id` int,
    `event_id` int,
    `Owner` varchar(90) NOT NULL,


    PRIMARY KEY (`id`),
    FOREIGN KEY (`event_id`) REFERENCES event(`id`)
);