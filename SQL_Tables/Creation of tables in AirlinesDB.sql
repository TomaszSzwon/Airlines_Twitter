USE AirlineTweetsDB;
GO

CREATE TABLE Dim_Airline (
    AirlineID INT IDENTITY(1,1) PRIMARY KEY,
    AirlineName NVARCHAR(100) NOT NULL UNIQUE
);

Select * FROM Dim_Airline;


CREATE TABLE Dim_Sentiment (
    SentimentID INT NOT NULL PRIMARY KEY,
    SentimentDescription NVARCHAR(100) NOT NULL
);

INSERT INTO Dim_Sentiment (SentimentID, SentimentDescription)
VALUES (0, 'Negative'), (1, 'Neutral'), (2, 'Positive');

Select * FROM Dim_Sentiment;


CREATE TABLE Dim_NegativeReason (
    NegativeReasonID INT IDENTITY(1,1) PRIMARY KEY,
    NegativeReasonDescription NVARCHAR(100) NOT NULL UNIQUE
);

Select * FROM Dim_NegativeReason;


CREATE TABLE Dim_Time (
    DateID BIGINT PRIMARY KEY, 
    FullDate DATETIME NOT NULL,  
    -- Kolumny obliczeniowe 
    Year AS YEAR(FullDate),  
    Month AS MONTH(FullDate),  
    Day AS DAY(FullDate), 
    DayOfWeek AS DATENAME(WEEKDAY, FullDate),  
    MonthName AS DATENAME(MONTH, FullDate)
);

CREATE TRIGGER trg_SetDateID 
ON Dim_Time 
INSTEAD OF INSERT 
AS 
BEGIN
    INSERT INTO Dim_Time (DateID, FullDate)
    SELECT 
        CAST(FORMAT(FullDate, 'yyyyMMddHHmmss') AS BIGINT), 
        FullDate
    FROM inserted;
END;

Select COUNT(*) FROM Dim_Time;
SELECT TOP (10) * FROM Dim_Time;


CREATE TABLE Fact_AirlinesTweets (
    TweetID BIGINT PRIMARY KEY,
    DateID BIGINT NOT NULL,
    NegativeReasonID INT NOT NULL,
    AirlineID INT NOT NULL,
    SentimentID INT NOT NULL,
	AirlineSentimentConfidence NVARCHAR(100) NULL,
	NegativeReasonConfidence NVARCHAR(100) NULL,
	AirlineSentimentGold NVARCHAR(100) NULL,
	NegativeReasonGold NVARCHAR(100) NULL,
	Name NVARCHAR(100) NULL,
	TweetCoord NVARCHAR(100) NULL,
	RetweetCount NVARCHAR(100) NULL,
	UserTimezone NVARCHAR(100) NULL
);

SELECT COUNT(*) FROM Fact_AirlinesTweets;

SELECT TOP(50) * FROM Fact_AirlinesTweets;



DROP TABLE Dim_Sentiment;
DROP TABLE Dim_Airline;
DROP TABLE Dim_NegativeReason;
DROP TABLE Dim_Time;
DROP TABLE Fact_AirlinesTweets;





