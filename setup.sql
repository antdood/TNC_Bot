CREATE TABLE members (
    member varchar(30),
    PRIMARY KEY (member)
);

INSERT INTO members VALUES
("Nayeon"),
("Jeongyeon"),
("Momo"),
("Sana"),
("Jihyo"),
("Mina"),
("Dahyun"),
("Chaeyoung"),
("Tzuyu");

CREATE TABLE rankings (
    user varchar(255),
    member varchar(30),
    ranking int,
    FOREIGN KEY (member) REFERENCES members(member)
);

