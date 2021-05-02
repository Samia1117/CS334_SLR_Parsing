size 70 70
begin
	cat crookshanks 20 12 north ;
	mouse scabbers 12 20 east ;
	hole 57 65 ;
	hole 45 54 ;
	6                           // "repeat 6" is what this line should be
		move crookshanks ;
		move scabbers ;
	end ;						// crookshanks is at (20,18), scabbers is at (18,20)
	clockwise crookshanks ;		// crookshanks is facing east
	clockwise scabbers ;
	clockwise scabbers ;
	clockwise scabbers ;		// scabbers is facing north
	repeat 5
		move scabbers ;
		move scabbers ;
		move crookshanks ;
	end ;						// crookshanks is at (25,18), scabbers is at (18,30)
	clockwise crookshanks ;
	clockwise crookshanks ;		// crookshanks is facing west
	move crookshanks 7 ;		// crookshanks is at (18,18)
	clockwise crookshanks ;		// crookshanks is facing north
	move crookshanks 8 ;		// crookshanks is at (18,26)
halt
