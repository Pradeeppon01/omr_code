
CREATE TABLE studentsPlaceholderData (
	sno int primary key,
	slno int default null,
        degreeWithBranch varchar(300) default null,
        candidateName varchar(300) default null,
        registerNumber varchar(300) default null,
        examDateAndSession varchar(300) default null,
        examCentreCode int default null,
        subjectCode varchar(100) default null,
        subjectTitle varchar(300) default null,
	questionCode int default null,
 	barCode1 bigint default null,
        barCode2 bigint default null,
        barCode3 bigint default null,
        barCode4 bigint default null,
        barCode5 bigint default null,
        barCode6 bigint default null,
        barCode7 bigint default null,
        barCode8 bigint default null,
        barCode9 bigint default null,
        barCode10 bigint default null,
        qrCode1 bigint default null,
        qrCode2 bigint default null,
        qrCode3 bigint default null,
        qrCode4 bigint default null,
        qrCode5 bigint default null,
        qrCode6 bigint default null,
        qrCode7 bigint default null,
        qrCode8 bigint default null,
        qrCode9 bigint default null,
        qrCode10 bigint default null
);

CREATE TABLE barcodeData (
	barcode bigint primary key,
	barcodeUsedSno bigint default null,
	barcodeLabel varchar(300) default null
);


CREATE TABLE serialNoMaxData(
        serialNoMax int primary key default 1
);


CREATE UNIQUE INDEX barcodeIndex on barcodeData(barcode);
CREATE UNIQUE INDEX slnoIndex on studentsPlaceholderData(slno);
