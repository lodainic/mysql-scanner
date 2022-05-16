# mysql-scanner
MySQL database scanner is a Python desktop application(developed on Ubuntu). The GUI was build using Tkinter and the backend is functional thanks to mysql.connector library. The application scans for basic database constraints violations and then offers the user to correct them.

The constraints are as follows:

1. Nullability Constraint.

    * Requirement

        check each table in the database for nullable. A table must have at least one column (an attribute), except for the primary key, which does NOT support null values.

    * Implementation

        after scanning the database show the user columns to select in order to add the null constraint.

2. Primary Key Constraints.

    * Requirement

        check the quallity of primary key of each table.
        
    * Implementation
        1. for each table with no primary key, a surrogate one is added.
        2. for each table in which:
            - there is a primary key on a single column but it is not numeric
            - there is a primary numeric key on several attributes (implemented for cases of two).

            the existing bad keys are deleted and the standard surrogate one is created. Also, the corresponding foreign keys are erased and relinked to new primary key.

3. Domain Constraints.

    * Requirement

        for all text, numeric and calendar data columns it is necessary to check if there is an associated domain constraint or not.
    
    * Implementation

        1. the calendar data field must have a minimum and a maximum value.

        2. narrow the maximum length of string in the text columns (if max string len = 18 then new len = 2^5(32)).

        3. for numeric columns do the same as text columns.


To run the app start with _app_gui.py_ .

_create_db.py_ creates a test MySQL database.

