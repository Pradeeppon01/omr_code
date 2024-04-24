CREATE TABLE studentsPlaceholderData (
	sno int auto_increment primary key,
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
        barCode10 bigint default null	
);

CREATE TABLE barcodeData (
	barcode bigint primary key,
	barcodeUsedSno bigint default null,
	barcodeLabel varchar(300) default null
);
