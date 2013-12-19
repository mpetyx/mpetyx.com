global stored 
stored = """CREATE OR REPLACE PROCEDURE addnewobject
	(
		p_RecordID			IN	NUMBER		,
		p_Title				IN	VARCHAR2	,
		p_CollectionID		IN	VARCHAR2	,
		p_Description		IN	VARCHAR2	,
		p_Marks				IN	VARCHAR2	,
		p_ProductionDate	IN  VARCHAR2	,
		p_Url				IN	VARCHAR2	,
		p_Height			IN	VARCHAR2	,
		p_Width				IN	VARCHAR2	,
		p_Depth				IN	VARCHAR2	,
		p_Diameter			IN	VARCHAR2	,
		p_Weight			IN	VARCHAR2	,
		p_Location			IN	VARCHAR2
	)
	IS
	BEGIN
		INSERT INTO Objects
			(
				RecordID,
				Title,
				CollectionID,
				Description,
				Marks,
				ProductionDate,
				Url,
				Height,
				Width,
				Depth,
				Diameter,
				Weight,
				Location
			)
		VALUES
			(
				p_RecordID,
				p_Title,
				p_CollectionID,
				p_Description,
				p_Marks,
				p_ProductionDate,
				p_Url,
				p_Height,
				p_Width,
				p_Depth,
				p_Diameter,
				p_Weight,
				p_Location
			);

		COMMIT;

	END addnewobject;

"""
